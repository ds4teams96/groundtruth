#!/usr/bin/python
# -*- coding: latin-1 -*-

# Importaciones
import common as t96
import pandas as pd
import os
import requests
from sqlalchemy import create_engine

# Variables globales
path_output = t96.path_tmp_pdf
url_error = t96.url_base + t96.url_base
url_base = t96.url_base

# Ejecucion principal
engine = create_engine(t96.sqlConnString)
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Download','Inicia proceso')")
df = pd.read_sql("select certificado, descargar from mt_sentencia where estado = 'Nuevo' limit 10", engine.connect())
df_sample = df.copy()
df_sample["descargar"] = list(map(lambda b: b.replace(url_error,url_base), df_sample["descargar"]))
df_sample = df_sample[df_sample["certificado"] != "Pendiente por subir soporte documental"]

if not os.path.isdir(path_output):
    os.makedirs(path_output)

n = 0
for row in df_sample.itertuples():
    link_download = row.descargar
    filename = os.path.join(path_output, row.certificado + ".pdf")
    myfile = requests.get(link_download, allow_redirects=True)
    open(filename, 'wb').write(myfile.content)
    print("DownLoad file: " + filename)
    strSQLUpdate = "update mt_sentencia set estado = 'Descargado' where certificado = '" + row.certificado + "'"
    engine.execute(strSQLUpdate)
    n+=1
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Download','Descargados " + str(n) + " pdfs')")
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Download','Fin proceso')")
