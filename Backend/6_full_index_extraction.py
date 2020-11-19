#!/usr/bin/python
# -*- coding: latin-1 -*-

### importacion de librerías
import common as t96
import os
import re
import numpy as np 
from nltk.tokenize import RegexpTokenizer
import unicodedata
from sqlalchemy import create_engine

### variables globales
dict_translate_enum_romano = {
    'I': 1,'II': 2,'III': 3,'IV': 4,'V': 5,'VI': 6,'VII': 7,'VIII': 8,'IX': 9,'X': 10,
    'XI': 11,'XII': 12,'XIII': 13,'XIV': 14,'XV': 15,'XVI': 16,'XVII': 17,'XVIII': 18,'XIX': 19,'XX': 20,
    'XXI': 21,'XXII': 22,'XXIII': 23,'XXIV': 24,'XXV': 25,'XXVI': 26,'XXVII': 27,'XXVIII': 28,'XXIX': 29,'XXX': 30,
    'XXXI': 31,'XXXII': 32,'XXXIII': 33,'XXXIV': 34,'XXXV': 35,'XXXVI': 36,'XXXVII': 37,'XXXVIII': 38,'XXXIX': 39,'XL': 40,
    'XLI': 41,'XLII': 42,'XLIII': 43,'XLIV': 44,'XLV': 45,'XLVI': 46,'XLVII': 47,'XLVIII': 48,'XLIX': 49,'L': 50,
    'LI': 51,'LII': 52,'LIII': 53,'LIV': 54,'LV': 55,'LVI': 56,'LVII': 57,'LVIII': 58,'LIX': 59,'LX': 60,
    'LXI': 61,'LXII': 62,'LXIII': 63,'LXIV': 64,'LXV': 65,'LXVI': 66,'LXVII': 67,'LXVIII': 68,'LXIX': 69,'LXX': 70,
    'LXXI': 71,'LXXII': 72,'LXXIII': 73,'LXXIV': 74,'LXXV': 75,'LXXVI': 76,'LXXVII': 77,'LXXVIII': 78,'LXXIX': 79,'LXXX': 80,
    'LXXXI': 81,'LXXXII': 82,'LXXXIII': 83,'LXXXIV': 84,'LXXXV': 85,'LXXXVI': 86,'LXXXVII': 87,'LXXXVIII': 88,'LXXXIX': 89,'XC': 90,
    'XCI': 91,'XCII': 92,'XCIII': 93,'XCIV': 94,'XCV': 95,'XCVI': 96,'XCVII': 97,'XCVIII': 98,'XCIX': 99,'C': 100
}

dict_translate_enum_letras = {
    'UNO': 1,'DOS': 2,'TRES': 3,'CUATRO': 4,'CINCO': 5,'SEIS': 6,'SIETE': 7,'OCHO': 8,'NUEVE': 9,'DIEZ': 10,
    'ONCE': 11,'DOCE': 12,'TRECE': 13,'CATORCE': 14,'QUINCE': 15,'DIECISEIS': 16,'DIECISIETE': 17,'DIECIOCHO': 18,'DIECINUEVE': 19,
    'VEINTE': 20,'VEINTI': 20,'TREINTA': 30,'CUARENTA': 40
}

dict_translate_enum_cardinal = {
    'PRIMERO': 1,'PRIMERA': 1,'SEGUNDO': 2,'SEGUNDA': 2,'TERCERO': 3,'TERCERA': 3,'CUARTO': 4,'CUARTA': 4,'QUINTO': 5,'QUINTA': 5,
    'SEXTO': 6,'SEXTA': 6,'SEPTIMO': 7,'SEPTIMA': 7,'OCTAVO': 8,'OCTAVA': 8,'NOVENO': 9,'NOVENA': 9,'DECIMO': 10,'DECIMA': 10,
    'VIGESIMO': 20,'VIGESIMA': 20,'TRIGESIMO': 30,'TRIGESIMA': 30,'CUADRAGESIMO': 40,'CUADRAGESIMA': 40,'QUINCUAGESIMO': 50,'QUINCUAGESIMA': 50,
    'SEXAGESIMO': 60,'SEXAGESIMA': 60,'SEPTUAGESIMO': 70,'SEPTUAGESIMA': 70,'OCTOGESIMO': 80,'OCTOGESIMA': 80,'NONAGESIMO': 90,'NONAGESIMA': 90,
    'UNDECIMO': 11,'UNDECIMA': 11,'DUODECIMO': 12,'DUODECIMA': 12
}

