#################################################################################################
'''
EXTRACTION OF RELEVANT INFORMATION:

-HEADER: Court,date_file			
[tt_encabezado]
-OPPONENT: Name and DNI possible opponents	
[tt_opositor]
-MAGISTRATE/JUDGE: Names possible magistrates or judges, class document 	
[tt_juez_magistrado]
-AREA: possibles land areas (low quality extraction! , is not possible to define the total area of the land)
[tt_area]
'''
##################################################################################################

import numpy as np
#########################
###     LIBRARIES     ###
#########################
import pandas as pd
import seaborn as sns;

sns.set()
import math

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
import re, string
from collections import Counter
from sqlalchemy import create_engine

#########################
### GLOBAL VARIABLES ####
#########################

path_input = 'data'
path_input_txt = 'tmp/text'
path_input_ocr = 'tmp/ocr'

file_despachos = 'Despachos.csv.csv'

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
                               "Antioquia","Agropecuaria","Carmen De Bolivar","Colombiano","Bienestar","Cuaderno","Ppal",
                              'Uaegrtd','PONENTE']
                               
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
                       'primero','segundo','tercero','gistrada','rada','magis','Magis rado',
                       'Ddr','auc','Notifíquese', 'Cúmplase','Magistrado','sustanciador','Notifíquese','cumplase',
                       'Notifíquese Cumplase','Uaegrtd','magistrada']


key_tribunal1=['tribunal superior del','tribunal superior de','tribunal superior']
key_opositor=['opositor','opone','opositores','oponen','opositora','oposltor']
key_opositor2=['oposición','oposocion']
black_list_opositor=['opositor','opone','opositores','Opositora','oponen','opositora','Resolución','nro','OPOSICION','es','se'
                    'Es','Registro','ministerio','publico','Ministerio Público','Comisiona','Segundo','“','.','"']


key_area=['area','extension ','hectarea','hectareas','hcs','predio','lote','parcela']
key_area2=['mt','mts cuadrados','m2','metros cuadrados','hectarea','hectareas','hcs','ha','has']
key_area3=['total','superficial','predio','extension']
black_list_area=[]


months=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
key_tipo_doc=['tribunal superior del','tribunal superior de','tribunal superior','fribunal','juzgado']
black_list_tipo_doc=[]

dicc_date={'enero':'01','febrero':'02','marzo':'03','abril':'04','mayo':'05','junio':'06',
          'julio':'07','agosto':'08','septiembre':'09','octubre':'10','noviembre':'11','diciembre':'12'}

WORD_JC = re.compile(r'\w+')


###########################
###   Simple Functions ###
##########################

### enlarge list of posibilities ##
def list_concordances_ltc(list_concors):
    list_temp1 = [list_concor.lower() for list_concor in list_concors]
    list_temp2 = [list_concor.upper() for list_concor in list_concors]
    list_temp3 = [list_concor.capitalize() for list_concor in list_concors]
    return list_temp1 + list_temp2 + list_temp3

### Replace accents in a text ##
def replace_accents(text):
    a,b = 'áéíóúüÁÉÍÓÚ','aeiouuAEIOU'
    trans = str.maketrans(a,b)
    return text.translate(trans)


### Calculate cosine2 for 2 inputs ###
def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

### count text ###    
def text_to_vector(text):
    return Counter(WORD_JC.findall(text))

### Return cosine2 for two text input ###    
def get_similarity(a, b):
    a = text_to_vector(a.strip().lower())
    b = text_to_vector(b.strip().lower())

    return get_cosine(a, b)

