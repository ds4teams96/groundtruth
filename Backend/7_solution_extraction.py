#!/usr/bin/python
# -*- coding: latin-1 -*-

### LOAD LIBRARIES
import os
import pandas as pd
import re
import string
from nltk.corpus import PlaintextCorpusReader
from sqlalchemy import create_engine
from tqdm import tqdm

# GLOBAL VARIABLES
path_input = 'data'
path_input_txt = 'tmp/text'
path_input_ocr = 'tmp/ocr'
path_output_csv = 'tmp/output'
file_ids = ".*.txt"
file_input_csv = 'Union.csv'
file_output_csv = 'resuelve.csv'

engine = create_engine('YOUR CONNECTION STRING')

txt_inicio = ["RESUELVE",
              "R E S U ELV E",
              "RESUELV E",
              "Resuelve",
              "RESUEL VE",
              "RESUELV",
              "RE SUE LV E",
              "RE S U E L V E",
              "RESU.ELVE",
              "R E S U E L V E",
              "RESUELVA",
              "DECISION:",
              "VI. DECISION",
              "FALLA",
              "ORDENES:",
              "ORDENES"
             ]
# Create corpus from sentences convert from PDF to TXT
corpus = PlaintextCorpusReader(path_input_txt, file_ids)
ids = corpus.fileids()
# Create corpus from sentences convert from PDF to OCR to TXT
corpus_ocr = PlaintextCorpusReader(path_input_ocr, file_ids)
ids_ocr = corpus_ocr.fileids()

no_exportado = []
exportado = []
no_resuelves = []
resuelves = []
n = 0

### FUNCTIONS

#This function replace vocals with accent mark to vocals without accent mark
def replace_accents(text):
    a,b = 'áéíóúüÁÉÍÓÚ','aeiouuAEIOU'
    trans = str.maketrans(a,b)
    return text.translate(trans)
#This function EXTRACT from TXT sentence the RESUELVE section
def extract_resuelve(fileid, corpus_temp): 
    counter = -1
    inicio = 0
    final = 0
    lines = corpus_temp.raw(fileid).replace("RESUELV E","RESUELVE").split('\r\n')
    for line in lines:
        counter=counter+1
        line_temp = replace_accents(re.sub(' +', ' ',line).strip().upper())
        for txt in txt_inicio:
            line = line.replace("?","").replace("•","")
            if bool(re.search(rf"{txt}\s*:*=*·*[.]*$", replace_accents(re.sub(' +', ' ',line).strip()))):
                inicio = counter
                final  = len(lines)
                break
    return lines, inicio, final
#This function returns the first position of specific word inside text
def findText(text, word_start):
    start_f = text.find(word_start)
    return start_f
#This function EXTRACT from TXT sentence the RESUELVE section as second options when extract_resuelve function fails
def extract_resuelve2(fileid, corpus_temp):
    inicio = 0
    final = 0
    lines = corpus_temp.raw(fileid)
    for txt in txt_inicio:
        val_temp = findText(corpus_temp.raw(fileid), txt)
        if val_temp > 0:
            inicio = findText(corpus_temp.raw(fileid), txt)
            final  = len(lines)
            break
    return lines, inicio, final

### EXECUTION
# txt document
print('\n ************** Un total de', len(ids), 'archivos transformados de pdf a txt')
for file in tqdm(range(len(ids))):
    lines, inicio, final = extract_resuelve(ids[file], corpus)
    text = lines[inicio:final]
    if len(text)==0:
        lines, inicio, final = extract_resuelve2(ids[file], corpus)
        text = lines[inicio:final]
        text = text.split('\r\n')
    text = [item.lower() for item in text]
    matches = [match for match in text if "primero" in match]
    if len(matches)>0:
        exportado.append(ids[file])
        resuelves.append(text)
    else:
        matches = [match for match in text if "1)" in match]
        if len(matches)>0:
            exportado.append(ids[file])
            resuelves.append(text)
        else:
            matches = [match for match in text if "1." in match]
            if len(matches)>0:
                exportado.append(ids[file])
                resuelves.append(text)
            else:
                no_exportado.append(ids[file])
                no_resuelves.append(text)