dict_translate_enum_numero = {}
for i in range(0,999):
    dict_translate_enum_numero[str(i)] = i

path_in_txt = t96.path_tmp_txt
path_in_ocr = t96.path_tmp_ocr

n_max_sublevels = 2

### funciones

# Quita tildes para dejar la sentencia estandar y poder comparar bien con las expresiones reguales
def clean_sentence_list(orig_sent_list):
    clean_list = []
    for sent_element in orig_sent_list:
        temp_sent = sent_element.replace("…","")
        temp_sent = temp_sent.upper()
        # Eliminar tildes y caracteres como ñ o tilde hacia atras (normalización )
        # https://es.stackoverflow.com/questions/135707/c%C3%B3mo-puedo-reemplazar-las-letras-con-tildes-por-las-mismas-sin-tilde-pero-no-l
        # -> NFD y eliminar diacríticos
        temp_sent = unicodedata.normalize("NFKD", temp_sent).encode("ascii","ignore").decode("ascii")
        temp_sent.replace("-"," ")
        clean_list.append(temp_sent)
    return clean_list


def translate_sentence(str_sent):
    
    trim_sent = re.sub('^[\s|\.|\:|\-]*','',str_sent)
    trim_sent = re.sub('[\s|\.|\:|\-]*$','',trim_sent)
    arr_item_sent = re.split('[\s|\.|\:|\-|\,|\)]+', trim_sent.upper())
    pattern_digito = re.compile('[0-9]+')
    
    list_translate = []
    only_num = True
    prev_term = ''
    item_num = ''
    str_sent = ''
    nivel = 0
    
    for term in arr_item_sent:
        num_style = 'NA'
        num_sep = 'NA'
        if only_num:
            if term in dict_translate_enum_numero:
                str_num_term = ('000'+str(dict_translate_enum_numero[term]))[-3:]
                num_style = 'NN'
            elif term in dict_translate_enum_romano:
                str_num_term = ('000'+str(dict_translate_enum_romano[term]))[-3:]
                num_style = 'NR'
            elif term in dict_translate_enum_letras:
                str_num_term = ('000'+str(dict_translate_enum_letras[term]))[-3:]
                num_style = 'NL'
            elif term in dict_translate_enum_cardinal:
                str_num_term = ('000'+str(dict_translate_enum_cardinal[term]))[-3:]
                num_style = 'NC'
            else:
                str_num_term = term
                only_num = False
            
            if prev_term == '':
                if only_num:
                    item_num = str_num_term
                else:
                    str_sent = str_num_term
            else:
                if only_num:
                    item_num = item_num + '.' + str_num_term
                    num_sep = 'NS'
                else:
                    str_sent = str_sent + ' ' + str_num_term
                    num_sep = 'NE'
                nivel+=1
            prev_term = term
        else:
            str_num_term = term
            str_sent = str_sent + ' ' + str_num_term
        list_translate.append([num_sep, str_num_term, num_style])
   
    return list_translate, item_num, str_sent.strip(), nivel
    
    