### Reduce options with probable same name -> keeping most differents ###
def reduce_similarity(table,var):
    if len(table)>1:
        list_similarity=[[i,j,get_similarity(x,y),len(word_tokenize(x.lower())),len(word_tokenize(y.lower()))] 
                         for i,x in enumerate(list(table[var])) 
                         for j,y in enumerate(list(table[var])) if i != j]
        similarity_table=pd.DataFrame(list_similarity)
        similarity_table['llave']=similarity_table[0]+similarity_table[1]
        similarity_table['total_words']=similarity_table[3]+similarity_table[4]
        similarity_table = similarity_table.drop_duplicates(subset=[2,'llave', 'total_words'], keep='first')
        similarity_table2=similarity_table[similarity_table[2]>0.35]
        similarity_table3a=similarity_table2.groupby([0])[[2,3]].max().reset_index()
        similarity_table3a=similarity_table3a[similarity_table3a[3]<=1]
        remove_similarity=list(similarity_table3a[0])
        similarity_table3b=similarity_table2.groupby([1])[[2,4]].max().reset_index()
        similarity_table3b=similarity_table3b[similarity_table3b[4]<=1]
        remove_similarity=remove_similarity+list(similarity_table3b[1])
    
        similarity_table4=similarity_table2[~similarity_table2[0].isin(remove_similarity)].reset_index(drop=True)
        similarity_table4=similarity_table4[~similarity_table4[1].isin(remove_similarity)].reset_index(drop=True)

        similarity_table4['value']=np.where(similarity_table4[3]<similarity_table4[4], similarity_table4[1],similarity_table4[0])
        remove_similarity += list(similarity_table4['value'])
        remove_similarity = list(dict.fromkeys(remove_similarity))

        similarity_table5=table[~table.index.isin(remove_similarity)].reset_index(drop=True)

    else:
        similarity_table5=table
    
    return(similarity_table5)


#### Function for extract colombian DNI ###
def extract_cedula(filter_name,file, corpus_temp):
    text_List = word_tokenize(replace_accents(corpus_temp.raw(file)))
    text_List = nltk.Text(text_List)
    list_concordances = ["cedula","cedulas","C.C.N","C.C","CC","C.C.N.°"]
    text_List_result = []
    
    #concordance cedula
    for concordance in list_concordances_ltc(list_concordances):
        text_List_temp = text_List.concordance_list(concordance, width=360)
        if len(text_List_temp)>0:
            text_List_temp = [elem[6] for elem in text_List_temp]
            text_List_result += text_List_temp
            
    #coincidence name
    results = []
    if len(text_List_result)>0:
        list_filter = [replace_accents(filter_name)]
        for text_result in text_List_result:
            if re.search(replace_accents(filter_name), text_result):
                results.append(text_result)
                
    regex = r"\d+\s*[.]*\s*\d+\s*[.]*\s*\d+\s*[.]*\s*\d+\s*[.]*\s*"
    list_cc = []
    #extract cc
    if len(results)>0:
        for each in results:
            for match in re.finditer(regex, each):
                cc = match.group()
                list_cc.append(cc)
        list_cc=[int(cedula.replace('.','').replace(',','').replace(' ','')) for cedula in  list_cc 
        if 999999 < int(cedula.replace('.','').replace(',','').replace(' ','')) < 1500000000]
        flat_cc = list(dict.fromkeys(list_cc))
    else:
        flat_cc=[]
    
    #search 2 
    clean_phrase=[]
    if len(flat_cc)>0:
        text_List_result2=[str.split(x) for x in text_List_result]
        for words in text_List_result2:
            y=[sub.replace('.', '') for sub in words]
            y=' '.join(y)
            clean_phrase.append(y)
    
    #search distance
    coincide_cc=[]
    if len(clean_phrase)>0:
        for cedula in flat_cc:
            for phrase in clean_phrase:
                if re.search(str(cedula), phrase):
                    coincide_cc.append(phrase)
    
    pairs=[]
    distance=0
    if len(coincide_cc)>0:  
        for cc in flat_cc:
            for prhase_cc in coincide_cc:
                pattern =replace_accents(filter_name) + "(.*?)" + str(cc)
                if re.search(pattern, prhase_cc):
                    substring = re.search(pattern, prhase_cc).group(1)
                else:
                    substring=''
                distance=len(word_tokenize(substring))
                pairs0=[cc,distance]
                pairs.append(pairs0)                   
    
    if pairs:
        table_distances = pd.DataFrame(pairs, columns = ['cc', 'distance'])
        table_distances = table_distances[table_distances['distance']>0]
        table_distances = table_distances.drop_duplicates().reset_index(drop=True)
        table_distances = table_distances.groupby('cc').mean().sort_values(by=['distance'],ascending=False)
    else:
         table_distances = pd.DataFrame(columns = ['cc', 'distance'])
            
    if len(table_distances):
        val=str(table_distances.index.values[0])
    else:
        val='Not found'
            
    return(val)


