#!/usr/bin/python
# -*- coding: latin-1 -*-

### LOAD LIBRARIES
import pandas as pd
import re
import string
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from tqdm import tqdm
from sqlalchemy import create_engine

### GLOBAL VARIABLES
path_data = 'tmp/output'
path_out_model = 'data'
file_in_resuelve = "resuelve.csv"

### LOAD MODELS
with open(path_out_model + '/' + 'ModelOrdenVivienda.pkl', 'rb') as file:
    ModelOrdenVivienda = pickle.load(file)
    
with open(path_out_model + '/' + 'ModelProyectosProductivos.pkl', 'rb') as file:
    ModelProyectosProductivos = pickle.load(file)
    
with open(path_out_model + '/' + 'ModelCompensacionVictimas.pkl', 'rb') as file:
    ModelCompensacionVictimas = pickle.load(file)

with open(path_out_model + '/' + 'ModelCompensacionTerceros.pkl', 'rb') as file:
    ModelCompensacionTerceros = pickle.load(file)

with open(path_out_model + '/' + 'ModelSegundosOcupantes.pkl', 'rb') as file:
    ModelSegundosOcupantes = pickle.load(file)

with open(path_out_model + '/' + 'ModelAlivioPredial.pkl', 'rb') as file:
    ModelAlivioPredial = pickle.load(file)

with open(path_out_model + '/' + 'ModelAlivioSPD.pkl', 'rb') as file:
    ModelAlivioSPD = pickle.load(file)

with open(path_out_model + '/' + 'ModelAlivioPasivosFinancieros.pkl', 'rb') as file:
    ModelAlivioPasivosFinancieros = pickle.load(file)

with open(path_out_model + '/' + 'ModelPagoCostas.pkl', 'rb') as file:
    ModelPagoCostas = pickle.load(file)

with open(path_out_model + '/' + 'ModelAdministracionProyectosProductivos.pkl', 'rb') as file:
    ModelAdministracionProyectosProductivos = pickle.load(file)

with open(path_out_model + '/' + 'ModelOtros.pkl', 'rb') as file:
    ModelOtros = pickle.load(file)

with open(path_out_model + '/' + 'ModelDireccionSocial.pkl', 'rb') as file:
    ModelDireccionSocial = pickle.load(file)

with open(path_out_model + '/' + 'ModelCatastro.pkl', 'rb') as file:
    ModelCatastro = pickle.load(file)


### EXECUTION

### LOAD DATA
engine = create_engine('postgresql://postgres:LFnnLUQZQMJ9@db-test2.cxqola6hllvk.us-east-2.rds.amazonaws.com/t96_dev')
DF = pd.read_sql("SELECT * from vw_pendiente_modelo", engine.connect())
resuelve_O = pd.read_csv(path_data + '/' + file_in_resuelve)
resuelve_e = DF
resuelve_O['key_temp'] = resuelve_O['certificado']+resuelve_O['radicado']

stopwords_spanish = stopwords.words('spanish')
resuelve_e['RE'] = ''
for r in tqdm(range(len(resuelve_e))):
    text_temp = resuelve_e['resuelve'][r]
    text_temp = re.sub(r'C.C.', r'CÉDULA', text_temp)
    text_temp = re.sub(r'No.', r'NÚMERO', text_temp)
    text_temp = sent_tokenize(text_temp.lower())
    text_temp2 = []
    for sentence in range(len(text_temp)):
        ou1 = ""
        for word in word_tokenize(text_temp[sentence]):
            if(word not in stopwords_spanish and word not in string.punctuation):
                ou1 += ' '+word
        text_temp2.append(ou1)
        ou2 = ""
        for sentence in text_temp2:
            ou2 += ' '+sentence
            resuelve_e['RE'][r] = ou2

resuelve_O['RE'] = ''
for r in tqdm(range(len(resuelve_O))):
    text_temp = resuelve_O['Resuelve'][r]
    text_temp = re.sub(r'C.C.', r'CÉDULA', text_temp)
    text_temp = re.sub(r'No.', r'NÚMERO', text_temp)
    text_temp = sent_tokenize(text_temp.lower())
    text_temp2 = []
    for sentence in range(len(text_temp)):
        ou1 = ""
        for word in word_tokenize(text_temp[sentence]):
            if(word not in stopwords_spanish and word not in string.punctuation):
                ou1 += ' '+word
        text_temp2.append(ou1)
        ou2 = ""
        for sentence in text_temp2:
            ou2 += ' '+sentence
            resuelve_O['RE'][r] = ou2