def pre_filter_items(list_files, path_files='', b_debug=False):
    tokenizer = RegexpTokenizer('\n+\n*[^\w\d]*', gaps=True)
    pattern_numeral = re.compile('^\d\d(\*\*\*NUM_SEP\*\*\*\d\d)*\*\*\*NUM_END\*\*\*')
    pattern_cardinal_combinado_re =  re.compile('^\s*(DECIMO|DECIMA|VIGESIMO|VIGESIMA|TRIGESIMO|TRIGESIMA' + 
                                                '|CUADRAGESIMO|CUADRAGESIMA|QUINCUAGESIMO|QUINCUAGESIMA|SEXAGESIMO|SEXAGESIMA|' + 
                                                'SEPTUAGESIMO|SEPTUAGESIMA|OCTOGESIMO|OCTOGESIMA|NONAGESIMO|NONAGESIMA){1}\s+' + 
                                                '(PRIMERO|PRIMERA|SEGUNDO|SEGUNDA|TERCERO|TERCERA|CUARTO|CUARTA|QUINTO|QUINTA|' + 
                                                'SEXTO|SEXTA|SEPTIMO|SEPTIMA|OCTAVO|OCTAVA|NOVENO|NOVENA){1}(.*)')
    pattern_cardinal_letra = re.compile('^\s*[A-HJ-Za-hj-z]{1}[\)\.\:]{1}\s*')
    dict_texto_capitulo = {'RESUELVE', 'DECISION'}

    list_indexes_all_files = []
    b_resuelve = False

    for txt_file in list_files:
        print(txt_file)

        if txt_file[-4:] == '.txt':
            if b_debug: print("File: '",path_files+txt_file,"'")
            with open(path_files+txt_file, encoding="utf8") as text_file_name:
                data =  text_file_name.readlines()

            data_text = ''.join(data)
            # data_text = '2 3 0 0 1 3 1 2 1 0 0 3 2 0 1 6 0 0 1 7 7 0 0 '
            if b_debug: print("data_text:", data_text)
            l2 = []

            sent_list = tokenizer.tokenize(data_text)
            
            l1_clean = clean_sentence_list(sent_list)
            if b_debug: print("Token: ")
            if b_debug: [print(l1_clean.index(s)+1,'\t' + "'" + s + "'") for s in l1_clean]
            
            # if b_debug: print("Clean de data")
            # if b_debug: print(["'" + s + "'" for s in clean_sentence_list(data)])
            # for s in clean_sentence_list(data):
            #     for c in s:
            #         if b_debug: print(c, ' = ', ord(c))
            

            l1_clean_orig = [re.sub('[^\w\d]*(.*)\n*','\g<1>',sentence).strip() for sentence in clean_sentence_list(data)]
            if b_debug: print("Original: ")
            if b_debug: [print(l1_clean_orig.index(s)+1,'\t' + "'" + s + "'") for s in l1_clean_orig]

            b_resuelve = True
                
            for sentence in l1_clean:
                int_replace = 0
                sent_orig = sentence
                sentence = re.sub('[\s\)\|\:\¡\!\/]*$','',sentence)
                sentence = re.sub('^([B-NP-XZ0]{1}\s)?','',sentence).strip()
                
                if sentence in dict_texto_capitulo:
                    token_line = l1_clean.index(sent_orig)
                    real_line = l1_clean_orig[max(0,token_line-1):].index(sent_orig.strip()) + max(0,token_line-1) + 1
                    if b_debug: print("Buscando: '", sent_orig, "' desde ", token_line, " = ", real_line)
                    l2.append([txt_file, real_line, sent_orig[0:70], 0, ['NA']]) 
                    b_resuelve = True
                if b_resuelve:
                    if pattern_cardinal_combinado_re.match(sentence):
                        rep_sent =  re.sub('^\s*(DECIMO|DECIMA|VIGESIMO|VIGESIMA|TRIGESIMO|TRIGESIMA' + 
                                           '|CUADRAGESIMO|CUADRAGESIMA|QUINCUAGESIMO|QUINCUAGESIMA|SEXAGESIMO|SEXAGESIMA|' + 
                                           'SEPTUAGESIMO|SEPTUAGESIMA|OCTOGESIMO|OCTOGESIMA|NONAGESIMO|NONAGESIMA){1}\s*' + 
                                           '(PRIMERO|PRIMERA|SEGUNDO|SEGUNDA|TERCERO|TERCERA|CUARTO|CUARTA|QUINTO|QUINTA|' + 
                                           'SEXTO|SEXTA|SEPTIMO|SEPTIMA|OCTAVO|OCTAVA|NOVENO|NOVENA){1}(.*)',
                                           '\g<1>***SEP_COM***\g<2>***SEP_SEN***\g<3>',
                                           sentence)
                        arr_cc = rep_sent.split('***SEP_SEN***')
                        arr_cc2 = arr_cc[0].split('***SEP_COM***')
                        if b_debug: print("Encontrado: ", sent_orig, arr_cc, arr_cc2)
                        new_sent = str(dict_translate_enum_cardinal[arr_cc2[0]]+dict_translate_enum_cardinal[arr_cc2[1]])+' '.join(arr_cc[1:])
                        int_replace = 1
                    else:
                        if pattern_cardinal_letra.match(sentence):
                            arr_cc = re.split('\)|\.|\:', sentence)
                            new_sent = str(ord(arr_cc[0].strip())-64)+' '.join(arr_cc[1:])
                            int_replace = 2
                        else:
                            new_sent = sentence

                    trim_sent = re.sub('^[\s|\.|\:|\-]*','',new_sent)
                    if b_debug: print("------PREV:", trim_sent)
                    tran_list, item_num, text_line, item_lev = translate_sentence(trim_sent)
                    if int_replace==1:
                        tran_list[0][2] = 'NC' # Numero Romano
                    if int_replace==2:
                        tran_list[0][2] = 'NX' # Numeración con letras
                    if b_debug: print("------POST:", tran_list, text_line, tran_list[-1:][0][0])

                    if item_num!='':
                        arr_text = re.split('\,|\.', text_line)
                        if arr_text[0].strip()!="" and tran_list[-1:][0][0]!='NS':
                            token_line = l1_clean.index(sent_orig)
                            if b_debug: print("'" + sentence + "'")
                            try:
                                real_line = l1_clean_orig[max(0,token_line-1):].index(sent_orig.strip()) + max(0,token_line-1) + 1
                            except:
                                real_line = real_line + 1
                            if b_debug: print("Buscando: '", sentence, "' desde ", token_line, " = ", real_line)
                            # busca si es un dividor de capitulos
                            if re.sub('[\s\)\|\:\¡\!\/]*$','',arr_text[0][0:70]).strip() in dict_texto_capitulo:
                                token_line = l1_clean.index(sent_orig)
                                real_line = l1_clean_orig[max(0,token_line-1):].index(sent_orig.strip()) + max(0,token_line-1) + 1
                                if b_debug: print("Buscando: '", sentence, "' desde ", token_line, " = ", real_line)
                                l2.append([txt_file, real_line, arr_text[0][0:70], 0, ['NA']]) 
                            else:
                                l2.append([txt_file, real_line, arr_text[0][0:70], item_num, [s[2] for s in tran_list[0:item_lev]]]) 

            list_indexes_all_files.extend(l2)

    return list_indexes_all_files