### Take a text of dates nd return a format date by numeric coincidences ###
def format_date(text):
    text=str(text)
    num_date=re.findall(r'\b\d+\b',text)
    month_date_key=[x for x in word_tokenize(text.lower()) if x in months]
    
    if len(num_date)>0:
        if month_date_key:
            month_date=[dicc_date.get(month_date_key[0])]
            if  len(num_date)==2 and len(month_date)==1:
                date=num_date[1]+'/'+month_date[0]+'/'+num_date[0]
            else:
                date='/'.join(num_date+month_date)
        if len(num_date)==2 and len(month_date_key)==0:
            date=num_date[1]+'/'+num_date[0]
        elif len(num_date)==1:
            date=num_date[0]
    else:
        date=''            
    return(date)
    

######################################################
###     EXTRACTION JUDGE AND MAGISTRATE NAME       ###
######################################################
def find_range(lista,rango):
    if len(lista)==0:
        flat_list=[]
    else:
        for i in range(rango+1):
            x=[list(range(x-i,x)) for x in lista]
            flat_list = [item for sublist in x for item in sublist if item not in lista]
    return(flat_list)

### Regex searching mayusc words and return a coincidence sentence
def find_MAYUSC(text, black_list_temp):
    convertion=' '.join(re.findall(r"\b[A-Z][A-Z]+\b", replace_accents(text)))
    list_words=[word for word in word_tokenize(convertion) if word.lower() not in black_list_temp and len(word)>2]
    convertion2=' '.join(list_words)
    if len(convertion2)<1 or convertion2 in black_list_temp:
        convertion2='NA'
    return(convertion2)

### Search probable human names in a string ###
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

### Principal function for extraction a Magistrate or judge name in a URI judgment text ###
def extrae_magister(n, corpus_temp, black_list_temp):
    bins_cat = [0, 0.05, 0.95,1]
    names_cat = ['Encabezado', 'Historico / Secundario', 'Firmas']
    key_words=list_concordances_ltc(key_magister + key_juez)
    key_words2=list_concordances_ltc(key_magister2)

    file=corpus_temp.fileids()[n]
    lines = corpus_temp.raw(file).split('\r\n')
    llave_sentencia=file.replace(".txt", "")
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
    table1['validate_name']=table1['extract_magistrado'].apply(find_MAYUSC, args=([black_list_temp]))
    table1['original']=1
    
    # evaluate lines near lines without PNN with key words
    list_recursive=list(table1.loc[(table1.validate_name =='NA') & (table1.extract_magistrado.str.split().str.len()==1)]['index'])
    list_recursive=find_range(list_recursive,2)
  
    # looking for names probable signatures
    if list_recursive:
        probable_firma=[]
        for i in list_recursive:
            probable_firma.append(lines[i])
    
        list_recursive_t=list_recursive
        table2=pd.DataFrame(probable_firma,list_recursive_t,columns=['extract_magistrado']).reset_index()
        table2['validate_name']=table2['extract_magistrado'].apply(get_human_names_2, args=([black_list_temp]))
        # Keeping names
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
 
    # new bolean variables
    table3['parte_']=table3['index']/len(lines) 
    table3['parte']=pd.cut(table3['parte_'], bins_cat, labels=names_cat)
    
    table3['index_lag'] = table3['index'].shift(-1)
    table3['extract_magistrado_lag'] = table3['extract_magistrado'].shift(-1).str.replace('[^\w\s]','')
    table3['validate_name_lag'] = table3['validate_name'].shift(-1)
    
    # reduce by conditions
    table3=table3.loc[(table3.validate_name !='NA') | (table3.original==1)]
    
    table3['cerca']=np.where(abs(table3['index']-table3['index_lag'])<=2,1,0)
    table3['ponente']=np.where(table3['extract_magistrado'].str.contains('|'.join(list_concordances_ltc(key_ponente))),1,0)
    table3['firma']=np.where((table3['cerca']==1) & (table3['validate_name']!=table3['extract_magistrado_lag']) &
                             (table3['extract_magistrado_lag'].str.contains('|'.join(list_concordances_ltc(key_magister)))),1,0)

    # final reduction
    table3=table3.sort_values(['index', 'firma']).drop_duplicates('index', keep='last')
    table3['key']=llave_sentencia
    table3['Nombre_JM']=table3['validate_name'].str.split().apply(lambda x: [w.capitalize() for w in x]).str.join(' ')
    table3['lead_sentence']=table3['extract_magistrado_lag']

    table3=table3.loc[(table3.validate_name !='NA')][['key','index','parte','original','Nombre_JM',#'extract_magistrado',
                                                      'ponente','lead_sentence']] #'extract_magistrado_lag']]
    
    table4=table3.sort_values(['Nombre_JM', 'ponente','index']).drop_duplicates('Nombre_JM', keep='last') 
    
    table5=reduce_similarity(table4,'Nombre_JM')
    
    if table5.empty:
        new_row = {'key':llave_sentencia, 'index':None, 'parte':None, 'original':None,'Nombre_JM':'Not found',
                  'ponente':None,'lead_sentence':None}
        table5 = table5.append(new_row, ignore_index=True)
    
    return(table5)

