#!/usr/bin/python
# -*- coding: latin-1 -*-

### importacion de librerías

#####Librerías para ocr_processing()
from tika import parser
from time import time
import os
from os import listdir
import fitz
import glob
import pytesseract
from PIL import Image
import cv2
from sqlalchemy import create_engine

#####Librerías para correct_text_n_words
import re 

#####librerías para prob_docs_errors_greater()
import numpy as np
from scipy.stats import poisson
import pandas as pd

#####librerías para doc_errors
import unidecode
from spellchecker import  SpellChecker
import pickle
from symspellpy import SymSpell, Verbosity
from nltk.tokenize import word_tokenize
from collections import Counter

### variables globales

#####Variables para ocr_processing()
path_input = "data"
path_input_pdf = "tmp/data"
path_tmp_image = "tmp/image"
path_output_txt = "tmp/text"
path_output_ocr = "tmp/ocr"
path_done_data = "done/data"

file_in_model = "model4_RF.pkl"
file_in_count = 'count_urt_v2_cleaned.txt'
file_in_es = 'es-100l_v2.txt'
file_in_no_error = 'no_error.pkl'

ocr = []
failed = []

#pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#####Variables para correct_text_n_words
no_search = {'ANTECEDENTES': ['ANTECEDENTE '],
             'ORDENES': ['ORDENE '],
             'FALLA': ['ALLA'],
             'FARC': ['FAC'],
             'ELN': ['EL ', 'EN', 'LN', 'EL N', 'ENL', 'LEN'],
             'PARAMILITARES': ['PARA MILITARES', 'PARAMILITAR ES'],
             'MAGISTRADA': ['MAGISTRAD '],
             'MAGISTRADOS': ['MAGISTRADO '],
             'PONENTE': ['MAGISTRADO '],
             'JUEZ': ['JUE ', 'JUZ'],
             'JUEZA': ['JUEZ ', 'JUEZ A'],
             'OPOSITORA': ['OPOSITOR ', 'OPOSITOR A'],
             'OPOSITORES': ['OPOSITOR ES'],
             'OPONE': ['PONE'],
             'PRIMERO': ['PRIMER '],
             'PRIMERA': ['PRIMER '],
             'SEGUNDA': ['SEGUND '],
             'TERCERO': ['TERCER '],
             'TERCERA': ['TERCER '],
             'CUARTO': ['CUATRO', 'CARTO'],
             'CUARTA': ['CARTA', 'CUART '],
             'QUINTO': 'QUITO',
             'QUINTA': ['QUINT ', 'QUITA'],
             'SEXTO': ['SEXO'],
             'SEXTA': ['SEXT ', 'SETA'],
             'SEPTIMA': ['SEPTIM '],
             'OCTAVA': ['OCTAV '],
             'NOVENO': ['NVENO'],
             'NOVENA': ['NOVEN '],
             'DECIMO': ['ECIMO', 'DECIO'],
             'DECIMA': ['ECIMA', 'DECIA', 'DECIM '],
             'VIGESIMO': ['IGESIMO'],
             'VIGESIMA': ['VIGESIM ', 'IGESIMA'],
             'TRIGESIMA': ['TRIGESIM '],
             'CUADRAGESIMA': ['CUADRAGESIM '],
             'QUINCUAGESIMA': ['QUINCUAGESIM '],
             'SEXAGESIMA': ['SEXAGESIM '],
             'SEPTUAGESIMA': ['SEPTUAGESIM '],
             'OCTOGESIMA': ['OCTOGESIM '],
             'NONAGESIMA': ['NONAGESIM '],
             'UNDECIMA': ['UNDECIM '], 'DUODECIMA': ['DUODECIM ']}