def confirm_next_item(actual_item, actual_style, new_item, new_style):
    al = len(actual_item) #cantidad de niveles del actual

    while len(actual_style)<al:
        actual_style.append('NN') # es el default
    actual_style = actual_style[0:al] # si hay mas estilos que numeros, recorta
    
    nl = len(new_item) # cantidad de niveles del nuevo
    
    while len(new_style)<nl:
        new_style.append('NN') # es el default
    new_style = new_style[0:nl] # si hay mas estilos que numeros, recorta

    chk_comp_new = False
    b_consecutivo = False
    nivel = 0    
    
    kid = 0
    b_identico = True
    b_mismo_estilo = True
    delta_nivel = 0
    while b_identico and kid<al and kid<nl: #si hay más elementos
        delta_nivel = int(new_item[kid]) - int(actual_item[kid])
        if new_style[kid]!='' and actual_style[kid]!='' and new_style[kid]!=actual_style[kid]: # si tienen el mismo valor o formato
            b_identico = False
            b_mismo_estilo = False
        else:
            if delta_nivel!=0:
                b_identico = False
            else:
                kid+=1
    
    if kid < al and kid < nl: # sobran cifras en ambos, se debe calcular el delta
        if b_mismo_estilo: # si tienen el mismo estilo en ese nivel
            if delta_nivel==1:
                # ver que sean solo 0 y 1 
                chk_comp_new = True
            else:
                b_consecutivo = False
                nivel = 0               
        else:
            b_consecutivo = False
            nivel = 0               
    else:
        if kid < nl: # si quedan cifras en el new, se debe validar que sean solo 0 y 1 
            chk_comp_new = True
        else: # no es aceptado como consecutivo en este nivel
            b_consecutivo = False
            nivel = 0

    if chk_comp_new:
        b_ceros = True
        b_unos = True
        i = kid+1
        while (b_ceros or b_unos) and i<nl: # valida que el resto de items del nuevo sean cero
            if new_item[i]!=0:
                b_ceros = False
            if new_item[i]!=1:
                b_unos = False
            i+=1
        
        if (b_ceros or b_unos): # cumple con todo, se acepta como consecutivo
            b_consecutivo = True
            nivel = kid
        else:
            b_consecutivo = False
            nivel = 0
        
    return b_consecutivo, nivel