######################################################
###        OPPONENT NAME EXTRACTION              ###
######################################################

### Principal function for name and DNI extraction of the opponent ###
def extrae_opositor(n, corpus_temp, black_list_temp):
    key_tribunal=list_concordances_ltc(key_tribunal1)
    key_words=list_concordances_ltc(key_opositor)
    key_words2=list_concordances_ltc(key_opositor2)
    
    file=corpus_temp.fileids()[n]
    lines = corpus_temp.raw(file).split('\r\n')
    llave_sentencia=file.replace(".txt", "")
    
    # Validate high court
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
    
    # match opositor by line 
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
    
    # reduce by conditions
    table2=table1.loc[(table1.validate_name !='NA')]
    if table2.empty:
        table1['validate_name']=table1['extract_opositor'].apply(get_human_names_2, args=([black_list_temp]))
    table2=table1.loc[(table1.validate_name !='NA')]
    
    table2['key']=llave_sentencia
    table2['Nombre_opositor']=table2['validate_name'].str.split().apply(lambda x: [w.capitalize() for w in x]).str.join(' ')
    table2=table2.sort_values(['Nombre_opositor','index']).drop_duplicates('Nombre_opositor', keep='last') 
    table2=table2.loc[(table2.validate_name !='NA')][['key','index','Nombre_opositor']].reset_index(drop=True)
  
    table2['cedula']=table2['Nombre_opositor'].apply(extract_cedula, args=([file, corpus_temp]))
    if verifica_tribunal:
        table2=table2
    else:
        table2= table2.iloc[0:0]
 
    if table2.empty:
        new_row = {'key':llave_sentencia, 'index':None, 'Nombre_opositor':'Not Found','cedula':'Not Found'}
        table2 = table2.append(new_row, ignore_index=True)
    
    table3=reduce_similarity(table2,'Nombre_opositor')

    return(table3)

#####################################
##      PROBABLES AREA EXTRACTION  ###
#####################################

### Regex and condition looking for area metrics phrases ###
def search_area(raw,key_list):
    text_List_result = []
    text_List = nltk.Text(word_tokenize(replace_accents(raw.lower()))
)
    list_concordances = key_list   
    list_exceptions = black_list_area
    text_List_result = []        
    for list_concordance in list_concordances:
        text_List_temp = text_List.concordance_list(list_concordance, width=100)
        phrase=[extrae[6] for extrae in text_List_temp]
        if len(phrase)>0:
            text_List_result.append(phrase)
        flat_list = [item for sublist in text_List_result for item in sublist if any(item.find(word)>0 for word in key_area2)]
        flat_list = list(dict.fromkeys(flat_list))
    # looking numeric areas in the prhases    
    coincide=[]   
    for prhase in flat_list:
        for key in key_area2:
            match=re.search(rf"\b\d*[.,]*\d+..{key}\b",prhase)
            if match != None: 
                coincide.append(match.group(0))
    count_coincide=Counter(coincide)
    df_count = pd.DataFrame.from_dict(count_coincide, orient='index').reset_index()


    return(df_count)