list_text = list(resuelve_O['RE'].values)
list_textP = list(resuelve_e['RE'].values)
count_vector = CountVectorizer(max_features=100, ngram_range=(1, 2))
matrix_text_cv = count_vector.fit_transform(list_text)
x = matrix_text_cv.toarray()
matrix_text_cv_p = count_vector.transform(list_textP)
x_p = matrix_text_cv_p.toarray()

resuelve_e['orden_vivienda'] = ModelOrdenVivienda.predict(x_p)
resuelve_e['orden_vivienda'] = np.where(resuelve_e['orden_vivienda']== 1, 'SI', 'NO')

resuelve_e['proyectos_productivos_beneficiarios_restitucion'] = ModelProyectosProductivos.predict(x_p)
resuelve_e['proyectos_productivos_beneficiarios_restitucion'] = np.where(resuelve_e['proyectos_productivos_beneficiarios_restitucion']== 1, 'SI', 'NO')

resuelve_e['compensacion_victimas'] = ModelCompensacionVictimas.predict(x_p)
resuelve_e['compensacion_victimas'] = np.where(resuelve_e['compensacion_victimas']== 1, 'SI', 'NO')

resuelve_e['compensacion_terceros'] = ModelCompensacionTerceros.predict(x_p)
resuelve_e['compensacion_terceros'] = np.where(resuelve_e['compensacion_terceros']== 1, 'SI', 'NO')

resuelve_e['segundos_ocupantes'] = ModelSegundosOcupantes.predict(x_p)
resuelve_e['segundos_ocupantes'] = np.where(resuelve_e['segundos_ocupantes']== 1, 'SI', 'NO')

resuelve_e['alivio_predial'] = ModelAlivioPredial.predict(x_p)
resuelve_e['alivio_predial'] = np.where(resuelve_e['alivio_predial']== 1, 'SI', 'NO')

resuelve_e['alivio_servicios_publicos'] = ModelAlivioSPD.predict(x_p)
resuelve_e['alivio_servicios_publicos'] = np.where(resuelve_e['alivio_servicios_publicos']== 1, 'SI', 'NO')

resuelve_e['alivio_pasivos_financieros'] = ModelAlivioPasivosFinancieros.predict(x_p)
resuelve_e['alivio_pasivos_financieros'] = np.where(resuelve_e['alivio_pasivos_financieros']== 1, 'SI', 'NO')

resuelve_e['pagos_costas_gastos_judiciales'] = ModelPagoCostas.predict(x_p)
resuelve_e['pagos_costas_gastos_judiciales'] = np.where(resuelve_e['pagos_costas_gastos_judiciales']== 1, 'SI', 'NO')

resuelve_e['administracion_proyectos_productivos_agroindustriales'] = ModelAdministracionProyectosProductivos.predict(x_p)
resuelve_e['administracion_proyectos_productivos_agroindustriales'] = np.where(resuelve_e['administracion_proyectos_productivos_agroindustriales']== 1, 'SI', 'NO')

resuelve_e['otras_ordenes'] = ModelOtros.predict(x_p)
resuelve_e['otras_ordenes'] = np.where(resuelve_e['otras_ordenes']== 1, 'SI', 'NO')

resuelve_e['ordenes_direccion_social'] = ModelDireccionSocial.predict(x_p)
resuelve_e['ordenes_direccion_social'] = np.where(resuelve_e['ordenes_direccion_social']== 1, 'SI', 'NO')

resuelve_e['ordenes_catastrales'] = ModelDireccionSocial.predict(x_p)
resuelve_e['ordenes_catastrales'] = np.where(resuelve_e['ordenes_catastrales']== 1, 'SI', 'NO')

resuelve_e['key_temp'] = resuelve_e['certificado']+resuelve_e['radicado']
vector_certificado = resuelve_O['key_temp'].unique()
resuelve_e = resuelve_e[resuelve_e['key_temp'].isin(vector_certificado.tolist()) == False]

resuelve_e = resuelve_e.drop('RE', axis=1)
resuelve_e = resuelve_e.drop('key_temp', axis=1)
resuelve_e['usa_modelo'] = 'SI'

strSQLDelete = "delete from tt_resuelve tr where certificado in (select certificado from vw_pendiente_modelo)"
engine.execute(strSQLDelete)
if not resuelve_e.empty:
    db_tosql = resuelve_e.copy()
    db_tosql.to_sql('tt_resuelve', engine, if_exists='append', index=False)