def print_index_file(final_index, n_level=3):
    if len(final_index)==0:
        print("Archivo sin resultados: ", final_index)
    else:
        print("\nArchivo: ", final_index[0][0])
        for item in final_index:
            titulo = re.sub('[^\d\w\.\:\s\-]*\n*', '', item[2]).strip()
            numeral = '.'.join([str(i) for i in item[3] if i!=0])
            if len(numeral.split('.'))<=n_level:
                print((numeral+' '*20)[0:10], ' ', titulo, '.'*(100-len(titulo)-len(str(item[1]))), item[1])


def save_index_file(final_index, DBengine, n_level=3, sType='Completo'):
    if len(final_index)!=0:
        strSQLDelete = "delete from tt_indice_sentencia where key = '" + str(final_index[0][0].split('.')[0]) + "'"
        DBengine.execute(strSQLDelete)
        for item in final_index:
            titulo = re.sub('[^\d\w\.\:\s\-]*\n*', '', item[2]).strip()
            numeral = '.'.join([str(i) for i in item[3] if i!=0])
            linea_num = item[1]
            if len(numeral.split('.'))<=n_level:
                DBengine.execute("insert into tt_indice_sentencia (key, numeral, texto, linea, tipo) values ('" + 
                                 final_index[0][0].split('.')[0] + "','" + str(numeral) + "','" + 
                                 str(titulo) + "'," + str(linea_num) + ",'" + sType + "')")