n_new_words = ('RESUELVE', 'RESUELVA', 'ANTECEDENTES', 'ORDENES', 'FALLA', 'DECISION', 'FARC', 'ELN', 'PARAMILITARES',
               'GUERRILLA', 'MAGISTRADO', 'MAGISTRADA', 'MAGISTRADOS', 'PONENTE', 'PROMISCUO', 'JUEZ', 'JUEZA',
               'OPOSITOR', 'OPOSITORA', 'OPOSITORES', 'OPONE', 'PRIMERO', 'PRIMERA', 'SEGUNDO', 'SEGUNDA', 'TERCERO',
               'TERCERA', 'CUARTO', 'CUARTA', 'QUINTO', 'QUINTA', 'SEXTO', 'SEXTA', 'SEPTIMO', 'SEPTIMA', 'OCTAVO',
               'OCTAVA', 'NOVENO', 'NOVENA', 'DECIMO', 'DECIMA', 'VIGESIMO', 'VIGESIMA', 'TRIGESIMO', 'TRIGESIMA',
               'CUADRAGESIMO', 'CUADRAGESIMA', 'QUINCUAGESIMO', 'QUINCUAGESIMA', 'SEXAGESIMO', 'SEXAGESIMA',
               'SEPTUAGESIMO', 'SEPTUAGESIMA', 'OCTOGESIMO', 'OCTOGESIMA', 'NONAGESIMO', 'NONAGESIMA', 'UNDECIMO',
               'UNDECIMA', 'DUODECIMO', 'DUODECIMA')

#####Variables para prob_docs_errors_greater()
max_words = 100000
lambda_val = 918.6446516714417
prob_list = []

# Funciones

def update_converted_document(DBengine, file_id, conv_status, file_type, n_pages):
    """Esta función actualiza los estados, tipos y número de páginas de las sentencias en la base de datos,
    colocádolas como corresponden según los parámetros enviados """
    strSQL = "update mt_sentencia set estado = '" + str(conv_status) + "', tipo_archivo = '" + str(file_type)
    strSQL = strSQL + "', paginas = '" + str(n_pages) + "' where certificado = '" + str(file_id) + "'"
    DBengine.execute(strSQL)

#####Función PDF_read_from_path() -- lectura de los PDF de una ruta
def PDF_read_from_path(path_input, path_image_output, path_output, path_OCR_output, path_processed, DBengine):
    """Dadas las rutas de entrada y salida, tomará todos los archivos PDF de path_input y los convertirá en textos
    (ya sea mediante lectura común o mediante OCR), corregirá los textos, extraerá medidas de calidad y generará un
    .txt con el texto convertido guardado en una de las dos carpetas de output (path_output, path_OCR_output).
    Esta función produce:
        (1)Un conjunto de archivos .txt almacenados en las carpetas de salida.
        (2)Una lista global (prob_list) con la información de métricas de calidad y una etiqueta (label_low_quality).
        (3) Un dataframe que indica si fue descargado (Dowload), cantidad de hojas (Npages) y
        tipo de procesamiento realizado (Type)"""
    start_time = time()
    index = -1

    df_content = pd.DataFrame(columns=["key", "Download", "Npages", "Type", "Status"])

    for file in listdir(path_input):
        path_to_pdf = os.path.join(path_input, file)
        [stem, ext] = os.path.splitext(file)
        if ext == ".pdf":
            try:
                pdf_contents = parser.from_file(path_to_pdf)
            except:
                print("Processing: Some error occured ", path_to_pdf)
                df_content.loc[index] = (stem, "No", None, None, 'Error reading file')
            else:
                if pdf_contents['content'] is None or "Scan" in pdf_contents.get('metadata', dict()).get('producer', ''):
                    if ocr_processing(path_to_pdf, path_image_output, path_OCR_output):
                        df_content.loc[index] = (stem, "Yes", pdf_contents.get('metadata', dict()).get('xmpTPg:NPages', ''), "OCR", 'Convertido')
                    else:
                        df_content.loc[index] = (stem, "No", None, None, 'Error convirtiendo')
                else:
                    file_name = stem + ".txt"
                    path_to_txt = os.path.join(path_output, file_name)
                    with open(path_to_txt, 'a',encoding='utf-8') as txt_file:
                        new_text = correct_text_n_words(pdf_contents['content'], n_new_words, no_search)
                        txt_file.write(new_text.strip())
                        if os.stat(path_to_txt).st_size < 1:
                            txt_file.close()
                            os.remove(path_to_txt)
                            if ocr_processing(path_to_pdf, path_image_output, path_OCR_output):
                                df_content.loc[index] = (stem, "Yes", pdf_contents.get('metadata', dict()).get('xmpTPg:NPages', ''), "OCR", 'Convertido')
                            else:
                                df_content.loc[index] = (stem, "No", None, None, 'Error convirtiendo')
                        else:
                            print("* Processing Normal - writing to " + path_to_txt)
                            df_content.loc[index] = (stem, "Yes", pdf_contents.get('metadata', dict()).get('xmpTPg:NPages', ''), "Text", 'Convertido')
                            prob, error_ratio, label_low_quality = prob_docs_errors_greater(new_text, lambda_val, max_words)
                            prob_list.append([stem, prob, error_ratio, label_low_quality])
        else:
            print("Processing: Data File not is PDF ", stem, ext)
            df_content.loc[index] = (stem,"No",None,"No PDF", 'No convertido')
        update_converted_document(DBengine, stem, df_content.loc[index]["Status"], df_content.loc[index]["Type"], df_content.loc[index]["Npages"])
        os.rename(path_input + "/" + file, path_processed + "/" + file)

    elapsed_time = time() - start_time
    print("Elapsed time TOTAL Processing: %0.10f seconds." % elapsed_time)

