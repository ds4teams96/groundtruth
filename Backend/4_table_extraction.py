#!/usr/bin/python
# -*- coding: latin-1 -*-

import numpy as np
### importacion de librerías
import pandas as pd
import seaborn as sns;
sns.set()
import math
import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
import re, string
from collections import Counter
from sklearn.cluster import KMeans
from collections import ChainMap
import geopandas
import warnings
warnings.filterwarnings('ignore')
from difflib import SequenceMatcher
from sqlalchemy import create_engine

### variables globales

path_input = 'data'
path_input_txt = 'tmp/text'
path_input_ocr = 'tmp/ocr'

file_in_dicc_csv = 'Dicc_Stop.csv'
file_in_geojson = 'shp_sinap.geojson'

file_ids_text = ".*.txt"
file_ids_ocr = ".*.txt"

pd.options.mode.chained_assignment = None

my_stop_words_names = ["TIERRAS","Y","RADICADO","OPOSITORES"]
my_stop_words_descapitalize = ["Cd","Representante","Examinado","Titulo","Ibague","Tolima","Credito","Agrario","Vereda",
                               "Año","Justicia","Transicional","Teoria","Sistema","Nacional","Paragrafo","Sala","Civil",
                               "Especializada","La","Exp","Valledupar","Mundo","Opositores","Señor","Opositor","Y","El",
                               "Rad","Magistrado","Ponente","Tierras","Accionante","Radicado","No","Codigo","Derechos",
                               "Unidad","Tambien","Bogota","Juzgado","Especializado","Sentencia","Pretende","Colombia",
                               "Tribunal","Superior","Resguardo","Indigena","Cucuta","Proyecto","Consecutivo","Expediente",
                               "Municipio","Pagina","Corte","Interamerican","Pueblo","Caja","Por","En","Relacion","Al",
                               "Partimos","Comp","Campo","Circuito","V","Alcaldia","Internacional","Distrito","Judicial",
                               "Cartagena","Gelpud","Consejo","Super","Bajo","Incluido","Desplazamiento","Monteria",
                               "Consejo","Comunitario","Renacer","Timbiqui","Notaria","Decimo","Ordenar","Victimas",
                               "Antioquia","Agropecuaria","Carmen De Bolivar","Colombiano","Bienestar","Cuaderno","Ppal"]
                               
stop_municipio = ["Departamento","Corregimiento","Vereda","Bloque","Policia","Municipio"]
txt_control = ["De","Los","Las","de","los","las"]

Punta_Gallinas=12.4461111111111
Rio_Amazonas =-4.20833333333333
Cabo_Manglares=79.0425
Isla_San_Jose =66.8483333333333

key_juez=['juez','jueza','j u e z']
key_magister=['magistrado','magistrada','magistrados','magis','rada','rado','gistrad','magis rado','Mag.']
key_magister2=['juez','magistrado','jueza','magistrada','magistrados']
key_ponente=['ponente']
black_list_magistrado=['magistrado','ponente','promiscuo','magistrados','oficinas','registro','instrumentos','públicos',
                       'juez','municipal','coyaima','tol','JuezRadicado','magistrada','Magistra','jueza',
                       'primero','segundo','tercero','gistrada','rada','magis','Magis rado']

key_tribunal1=['tribunal superior del','tribunal superior de']
key_opositor=['opositor','opone','opositores','oponen','opositora']
key_opositor2=['oposición','oposocion']
black_list_opositor=['opositor','opone','opositores','oponen','opositora','Resolución','nro','OPOSICION','es','se']

ordinales = [["PRIMERO"],
             ["SEGUNDO"],
             ["TERCERO"],
             ["CUARTO"],
             ["QUINTO"],
             ["SEXTO"],
             ["SÉPTIMO"],
             ["OCTAVO"],
             ["NOVENO"],
             ["DÉCIMO"],
             ["UNDÉCIMO","DÉCIMO PRIMERO"],
             ["DUODÉCIMO","DÉCIMO SEGUNDO"],
             ["DÉCIMO TERCERO"],
             ["DÉCIMO CUARTO"],
             ["DÉCIMO QUINTO"],
             ["DECIMO SEXTO"],
             ["DECIMO SÉPTIMO"],
             ["DECIMO OCTAVO"],
             ["DÉCIMO NOVENO"],
             ["VIGÉSIMO"],
             ["VIGÉSIMO PRIMERO"],
             ["VIGÉSIMO SEGUNDO"],
             ["VIGÉSIMO TERCERO"],
             ["VIGÉSIMO CUARTO"],
             ["VIGÉSIMO QUINTO"],
             ["VIGÉSIMO SÉPTIMO"],
             ["VIGÉSIMO OCTAVO"],
             ["VIGÉSIMO NOVENO"],
             ["TRIGÉSIMO"],
             ["TRIGÉSIMO PRIMERO"],
             ["TRIGÉSIMO SEGUNDO"],
             ["TRIGÉSIMO TERCERO"],
             ["TRIGÉSIMO CUARTO"],
             ["TRIGÉSIMO QUINTO"],
             ["TRIGÉSIMO SEXTO"],
             ["TRIGÉSIMO SÉPTIMO"],
             ["TRIGÉSIMO OCTAVO"],
             ["TRIGÉSIMO NOVENO"],
             ["CUADRAGÉSIMO"],
             ["CUADRAGÉSIMO PRIMERO"],
             ["CUADRAGÉSIMO SEGUNDO"],
             ["CUADRAGÉSIMO TERCERO"],
             ["CUADRAGÉSIMO CUARTO"],
             ["CUADRAGÉSIMO QUINTO"],
             ["CUADRAGÉSIMO SEXTO"]]

# Funciones

def list_concordances_ltc(list_concors):
    list_temp1 = [list_concor.lower() for list_concor in list_concors]
    list_temp2 = [list_concor.upper() for list_concor in list_concors]
    list_temp3 = [list_concor.capitalize() for list_concor in list_concors]
    return list_temp1 + list_temp2 + list_temp3

def replace_accents(text):
    a,b = 'áéíóúüÁÉÍÓÚ','aeiouuAEIOU'
    trans = str.maketrans(a,b)
    return text.translate(trans)
    
def names_prob(raw):
    text_List_result = []
    text_List = nltk.Text(word_tokenize(raw))
    list_concordances = ["solicitante","solicitantes",
                         "ponente","ponentes",
                         "instaurada","instauradas","formulada","resuelve",
                         "representación",
                         "favor","reconocer","compense","reparación",
                         "víctimas","víctima"] # Sobreajusta ,"señor","señora","señores","reclamante","reclamantes"]
    list_exceptions = ["testigo"]
    text_List_result = []        
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(list_concordance, width=280)
        if len(text_List_temp)>0:
            text_List_temp_copy = text_List_temp
            for elem in text_List_temp_copy:
                for exceptions in list_exceptions:
                    if exceptions in elem[5] and elem in text_List_temp:
                        text_List_temp.remove(elem)
            text_List_temp = [elem[5] for elem in text_List_temp]                        
            text_List_result = text_List_result + text_List_temp

    results =  set(text_List_result)
    results = ' punto de interrupcion entre sustantivos '.join(results)
    results = replace_accents(results)
    results = re.sub(","," separador nombre ",results)
    results = re.sub('[%s]'%re.escape(string.punctuation),' ',results)
    regex = r"\b[A-Z][A-Z]+\b"
    replaceds = set(re.findall(regex, results))
    replaceds = [w for w in replaceds if not w in my_stop_words_names]
    for replaced in replaceds:
        results = re.sub(rf"\b{replaced}\b"," "+replaced.capitalize()+" ",results)
    for descapitalize in my_stop_words_descapitalize:
        results = re.sub(rf"\b{descapitalize}\b"," "+descapitalize.lower()+" ",results)
    results = re.sub(' +', ' ',results)    
    
    return results

def get_human_names(text):
    person_list = []
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)

    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        person = []
        name = ""
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1:
            for part in person:
                name += part + ' '
            person_list.append(name) 
    
    person_list = list(map(str.strip, person_list))
    person_list = [elem.title() for elem in person_list]
    return person_list 

def max_values(dict_def):
    return {name_def:n_def for name_def, n_def in dict_def.items() if n_def == max(list(dict_def.values()))}

def dict_reduce(mydict):
    intro = True 
    while intro:
        intro = False
        mydict_copy = mydict.copy()
        for name_search, n_search in mydict_copy.items():
            mydict_temp = {}
            for name_dic, n_dic in mydict.items():
                if name_search != name_dic:
                    if name_search in name_dic:
                        mydict_temp.setdefault(name_dic,mydict[name_dic])
            if len(mydict_temp)>0:
                mydict_temp = max_values(mydict_temp)
                #verificar casos mayores que len > 1
                mydict[list(mydict_temp.keys())[0]] = list(mydict_temp.values())[0] + n_search 
                del mydict[name_search]
                intro = True
    return mydict   

def dict_create(file, corpus_temp):
    person_names=[]
    results = names_prob(corpus_temp.raw(file)) 
    person_names = set(get_human_names(results))    
    if len(person_names)>0:
        dict_create_temp = dict_reduce({person_name:results.count(person_name) for person_name in person_names if results.count(person_name)>1})
    else:
        dict_create_temp = {}
    return dict_create_temp

def create_pp(df,km):
    list_pp = []
    list_prob = []    
    for a, b in zip(df.Cluster, km.labels_): 
        if a == "Principal":
            cluster_p = b
            break
    for a, b, c in zip(df.Cluster, km.labels_, df.index):
        if b == cluster_p:
            if a == "Principal":
                list_pp.append("Principal")
                list_prob.append({c:1})
            else:
                list_pp.append("Probable")
                list_prob.append({c:0})
        else:
            list_pp.append("No Problable")
    return list_prob, list_pp

def create_ps(df):
    list_pp = []
    list_prob = []
    cnt = 0
    for a, b, c in zip(df.Cluster, df.Weigth, df.index):
        if cnt == 0:
            at, bt, ct = a, b, c
        else:
            if bt == b:
                list_pp, list_prob = ["Principal"]*2, [{ct:1},{c:1}]
            elif bt > b:
                if 0 < bt-b < 0.25:
                    list_pp, list_prob = ["Principal","Probable"], [{ct:1},{c:0}]
                else:
                    list_pp, list_prob = ["Principal","No Probable"], [{ct:1}]
            else:
                if 0 < b-bt < 0.25:
                    list_pp, list_prob = ["Probable","Principal"], [{ct:0},{c:1}]
                else:
                    list_pp, list_prob = ["No Probable","Principal"], [{c:1}]                
        cnt+=1    
    return list_prob, list_pp


def select_best(file, corpus_temp):
    df_names = pd.DataFrame(columns=['Name', 'Count'])
    list_prob = {}
    dict_names = dict_create(file, corpus)
    if dict_names != {}:
        df_names = pd.DataFrame([[key, dict_names[key]] for key in dict_names.keys()], columns=['Name', 'Count'])
        df_names["Weigth"] = df_names.Count / df_names.Count.sum()
        df_names["std"] = (df_names.Count - df_names.Count.mean()) / df_names.Count.std()
        df_names["odd_Ratio"] = (df_names.Count / df_names.Count.sum()) / (1 / df_names.Count.count())
        df_names["prepro_1x"] = 1 / df_names.Count
        df_names["Cluster"] = np.where(df_names['Count'] == df_names['Count'].max(), 'Principal', 'No probables')
        df_names.index = df_names.Name
        df_names.drop(['Name'], axis='columns', inplace=True)
        if df_names.shape[0] > 1:
            if df_names.shape[0] == 2:
                list_prob, df_names["Cluster"] = create_ps(df_names)
            else:
                df_names["Cluster_1D"] = KMeans(n_clusters=2).fit(np.array(df_names['Count']).reshape(-1, 1)).labels_
                kmeans = KMeans(n_clusters=2)
                if len(df_names.Count.unique()) > 1:
                    y_kmeans = kmeans.fit(df_names[["std", "odd_Ratio", "prepro_1x"]])
                    list_prob, df_names["Cluster"] = create_pp(df_names, kmeans)
                else:
                    list_pp = []
                    list_prob = []
                    for a, c in zip(df_names.Count, df_names.index):
                        list_pp.append("Principal")
                        list_prob.append({c: 1})
                    list_prob, df_names["Cluster"] = list_prob, list_pp
        else:
            list_prob = [{df_names.index[0]: 1}]
    else:
        print("Proceso de busqueda Nombre Solicitante no ha encontrado coincidencias")

    return df_names, list_prob