def generate_index_file(option_list, q_sublevels=5, n_level_id=[], style_level_id=[], chapter=1, b_debug=False):
    
    ident = '\t'*(max(len(n_level_id),q_sublevels)-q_sublevels)
    if b_debug: print(ident, "---BP00 Inicio---")
    final_index = []
    jump_list = []

    if q_sublevels!=0:
        if len(n_level_id)==0:
            n_level_id = [0]*q_sublevels
            style_level_id = ['']*q_sublevels
        if b_debug: print(ident, "BP10 n_level_id: ", n_level_id, style_level_id)
        if b_debug: print(ident, "BP20: q: ", option_list)
        for line in option_list:
            b_insert_item = False
            file_name, file_line, line_text, item_num, style_list = line[0], line[1], line[2], line[3], line[4]
                
            if b_debug: print(ident, "BP30: ", item_num, " : ", line_text, style_list)
            if item_num==0 and len(option_list)>1: # si no tiene item (posible capitulo) y hay más de 1 en la lista, lo deja al final
                if b_debug: print(ident, "BP35: Salto capitulo ", line)
                jump_list.append(line)
            else:
                max_q = max(q_sublevels,len(n_level_id)) # determina de cuantos elementos debe estar compuesto el ID
                arr_levels = [] # Niveles del item actual
                arr_styles = [] # Estilos de los niveles del item actual

                if len(n_level_id)>q_sublevels: # cuando esto pasa se entiende que está dentro de una funcion recursiva
                    arr_levels = n_level_id[:-q_sublevels] # toma los primeros niveles para completar el array
                    arr_styles = style_level_id[:-q_sublevels]
                arr_levels.extend([int(i) for i in str(item_num).split('.')[0:q_sublevels]]) # completa el nivel con el numeral actual
                arr_styles.extend([i for i in style_list[0:q_sublevels]]) # completa el nivel con el numeral actual

                while len(arr_levels) < max_q: # completa al nivel del recursivo
                    arr_levels.append(0)
                    arr_styles.append('')
                    
                b_valido,_ = confirm_next_item(n_level_id, style_level_id, arr_levels, arr_styles)
                if b_debug: print(ident, "BP39: b_valido ", b_valido, n_level_id, style_level_id, arr_levels, arr_styles)
                if b_valido:
                    if b_debug: print(ident, "BP40: Aprobado por la funcion ", n_level_id, arr_levels)
                    # se revisa si este es el único para insertar, va directo
                    # o si este sería el primer dato de la lista
                    if len(jump_list)==0 or (n_level_id[0]==0 and arr_levels[0]==1): 
                        b_insert_item = True
                    else: # revisa los que tiene como opcionados
                        if b_debug: print(ident, "BP50 - Recursivo: ", n_level_id[len(n_level_id)-q_sublevels])
                        if n_level_id[len(n_level_id)-q_sublevels]!=0:
                            # solo baja de nivel cual en el nivel actual no va en cero la numeración
                            if b_debug: print(ident, "BP51 - Pendientes: ", jump_list)
                            if jump_list[0][3] == 0: # se insertó como un posible capitulo
                                if b_debug: print(ident, "BP52 - Nuevo capitulo ", jump_list[0])
                                chapter+=1
                                final_index.append([jump_list[0][0], 
                                                    jump_list[0][1], 
                                                    '*****' + str(jump_list[0][2]) + ' - CAP(' + str(chapter) + ')*****', 
                                                    [0] * max(q_sublevels,len(n_level_id))])
                                n_level_id = [0] * q_sublevels
                                style_level_id = [''] * q_sublevels
                                arr_levels = n_level_id
                                arr_styles = style_level_id
                                if b_debug: print(ident, "BP53 - niveles: ", n_level_id, arr_levels)
                                tout_1, tout_2, tout_3 = generate_index_file(jump_list[1:],q_sublevels, n_level_id, style_level_id, b_debug=b_debug)
                            else:
                                jump_list.append(line)
                                if b_debug: print(ident, "BP54 - niveles: ", n_level_id, arr_levels, jump_list, q_sublevels-1, n_level_id, style_level_id)
                                tout_1, tout_2, tout_3 = generate_index_file(jump_list, q_sublevels-1, n_level_id, style_level_id, b_debug=b_debug)
                                if b_debug: print(ident, "BP54A - termina llamado recursivo: ", tout_1, tout_2, tout_3)
                            n_level_id = tout_2
                            style_level_id = tout_3
                        
                            if len(tout_1)>0:
                                if b_debug: print(ident, "Fusion de ", len(tout_1), " filas.")
                                final_index.extend(tout_1)
                                if b_debug: print(ident, "BP55 - Validar último item: ", n_level_id, line_text, " vs tout_1 ", tout_1)
                                if tout_1[-1:][0][2]!=line_text: # la fila actual no fue insertada, pero a este nivel si es válida
                                    if b_debug: print(ident, "BP56 - Recuperar último item: ", n_level_id, line_text)
                                    b_insert_item = True
                            else:
                                b_insert_item = True
                        else:
                            b_insert_item = True
                        jump_list = []
                        if b_debug: print(ident, "BP59 - Finalizada recursividad: ")
                    if b_insert_item: # esta es la funcion básica de inserción de la funcion recursiva
                        n_level_id = [i for i in arr_levels]
                        style_level_id = [i for i in arr_styles]
                        final_index.append([file_name, file_line, line_text, n_level_id])
                        if b_debug: print(ident, "Inserta: ", arr_levels, " (", arr_styles, ") : ", line_text)
                        jump_list = []
                else:
                    jump_list.append(line)  
        # Aqui termina el For

        if len(jump_list)!=0 and n_level_id[len(n_level_id)-q_sublevels]!=0:
            # solo baja de nivel cuando hay posibilidades saltadas en numeración y el nivel actual es distinto de cero
            if b_debug: print(ident, "BP60 - Complemento Recursivo: ", jump_list)
            if jump_list[0][3] == 0: # se insertó como un posible capitulo
                chapter+=1
                final_index.append([jump_list[0][0], 
                                    jump_list[0][1], 
                                    '*****' + str(jump_list[0][2]) + ' - CAP(' + str(chapter) + ')*****', 
                                    [0] * max(q_sublevels,len(n_level_id))])
                n_level_id = [0] * q_sublevels
                style_level_id = [''] * q_sublevels
                arr_levels = n_level_id
                arr_styles = style_level_id
                if b_debug: print(ident, "BP61 - niveles: ", n_level_id, arr_levels)
                tout_1, tout_2, tout_3 = generate_index_file(jump_list[1:], max(q_sublevels,len(n_level_id)), 
                                                             n_level_id, style_level_id, b_debug=b_debug)
                # arr_levels = tout_2
                if b_debug: print(ident, "BP62 - niveles: ", n_level_id, arr_levels)
            else:
                tout_1, tout_2, tout_3 = generate_index_file(jump_list, q_sublevels-1, n_level_id, 
                                                             style_level_id, b_debug=b_debug)

            final_index.extend(tout_1)
            n_level_id = tout_2
            style_level_id = tout_3
    
    if b_debug: print(ident, "BP99 Termina: ", n_level_id, final_index)
    return final_index, n_level_id, style_level_id