#####Funciones para ocr_processing()
def ocr_processing(path_to_pdf, path_image_output, path_OCR_output):
    """Comienza el proceso de conversión por OCR y mide el tiempo que se tarda el proceso. Devolverá falso si el
    proceso falla y verdadero si se ejecuta exitosamente"""
    print("* Processing OCR: " + path_to_pdf)
    start_time_ocr = time()
    remove_image(path_image_output)
    failed.append(path_to_pdf)
    if create_image(path_to_pdf, path_image_output, path_OCR_output):
        elapsed_time = time() - start_time_ocr
        print("Elapsed time Processing OCR: %0.10f seconds." % elapsed_time)
        return True
    else:
        return False

def remove_image(path_image):
    """Dada una carpeta, eliminará todas las imágenes presentes en ellas (en realidad todos los archivos)"""
    folder_image = path_image
    if not os.path.isdir(folder_image):
        os.makedirs(folder_image)
    for image in listdir(folder_image):
        os.remove(os.path.join(folder_image, image))

def thresholded_image(path_image):
    """Se aplica un umbral a la imagen. Devuelve la imagen modificada"""
    image = cv2.imread(path_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return image 

def create_image(path_file_pdf, path_image_output, path_OCR_output):
    """Esta función toma el PDF, crea imágenes, las convierte en texto, corrige dicho texto, cuenta la cantidad de
    errores presentes, aplica una etiqueta de calidad y escribe el string resultante en un archivo .txt"""
    try:
        doc = fitz.open(path_file_pdf)
        _ = doc[0]
    except:
        print ("Processing OCR: Some error occured ", path_file_pdf)
        return False
    
    fullText = ""

    for page in doc:
        path_image = os.path.join(path_image_output, "page%s.png" % (page.number+1))
        pix = page.getPixmap(alpha=False, matrix=fitz.Matrix(150/72, 150/72))
        pix.writeImage(path_image)
        custom_config = r'--oem 3 --psm 6'
        text = str(((pytesseract.image_to_string(thresholded_image(path_image), config=custom_config, lang = 'spa'))))
        fullText += text
    fullText = correct_text_n_words(fullText, n_new_words, no_search)
    prob, error_ratio, label_low_quality = prob_docs_errors_greater(fullText, lambda_val, max_words)
    file = os.path.splitext(os.path.split(path_file_pdf)[1])[0] + ".txt"
    path_to_pdf = os.path.join(path_OCR_output, file)
    prob_list.append([file[:-4], prob, error_ratio, label_low_quality]) #save probability
    with open(path_to_pdf, 'a',encoding='utf-8') as txt_file:
        txt_file.write(fullText.strip())
    return True

#####Funciones para correct_text_n_words
def correct_text_n_words(original_text, n_new_word, no_search):
    """Dado un texto, una lista de n palabras a corregir y un diccionario de excepciones, ejecutar por cada palabra a
    corregir la función correct_text_one_word(). Devuelve el texto corregido"""
    new_text = original_text
    for new_word in n_new_words:
        new_text = correct_text_one_word(new_text, new_word, no_search)
    return new_text

def correct_text_one_word(original_text, new_word, no_search):
    """Dado un texto, una palabra a corregir y un diccionario de excepciones genera un conjunto de posibles errores y
    corrige esos errores con la función replace_options(). Devuelver el texto corrregido"""
    option_set = options(new_word) #generación de opciones
    option_set = avoid_search(option_set, no_search, new_word) #eliminar opciones no deseadas (por ejemplo, un match incorrecto con un singular)
    return replace_options(original_text, option_set, new_word)

def options(word):
    """Dada una palabra, generar una serie de errores probables que incluyan todas las posibilidades en que hayan:
        (1) Hasta 4 espacios dentro de la palabra original.
        (2) omisión de solo uno de los caracteres.
        (3)transposición de un par de letras adyacentes.
        (4)Todas las letras de la palabra separadas por un espacio.
    La función devuelve un objeto tipo set con todas las posibilidades generadas"""
    result = []    
    for i in range(1, len(word)): #ciclo for para generar divisiones y subdivisiones de hasta 4 espacios
        if len(word[:i])>=2:
            out1 = split1(word[:i])
        else:
            out1 = [word[:i]]
        if len(word[i:])>=2:
            out2 = split1(word[i:])
            out2 = out2 + [' ' + word[i:]]
        else:
            out2 = [word[i:]]
        for a in out1:
            for b in out2:
                result.append(a+b)
                result.append(a + ' ' + b)
    #omisiones y transposiciones
    divisions      = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    omissions      = [L + R[1:] for L, R in divisions[:-2] if R]
    omissions      = omissions + [divisions[-2][0] + ' ']
    transpositions = [L + R[1] + R[0] + R[2:] for L, R in divisions if len(R)>1]
    spaced_word = ' '.join(word) #palabra con todos sus caracteres espaciados
    result = result + split1(word) + omissions + transpositions + [spaced_word]
    return set(result) - set([word, word + ' '])

def split1(palabra):
    """Dada una palabra, generar una serie de errores probables que incluyan todas las posibilidades en que haya:
    Un espacio separando a la palabra en 2 seccciones. La función devolverá un objeto tipo list con todas las
    posibilidades generadas"""
    return [palabra[:i] + ' ' + palabra[i:] for i in range(1, len(palabra))].copy()

def avoid_search(option_set, no_search, new_word):
    """Dado un conjunto de opciones de errores, un diccionario de exclusiones y una palabra correcta, la función
    devolverá un nuevo set que no contenga las exclusiones"""
    return option_set - set(no_search.get(new_word, ['']))

def replace_options(original_text, option_set, new_word):
    """Dado un texto sin corregir, un conjunto de posibles errores y la palabra correcta esta función buscará
    interativamente todos los posibles errores, si los encuentra ubicará la palabra correcta en ese espacio y
    continuará la búsqueda. La función devuelve el texto corregido"""
    condition = '|'.join(option_set)
    condition = '([\W\n\r\t])(' + condition + ')([\W\n\r\t])'
    new_text = original_text
    found = re.search(condition, new_text, re.IGNORECASE)
    while found:
        word = new_text[found.start(2):found.end(2)]
        i_new_word = new_word_by_condition(word, new_word)
        new_text = new_text[:found.start(2)] + i_new_word + new_text[found.end(2):]
        found = re.search(condition,  new_text, re.IGNORECASE)
    return new_text

def new_word_by_condition(word, new_word):
    """Dada una palabra incorrecta y una palabra correcta, esta función decididrá si la nueva palabra correcta debe
    ser escrita en minúculas, mayúsculas o mayúscula inicial"""
    total_len = sum(map(str.isalpha, word))
    if str.isupper(word[0]) and count_lower(word[1:]) == (total_len - 1):
        new_word = new_word[0].upper() + new_word[1:].lower()
    elif count_upper(word) >= count_lower(word):
        new_word = new_word.upper()
    else:
        new_word = new_word.lower()
    return new_word

def count_upper(word):
    """Función que cuenta la cantidad de mayúsculas en un string de entrada"""
    return sum(map(str.isupper, word))

def count_lower(word):
    """Función que cuenta la cantidad de minúsculas en un string de entrada"""
    return sum(map(str.islower, word))

#####Funciones para prob_docs_errors_greater()
def prob_docs_errors_greater(original_text, lambda_val, max_words):
    """Dado un texto, una cantidad de errores esperados y una cantidad de palabras de un texto modelo, esta función
    estima mediante la distribución de Poisson la probabilidad de encontrar un texto con esa cantidad de errores o más.
    La función devuelve la probabilidad, la taza de error y una etiqueta de calidad del documento analizado"""
    errors, total_words = doc_errors(original_text, False)
    total_errors = sum(errors.values())
    error_mapped = error_map_max(total_words, total_errors, max_words)
    prob = 1-poisson.cdf(error_mapped, lambda_val)
    label_low_quality = get_label_low_quality(' ', original_text) ###modificación
    if total_words != 0:
        error_ratio = total_errors/total_words
    else:
        error_ratio = 1
    return prob, error_ratio, label_low_quality

def expected_errors(doc_words, lambda_val, max_words):
    """Mapea la cantidad de palabras de un documento al modelo ideal"""
    return doc_words/max_words*lambda_val

def error_map_max(doc_words, errors, max_words):
    """Mapea la cantidad de errores de un texto a la cantidad de errores en un modelo ideal"""
    try:
        answer = errors/doc_words*max_words
    except:
        answer = np.nan
    return answer

#####Funciones para label_low_quality()

def get_label_low_quality(filename, raw): ###modificación de la función completa
    """Dado el nombre de un archivo(no es necesario) y un texto, tomar métricas de la calidad del documento y
    alimentar a un modelo de Random Forest preentrenado para que determine si el documento está bien (y[0] == 0) o si
    tiene baja calidad (y[0] == 1). Devuelve una etiqueta con valor 0 o 1 """
    x = metrics_errors(filename, raw)[1:] + metrics_esp_char(filename, raw)[1:]
    if x[0] != 0:
        x = x[:2] + x[3:5] + [x[5]/x[0]] + [x[-1]] ### ajuste al tipo de entrada esperado por el scaler
    else:
        x = x[:2] + x[3:5] + [1] + [x[-1]]
    x = scaler2.transform([x,])
    y = model4_RF.predict(x)
    return y[0]

def metrics_errors(filename, raw):
    """Dado el nombre de un archivo(no es necesario) y un texto, tomar métricas de la calidad del documento. Devuelve
    una lista con el nombre del archivo, cantidad de errores, de palabras y el ratio del error """
    errors, total_words = doc_errors(raw, False)
    if total_words != 0:
        error_ratio = sum(errors.values())/total_words
    else:
        print(filename)
        print(raw)
        print()
        error_ratio = 1
    error_by_doc = sum(errors.values())
    return [filename, total_words, error_by_doc, error_ratio]

##### métrica de caracteres especiales
def metrics_esp_char(filename, raw):
    """Dado el nombre de un archivo(no es necesario) y un texto, tomar métricas de la calidad del documento. Devuelve
    una lista con el nombre del archivo, cantidad de líneas, cantidad de letras, cantidad de espacios y de caracteres
    especiales """
    list_temp = []
    lines = raw.split('\r\n')
    letters = len(raw)
    spaces = raw.count(' ')
    special_character = character_special(raw)
    list_temp = [filename, len(lines), letters, spaces, special_character]
    return list_temp

def character_special(raw): ###nueva función
    """cuenta la cantidad de caracteres especiales en un texto dado"""
    punctuations = '''!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'''
    return sum([v for k, v in Counter(raw).items() if k in punctuations])

def split(word): ###nueva función
    """Entrega una palabra sin incluir sus caracteres especiales"""
    punctuations = '''!()-[];:'"\,<>./?@#$%^*'''
    [char for char in word if char not in punctuations]
    return word


#####Funciones para doc_errors()
def doc_errors(raw, Verbose):
    """Dado un texto de entrada y una serie de diccionarios cargados como variables globales, esta función detectará
    palabras que no hagan parte de dichos diccionarios y determinará su frecuencia individual. Devuelve un
    diccionario de errores y la cantidad de palabras en el documento """
    count_one_ocr = dict()
    tokens = word_tokenize(raw)
    tokens_words = [unidecode.unidecode(token).lower() for token in tokens if re.match(r'[a-z]{2,}', token) != None and re.match(r'^[A-Za-z]+$', unidecode.unidecode(token)) != None]
    for token in tokens_words:
        count_one_ocr[token] = count_one_ocr.get(token, 0) + 1
    errors = {key:value for key, value in count_one_ocr.items() if not(key in count_urt)}
    if Verbose: print('Errors dict URT', len(errors))
    not_included = spell.unknown(list(errors.keys()))
    errors = dict((k, errors[k]) for k in not_included if k in errors)
    if Verbose: print('Errors spellChecker', len(errors))
    errors = {key:value for key, value in errors.items() if not(key in count_symspell)}
    if Verbose: print('Errors SymSpell Dict', len(errors))
    errors = {key:value for key, value in errors.items() if not(key in count_no_error)}
    if Verbose: print('Errors limp. manual', len(errors))
    count_words = len(tokens_words)
    return errors, count_words

def file_to_dict(name):
    """Esta función está creada para convertir archivos txt que contenga solo una columna en formato <<Palabra
    Número>> y genere con ellos un diccionario donde la llave es Palabra y el valor del diccionario es Número """
    file  = open(name, 'r', encoding = 'UTF-8')
    count_urt = dict()
    for line in file:
        word, num = line.split()
        num = int(num)
        count_urt[word] = num
    file.close()
    return count_urt

def load_gen_pkl(ruta):
    """Esta función permite leer cualquier archivo pkl a partir de la ruta con el nombre del archivo"""
    pkl_file = open(ruta, 'rb')
    file = pickle.load(pkl_file)
    pkl_file.close()
    return file

### Ejecución principal

scaler2, model4_RF = load_gen_pkl(path_input + '/' + file_in_model) ###agregado

# conecta con base de datos
engine = create_engine('postgresql://postgres:LFnnLUQZQMJ9@db-test2.cxqola6hllvk.us-east-2.rds.amazonaws.com/t96_dev')

#####Variables para doc_errors()
spell = SpellChecker(language = 'es')
count_urt = file_to_dict(path_input + '/' + file_in_count)
count_symspell = file_to_dict(path_input + '/' + file_in_es)
count_no_error = load_gen_pkl(path_input + '/' + file_in_no_error)

# Lectura del PDF
PDF_read_from_path(path_input_pdf, path_tmp_image, path_output_txt, path_output_ocr, path_done_data, engine)

# Generacion df de métricas de calidad
metrics_df = pd.DataFrame(prob_list, columns = ['key', 'probability', 'error_ratio', 'low_quality'])

# Inserta en base de datos lo relacionado a las métricas
if not metrics_df.empty: 
    db_tosql = metrics_df.copy()
    db_tosql.to_sql('tt_carga_pdf', engine, if_exists='append', index=False)