def DNI_prob(file, corpus_temp, filter_name):
    text_List = word_tokenize(replace_accents(corpus_temp.raw(file)))
    text_List = nltk.Text(text_List)
    list_concordances = ["cedula", "cedulas", "C.C.N", "C.C", "CC", "C.C.N.°"]
    text_List_result = []

    for concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(concordance, width=360)
        if len(text_List_temp) > 0:
            text_List_temp = [elem[6] for elem in text_List_temp]
            text_List_result += text_List_temp
    list_filter = [filter_name]
    results = []
    for elem_f in list_concordances_ltc(list_filter):
        for text_result in text_List_result:
            if bool(re.search(rf"{elem_f}.+", text_result)):
                results.append(re.search(rf"{elem_f}.+", text_result).group())
    regex = r"\d+\s*[.]*\s*\d+\s*[.]*\s*\d+\s*[.]*\s*\d+\s*[.]*\s*"
    list_cc = []
    cnt = 0
    for each in results:
        intro = True
        cnt += 1
        list_cc_temp = []
        cnt_cc, temp_star, acu_dist_cc, value_dist_cc = 0, 0, 0, 0
        for match in re.finditer(regex, each):
            cc = clean_number(match.group())
            if 999999 < cc < 1500000000:
                if intro:
                    each_names = get_nucleo_names2(clean_step2(each[0:match.start()]))
                    intro = False
                cnt_cc += 1
                if cnt_cc > 1: value_dist_cc = match.start() - len(str(cc)) - temp_star
                acu_dist_cc += value_dist_cc
                list_cc_temp.append(
                    {"Id": cnt, "order": cnt_cc, "CC": cc, "dist_name": match.start(), "dist_icc": value_dist_cc,
                     "n_apriori": len(each_names)})
                temp_star = match.start()
        for i, each_dic in enumerate(list_cc_temp):
            each_dic["size"] = len(list_cc_temp)
            each_dic["avg_icc"] = acu_dist_cc / len(list_cc_temp)
            if len(each_names) >= len(list_cc_temp):
                each_dic["inv_ord"] = cnt_cc - i
                each_dic["weight"] = (cnt_cc - i) / ((len(list_cc_temp) * (len(list_cc_temp) + 1)) / 2)
            else:
                if len(each_names) != 1:
                    each_dic["inv_ord"] = cnt_cc - len(each_names) + 1 - i
                    each_dic["weight"] = 2 / (cnt_cc + 1) if each_dic["inv_ord"] == 1 else 1 / (cnt_cc + 1)
                else:
                    if each_dic["avg_icc"] > 25:
                        each_dic["inv_ord"] = cnt_cc - i
                        each_dic["weight"] = (cnt_cc - i) / ((len(list_cc_temp) * (len(list_cc_temp) + 1)) / 2)
                    else:
                        each_dic["inv_ord"] = cnt_cc - len(each_names) + 1 - i
                        each_dic["weight"] = 2 / (cnt_cc + 1) if each_dic["inv_ord"] == 1 else 1 / (cnt_cc + 1)

            list_cc.append(each_dic)
    return results, list_cc

def clean_number(txt_cc):
    txt_cc = txt_cc.replace(".", "")
    txt_cc = txt_cc.replace(" ", "")
    return int(txt_cc)

def list_concordances_CC(list_concors):
    list_temp1 = [list_concor.upper() for list_concor in list_concors]
    return list_concors + list_temp1
 
 
def radicado_prob(file, corpus_temp):
    text_List = word_tokenize(corpus_temp.raw(file).replace("\r\n", " ~ "))
    text_List = nltk.Text(text_List)
    list_concordances = ["Solicitud","Radicación","Radicado","Ref",
                         "Rad","CIU","Pág","Tribunal","Sentencia","Prescripción",
                         "Acción","Expediente"]
    text_List_result = []    
    
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(list_concordance, width=90)
        if len(text_List_temp)>0:
            text_List_temp = [elem[6] for elem in text_List_temp]
            text_List_result = text_List_result + text_List_temp
    text_List_result =  list(set(text_List_result))
    results = ''.join(text_List_result)
    results = results.replace(" ", "").replace("i", "1").replace("I", "1").replace("Í", "1").replace("o", "0").replace("O", "0").replace("W", "4").replace("N0.", "").replace(".", "").replace("-", "")  
    regex = r"\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*"
    radicado = re.findall(regex, results)
    radicado = [clean_radicado(rad) for rad in radicado if clean_radicado(rad) != ""]
    radicado = Counter(radicado)
    return dict_reduce(radicado)

def clean_radicado(txt_rad):
    boolean = False
    txt_rad = txt_rad.replace("_", "")
    txt_rad = txt_rad.replace("-", "")
    txt_rad = txt_rad.replace(".", "")
    txt_rad = txt_rad.replace(" ", "")
    if 22 <= len(txt_rad) <= 24:
        return txt_rad.lstrip('+-0')
    elif 8 <=len(txt_rad) <= 12:
        if str(int(txt_rad[0:5])) in [str(year) for year in range(2000,2023)]:
            return txt_rad[1:].lstrip('+-0')
        elif str(int(txt_rad[0:4])) in [str(year) for year in range(2000,2023)]:
            return txt_rad.lstrip('+-0')
        else:
            return ""
    else:
        return ""
    
def select_best_rad(file, corpus_temp):
    df_names = pd.DataFrame(columns=['Radicado', 'Count'])
    list_prob = {}
    dict_names = radicado_prob(file, corpus_temp)
    if dict_names != {}:
        df_names = pd.DataFrame([[key, dict_names[key]] for key in dict_names.keys()], columns=['Radicado', 'Count'])
        df_names["Weigth"]=df_names.Count/df_names.Count.sum()        
        df_names["std"]=(df_names.Count-df_names.Count.mean())/df_names.Count.std()
        df_names["odd_Ratio"] = (df_names.Count/df_names.Count.sum())/(1 / df_names.Count.count())
        df_names["prepro_1x"] = 1 / df_names.Count
        df_names["Cluster"] = np.where(df_names['Count'] == df_names['Count'].max(), 'Principal', 'No probables')
        df_names.index = df_names.Radicado
        df_names.drop(['Radicado'], axis = 'columns', inplace=True)
        if df_names.shape[0]>1:
            if df_names.shape[0]==2:
                list_prob, df_names["Cluster"] = create_ps(df_names)            
            else:
                df_names["Cluster_1D"] = KMeans(n_clusters=2).fit(np.array(df_names['Count']).reshape(-1,1)).labels_
                print(df_names)
                kmeans = KMeans(n_clusters=2)    
                y_kmeans = kmeans.fit(df_names[["Weigth","odd_Ratio","prepro_1x"]])
                list_prob, df_names["Cluster"] = create_pp(df_names,kmeans)
        else:
            list_prob = [{df_names.index[0]:1}]
    else:
        print("Proceso de busqueda Radicado no ha encontrado coincidencias")
    return df_names, list_prob  
    
def Matricula_Inmobiliaria_prob(file, corpus_temp):
    text_List = word_tokenize(corpus_temp.raw(file).replace("\r\n", "").replace("inmobil iaria","inmobiliaria").replace("lnmobiliaria","inmobiliaria").replace("I n m o b i l i a r i a","inmobiliaria"))
    text_List = nltk.Text(text_List)
    list_concordances = ["Inmobiliaria","FMI","M.I"]
    
    text_List_result = []
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(list_concordance, width=100)
        if len(text_List_temp)>0:
            text_List_temp = [elem[5] for elem in text_List_temp]
            text_List_result = text_List_result + text_List_temp
    text_List_result =  list(set(text_List_result))
    results = ''.join(text_List_result)
    results = results.replace(" ", "").replace(".", "").replace("-", "").replace("_", "")  
    regex = r"\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*"
    Matricula_Inmobiliaria = re.findall(regex, results)
    Matricula_Inmobiliaria = [clean_radicado(mi) for mi in Matricula_Inmobiliaria if clean_radicado(mi) != ""]
    Matricula_Inmobiliaria = Counter(Matricula_Inmobiliaria)
    return dict_reduce(Matricula_Inmobiliaria)

def clean_radicado(txt_rad):
    boolean = False
    txt_rad = txt_rad.replace("_", "")
    txt_rad = txt_rad.replace("-", "")
    txt_rad = txt_rad.replace(".", "")
    txt_rad = txt_rad.replace(" ", "")
    return txt_rad.lstrip('+-0')


def select_best_m_inm(file, corpus_temp):
    df_names = pd.DataFrame(columns=['mat_inm', 'Count'])
    list_prob = {}
    dict_names = Matricula_Inmobiliaria_prob(file, corpus_temp)
    if dict_names != {}:
        print(dict_names)
        df_names = pd.DataFrame([[key, dict_names[key]] for key in dict_names.keys()], columns=['mat_inm', 'Count'])
        df_names["Weigth"] = df_names.Count / df_names.Count.sum()
        df_names["std"] = (df_names.Count - df_names.Count.mean()) / df_names.Count.std()
        df_names["odd_Ratio"] = (df_names.Count / df_names.Count.sum()) / (1 / df_names.Count.count())
        df_names["prepro_1x"] = 1 / df_names.Count
        df_names["Cluster"] = np.where(df_names['Count'] == df_names['Count'].max(), 'Principal', 'No probables')
        df_names.index = df_names.mat_inm
        df_names.drop(['mat_inm'], axis='columns', inplace=True)
        print(df_names)
        if df_names.shape[0] > 1:
            if df_names.shape[0] == 2:
                list_prob, df_names["Cluster"] = create_ps(df_names)
            else:
                df_names["Cluster_1D"] = KMeans(n_clusters=2).fit(np.array(df_names['Count']).reshape(-1, 1)).labels_
                kmeans = KMeans(n_clusters=2)
                if len(df_names.Count.unique()) > 1:
                    y_kmeans = kmeans.fit(df_names[["std", "odd_Ratio", "prepro_1x"]])
                    list_prob, df_names["Cluster"] = create_pp(df_names, kmeans)
                else:
                    list_pp = []
                    list_prob = []
                    for a, c in zip(df_names.Count, df_names.index):
                        list_pp.append("Principal")
                        list_prob.append({c: 1})
                    list_prob, df_names["Cluster"] = list_prob, list_pp
        else:
            list_prob = [{df_names.index[0]: 1}]
    else:
        print("Proceso de busqueda Matricula Inmobiliaria no ha encontrado coincidencias")

    return df_names, list_prob

def cedula_catastral_prob(file, corpus_temp):
    text_List = word_tokenize(corpus_temp.raw(file).replace("\r\n", "").replace("i", "1").replace("I", "1").replace("Í", "1").replace("o", "0").replace("O", "0").replace("W", "4").replace("n0", "").replace("N0", "").replace("Nr0.", "").replace("N0.", "").replace("n0.", "").replace("=", "").replace("c a t a s t r a l","catastral"))
    text_List = nltk.Text(text_List)
    list_concordances = ["catastral","catastrales"]
    text_List_result = []    
    
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(list_concordance, width=125)
        if len(text_List_temp)>0:
            text_List_temp = [elem[5] for elem in text_List_temp]
            text_List_result = text_List_result + text_List_temp
    text_List_result =  list(set(text_List_result))
    results = ''.join(text_List_result)
    results = results.replace(" ", "").replace(".", "").replace("-", "").replace("_", "")  
    regex = r"\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*\d+-*_*[.]*"
    cedula_catastral = re.findall(regex, results)
    cedula_catastral = [clean_cedula_catastral(mi) for mi in cedula_catastral]
    cedula_catastral = Counter(cedula_catastral)
    return dict_reduce(cedula_catastral)