print('Exportado: ', len(exportado))
print('No exportado: ', len(no_exportado))

# ocr document
print('\n ************** Un total de', len(ids_ocr), 'archivos transformados de pdf a ocr a txt')
for file in tqdm(range(len(ids_ocr))):
    lines, inicio, final = extract_resuelve(ids_ocr[file], corpus_ocr)
    text = lines[inicio:final]
    if len(text)==0:
        lines, inicio, final = extract_resuelve2(ids_ocr[file], corpus_ocr)
        text = lines[inicio:final]
        text = text.split('\r\n')
    text = [item.lower() for item in text]
    matches = [match for match in text if "primero" in match]
    
    if len(matches)>0:
        exportado.append(ids_ocr[file])
        resuelves.append(text)
    else:
        matches = [match for match in text if "1)" in match]
        if len(matches)>0:
            exportado.append(ids_ocr[file])
            resuelves.append(text)
        else:
            matches = [match for match in text if "1." in match]
            if len(matches)>0:
                exportado.append(ids_ocr[file])
                resuelves.append(text)
            else:
                no_exportado.append(ids_ocr[file])
                no_resuelves.append(text)

print('Exportado: ', len(exportado))
print('No exportado: ', len(no_exportado))

new_resuelves = []
x = ''
for n in range(len(resuelves)):
    resuelve_text = x.join(resuelves[n])
    new_resuelves.append(resuelve_text)
#get names of files  than we can transform
exportado = [os.path.splitext(x)[0] for x in exportado]
#Dataframe with id sentence and RESUELVE section extracted
dict_resuelve = {'Certificado': exportado, 'Resuelve': new_resuelves}
df_resuelve = pd.DataFrame(dict_resuelve) 
#CSV provided by URT with classifications variables that we use to train models
df = pd.read_csv(path_input + '/' + file_input_csv)
df_resuelve = df_resuelve.merge(df[['certificado', 'radicado', 'ORDEN DE VIVIENDA',
                                    'PROYECTOS PRODUCTIVOS PARA BENEFICIARIOS DE RESTITUCIÓN', 'COMPENSACIÓN VICTIMAS', 
                                    'COMPENSACIÓN TERCEROS', 'SEGUNDOS OCUPANTES', 'ALIVIO PREDIAL', 
                                    'ALIVIO DE SERVICIOS PÚBLICOS', 'ALIVIO DE PASIVOS FINANCIEROS', 
                                    'PAGOS DE COSTAS Y GASTOS JUDICIALES', 
                                    'ADMINISTRACIÓN PROYECTOS PRODUCTIVOS AGROINDUSTRIALES', 'OTRAS ÓRDENES', 
                                    'ORDENES A DIRECCIÓN SOCIAL', 'ORDENES CATASTRALES']], how = 'left', on = 'Certificado')
df_resuelve_radicado = df_resuelve.copy()
df_resuelve_radicado.dropna(axis = 0, subset = ['Radicado'], inplace = True)

# Converto to CSV and Export to PostgreSQL
df_resuelve_radicado.to_csv(path_output_csv + '/' + file_output_csv, index = False)

strSQLDelete = "delete from tt_resuelve"
engine.execute(strSQLDelete)
if not df_resuelve_radicado.empty:
    db_tosql = df_resuelve_radicado.copy()
    db_tosql.columns = [
        "certificado","resuelve","radicado","orden_vivienda","proyectos_productivos_beneficiarios_restitucion",
        "compensacion_victimas","compensacion_terceros","segundos_ocupantes","alivio_predial","alivio_servicios_publicos",
        "alivio_pasivos_financieros","pagos_costas_gastos_judiciales","administracion_proyectos_productivos_agroindustriales",
        "otras_ordenes","ordenes_direccion_social","ordenes_catastrales"]
    db_tosql.to_sql('tt_resuelve', engine, if_exists='append', index=False)

