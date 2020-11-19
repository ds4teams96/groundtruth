#!/usr/bin/python
# -*- coding: latin-1 -*-

### importacion de librerÃ­as
import common as t96
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd 
from sqlalchemy import create_engine

### Variables 
path_driver_1 = t96.path_driver_sl
path_files_scraping_1 = t96.path_in_static_data

### Funciones
def create_df_scraping(path_files_scraping, path_driver):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--disable-browser-side-navigation')
	chrome_options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(path_driver, options=chrome_options)

	url = t96.url_scraping
	driver.get(url)

	page_ini = BeautifulSoup(driver.page_source,"html5lib")
	print("Source General OK")
	tables_ini = page_ini.find_all("table")[1]
	tables_ini = tables_ini.find('tbody')

	data_ini = []
	n = 1 
	for td in tables_ini.find_all('tr'):
		if n > 1:
			row = [i.text for i in td.find_all('td')] 
			data_ini.append(row)
		n+=1

	link = driver.find_elements_by_link_text("Select")
	time.sleep(1)
	link[0].click()
	time.sleep(1)
	page = BeautifulSoup(driver.page_source,"html5lib")
	tbody = page.find('tbody')

	data = []
	n = 1 
	for td in tbody.find_all('tr'):
		if n > 1:
			row = [i.text for i in td.find_all('td')]
			row[0] = str(1)
			data.append(row)
		n+=1

	# print("LEN data:", len(data))
	linkspage = [tag.get("href") for tag in page.findAll(attrs={'class': "btn btn-success"})]
	# print("LEN linkspage:", len(linkspage))

	print("Tables OK")

	# for i in range(1,20):
	for i in range(1,len(link)):
		print("For init", i)
		driver.get(url)
		link = driver.find_elements_by_link_text("Select")
		# time.sleep(1)
		link[i].click()
		# time.sleep(1)
		page = BeautifulSoup(driver.page_source,"html5lib")
		tbody = page.find('tbody')
		linkspage_tem =  [tag.get("href") for tag in page.findAll(attrs={'class': "btn btn-success"})]
		linkspage+=linkspage_tem
		# print("LEN linkspage A:", len(linkspage))
		n = 1
		for td in tbody.find_all('tr'):
			if n > 1:
				row = [i.text for i in td.find_all('td')]
				row[0] = str(i+1)
				data.append(row)
			n+=1 

	print("Cerrando driver")
	driver.close()

	print("Nueva URL Base")
	url_base = t96.url_base
	linkspage = ["{}{}".format(url_base,i) for i in linkspage]
	# print("LEN linkspage 2:", len(linkspage))

	#DataFrame Download
	print("Creando DF download")
	columns_names = ["Reg","Radicación","Clase","Nombre del Predio","Municipio/Vereda del predio","Fecha Providencia","Certificado","Descargar"]
	df2 = pd.DataFrame(data, columns = columns_names)
	df2 = df2.apply(lambda x: x.str.strip())
	print("df2", df2.size)
	df2["Descargar"] = linkspage
	df2.set_index("Reg", inplace = True) 
	df2.index = df2.index.astype(int)

	#DataFrame Principal
	print("Creando otro DF")
	columns_names = ["Reg","Ciudad","IdDespacho","Despacho Judicial","Año","Cantidad Sentencias","Adiciona Complementa","Fecha Ultima Sentencia"]
	df1 = pd.DataFrame(data_ini, columns = columns_names)
	df1 = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
	df1["Reg"] = df1.index+1
	df1.set_index("Reg", inplace = True) 
	df1.index = df1.index.astype(int)

	print("Scraping Download")
	df_work = pd.merge(df2, df1, how="left", left_index=True, right_index=True)
	print("Finalizando")
	return df_work

def create_new_dowload(df_work_now, DBengine):
	df_work_old = pd.read_sql("SELECT * from vw_certificado_radicacion_finalizado", DBengine.connect())
	print("Datos Historicos: ", df_work_old.shape)
	new_dowload = df_work_now.merge(df_work_old.drop_duplicates(), on=["Radicación","Certificado"], how='left', indicator=True)
	new_dowload = new_dowload[new_dowload["_merge"]=="left_only"] 
	new_dowload = new_dowload.iloc[:,0:14]
	new_dowload.columns = df_work_now.columns
	new_dowload.drop(new_dowload[new_dowload['Certificado']=='Pendiente por subir soporte documental'].index, inplace=True)
	if not new_dowload.empty:
		db_tosql = new_dowload.reset_index()[['Certificado','Clase','Descargar','Ciudad']].drop_duplicates().copy()
		db_tosql.columns = ["certificado","clase","descargar","ciudad"]
		db_tosql.to_sql('mt_sentencia', engine, if_exists='append', index=False)
		db_tosql = new_dowload.reset_index()[["Certificado", "Radicación", "Nombre del Predio",
											  "Municipio/Vereda del predio", "Fecha Providencia", "IdDespacho",
											  "Despacho Judicial", "Año", "Cantidad Sentencias",
											  "Adiciona Complementa", "Fecha Ultima Sentencia"]].copy()
		db_tosql.columns = ["certificado", "radicacion", "nombre_predio", "municipio_vereda",
							"fecha_providencia", "id_despacho", "despacho_judicial", "anio",
							"cantidad_sentencias", "adiciona_complementa", "fecha_ultima_sentencia"]
		db_tosql.to_sql('tt_radicado', engine, if_exists='append', index=False)
	# new_dowload.to_csv(path_files_scraping_1+"new_dowload.csv",encoding='utf-8-sig')
	# df_work_old_copy.to_csv(path_files_scraping_1+"Data_final_old_copy.csv",encoding='utf-8-sig')
	# df_work_old = pd.concat([df_work_old,new_dowload])
	# df_work_old.to_csv(path_files_scraping_1+"Data_final_old.csv",encoding='utf-8-sig')
	print("Nueva Unificacion: ", df_work_old.shape)
	print("Scraping Actual:" ,df_work_now .shape)
	engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Webscraping','Registros validados " + str(df_work_now.shape) + "')")
	print("Registros Nuevos:" ,new_dowload.shape)
	engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Webscraping','Registros Nuevos " + str(new_dowload.shape) + "')")


### main
engine = create_engine(t96.sqlConnString)
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Webscraping','Inicia proceso')")
df_scrap = create_df_scraping(path_files_scraping_1, path_driver_1)
create_new_dowload(df_scrap, engine)
engine.execute("insert into tt_log_transaccion (operacion, comentario) values ('Webscraping','Fin proceso')")
