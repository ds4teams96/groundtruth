#!/usr/bin/python
# -*- coding: latin-1 -*-

### LOAD LIBRARIES
import common as t96
import os
import pandas as pd
import re
from nltk.corpus import PlaintextCorpusReader
from sqlalchemy import create_engine
from tqdm import tqdm

# GLOBAL VARIABLES
path_input = t96.path_in_static_data[:-1]
path_input_txt = t96.path_tmp_txt[:-1]
path_input_ocr = t96.path_tmp_ocr[:-1]
path_output_csv = t96.path_tmp_output[:-1]

file_input_csv = t96.file_in_union_csv
file_ids = ".*.txt"

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
    lines = corpus_temp.raw(fileid).replace("RESUELV E","RESUELVE").splitlines()
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
engine = create_engine(t96.sqlConnString)
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Resuelve','Inicia proceso')")

print('\n ************** Un total de', len(ids), 'archivos transformados de pdf a txt')
for file in tqdm(range(len(ids))):
    lines, inicio, final = extract_resuelve(ids[file], corpus)
    text = lines[inicio:final]
    if len(text)==0:
        lines, inicio, final = extract_resuelve2(ids[file], corpus)
        text = lines[inicio:final]
        text = text.splitlines()
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
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Resuelve','Exportado en formato TXT: " + str(len(exportado)) + "')")
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Resuelve','No exportado en formato TXT: " + str(len(no_exportado)) + "')")

# ocr document
print('\n ************** Un total de', len(ids_ocr), 'archivos transformados de pdf a ocr a txt')
for file in tqdm(range(len(ids_ocr))):
    lines, inicio, final = extract_resuelve(ids_ocr[file], corpus_ocr)
    text = lines[inicio:final]
    if len(text)==0:
        lines, inicio, final = extract_resuelve2(ids_ocr[file], corpus_ocr)
        text = lines[inicio:final]
        text = text.splitlines()
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
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Resuelve','Exportado con OCR: " + str(len(exportado)) + "')")
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Resuelve','No exportado con OCR: " + str(len(no_exportado)) + "')")

new_resuelves = []
x = ''
for n in range(len(resuelves)):
    resuelve_text = x.join(resuelves[n])
    new_resuelves.append(resuelve_text)
#get names of files  than we can transform
exportado = [os.path.splitext(x)[0] for x in exportado]
#Dataframe with id sentence and RESUELVE section extracted
dict_resuelve = {'certificado': exportado, 'resuelve': new_resuelves}
df_resuelve = pd.DataFrame(dict_resuelve) 
#CSV provided by URT with classifications variables that we use to train models
df = pd.read_csv(path_input + '/' + file_input_csv)
df_resuelve = df_resuelve.merge(df[['certificado', 'radicacion', 'orden de vivienda',
                                    'proyectos productivos para beneficiarios de restitucion', 'compensacion victimas',
                                    'compensacion terceros', 'segundos ocupantes', 'alivio predial',
                                    'alivio de servicios publicos', 'alivio de pasivos financieros',
                                    'pagos de costas y gastos judiciales',
                                    'administracion proyectos productivos agroindustriales', 'otras ordenes',
                                    'ordenes a direccion social', 'ordenes catastrales']], how = 'left', on = 'certificado')

if not df_resuelve.empty:
    db_tosql = df_resuelve[['certificado']].copy()
    db_tosql.to_sql('temp_new_resuelve', engine, if_exists='replace', index=False)

strSQLDelete = "delete from tt_resuelve where certificado in (select certificado from temp_new_resuelve)"
engine.execute(strSQLDelete)
if not df_resuelve.empty:
    db_tosql = df_resuelve.copy()
    db_tosql.columns = [
        "certificado","resuelve","radicado","orden_vivienda","proyectos_productivos_beneficiarios_restitucion",
        "compensacion_victimas","compensacion_terceros","segundos_ocupantes","alivio_predial","alivio_servicios_publicos",
        "alivio_pasivos_financieros","pagos_costas_gastos_judiciales","administracion_proyectos_productivos_agroindustriales",
        "otras_ordenes","ordenes_direccion_social","ordenes_catastrales"]
    db_tosql.to_sql('tt_resuelve', engine, if_exists='append', index=False)

engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Extracion Resuelve','Fin proceso')")