def clean_cedula_catastral(txt_rad):
    txt_rad = txt_rad.replace("_", "")
    txt_rad = txt_rad.replace("-", "")
    txt_rad = txt_rad.replace(".", "")
    txt_rad = txt_rad.replace(" ", "")
    return txt_rad.lstrip('+-0')


def select_best_cc_cat(file, corpus_temp):
    df_names = pd.DataFrame(columns=['CC_cat', 'Count'])
    list_prob = {}
    dict_names = cedula_catastral_prob(file, corpus_temp)
    if dict_names != {}:
        df_names = pd.DataFrame([[key, dict_names[key]] for key in dict_names.keys()], columns=['CC_cat', 'Count'])
        df_names["Weigth"] = df_names.Count / df_names.Count.sum()
        df_names["std"] = (df_names.Count - df_names.Count.mean()) / df_names.Count.std()
        df_names["odd_Ratio"] = (df_names.Count / df_names.Count.sum()) / (1 / df_names.Count.count())
        df_names["prepro_1x"] = 1 / df_names.Count
        df_names["Cluster"] = np.where(df_names['Count'] == df_names['Count'].max(), 'Principal', 'No probables')
        df_names.index = df_names.CC_cat
        df_names.drop(['CC_cat'], axis='columns', inplace=True)
        if df_names.shape[0] > 1:
            if df_names.shape[0] == 2:
                list_prob, df_names["Cluster"] = create_ps(df_names)
            else:
                df_names["Cluster_1D"] = KMeans(n_clusters=2).fit(np.array(df_names['Count']).reshape(-1, 1)).labels_
                kmeans = KMeans(n_clusters=2)
                if len(df_names.Count.unique()) > 1:
                    y_kmeans = kmeans.fit(df_names[["std", "odd_Ratio", "prepro_1x"]])
                    list_prob, df_names["Cluster"] = create_pp(df_names, kmeans)
                else:
                    list_pp = []
                    list_prob = []
                    for a, c in zip(df_names.Count, df_names.index):
                        list_pp.append("Principal")
                        list_prob.append({c: 1})
                    list_prob, df_names["Cluster"] = list_prob, list_pp
        else:
            list_prob = [{df_names.index[0]: 1}]
    else:
        print("Proceso de busqueda CC Catastral  Solicitante no ha encontrado coincidencias")

    return df_names, list_prob


def municipio_prob(file, corpus_temp):
    text_List = word_tokenize(replace_accents(corpus_temp.raw(file).replace("\r\n", "")))
    text_List = nltk.Text(text_List)
    list_concordances = ["municipio","municipios"]
    text_List_result = []    
    
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(list_concordance, width=120)
        if len(text_List_temp)>0:
            text_List_temp = [elem[5] for elem in text_List_temp]
            text_List_result = text_List_result + text_List_temp
            
    return text_List_result

def clean_General(text_clean):
    text_clean = replace_accents(text_clean)
    text_clean = re.sub("[,|.|-]"," separador nombre ",text_clean) 
    regex = r"\b[A-Z][A-Z]+\b"
    replaceds = set(re.findall(regex, text_clean))
    for replaced in replaceds:
        text_clean = re.sub(rf"\b{replaced}\b"," "+replaced.capitalize()+" ",text_clean)
    for replaced in stop_municipio:
        text_clean = re.sub(rf"\b{replaced}\b"," "+replaced.lower()+" ",text_clean)    
    
    text_clean = text_clean.replace("Ã±","ñ")#Ã±
    text_clean = text_clean.replace(" de "," De ")
    text_clean = text_clean.replace(" y "," separador ")
    text_clean = text_clean.replace("[||||¿||||_|_]"," ")
    text_clean = re.sub(' +', ' ',text_clean)    
    return text_clean

