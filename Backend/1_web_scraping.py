#!/usr/bin/python
# -*- coding: latin-1 -*-

### importacion de librerÃ­as
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd 

### Variables 
# path_driver_1 = "C:\Instaladores\chromedriver.exe"
path_driver_1 = "/home/ubuntu/driver/chromedriver"
path_files_scraping_1 = "data/"

### Funciones
def create_df_scraping(path_files_scraping, path_driver):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument('--disable-browser-side-navigation')
	chrome_options.add_argument('--no-sandbox')
	driver = webdriver.Chrome(path_driver, options=chrome_options)

	url = "http://190.217.24.108/restituciontierras/views/old/sentencias.aspx"
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
	Select_cnt = 0
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

	linkspage = [tag.get("href") for tag in page.findAll(attrs={'class': "btn btn-success"})]

	print("Tables OK")

	# for i in range(1,2):
	for i in range(1,len(link)):
		print("For init", i)
		driver.get(url)
		link = driver.find_elements_by_link_text("Select")
		time.sleep(1)
		link[i].click()
		time.sleep(1)
		page = BeautifulSoup(driver.page_source,"html5lib")
		tbody = page.find('tbody')
		linkspage_tem =  [tag.get("href") for tag in page.findAll(attrs={'class': "btn btn-success"})]
		linkspage+=linkspage_tem
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
	url_base = "http://190.217.24.108/restituciontierras/views/old/"
	linkspage = ["{}{}".format(url_base,i) for i in linkspage]
	now = str(datetime.now().date())

	#DataFrame Download
	print("Creando DF download")
	columns_names = ["Reg","Radicación","Clase","Nombre del Predio","Municipio/Vereda del predio","Fecha Providencia","Certificado","Descargar"]
	df2 = pd.DataFrame(data, columns = columns_names)
	df2 = df2.apply(lambda x: x.str.strip())
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
	name_file_scrap = "Data_final-"+ now
	df_work = pd.merge(df2, df1, how="left", left_index=True, right_index=True)
	df_work.to_csv(path_files_scraping+name_file_scrap+".csv",encoding='utf-8-sig')

	print("Finalizando")

def create_new_dowload(): 
	now = str(datetime.now().date())
	# Data_Download_final por Data_final
	name_file_scrap = "Data_final-"+ now
	# read_pickle por read_csv
	df_work_now = pd.read_csv(path_files_scraping_1+name_file_scrap+".csv")
	df_work_old = pd.read_csv(path_files_scraping_1+"Data_final_old.csv")
	print("Datos Historicos: ", df_work_old.shape)
	df_work_old_copy = df_work_old.copy()
	new_dowload = df_work_now.merge(df_work_old.drop_duplicates(), on=["Radicación","Certificado"], how='left', indicator=True)
	new_dowload = new_dowload[new_dowload["_merge"]=="left_only"] 
	new_dowload = new_dowload.iloc[:,0:15]
	new_dowload.columns = df_work_now.columns
	new_dowload.to_csv(path_files_scraping_1+"new_dowload.csv",encoding='utf-8-sig')
	df_work_old_copy.to_csv(path_files_scraping_1+"Data_final_old_copy.csv",encoding='utf-8-sig')
	df_work_old = pd.concat([df_work_old,new_dowload])
	df_work_old.to_csv(path_files_scraping_1+"Data_final_old.csv",encoding='utf-8-sig')
	print("Nueva Unificacion: ", df_work_old.shape)
	print("Scraping Actual:" ,df_work_now .shape)
	print("Registros Nuevos:" ,new_dowload.shape)


### main
create_df_scraping(path_files_scraping_1, path_driver_1)
create_new_dowload()