### Principal extraction function area ###
def extrae_area(n, corpus_temp, black_list_temp):
    key_words=list_concordances_ltc(key_area)

    file=corpus_temp.fileids()[n]
    raw_data=corpus_temp.raw(file)
    lines = corpus_temp.raw(file).split('\r\n')
    llave_sentencia=file.replace(".txt", "")

    prob_prhases=search_area(raw_data,key_words)
    prob_prhases = prob_prhases.rename(columns={0: 'count'})
    
    if len(prob_prhases)>0:
        prob_prhases['key']=llave_sentencia
        prob_prhases=prob_prhases[['key','index','count']]
    
    elif prob_prhases.empty:
        new_row = {'key':llave_sentencia, 'index':None, 'count':None}
        prob_prhases = prob_prhases.append(new_row, ignore_index=True)
        prob_prhases=prob_prhases[['key','index','count']]
    
    prob_prhases.columns=['key','area','count']
    
    return(prob_prhases)

###############################################
###  COURT CLASS, COURT NAME, DATE FILE 
###############################################
def valida_contain_JM(string):
    x=""
    if any(word in string.lower() for word in ['juzgado']):
        x='JUZGADO'
    elif any(word in string.lower() for word in ['tribunal','fribunal']):
        x='TRIBUNAL'
    return(x)

def extrae_tipo_doc(n, corpus_temp, black_list_temp):
    key_words=list_concordances_ltc(key_tipo_doc)
    key_months=list_concordances_ltc(months)

    file=corpus_temp.fileids()[n]
    raw_data=corpus_temp.raw(file)
    lines = corpus_temp.raw(file).split('\r\n')
    llave_sentencia=file.replace(".txt", "")

    verifica_tribunal=[]
    verifica_tribunal_index=[]
    date_list=[]
    date_index=[]
    counter=-1
    for line in lines:
        counter=counter+1
            ### type document ###
        for key in key_words:
            match=re.search(rf"{key}.*$",line)
            if match != None: 
                verifica_tribunal.append(match.group(0))
                verifica_tribunal_index.append(counter)
            ### date document ###
        for key in key_months:
            match_date=re.search(rf"^.*{key}.*$",line)
            if match_date != None: 
                date_list.append(match_date.group(0))
                date_index.append(counter)
                
    #subtext of judgment ##
    valid_description=['sala','civil','de','especializada','circuito','tierras']  
    description_doc=[]
    if len(verifica_tribunal_index)>0 and len(date_index)>0:
        init=min(verifica_tribunal_index)+1
        end=min(date_index)
        if init<end:
            for line in list(range(init,end)):
                for key in valid_description:
                    sentence=corpus_temp.raw(file).split('\r\n')[line] 
                    match=re.search(rf"{key}",sentence.lower())
                    if match != None: 
                        description_doc.append(sentence)
        
    description_text=' '.join(list(dict.fromkeys(description_doc))).replace('_','').upper()
    
    table1=pd.DataFrame(verifica_tribunal,columns=['Description']).reset_index(drop=True)[:1]
    table1['clase_doc']=table1["Description"].apply(valida_contain_JM)
    table1['Description']=table1["Description"]+' '+description_text
    table1['Description'] = table1['Description'].str.upper().replace(r'[^a-zA-Z ]\s?',r'',regex=True) 
    table2=pd.DataFrame(date_list,columns=['fecha']).reset_index(drop=True)[:1]    
    
    ###format Date ###
    table3 = pd.concat([table1.reset_index(drop=True), table2], axis=1)
    table3['key']=llave_sentencia
    table3['fecha']=table3['fecha'].str.upper()
    table3['fecha_format']=table3['fecha'].apply(format_date)
    table3=table3[['key','clase_doc','Description','fecha','fecha_format']]

    if table1.empty:
        new_row = {'Description':'Not found', 'clase_doc':'Not Found'}
        table1 = table1.append(new_row, ignore_index=True)
        table1=table1[['Description','clase_doc']]
        
    return(table3)

# Ejecucion principal

# charge corpus txt
corpus = PlaintextCorpusReader(path_input_txt, file_ids_text)
ids = corpus.fileids()

# charge corpus ocr
corpus_ocr = PlaintextCorpusReader(path_input_ocr, file_ids_ocr)
ids_ocr = corpus_ocr.fileids()

# black_lists expansion with more posibilities
black_list_magistrado=list_concordances_ltc(black_list_magistrado)
black_list_opositor=list_concordances_ltc(black_list_opositor)
black_list_area=list_concordances_ltc(black_list_area)