### main
engine = create_engine(t96.sqlConnString)
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Autoindex','Inicia proceso')")

list_files_text = os.listdir(path_in_txt)
list_files_ocr = os.listdir(path_in_ocr)

# cálculo de indice para corpus text
temp_list_index_items_text = pre_filter_items(list_files_text, path_in_txt, False)
list_files_index_text = np.unique([item[0] for item in temp_list_index_items_text])

for file_name in list_files_index_text:
    index_items_text, _, _ = generate_index_file([item for item in temp_list_index_items_text if item[0]==file_name], q_sublevels=n_max_sublevels, b_debug=False)
    save_index_file(index_items_text, engine, sType='Completo', n_level=n_max_sublevels)

# cálculo de indice para corpus ocr
temp_list_index_items_ocr = pre_filter_items(list_files_ocr, path_in_ocr, False)
list_files_index_ocr = np.unique([item[0] for item in temp_list_index_items_ocr])

for file_name in list_files_index_ocr:
    index_items_ocr, _, _ = generate_index_file([item for item in temp_list_index_items_ocr if item[0]==file_name], q_sublevels=n_max_sublevels, b_debug=False)
    save_index_file(index_items_ocr, engine, sType='Completo', n_level=n_max_sublevels)

engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Autoindex','Fin proceso')")