def get_simple_namepropio(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    name = ""; inicio_bool = True; cnt = 0
    regex = r"^[A-Z][a-z]+"
    for element in tokens:
        cnt +=1
        if inicio_bool and cnt<7:
            if bool(re.search(regex, element)):
                name += element + " "
            else:
                if name != "":
                    inicio_bool = False
        else:
            break
    name = re.sub("\d+", " ", name)        
    return clean_name(name).strip().title() 

def extrac_municipio(file, corpus_temp):
    result = municipio_prob(file, corpus_temp)
    list_pro_municipio = []
    if len(result)>1:
        for prob_item in result:
            prob_item = clean_General(prob_item)
            prob_item = get_simple_namepropio(prob_item)
            if prob_item != "" and not prob_item in ["De"]:
                list_pro_municipio.append(prob_item.replace("San Jose De Cucuta","Cucuta"))
        list_pro_municipio = Counter(list_pro_municipio)
    else:
        print("Proceso de busqueda Municipio no ha encontrado coincidencias")
    return list_pro_municipio

def departamento_prob(file, corpus_temp, filter_mun):
    raw_file = corpus_temp.raw(file).replace("\r\n", "")
    text_List = word_tokenize(clean_General(replace_accents(raw_file)))
    text_List = nltk.Text(text_List)
    list_concordances = ["departamento"]
    text_List_result = []
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_base = text_List.concordance_list(list_concordance, width=240)
        if len(text_List)>0:
            text_List_temp = [elem[5][0:30] for elem in text_List_base if bool(re.search(filter_mun, elem[6]))]
            text_List_result = text_List_result + text_List_temp
    return text_List_result

def extrac_departamento(file, corpus_temp, filter_mun):
    result = departamento_prob(file, corpus_temp, filter_mun)
    list_pro_departamento = []
    if len(result)>1:
        for prob_item in result:
            prob_item = clean_General(prob_item)
            prob_item = get_simple_namepropio(prob_item)
            if prob_item != "" and not prob_item in ["De"]:
                list_pro_departamento.append(prob_item)
    else:
        print("Proceso de busqueda Departamento no ha encontrado coincidencias")
    return Counter(list_pro_departamento)

def vereda_prob(file, corpus_temp, filter_mun):
    raw_file = corpus_temp.raw(file).replace("\r\n", "")
    text_List = word_tokenize(clean_General(replace_accents(raw_file)))
    text_List = nltk.Text(text_List)
    list_concordances = ["vereda"]
    text_List_result = []    
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_base = text_List.concordance_list(list_concordance, width=240)
        if len(text_List_base)>0:
            text_List_temp = [elem[5][0:30] for elem in text_List_base if bool(re.search(filter_mun, elem[6]))]
            text_List_result = text_List_result + text_List_temp  
    return text_List_result

def extrac_vereda(file, corpus_temp, filter_mun):
    result = vereda_prob(file, corpus_temp, filter_mun)
    list_pro_vereda = []
    if len(result)>1:
        for prob_item in result:
            prob_item = clean_General(prob_item)
            prob_item = get_simple_namepropio(prob_item)
            if prob_item != "" and not prob_item in ["De"]:
                list_pro_vereda.append(clean_General(prob_item))
    else:
        print("Proceso de busqueda Vereda no ha encontrado coincidencias")
    return Counter(list_pro_vereda)

def corregimiento_prob(file, corpus_temp, filter_mun):
    raw_file = corpus_temp.raw(file).replace("\r\n", "")
    text_List = word_tokenize(clean_General(replace_accents(raw_file)))
    text_List = nltk.Text(text_List)
    list_concordances = ["corregimiento"]
    text_List_result = []    
    
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_base = text_List.concordance_list(list_concordance, width=240)
        if len(text_List_base)>0:
            text_List_temp = [elem[5][0:30] for elem in text_List_base if bool(re.search(filter_mun, elem[6]))]
            text_List_result = text_List_result + text_List_temp       
    return text_List_result

def extrac_corregimiento(file, corpus_temp, filter_mun):
    result = corregimiento_prob(file, corpus_temp, filter_mun)
    list_pro_corregimiento = []
    if len(result)>1:
        for prob_item in result:
            prob_item = clean_General(prob_item)
            prob_item = get_simple_namepropio(prob_item)
            if prob_item != "" and not prob_item in ["De"]:
                list_pro_corregimiento.append(clean_General(prob_item))
    else:
        print("Proceso de busqueda corregimiento no ha encontrado coincidencias")
    return Counter(list_pro_corregimiento)

def consolidate_dep_mun_ver_corr(file, corpus_temp):
    list_municipio, list_departamento, list_vereda, list_corregimiento = [],[],[],[]
    list_municipio = extrac_municipio(file, corpus_temp)
    if list_municipio != []:
        search_text = list(max_values(list_municipio).keys())[0]
        list_departamento = extrac_departamento(file, corpus_temp,search_text)
        list_vereda= extrac_vereda(file, corpus_temp,search_text)
        list_corregimiento= extrac_corregimiento(file, corpus_temp,search_text)
    return list_municipio, list_departamento, list_vereda, list_corregimiento

def best_departamento(list_departamento):
    departamento_temp = replace_accents(list(max_values(list_departamento).keys())[0]).lower()
    if departamento_temp=="valle":
        departamento_temp="valle del cauca"
    list_dep_scores = []
    for index, row in Departamento_df.iterrows():
        dep_compare = replace_accents(row["Nombre Departamento"]).lower()
        higher_score = SequenceMatcher(None, dep_compare, departamento_temp).ratio()
        list_dep_scores.append({"Departamento":row["Nombre Departamento"],"Código Departamento":row["Código Departamento"],"score":higher_score})        
    list_dep_scores = pd.DataFrame(list_dep_scores)
    higher_score= list_dep_scores.score.max()
    if higher_score > 0.85:
        list_dep_scores = list_dep_scores[list_dep_scores["score"]>0.85].to_dict("r")
    else:
        list_dep_scores = pd.DataFrame().to_dict("r")    
    return list_dep_scores
 
def best_municipio(list_municipio):
    municipio_temp = replace_accents(list(max_values(list_municipio).keys())[0]).lower()
    list_municipio_scores = []
    for index, row in Municipio_df.iterrows():
        mun_compare = replace_accents(row["Nombre Municipio"]).lower()
        higher_score = SequenceMatcher(None, mun_compare, municipio_temp).ratio()
        list_municipio_scores.append({"Municipio":row["Nombre Municipio"],"Código Municipio":row["Código Municipio"],"score":higher_score})        
    list_municipio_scores = pd.DataFrame(list_municipio_scores)
    higher_score= list_municipio_scores.score.max()
    if higher_score > 0.85:
        list_municipio_scores = list_municipio_scores[list_municipio_scores["score"]>0.85].to_dict("r")
    else:
        list_municipio_scores = pd.DataFrame().to_dict("r")
    return list_municipio_scores    

def best_corregimiento(list_corregimiento):
    corregimiento_temp = replace_accents(list(max_values(list_corregimiento).keys())[0]).lower()
    list_corregimiento_scores = []
    for index, row in codane.iterrows():
        corregimiento_compare = replace_accents(row["Nombre Centro Poblado"]).lower()
        higher_score = SequenceMatcher(None, corregimiento_compare, corregimiento_temp).ratio()
        list_corregimiento_scores.append({"Centro Poblado":row["Nombre Centro Poblado"],"Código Centro Poblado":row["Código Centro Poblado"],"score":higher_score})        
    list_corregimiento_scores = pd.DataFrame(list_corregimiento_scores)
    higher_score= list_corregimiento_scores.score.max()
    if higher_score > 0.85:
        list_corregimiento_scores = list_corregimiento_scores[list_corregimiento_scores["score"]>0.85].to_dict("r")
    else:
        list_corregimiento_scores = pd.DataFrame().to_dict("r")    
    return list_corregimiento_scores

def extrac_location(file,corpus_tem):
    list_municipio, list_departamento, list_vereda, list_corregimiento = consolidate_dep_mun_ver_corr(file,corpus_tem)
    df_work_temp = df_work[df_work["Certificado"] == file.split(".")[0]]
    txt_dmv = str(list(df_work_temp["Municipio/Vereda del predio"])[0]).strip()
    if bool(re.search('ADICIONA/', txt_dmv))==False and txt_dmv != "":
        if bool(re.search('\(([^)]+)', txt_dmv)):
            Dep_processing1 = re.search('\(([^)]+)', txt_dmv).group(1).strip()
        else:
            Dep_processing1 = "Not Found"
        if bool(re.match(r"^(.*)\(", txt_dmv)):
            cor_processing1 = re.match(r"^(.*)\(", txt_dmv).group(1).strip()
        else:
            cor_processing1 = "Not Found"
        if bool(re.search('\)(.*)', txt_dmv)):
            if re.search('\)(.*)', txt_dmv).group(1).split(":")[1].strip() != "":
                Vereda_processing1 = re.search('\)(.*)', txt_dmv).group(1).split(":")[1].strip()
            else:
                Vereda_processing1 = "Not Found"
        else:
            Vereda_processing1 = "Not Found"
    else:
        Dep_processing1 = "Not Found"
        cor_processing1 = "Not Found"
        Vereda_processing1 = "Not Found"

    list_departamento_copy = list_departamento
    print("Departamento Principal :",Dep_processing1)
    print("Probables Departamento:", list_departamento_copy)
    if len(list_departamento)>0: list_departamento = best_departamento(list_departamento)
    if len(list_departamento) == 0 and Dep_processing1!="Not Found":
        print("Departamento reprocesado Desde Base")
        list_departamento = best_departamento(Counter([Dep_processing1]))
    print("Departamento Extraido :", list_departamento)

    print("\n")
    list_municipio_copy = list_municipio
    print("Municipio/Corregimiento Principal :",cor_processing1)
    print("Probables Municipio:", list_municipio_copy)
    if len(list_municipio)>0:
        cod_dep = 0
        if len(list_departamento)>0: cod_dep = int(list_departamento[0]["Código Departamento"]) ##############
        list_municipio = best_municipio(list_municipio)
        print("Probables Municipio Codane:", list_municipio)
        list_municipio_join = []
        for each_dic in list_municipio:
            cod_dep_temp = str(each_dic['Código Municipio'])[0:2] if len(str(each_dic['Código Municipio'])) == 5 else str(each_dic['Código Municipio'])[0:1]
            if cod_dep == 0 and len(list_municipio)==1:
                for index, row in Departamento_df.iterrows():
                    if int(row["Código Departamento"]) == int(cod_dep_temp):
                        cod_dep = int(row["Código Departamento"])
                        list_departamento = [{"Departamento":row["Nombre Departamento"],"Código Departamento":row["Código Departamento"],"score":1}]
                        print("Departamento reprocesado Desde Munucipio")
                        print("Departamento Extraido :", list_departamento)
                        break
            if cod_dep==int(cod_dep_temp):
                list_municipio_join.append(each_dic)
        if len(list_municipio_join)>0:
            print("Municipio Extraido :", list_municipio_join)
            list_municipio = list_municipio_join
        else:
            print("Municipio Extraidos Eliminados")
            list_municipio = [{"Municipio":"Not Found","Código Municipio":"Not Found","score":"Not Found"}]
    else:
        list_municipio = [{"Municipio":"Not Found","Código Municipio":"Not Found","score":"Not Found"}]

    if len(list_departamento) == 0: list_departamento = [{'Departamento': 'Not Found', 'Código Departamento': "Not Found", 'score': "Not Found"}]

    print("\n")
    list_corregimiento_copy = list_corregimiento
    print("Municipio/Corregimiento Principal :",cor_processing1)
    print("Probables Corregimiento:", list_corregimiento_copy)
    cod_mun = -1
    if len(list_corregimiento)>0:
        if len(list_municipio)>0 and list_municipio[0]["Código Municipio"] != "Not Found":
            cod_mun = int(list_municipio[0]["Código Municipio"])
        list_corregimiento = best_corregimiento(list_corregimiento)
        print("Probables Corregimiento Codane:", list_corregimiento)
        list_corregimiento_join = []
        for each_dic in list_corregimiento:
            cod_mun_temp = str(each_dic['Código Centro Poblado'])[0:5] if len(str(each_dic['Código Centro Poblado'])) == 8 else str(each_dic['Código Centro Poblado'])[0:4]
            if int(cod_mun)==int(cod_mun_temp):
                list_corregimiento_join.append(each_dic)
        if len(list_corregimiento_join)>0:
            print("Corregimiento Extraido Codane:", list_corregimiento_join)
            list_corregimiento = list_corregimiento_join
        else:
            print("Corregimiento Extraidos No codane:",list(max_values(list_corregimiento_copy).keys())[0])
            list_corregimiento = [{"Centro Poblado":list(max_values(list_corregimiento_copy).keys())[0],"Código Centro Poblado":'Not Found',"score":'Not Found'}]
    else:
        list_corregimiento = [{"Centro Poblado":'Not Found',"Código Centro Poblado":'Not Found',"score":'Not Found'}]

    print("\n")
    list_vereda_copy = list_vereda
    print("Vereda Principal :",Vereda_processing1)
    print("Probables vereda:", list_vereda_copy)
    cod_mun = -1
    if len(list_vereda)>0:
        if len(list_municipio)>0 and list_municipio[0]["Código Municipio"] != "Not Found":
            cod_mun = int(list_municipio[0]["Código Municipio"])
        list_vereda = best_corregimiento(list_vereda)
        print("Probables Vereda Codane:", list_vereda)
        list_vereda_join = []
        for each_dic in list_vereda:
            cod_mun_temp = str(each_dic['Código Centro Poblado'])[0:5] if len(str(each_dic['Código Centro Poblado'])) == 8 else str(each_dic['Código Centro Poblado'])[0:4]
            if cod_mun==int(cod_mun_temp):
                list_vereda_join.append(each_dic) 
        if len(list_vereda_join)>0:
            print("Vereda Extraido Codane:", list_vereda_join)
            list_vereda = list_vereda_join
        else: 
            print("Vereda Extraidos No codane:",list(max_values(list_vereda_copy).keys())[0]) 
            list_vereda = [{"Centro Poblado":list(max_values(list_vereda_copy).keys())[0],"Código Centro Poblado":'Not Found',"score":'Not Found'}]
    else:        
        list_vereda = [{"Centro Poblado":'Not Found',"Código Centro Poblado":'Not Found',"score":'Not Found'}]

    df_departamento = pd.DataFrame(list_departamento).drop(["score"], axis=1)
    df_departamento["Certificado"] = list(df_work_temp["Certificado"])[0]
    df_departamento.set_index("Certificado",inplace=True)
    df_municipio = pd.DataFrame(list_municipio).drop(['score'], axis=1)
    df_municipio["Certificado"] = list(df_work_temp["Certificado"])[0]
    df_municipio.set_index("Certificado",inplace=True)
    df_corregimiento = pd.DataFrame(list_corregimiento).rename(columns={'Centro Poblado': 'Corregimiento', 'Código Centro Poblado': 'Código Corregimiento'}).drop(['score'], axis=1)
    df_corregimiento["Certificado"] = list(df_work_temp["Certificado"])[0]
    df_corregimiento.set_index("Certificado",inplace=True)
    df_vereda = pd.DataFrame(list_vereda).rename(columns={'Centro Poblado': 'Vereda', 'Código Centro Poblado': 'Código Vereda'}).drop(['score'], axis=1)
    df_vereda["Certificado"] = list(df_work_temp["Certificado"])[0]
    df_vereda.set_index("Certificado",inplace=True)
    df_locate = pd.merge(pd.merge(pd.merge(df_departamento, df_municipio, right_index=True, left_index=True), df_corregimiento, right_index=True, left_index=True), df_vereda, right_index=True, left_index=True)
    print("\n")
    return df_locate
    
def validate_name(name_text):
    if name_text in txt_control:
        return False
    else:
        return True

def clean_name(name_text):
    intro = True
    apriori = True
    aposteriori = True
    while intro:
        name_text = name_text.split()
        if len(name_text)>1:
            if name_text[0] in txt_control:
                del name_text[0]
            else:
                apriori = False
            if name_text[len(name_text)-1] in txt_control:
                del name_text[len(name_text)-1]
            else:
                aposteriori = False
        else:
            intro = False
        name_text = " ".join(name_text)
        if apriori == False and aposteriori == False:
            intro = False
    return name_text

def nucleo_familiar_prob2(file, corpus_temp):
    text_List = word_tokenize(corpus_temp.raw(file))
    text_List = nltk.Text(text_List)
    list_concordances = ["núcleo","reconocer","beneficiarios","reparación"]  
    
    text_List_result = []    
    
    for list_concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(list_concordance, width=1500)
        if len(text_List_temp)>0:
            text_List_temp = [elem[6] for elem in text_List_temp]
            text_List_result = text_List_result + text_List_temp
    text_List_result =  list(set(text_List_result))
    
    list_filter = ["conformado","víctima","ingrese","favor"]
    
    results = []
    for elem_f in list_concordances_ltc(list_filter):
        for text_result in text_List_result:
            if bool(re.search(elem_f, text_result)):
                results.append(text_result[600:])
    return results

def get_nucleo_names2(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    person_list = []; name = ""; inicio_bool = False; count = 0 
    
    regex = r"^[A-Z][a-z]+"
    for element in tokens:
        if count < 50: 
            if bool(re.search(regex, element)) and element.capitalize() not in my_stop_words_descapitalize_nucleo:
                name += element + " "
            else:
                if inicio_bool:
                    count+=1
                if name != "":
                    if len(name.split())>1:
                        inicio_bool = True
                        count = 0 
                        person_list.append(name.strip())
                    name = ""    
        else:
            break

    person_list = [clean_name(name) for name in person_list]
    person_list = [name for name in person_list if len(name.split())>=2] 
    person_list = list(map(str.strip, person_list))
    person_list = [elem.title() for elem in person_list]
    return person_list 

def max_values2(dict_def):
    return {name_def:n_def for name_def, n_def in dict_def.items() if n_def == max(list(dict_def.values()))}

def dict_reduce2(mydict):
    intro = True 
    while intro:
        intro = False
        mydict_copy = mydict.copy()
        for name_search, n_search in mydict_copy.items():
            mydict_temp = {}
            for name_dic, n_dic in mydict.items():
                if name_search != name_dic:
                    if name_search in name_dic:
                        mydict_temp.setdefault(name_dic,mydict[name_dic])
            if len(mydict_temp)>0:
                mydict_temp = max_values(mydict_temp)
                mydict[list(mydict_temp.keys())[0]] = list(mydict_temp.values())[0] + n_search 
                del mydict[name_search]
                intro = True
    return mydict   

def clean_step2(text_clean):
    text_clean = replace_accents(text_clean)
    text_clean = re.sub(","," separador nombre ",text_clean)
    text_clean = re.sub('[%s]'%re.escape(string.punctuation),' ',text_clean)
    regex = r"\b[A-Z][A-Z]+\b"
    replaceds = set(re.findall(regex, text_clean))
    for replaced in replaceds:
        text_clean = re.sub(rf"\b{replaced}\b"," "+replaced.capitalize()+" ",text_clean)
    text_clean = text_clean.replace("Ã±","ñ")#Ã±
    text_clean = text_clean.replace(" de "," De ")
    text_clean = text_clean.replace(" y "," separador ")
    text_clean = text_clean.replace(""," ")
    text_clean = text_clean.replace(""," ")
    text_clean = text_clean.replace(""," ")
    text_clean = text_clean.replace(""," ")
    text_clean = text_clean.replace("¿"," ")
    text_clean = text_clean.replace(""," ")
    text_clean = text_clean.replace(""," ")
    text_clean = text_clean.replace(""," ")
    
    for descapitalize in my_stop_words_descapitalize_nucleo:
        text_clean = re.sub(rf"\b{descapitalize}\b"," "+descapitalize.lower()+" ",text_clean)
    text_clean = re.sub(' +', ' ',text_clean)    
    return text_clean

def nucleo_create2(file, corpus_temp):
    results = nucleo_familiar_prob2(file, corpus_temp) 
    list_cluster=[]
    for result in results:
        result = clean_step2(result)
        person_names = get_nucleo_names2(result)
        if len(person_names)>0:
            dict_create_temp = dict_reduce2({person_name:1 for person_name in person_names if person_name not in ["De","Las","Los","La"]})
            if dict_create_temp !={}:
                list_cluster.append(dict_create_temp)
    return list_cluster

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def sequence_sim(result_intro):
    intro = True 
    while intro:
        intro = False
        result_temp = result_intro.copy()
        count_list = 1
        if len(result_temp)>1:
            for element_base , dic_base in enumerate(result_temp):
                for element_compare, dic_compare in enumerate(result_temp[count_list:]):
                    for key_base in list(dic_base.keys()):
                        for key_compare in list(dic_compare.keys()):
                            if (len(key_base) != len(key_compare)) and (key_base in key_compare or key_compare in key_base):
                                intro = True
                                if len(key_base) > len(key_compare):
                                    print("Change to " + key_compare + "-> " + key_base)
                                    result_intro[element_compare+count_list].update({key_base:1})
                                    if key_compare in result_intro[element_compare+count_list]:
                                        trash = result_intro[element_compare+count_list].pop(key_compare)
                                else: 
                                    print("Change to " + key_base + "-> " + key_compare)
                                    result_intro[element_base].update({key_compare:1})
                                    if key_base in result_intro[element_base]:
                                        trash = result_intro[element_base].pop(key_base)
                count_list+=1
        return result_temp
    
def select_nucleo(result): 
    count_similarity = 0
    names = ["group_"+ str(elem) for elem in list(range(1,len(result)+1))]
    array_similarity = np.identity(len(result))
    
    for row , each_fixed in enumerate(result):
        for col, each_dynamic in enumerate(result[count_similarity:]):
            if col+count_similarity != row:
                temp_similarity = counter_cosine_similarity(each_fixed, each_dynamic)
                array_similarity[col+count_similarity,row] , array_similarity[row,col+count_similarity] = temp_similarity, temp_similarity
        count_similarity = count_similarity + 1    
    df_similarity = pd.DataFrame(array_similarity, columns=names, index=names)
    
    count_select = 1
    list_select = []
    list_prob = []
    for col, column in enumerate(list(df_similarity.columns)):
        list_temp = []
        for elem, element_compare in enumerate(list(df_similarity[column][count_select:])):
            if round(element_compare,2) == 1:
                list_temp.append(elem+count_select)
        if list_temp != []:
            list_select.append([col] + list_temp)
        count_select+=1
    if list_select == []:
        if len(result) <= 2:
            for element in result:
                list_prob.append(list(element))
        else:
            kmeans = KMeans(n_clusters=2)
            y_kmeans = kmeans.fit(df_similarity)
            df_similarity["sum"] = df_similarity.sum(axis=1)
            df_similarity["cluster"] = kmeans.labels_
            df_cluster = df_similarity.groupby("cluster")["sum"].sum().reset_index()
            max_cluster = list(df_cluster[df_cluster["sum"]==df_cluster["sum"].max()]["cluster"])
            count_step = 0
            for index, row in df_similarity.iterrows():
                if row["cluster"] == max_cluster:
                    list_prob.append(list(result[count_step]))
                count_step+=1
    else:
        max_group = [len(elem) for elem in list_select]
        max_group = max(max_group)
        for elem in list_select:
            if len(elem) == max_group:
                list_prob.append(list(result[elem[0]]))
    return df_similarity, list_prob    

def extrac_nucleo_familiar(file, corpus_temp):
    list_prob = []
    df_similarity_1 = []
    result = nucleo_create2(file, corpus_temp)
    if len(result)>1:
        result = sequence_sim(result) #Estandarizacion
        len_result = [len(each) for each in result]
        cluster_nucleo = list(KMeans(n_clusters=2).fit(np.array(len_result).reshape(-1,1)).labels_)
        max_value = max(len_result)
        for a, b in zip(len_result, cluster_nucleo): 
            if a == max_value:
                cluster_select = b
                break
        result = [relem for relem, cn in zip(result, cluster_nucleo) if cn == cluster_select]
        df_similarity_1, list_prob = select_nucleo(result)
    else:
        if len(result)==1:
            df_similarity_1, list_prob, result = [],list(result[0].keys()),list(result[0].keys())
        else:    
            df_similarity_1, list_prob, result = [],[],[]
            print("Proceso de busqueda no ha encontrado coincidencias")
    return df_similarity_1, list_prob, result


def clean_coordenadas(cor):
    cor = cor.replace("\"","°")
    cor = cor.replace("\'","°")
    cor = cor.replace("*","°")
    cor = cor.replace("","°")
    cor = cor.replace("","°")
    cor = cor.replace("","°")
    cor = cor.replace("º","°")
    cor = cor.replace("®","°")
    cor = re.sub(' +', ' ',cor)
    cor = re.sub('\.+', '.',cor)
    cor = cor.split("°")
    cor = [re.sub('\.+', '.',each.strip().replace(" ",".").replace(",",".")) for each in cor if each!=""]
    if len(cor) == 3:
        value_coordenada = 0
        cnt_coordenada = 0
        for each in cor:
            cnt_coordenada += 1
            if cnt_coordenada == 1:
                value_coordenada += float(each)
            elif cnt_coordenada == 2:
                value_coordenada += float(each)/60
            else:
                value_coordenada += float(each)/3600
    else:
        value_coordenada = "" 
    return value_coordenada

def extrac_coordenadas(file, corpus_temp):
    lines = corpus_temp.raw(file).split ('\r\n')
    regex = r"\d+\s*[\°\"\'\*\\\\º\®]\s*\d+\s?[\°\"\'\*\\\\º\®]\s*\d+\.?\,?\s?\d+\s?[\°\"\'\*\\\\º\®]"
    list_coordenadas = []
    intro = True
    for line in lines:
        coordenadas = re.findall(regex, line)
        if coordenadas != []:
            list_coordenadas_temp = []
            if intro:
                intro = False
            for coord in coordenadas:
                coord = clean_coordenadas(coord)
                list_coordenadas_temp.append(coord)
            list_coordenadas.append(list_coordenadas_temp)
    return list_coordenadas

def calculate__coordenadas(file, corpus_temp):
    coordenadas = extrac_coordenadas(file, corpus_temp)
    coordenadas = [lista for item in coordenadas for lista in item]
    list_lat = [item for item in coordenadas if Rio_Amazonas < item < Punta_Gallinas]
    list_lon = [item for item in coordenadas if Isla_San_Jose < item < Cabo_Manglares]
    list_lat = [item for item in list_lat if abs(item-np.mean(list_lat))<0.5]
    list_lon = [item for item in list_lon if abs(item-np.mean(list_lon))<0.5]
    return list_lat, list_lon
    

def return_cc(file , corpus_temp, e_pers, t_iter, df_work_temp):
    text_cc = "CC: "+ t_iter
    results_pp, list_cc_pp = DNI_prob(file, corpus_temp, e_pers)
    if len(list_cc_pp)>0:
        temp_pp = pd.DataFrame(list_cc_pp)
        print(temp_pp)
        temp_pp = temp_pp.groupby(["CC"]).agg({"Id":"count","dist_name":"mean","dist_icc":"mean","avg_icc":"mean","weight":"mean"}).reset_index()
        temp_pp = list(temp_pp[temp_pp["weight"]==temp_pp["weight"].max()]["CC"])    
        print(str(text_cc) + " - " + str(temp_pp[0]))
        df_work_temp[text_cc], return_cc = temp_pp[0], temp_pp[0]
    else:
        print(str(text_cc))
        df_work_temp[text_cc], return_cc = "Not Found","Not Found" 
    return return_cc

def return_tables_work(file, corpus_temp):
    
    df_work_temp = df_work[df_work["Certificado"] == file.split(".")[0]]
    df_work_table = df_work_temp.copy() 

    #Municipio/Vereda/Departamento
    print("\n")
    print("Inicio extraccion Municipio/Vereda/Departamento")    
    df_locates = extrac_location(file, corpus_temp)

    #Nombre
    print("\n")
    print("Inicio extraccion Solicitante y cedulas")
    chache_dic = {}
    list_pp = ["Nombre Principal " + str(_) for _ in list(range(1,6))]
    list_prob = ["Nombre Probable " + str(_) for _ in list(range(1,11))]
    df_name, list_probs = select_best(file, corpus_temp)

    list_probs = dict(ChainMap(*list_probs))
    df_pp = pd.DataFrame()

    pp = []
    prob = []
    if list_probs != {}:
        list_cedulas_pp = []
        df_pp = pd.DataFrame.from_dict(list_probs, orient ='index', columns=['PP']).reset_index().rename(columns={'index': 'Nombre'})
        df_pp["key"] = list(df_work_temp["Certificado"])[0]
        pp = [key for key, value in list_probs.items() if value == 1]
        prob = [key for key, value in list_probs.items() if value == 0]
        if len(pp)>0:
            for i, p in enumerate(pp):
                df_work_temp[list_pp[i]] = p
                if p in chache_dic:
                    list_cedulas_pp.append(chache_dic[p]);print(p + " Ya calculado: "+ str(chache_dic[p]))
                else:    
                    cc_final = return_cc(file, corpus_temp, p, list_pp[i], df_work_temp)
                    chache_dic[p] = cc_final
                    list_cedulas_pp.append(cc_final)    
        if len(prob)>0:
            for i, pro in enumerate(prob):
                df_work_temp[list_prob[i]] = pro
                if pro in chache_dic:
                    list_cedulas_pp.append(chache_dic[pro]);print(pro + " Ya calculado: "+ str(chache_dic[pro]))
                else:    
                    cc_final = return_cc(file, corpus_temp, pro, list_prob[i], df_work_temp)
                    chache_dic[pro] = cc_final
                    list_cedulas_pp.append(cc_final)
        df_pp["cedula"] = list_cedulas_pp        
    else:
        df_work_temp[list_pp[0]] = "NA"

    #Nucleo Familiar
    print("\n")
    print("Inicio extraccion Nucleo Familiar y cedulas")
    array_similarity, list_result, list_prob = extrac_nucleo_familiar(file, corpus_temp)
    nucleo_familiar = pd.DataFrame()

    if list_result != []:
        list_cedulas_pp = []
        nucleo_familiar = pd.DataFrame([{"group":nn+1, "n_persona":i+1, "Name":each } for nn, nucleo in enumerate(list_result) for i, each in enumerate(nucleo)])
        nucleo_familiar["key"] = list(df_work_temp["Certificado"])[0]
        for nn, nucleo in enumerate(list_result):
            for i, each in enumerate(nucleo):
                id_Person = "Nucleo Familiar " + str(nn+1) + " Id Person: " + str(i+1)
                text_cc = "CC: "+ id_Person
                df_work_temp[id_Person] = each
                if each in chache_dic:
                    list_cedulas_pp.append(chache_dic[each]);print(each + " Ya calculado: "+ str(chache_dic[each]))
                    df_work_temp[text_cc] = chache_dic[each]
                else:    
                    cc_final = return_cc(file, corpus_temp, each, id_Person, df_work_temp)
                    chache_dic[each] = cc_final
                    list_cedulas_pp.append(cc_final)
        nucleo_familiar["cedula"] = list_cedulas_pp

    #Radicado
    list_rad = ["Radicado Principal " + str(_) for _ in list(range(1,11))]
    list_rad_pro = ["Radicado Probable " + str(_) for _ in list(range(1,11))]
    print("\n")
    print("Inicio extraccion Radicado")
    df_rad_fn, rad_prob_fn = select_best_rad(file, corpus_temp)
    rad_prob_fn = dict(ChainMap(*rad_prob_fn))

    df_rad = pd.DataFrame()

    rad = []
    rad_prob = []
    if rad_prob_fn != {}:
        list_radicado = []
        df_rad = pd.DataFrame.from_dict(rad_prob_fn, orient ='index', columns=['PP']).reset_index().rename(columns={'index': 'Radicado'})
        df_rad["key"] = list(df_work_temp["Certificado"])[0]
        rad = [key for key, value in rad_prob_fn.items() if value == 1]
        rad_prob = [key for key, value in rad_prob_fn.items() if value == 0]    
        if len(rad)>0:
            for i, p in enumerate(rad):
                df_work_temp[list_rad[i]] = p
                list_radicado.append(p)    
        if len(rad_prob)>0:
            for i, pro in enumerate(rad_prob):
                df_work_temp[list_rad_pro[i]] = pro
                list_radicado.append(pro)
        df_rad["Radicado"] = list_radicado        
    else:
        df_work_temp[list_rad[0]] = "NA"           


    #CC catastral 
    list_cc_cat = ["CC Catastral Principal " + str(_) for _ in list(range(1,11))]
    list_cc_cat_pro = ["CC Catastral Probable " + str(_) for _ in list(range(1,11))]
    print("\n")
    print("Inicio extraccion Cedula Catastral")
    df_cc_cat_fn, cc_cat_prob_fn = select_best_cc_cat(file, corpus_temp)
    cc_cat_prob_fn = dict(ChainMap(*cc_cat_prob_fn))

    df_cc_cat = pd.DataFrame()

    cc_cat = []
    cc_cat_prob = []
    if cc_cat_prob_fn != {}:
        list_cedula_cat = []
        df_cc_cat = pd.DataFrame.from_dict(cc_cat_prob_fn, orient ='index', columns=['PP']).reset_index().rename(columns={'index': 'CC Catastral'})
        df_cc_cat["key"] = list(df_work_temp["Certificado"])[0]
        cc_cat = [key for key, value in cc_cat_prob_fn.items() if value == 1]
        cc_cat_prob = [key for key, value in cc_cat_prob_fn.items() if value == 0]    
        if len(cc_cat)>0:
            for i, p in enumerate(cc_cat):
                df_work_temp[list_cc_cat[i]] = p
                list_cedula_cat.append(p)    
        if len(cc_cat_prob)>0:
            for i, pro in enumerate(cc_cat_prob):
                df_work_temp[list_cc_cat_pro[i]] = pro
                list_cedula_cat.append(pro)
        df_cc_cat["CC Catastral"] = list_cedula_cat        
    else:
        df_work_temp[list_cc_cat[0]] = "NA"    

    #Matricula Inmobiliaria
    list_m_inm = ["Matricula Inmobiliaria Principal " + str(_) for _ in list(range(1,11))]
    list_m_inm_pro = ["Matricula Inmobiliaria Probable " + str(_) for _ in list(range(1,11))]
    print("\n")
    print("Inicio extraccion Matricula Inmobiliaria")
    df_m_inm_fn, m_inm_prob_fn = select_best_m_inm(file, corpus_temp)
    m_inm_prob_fn = dict(ChainMap(*m_inm_prob_fn))

    df_m_inm = pd.DataFrame()

    m_inm = []
    m_inm_prob = []

    if m_inm_prob_fn != {}:
        list_matricula_inm = []
        df_m_inm = pd.DataFrame.from_dict(m_inm_prob_fn, orient ='index', columns=['PP']).reset_index().rename(columns={'index': 'Matricula Inmobiliaria'})
        df_m_inm["key"] = list(df_work_temp["Certificado"])[0]
        m_inm = [key for key, value in m_inm_prob_fn.items() if value == 1]
        m_inm_prob = [key for key, value in m_inm_prob_fn.items() if value == 0]    
        if len(m_inm)>0:
            for i, p in enumerate(m_inm):
                df_work_temp[list_m_inm[i]] = p
                list_matricula_inm.append(p)    
        if len(m_inm_prob)>0:
            for i, pro in enumerate(m_inm_prob):
                df_work_temp[list_m_inm_pro[i]] = pro
                list_matricula_inm.append(pro)
        df_m_inm["Matricula Inmobiliaria"] = list_matricula_inm        
    else:
        df_work_temp[list_m_inm[0]] = "NA"

    #Georefenciacion
    print("\n")
    print("Inicio extraccion Georefenciacion")
    list_latf, list_lonf = calculate__coordenadas(file, corpus_temp)
    list_locate = []
    if list_latf !=[] and list_lonf !=[]:
        print(np.mean(list_latf))
        print(np.mean(list_lonf))
        list_locate = [np.mean(list_latf),np.mean(list_lonf)*-1]
        df_Georefenciacion = pd.DataFrame([{"key":list(df_work_temp["Certificado"])[0],"Latitud":list_locate[0],"Longitud":list_locate[1]}])
    else:
        print("Georefenciacion Not found")
        df_Georefenciacion = pd.DataFrame([{"key":list(df_work_temp["Certificado"])[0],"Latitud":"Not Found","Longitud":"Not Found"}])
   
    return df_work_temp, df_work_table, df_locates, df_pp, nucleo_familiar, df_rad, df_cc_cat, df_m_inm, df_Georefenciacion, list_locate

def split(word): 
    #punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    punctuations = '''!()-[];:'"\,<>./?@#$%^*'''
    [char for char in word if char not in punctuations]
    return word
    
######################################################
###     EXTRACCIÓN NOMBRE JUEZ Y MAGISTRADO       ###
######################################################

def find_range(lista,rango):
    if len(lista)==0:
        flat_list=[]
    else:
        for i in range(rango+1):
            x=[list(range(x-i,x)) for x in lista]
            flat_list = [item for sublist in x for item in sublist if item not in lista]
    return(flat_list)


def find_MAYUSC(text, black_list_temp):
    convertion=' '.join(re.findall(r"\b[A-Z][A-Z]+\b", replace_accents(text)))
    if len(convertion)<1 or convertion in black_list_temp:
        convertion='NA'
    return(convertion)
    
def get_human_names_2(text, black_list_temp):
    person_list = []
    text=re.sub('[%s]'%re.escape(string.punctuation),' ',text)
    regex = r"\b[A-Z][A-Z]+\b" # r"\b[A-Z].*?\b"
    replaceds = set(re.findall(regex, text))
    replaceds = [w for w in replaceds if not w in black_list_temp]
    for descapitalize in my_stop_words_descapitalize:
        text = re.sub(rf"\b{descapitalize}\b"," "+descapitalize.lower()+" ",text)
    text = re.sub(' +', ' ',text)    

    tokens = nltk.tokenize.word_tokenize(text)
    tagged_word = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(tagged_word, binary = False)
  
    person_list = [word for word,pos in tagged_word if pos == 'NNP' and word not in black_list_temp]
    if len(person_list)!=0:
        person=' '.join(person_list)
    else:
        person='NA'
    return person


def extrae_magister(n, corpus_temp, black_list_temp):
    bins_cat = [0, 0.05, 0.95,1]
    names_cat = ['Encabezado', 'Historico / Secundario', 'Firmas']
    key_words=list_concordances_ltc(key_magister + key_juez)
    key_words2=list_concordances_ltc(key_magister2)

    file=corpus_temp.fileids()[n]
    lines = corpus_temp.raw(file).split('\r\n')
    llave_sentencia=file
    #lines=[line.lower() for line in lines]
    list_juez_text=[]
    list_juez_index=[]
    counter=-1
    for line in lines:
        counter=counter+1
        for key in key_words:
            match=re.search(rf"^{key}.*$",line)
            if match != None: 
                list_juez_text.append(match.group(0))
                list_juez_index.append(counter)
    table1=pd.DataFrame(list_juez_text,list_juez_index,columns=['extract_magistrado']).reset_index()
    #table1['validate_name']=re.findall(r"\b[A-Z][A-Z]+\b", table1['extract_magistrado'])
    table1['validate_name']=table1['extract_magistrado'].apply(find_MAYUSC, args=([black_list_temp]))
    table1['original']=1
    
    ### evaluate lines near lines without PNN with key words
    list_recursive=list(table1.loc[(table1.validate_name =='NA') & (table1.extract_magistrado.str.split().str.len()==1)]['index'])
    list_recursive=find_range(list_recursive,2)
  
    ### looking for names probable signatures
    if list_recursive:
        probable_firma=[]
        for i in list_recursive:
            probable_firma.append(lines[i])
    
        #list_recursive_t=list_recursive1+list_recursive2
        list_recursive_t=list_recursive
        table2=pd.DataFrame(probable_firma,list_recursive_t,columns=['extract_magistrado']).reset_index()
        table2['validate_name']=table2['extract_magistrado'].apply(get_human_names_2, args=([black_list_temp]))
        ### Keeping names ###
        table3=pd.concat([table1,table2],ignore_index=True).sort_values('index')
        table3=table3.loc[(table3.validate_name !='NA') | (table3.extract_magistrado.str.split().str.len()==1)]
    else:
        table3=table1.sort_values('index')
        table3=table3.loc[(table3.validate_name !='NA') | (table3.extract_magistrado.str.split().str.len()==1)]
    
    
    if table1.empty:
        for line in lines:
            counter2=-1
            counter2=counter2+1
            for key in key_words2:
                match=re.search(rf"{key}.*$",line)
                if match != None: 
                    list_juez_text.append(match.group(0))
                    list_juez_index.append(counter2)
        table1=pd.DataFrame(list_juez_text,list_juez_index,columns=['extract_magistrado']).reset_index()
        table3['validate_name']=table1['extract_magistrado'].apply(get_human_names_2, args=([black_list_temp]))
        table3['original']=2

        
    
    ### new bolean variables ###
    table3['parte_']=table3['index']/len(lines) 
    table3['parte']=pd.cut(table3['parte_'], bins_cat, labels=names_cat)
    
    table3['index_lag'] = table3['index'].shift(-1)
    table3['extract_magistrado_lag'] = table3['extract_magistrado'].shift(-1).str.replace('[^\w\s]','')
    table3['validate_name_lag'] = table3['validate_name'].shift(-1)
    
    ## reduce by conditions ##
    table3=table3.loc[(table3.validate_name !='NA') | (table3.original==1)]
    
    table3['cerca']=np.where(abs(table3['index']-table3['index_lag'])<=2,1,0)
    table3['ponente']=np.where(table3['extract_magistrado'].str.contains('|'.join(list_concordances_ltc(key_ponente))),1,0)
    table3['firma']=np.where((table3['cerca']==1) & (table3['validate_name']!=table3['extract_magistrado_lag']) &
                             (table3['extract_magistrado_lag'].str.contains('|'.join(list_concordances_ltc(key_magister)))),1,0)

    ## final reduction ##
    table3=table3.sort_values(['index', 'firma']).drop_duplicates('index', keep='last')
    table3['key']=llave_sentencia
    table3['Nombre_JM']=table3['validate_name'].str.split().apply(lambda x: [w.capitalize() for w in x]).str.join(' ')
    table3['lead_sentence']=table3['extract_magistrado_lag']

    table3=table3.loc[(table3.validate_name !='NA')][['key','index','parte','original','Nombre_JM',#'extract_magistrado',
                                                      'ponente','lead_sentence']] #'extract_magistrado_lag']]
    
    table4=table3.sort_values(['Nombre_JM', 'ponente','index']).drop_duplicates('Nombre_JM', keep='last') 
    
    
    return(table4)

######################################################
###     EXTRACCIÓN NOMBRE OPOSITOR       ###
######################################################

def extrae_opositor(n, corpus_temp, black_list_temp):
    key_tribunal=list_concordances_ltc(key_tribunal1)
    key_words=list_concordances_ltc(key_opositor)
    key_words2=list_concordances_ltc(key_opositor2)
    
    file=corpus_temp.fileids()[n]
    lines = corpus_temp.raw(file).split('\r\n')
    llave_sentencia=file
    #lines=[line.lower() for line in lines]
    ### Validación tribunal superior ####
    verifica_tribunal=[]
    counter=-1
    for line in lines:
        counter=counter+1
        for key in key_tribunal:
            match=re.search(rf"{key}.*$",line)
            if match != None: 
                verifica_tribunal.append(match.group(0))
    if verifica_tribunal:
        valida_tribunal='Tribunal superior - se espera opositor'
        print('Tribunal superior - se espera opositor')
    else:
        valida_tribunal='Juzgado - No se espera opositor'
        print('Juzgado - No se espera opositor')
    
    ### match opositor by line ###
    list_opositor_text=[]
    list_opositor_index=[]
    counter=-1
    for line in lines:
        counter=counter+1
        for key in key_words:
            match=re.search(rf"{key}.*$",line)
            if match != None: 
                list_opositor_text.append(match.group(0))
                list_opositor_index.append(counter)
    table1=pd.DataFrame(list_opositor_text,list_opositor_index,columns=['extract_opositor']).reset_index()
    table1['validate_name']=table1['extract_opositor'].apply(find_MAYUSC, args=([black_list_temp]))
    table1['original']=1
    
    ## reduce by conditions ##
    table2=table1.loc[(table1.validate_name !='NA')]
    if table2.empty:
        table1['validate_name']=table1['extract_opositor'].apply(get_human_names_2, args=([black_list_temp]))
    table2=table1.loc[(table1.validate_name !='NA')]
    
    table2['key']=llave_sentencia
    table2['Nombre_opositor']=table2['validate_name'].str.split().apply(lambda x: [w.capitalize() for w in x]).str.join(' ')
    table2=table2.sort_values(['Nombre_opositor','index']).drop_duplicates('Nombre_opositor', keep='last') 
    table2=table2.loc[(table2.validate_name !='NA')][['key','index','Nombre_opositor']]
    return(table2)


def extrac_resuelve(file, corpus_temp):
    txt_final = ["_ NOTIFIQUESE",
                 ": NOTIFICAR",
                 ": NOTIFIQUESE",
                 "- NOTIFIQUESE",
                 "NOTIFIQUESE,",
                 "NOTIFI MPLASE",
                 "NOTIFIQ CUMP",
                 "NOTIFIQUE Y CUMPLASE",
                 "NOTIFIQUESE UMPLASE",
                 "NOTIFIQUISE--Y-CUMPLASE",
                 "NOTIFIQUES CUMPLASE",
                 "NOTIFIQUE E Y CUMPLASE",
                 "NOTIFIQU \tUMPLASE",
                 "NOTIFIQ \tUMPLASE",
                 "NOTIFIQUES \tUMPLASE",
                 "NOTIFIQUESE Y C",
                 "NOTIFIQUESE, COMUNIQUESE Y CUMPLASE",
                 "NOTIFIQUESE / CUMPLASE",
                 "NO \tESE Y CUMPLASE",
                 "NOTIFIQUESE POR COMU",
                 "NOTIFIQUESE, COMU1JFESE Y C4JMPLASE",
                 "NOTIFI \t MPLASE",
                 "- COMUNIQUESE",
                 "NOTIFIQ SE Y CUMPLASE",
                 "COPIESE, NOT",
                 "QUINTO.- NOTIFIQUESE LA PRESENTE PROVIDENCIA"]

    txt_inicio = ["RESUELVE", "R E S U ELV E", "Resuelve", "RESUEL VE", "RESUELV", "RE SUE LV E", "RE S U E L V E",
                  "RESU.ELVE",
                  "R E S U E L V E", "RESUELVA", "DECISION:", "VI. DECISION",  # "^DECISION$"
                  "FALLA", "ORDENES:", "ORDENES", ". ORDENAR"]
    txt_final = "|".join(txt_final)

    counter = -1
    inicio = 0
    final = 0
    lines = corpus_temp.raw(file).replace("RESUELV E", "RESUELVE").split('\r\n')
    for line in lines:
        counter = counter + 1
        line_temp = replace_accents(re.sub(' +', ' ', line).strip().upper())
        for txt in txt_inicio:
            line = line.replace("?", "").replace("?", "")
            if bool(re.search(rf"{txt}\s*:*=*·*[.]*$", replace_accents(re.sub(' +', ' ', line).strip()))):
                inicio = counter
                break
        if bool(re.search(rf"({txt_final})", line_temp)):
            final = counter
    if final == 0 and inicio > 0:
        final = len(lines)
    return lines, inicio, final


def clean_resuelve(name_text):
    txt_control = ["Del", "De", "Los", "Las", "Para", "La", "Y", "A", "Al"]
    intro = True
    apriori = True
    aposteriori = True
    while intro:
        name_text = name_text.split()
        if len(name_text) > 1:
            if name_text[0] in txt_control:
                del name_text[0]
            else:
                apriori = False
            if name_text[len(name_text) - 1] in txt_control:
                del name_text[len(name_text) - 1]
            else:
                aposteriori = False
        else:
            intro = False
        name_text = " ".join(name_text)
        if apriori == False and aposteriori == False:
            intro = False
    return name_text


# metodo extraccion solo multiples coincidencias regularizada
def get_simple_namepropio2(text):
    tokens = nltk.tokenize.word_tokenize(text)
    person_list = [];
    name = "";
    inicio_bool = False;
    count = 0
    regex = r"^[A-Z][a-z]*"
    for element in tokens:
        if count < 10:
            if bool(re.search(regex, element)):
                name += element + " "
            else:
                name = clean_resuelve(name).strip()
                if inicio_bool:
                    count += 1
                if name != "":
                    if len(name.split()) > 1:
                        inicio_bool = True
                        count = 0
                        person_list.append(name.strip())
                    else:
                        if name.strip() in ["Corantioquia", "Incoder", "Uaegrtd", "Sena", "Uariv"]:
                            inicio_bool = True
                            count = 0
                            person_list.append(name.strip())
                    name = ""
        else:
            break

    #    person_list = [clean_name(name) for name in person_list]
    #    person_list = [name for name in person_list if len(name.split())>=2]
    person_list = list(map(str.strip, person_list))
    person_list = [elem.title() for elem in person_list]
    return person_list


def clean_item_resuelve(text):
    text = replace_accents(text).replace(",", " interruptor ")
    text = text.replace("?", " ")
    text = re.sub(' +', ' ', text)
    text = text.replace(" a las V", " A Las V").replace(" de las V", " De Las V").replace(" del M", " Del M").replace(
        "No.", "").replace(" instrumentos ", " Instrumentos ")
    text = text.replace(" para ", " Para ").replace(" de ", " De ").replace(" la ", " La ").replace(" y ",
                                                                                                    " Y ").replace(
        " e ", " E ").replace(" las ", " Las ").replace(" del ", " Del ")
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    regex = r"\b[A-Z][A-Z]+\b"
    replaceds = set(re.findall(regex, text))
    for replaced in replaceds:
        text = re.sub(rf"\b{replaced}\b", " " + replaced.capitalize() + " ", text)
    return text


def clean_item_resuelve_general(text):
    return replace_accents(text).lower().replace(" ", "")


def clean_item_1448(text):
    text = re.sub("(?<=\d)\s+(?=\d)", "", text)
    text = replace_accents(text).lower().replace(".", "").replace("1448", " 1448 ")
    text = re.sub(' +', ' ', text)
    return text


def extract_step_resuelve(file, corpus_temp):
    lines, inicio, final = extrac_resuelve(file, corpus_temp)
    lines = list(map(str.strip, lines))
    Counter_lines_eliminate = {name_def: n_def for name_def, n_def in Counter(lines).items() if
                               n_def > 5 and name_def != ""}

    resuelve_work = "\r\n".join(lines[inicio:final + 1]).replace("TERCERO ", "TERCERO: ").replace("ORDENAR,",
                                                                                                  "ORDENAR").replace(
        "ordenar,", "ordenar")

    lines = resuelve_work.split('\r\n')
    lines_clean = []
    for line in lines:
        line = re.sub(' +', ' ', line).strip()
        include = True
        line_temp = replace_accents(line).lower()
        if line == "": include = False
        if bool(re.findall(r"pag[.]*\w*\s*\d+", line_temp)) or bool(re.findall(r"^\d+$", line_temp)): include = False
        if include == True: lines_clean.append(line)

    lines_clean_vf = []
    for line in lines_clean:
        include = True
        for name_def, n_def in Counter_lines_eliminate.items():
            if line == name_def:
                include = False
                break
        if include == True:
            lines_clean_vf.append(line)

    intro = False
    cnt = 0
    list_start = []
    for index, line in enumerate(lines_clean_vf):
        line = clean_steep1(line)
        ver = re.findall(r"^(.+?)[:|.]\s", line)
        if ver != [] and len(ver[0]) < 25 and len(ver[0]) > 4:
            search_intro = ordinales[cnt]
            for search in search_intro:
                if SequenceMatcher(None, clean_item_resuelve_general(ver[0]),
                                   clean_item_resuelve_general(search)).ratio() > 0.9:
                    cnt += 1
                    list_start.append({"index": cnt, "len_string": len(ver[0]) + 2, "start": index})
                    if intro: list_start[cnt - 2]["final"] = index - 1
                    intro = True
                    break
    list_resuelves = []
    list_resuelves_work = []
    if intro:
        list_start[cnt - 1]["final"] = len(lines_clean_vf) - 1
        for lt in list_start:
            lt_text = lines_clean_vf[lt["start"]:lt["final"] + 1]
            list_resuelves.append(lt_text)
            lt_text_copy = lt_text.copy()
            lt_text_copy[0] = clean_steep1(lt_text_copy[0])[lt["len_string"]:]
            list_resuelves_work.append(lt_text_copy)
        print("Resuelve fragmentado Parte 1\n")
    else:
        print("Resuelve no desfragmentado Parte 1\n")

    if list_resuelves == []:
        ordinales_numeric = range(1, 100)
        intro = False
        cnt = 0
        list_start = []
        for index, line in enumerate(lines_clean_vf):
            line = clean_steep2(line)
            ver = re.findall(r"^\d{1,2}[.]\)?-?_?\s", line)
            if ver != []:
                search_intro = int(ordinales_numeric[cnt])
                search_numeric = int(re.findall('\\b\\d+\\b', ver[0])[0])
                if search_numeric == search_intro:
                    cnt += 1
                    list_start.append({"index": cnt, "len_string": len(ver[0]), "start": index})
                    if intro: list_start[cnt - 2]["final"] = index - 1
                    intro = True
        list_resuelves = []
        list_resuelves_work = []
        if intro:
            list_start[cnt - 1]["final"] = len(lines_clean_vf) - 1
            for lt in list_start:
                lt_text = lines_clean_vf[lt["start"]:lt["final"] + 1]
                list_resuelves.append(lt_text)
                lt_text_copy = lt_text.copy()
                lt_text_copy[0] = clean_steep2(lt_text_copy[0])[lt["len_string"]:]
                list_resuelves_work.append(lt_text_copy)
            print("Resuelve fragmentado Parte 2\n")
        else:
            print("Resuelve no desfragmentado Parte 2\n")

    return list_resuelves, list_resuelves_work


def create_df_resuelve(resuelvesf, resuelves_workf, file):
    #    refe = "Unidad Administrativa Especial de Gestión de Restitución de Tierras Despojadas"
    str_1 = "a|la|al|en"
    str_2 = "restituir|restitucion|restituirle|proteccion|entrega|inscripcion|protección|favor|señor"
    art_string1 = ["art " + str(_) for _ in list(range(1, 209))]
    art_string2 = ["articulo " + str(_) for _ in list(range(1, 209))]
    ordernar_text = ["ordenar", "ordena", "ordenese", "oficiar"]
    ordenar_beneficios = ["restituir", "restitucion", "restituirle", "proteccion", "entrega", "inscripcion",
                          "protección", "favor"]

    ordenar_list = []
    columns_dfr = ["id", "Resuelve_cnt", "Text Resuelve", "Ordena", "beneficios", "articulos"]
    columns_dfo = ["id", "Resuelve_cnt", "Entidad"]
    columns_dfb = ["id", "Resuelve_cnt", "Beneficio"]
    df_resuelve = pd.DataFrame(columns=columns_dfr)
    df_ordena_entidades = pd.DataFrame(columns=columns_dfo)
    df_ordena_beneficios = pd.DataFrame(columns=columns_dfb)

    cnt_ordena_entidades = 0
    cnt_ordena_beneficios = 0

    for index, item in enumerate(resuelves_workf):

        item = " \r\n ".join(item)

        item_List_1448 = nltk.Text(word_tokenize(clean_item_1448(item)))
        art_search_temp = item_List_1448.concordance_list("1448", width=120)
        articulo_text = []
        if len(art_search_temp) > 0:
            art_search_temp = [elem[6] for elem in art_search_temp]
            print(art_search_temp)
            for artt in art_search_temp:
                artt_search = re.search('\sart[iculos]?(.*)1448', artt.replace("-", ""), re.IGNORECASE)
                if artt_search is not None:
                    art_numbers = [int(word) for word in artt_search.group(1).split() if word.isdigit()]
                    print(art_numbers)
                    if art_numbers != []: articulo_text.append(art_numbers)
        if articulo_text != []:
            articulo_text = [item for lista in articulo_text for item in lista]
            articulo_text = ",".join([str(a) for a in set(articulo_text)])
            print(articulo_text)
        else:
            articulo_text = "Not found"

        item_List = nltk.Text(word_tokenize(clean_item_resuelve(item)))
        ordenar_search_lista = []
        for ordernar in ordernar_text:
            ordenar_search_temp = item_List.concordance_list(ordernar, width=480)
            if len(ordenar_search_temp) > 0:
                ordenar_search_temp = [elem[5] for elem in ordenar_search_temp]
                ordenar_search_lista += ordenar_search_temp

        osl_list_entidades = []
        osl_list_beneficios = []
        for osl in ordenar_search_lista:
            ordenar_select = re.findall(rf"^({str_1})?\s?({str_2})", osl, re.IGNORECASE)
            if ordenar_select == []:
                osl_list_entidades_temp = [get_simple_namepropio2(text) for text in ordenar_search_lista]
                osl_list_entidades += osl_list_entidades_temp
            else:
                osl_list_beneficios.append(osl)
        osl_list_entidades = [item for lista in osl_list_entidades for item in lista]

        if osl_list_entidades != [] and osl_list_entidades != [""]:
            cat_ordernar = "Si"
            for osl in set(osl_list_entidades):
                df_ordena_entidades.loc[cnt_ordena_entidades] = (file.split(".")[0], index + 1, osl)
                cnt_ordena_entidades += 1
        else:
            cat_ordernar = "No"

        if osl_list_beneficios != [] and osl_list_beneficios != [""]:
            cat_beneficio = "Si"
            for oslb in set(osl_list_beneficios):
                df_ordena_beneficios.loc[cnt_ordena_beneficios] = (file.split(".")[0], index + 1, oslb)
                cnt_ordena_beneficios += 1
        else:
            cat_beneficio = "No"

        ordenar_list.append(ordenar_search_lista)
        df_resuelve.loc[index] = (
        file.split(".")[0], index + 1, "\r\n".join(resuelvesf[index]), cat_ordernar, cat_beneficio, articulo_text)
    return df_resuelve, df_ordena_entidades, df_ordena_beneficios

def clean_steep1(text):
    text = text.replace(":", ": ").replace(".", ". ").replace(" :", ":").replace(" .", ".")
    text = re.sub(' +', ' ', text).strip()
    return text

def clean_steep2(text):
    text = text.replace(")", ".)").replace("_", "_ ")
    text = re.sub(' +', ' ', text).strip()
    text = re.sub('[.]+', '.', text).strip()
    return text

### Ejecución principal

############################
#New Load Postgrest
############################

engine = create_engine('postgresql://postgres:LFnnLUQZQMJ9@db-test2.cxqola6hllvk.us-east-2.rds.amazonaws.com/t96_dev')
df_work = pd.read_sql("SELECT * from mt_sentencia", engine.connect())
df_work.columns = ['certificado','clase','descargar','Municipio/Vereda del predio','estado','paginas','tipo_archivo']

codane = pd.read_sql("SELECT * from mt_dane_GEO", engine.connect())
codane.columns = ['Código Departamento', 'Código Municipio', 'Código Centro Poblado',
       'Nombre Departamento', 'Nombre Municipio', 'Nombre Centro Poblado',
       'Tipo Centro Poblado', 'Longitud', 'Latitud', 'Nombre Distrito',
       'Municipio/Áreas No Municipalizadas (ANM)',
       'Nombre Área Metropolitana']

Municipio_df = codane.loc[:,["Código Departamento","Código Municipio","Nombre Departamento","Nombre Municipio"]]
Municipio_df = Municipio_df.drop_duplicates().reset_index(drop=True)
Departamento_df = Municipio_df.loc[:,["Código Departamento","Nombre Departamento"]]
Departamento_df = Departamento_df.drop_duplicates().reset_index(drop=True)

#MY_STOP_DICC
Dicc_Stop = pd.read_csv(path_input + "/" + file_in_dicc_csv, encoding="ISO-8859-1") 
Dicc_Stop = list(Dicc_Stop.Palabras)

my_stop_words_descapitalize_nucleo = Dicc_Stop

#SHP
pnn_orig = geopandas.read_file(path_input + "/shp_sinap/" + file_in_geojson, driver = "GeoJSON")
pnn_orig = pnn_orig.loc[:,["nombre","categoria","geometry"]]

# carga corpus txt
corpus = PlaintextCorpusReader(path_input_txt, file_ids_text)
ids = corpus.fileids()

# carga corpus ocr
corpus_ocr = PlaintextCorpusReader(path_input_ocr, file_ids_ocr)
ids_ocr = corpus_ocr.fileids()

# lista de concordancias en las black_lists
black_list_magistrado=list_concordances_ltc(black_list_magistrado)
black_list_opositor=list_concordances_ltc(black_list_opositor)

#conecta con base de datos
engine = create_engine('YOUR CONNECTION STRING')

# Inserta en base de datos lo relacionado al corpus txt
for n in range(0,len(ids)):
    print("Procesando Archivo OCR ", ids[n])
    try:
        df_work_temp_fn, df_work_table_fn, df_locates_fn, df_pp_fn, nucleo_familiar_fn, df_rad_fn, df_cc_cat_fn, df_m_inm_fn, df_Georefenciacion_fn, list_locate_fn = return_tables_work(ids[n], corpus)
    except BaseException as ErrMsj:
        print("Error extrayendo información general. Archivo: ", ids[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_solicitante where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_pp_fn.empty: 
            db_tosql = df_pp_fn.copy()
            db_tosql.columns = ["nombre", "principal", "key", "cedula"]
            db_tosql.to_sql('tt_solicitante', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_grupo_familiar where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not nucleo_familiar_fn.empty:
            db_tosql = nucleo_familiar_fn.copy()
            db_tosql.columns = ["grupo", "n_persona", "name", "key", "cedula"]
            db_tosql.to_sql('tt_grupo_familiar', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_cedula_catastral where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_cc_cat_fn.empty:
            db_tosql = df_cc_cat_fn.copy()
            db_tosql.columns = ["cedula_catastral", "principal", "key"]
            db_tosql.to_sql('tt_cedula_catastral', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_matricula_inmobiliaria where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_m_inm_fn.empty:
            db_tosql = df_m_inm_fn.copy()
            db_tosql.columns = ["matricula_inmobiliaria", "principal", "key"]
            db_tosql.to_sql('tt_matricula_inmobiliaria', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_sentencia_geo where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_Georefenciacion_fn.empty:
            db_tosql = df_Georefenciacion_fn.copy()
            db_tosql.columns = ["key", "latitud", "longitud"]
            db_tosql.to_sql('tt_sentencia_geo', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_localizacion where certificado = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_locates_fn.empty:
            db_tosql = df_locates_fn.copy().reset_index()
            db_tosql.columns = [
                "certificado", "departamento", "codigo_departamento", "municipio", "codigo_municipio", 
                "corregimiento", "codigo_corregimiento", "vereda", "codigo_vereda"]
            db_tosql.to_sql('tt_localizacion', engine, if_exists='append', index=False)
    
    try:
        list_resuelvesf, list_resuelves_workf = extract_step_resuelve(ids[n], corpus)
        df_resuelve_w, df_ordena_entidades_w, df_ordena_beneficios_w = create_df_resuelve(list_resuelvesf, list_resuelves_workf, ids[n])
    except BaseException as ErrMsj:
        print("Error extrayendo resuelve. Archivo: ", ids[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_resuelve_text where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_resuelve_w.empty:
            db_tosql = df_resuelve_w.copy()
            db_tosql.columns = ["key", "contador", "texto", "orderna", "beneficios", "articulos"]
            db_tosql.to_sql('tt_resuelve_text', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_ordena_entidades where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_ordena_entidades_w.empty:
            db_tosql = df_ordena_entidades_w.copy()
            db_tosql.columns = ["key", "contador", "entidad"]
            db_tosql.to_sql('tt_ordena_entidades', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_ordena_beneficios where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_ordena_beneficios_w.empty:
            db_tosql = df_ordena_beneficios_w.copy()
            db_tosql.columns = ["key", "contador", "beneficio"]
            db_tosql.to_sql('tt_ordena_beneficios', engine, if_exists='append', index=False)


# Inserta en base de datos lo relacionado al corpus OCR
for n in range(0,len(ids_ocr)):
    print("Procesando Archivo OCR ", ids_ocr[n])
    try:
        df_work_temp_fn, df_work_table_fn, df_locates_fn, df_pp_fn, nucleo_familiar_fn, df_rad_fn, df_cc_cat_fn, df_m_inm_fn, df_Georefenciacion_fn, list_locate_fn = return_tables_work(ids_ocr[n], corpus_ocr)
    except BaseException as ErrMsj:
        print("Error extrayendo información general. Archivo: ", ids_ocr[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_solicitante where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_pp_fn.empty:
            db_tosql = df_pp_fn.copy()
            db_tosql.columns = ["nombre", "principal", "key", "cedula"]
            db_tosql.to_sql('tt_solicitante', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_grupo_familiar where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not nucleo_familiar_fn.empty:
            db_tosql = nucleo_familiar_fn.copy()
            db_tosql.columns = ["grupo", "n_persona", "name", "key", "cedula"]
            db_tosql.to_sql('tt_grupo_familiar', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_cedula_catastral where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_cc_cat_fn.empty:
            db_tosql = df_cc_cat_fn.copy()
            db_tosql.columns = ["cedula_catastral", "principal", "key"]
            db_tosql.to_sql('tt_cedula_catastral', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_matricula_inmobiliaria where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_m_inm_fn.empty:
            db_tosql = df_m_inm_fn.copy()
            db_tosql.columns = ["matricula_inmobiliaria", "principal", "key"]
            db_tosql.to_sql('tt_matricula_inmobiliaria', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_sentencia_geo where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_Georefenciacion_fn.empty:
            db_tosql = df_Georefenciacion_fn.copy()
            db_tosql.columns = ["key", "latitud", "longitud"]
            db_tosql.to_sql('tt_sentencia_geo', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_localizacion where certificado = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_locates_fn.empty:
            db_tosql = df_locates_fn.copy().reset_index()
            db_tosql.columns = [
                "certificado", "departamento", "codigo_departamento", "municipio", "codigo_municipio", 
                "corregimiento", "codigo_corregimiento", "vereda", "codigo_vereda"]
            db_tosql.to_sql('tt_localizacion', engine, if_exists='append', index=False)

    try:
        list_resuelvesf, list_resuelves_workf = extract_step_resuelve(ids_ocr[n], corpus_ocr)
        df_resuelve_w, df_ordena_entidades_w, df_ordena_beneficios_w = create_df_resuelve(list_resuelvesf, list_resuelves_workf, ids_ocr[n])
    except BaseException as ErrMsj:
        print("Error extrayendo resuelve. Archivo: ", ids_ocr[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_resuelve_text where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_resuelve_w.empty:
            db_tosql = df_resuelve_w.copy()
            db_tosql.columns = ["key", "contador", "texto", "orderna", "beneficios", "articulos"]
            db_tosql.to_sql('tt_resuelve_text', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_ordena_entidades where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_ordena_entidades_w.empty:
            db_tosql = df_ordena_entidades_w.copy()
            db_tosql.columns = ["key", "contador", "entidad"]
            db_tosql.to_sql('tt_ordena_entidades', engine, if_exists='append', index=False)

        strSQLDelete = "delete from tt_ordena_beneficios where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_ordena_beneficios_w.empty:
            db_tosql = df_ordena_beneficios_w.copy()
            db_tosql.columns = ["key", "contador", "beneficio"]
            db_tosql.to_sql('tt_ordena_beneficios', engine, if_exists='append', index=False)