########################
###  RDS connection  ###
########################
engine = create_engine('YOUR CONNECTION STRING')

# Insert extraction in data base
for n in range(0,len(ids)):
    print("Procesando Archivo texto ", ids[n])
    try:
        df_magistrado=extrae_magister(n, corpus, black_list_magistrado)
    except BaseException as ErrMsj:
        print("Error extrayendo magistrado. Archivo: ", ids[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_juez_magristrado where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_magistrado.empty:
            db_tosql = df_magistrado.copy()
            db_tosql.columns = ["key", "index", "parte", "original", "nombre_jm", "ponente", "lead_sentence"]
            db_tosql.to_sql('tt_juez_magristrado', engine, if_exists='append', index=False)
   
    try:
        df_opositor=extrae_opositor(n, corpus, black_list_opositor)
    except BaseException as ErrMsj:
        print("Error extrayendo opositor. Archivo: ", ids[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_opositor where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_opositor.empty:
            db_tosql = df_opositor.copy()
            db_tosql.columns = ["key", "index", "nombre_opositor", "cedula"]
            db_tosql.to_sql('tt_opositor', engine, if_exists='append', index=False)

    try:
        df_area=extrae_area(n, corpus, black_list_area)
    except BaseException as ErrMsj:
        print("Error extrayendo area. Archivo: ", ids[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_area where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_area.empty:
            db_tosql = df_area.copy()
            db_tosql.columns = ["key", "area", "conteo"]
            db_tosql.to_sql('tt_area', engine, if_exists='append', index=False)

    try:
        df_encabezado=extrae_tipo_doc(n, corpus, black_list_tipo_doc)
    except BaseException as ErrMsj:
        print("Error extrayendo Encabezado. Archivo: ", ids[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_encabezado where key = '" + str(ids[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_encabezado.empty:
            db_tosql = df_encabezado.copy()
            db_tosql.columns = ["key", "clase", "descripcion", "fecha", "fecha_formato"]
            db_tosql.to_sql('tt_encabezado', engine, if_exists='append', index=False)
                        
# Inserta en base de datos lo relacionado al corpus OCR
for n in range(0,len(ids_ocr)):
    print("Procesando Archivo OCR ", ids_ocr[n])
    try:
        df_magistrado=extrae_magister(n, corpus_ocr, black_list_magistrado)
    except BaseException as ErrMsj:
        print("Error extrayendo magistrado. Archivo: ", ids_ocr[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_juez_magristrado where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_magistrado.empty:
            db_tosql = df_magistrado.copy()
            db_tosql.columns = ["key", "index", "parte", "original", "nombre_jm", "ponente", "lead_sentence"]
            db_tosql.to_sql('tt_juez_magristrado', engine, if_exists='append', index=False)
   
    try:
        df_opositor=extrae_opositor(n, corpus_ocr, black_list_opositor)
    except BaseException as ErrMsj:
        print("Error extrayendo opositor. Archivo: ", ids_ocr[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_opositor where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_opositor.empty:
            db_tosql = df_opositor.copy()
            db_tosql.columns = ["key", "index", "nombre_opositor", "cedula"]
            db_tosql.to_sql('tt_opositor', engine, if_exists='append', index=False)
            
    try:
        df_area=extrae_area(n, corpus_ocr, black_list_area)
    except BaseException as ErrMsj:
        print("Error extrayendo area. Archivo: ", ids_ocr[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_area where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_area.empty:
            db_tosql = df_area.copy()
            db_tosql.columns = ["key", "area", "conteo"]
            db_tosql.to_sql('tt_area', engine, if_exists='append', index=False)

    try:
        df_encabezado=extrae_tipo_doc(n, corpus_ocr, black_list_tipo_doc)
    except BaseException as ErrMsj:
        print("Error extrayendo Encabezado. Archivo: ", ids_ocr[n], ErrMsj)
    else:
        strSQLDelete = "delete from tt_encabezado where key = '" + str(ids_ocr[n].replace(".txt", "")) + "'"
        engine.execute(strSQLDelete)
        if not df_encabezado.empty:
            db_tosql = df_encabezado.copy()
            db_tosql.columns = ["key", "clase", "descripcion", "fecha", "fecha_formato"]
            db_tosql.to_sql('tt_encabezado', engine, if_exists='append', index=False)
