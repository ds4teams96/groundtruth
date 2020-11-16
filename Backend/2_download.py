#!/usr/bin/python
# -*- coding: latin-1 -*-

import pandas as pd
import os
import requests


path_input_csv = 'data'
path_output = "tmp/data"
file_input_csv = 'Data_Download_final.csv'
url_error = "http://190.217.24.108/restituciontierras/views/old/http://190.217.24.108/restituciontierras/views/old/"
url_base = "http://190.217.24.108/restituciontierras/views/old/"

df = pd.read_csv(path_input_csv + '/' + file_input_csv)
df_sample = df.copy()

df_sample["Descargar"] = list(map(lambda b: b.replace(url_error,url_base), df_sample["Descargar"]))
df_sample = df_sample[df_sample["Certificado"] != "Pendiente por subir soporte documental"]

if not os.path.isdir(path_output):
    os.makedirs(path_output)

for row in df_sample.itertuples():
    link_download = row.Descargar
    filename = os.path.join(path_output, row.Certificado + ".pdf")
    myfile = requests.get(link_download, allow_redirects=True)
    open(filename, 'wb').write(myfile.content)
    print("DownLoad file: " + row.Certificado + ".pdf")
