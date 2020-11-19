# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table
import time
import json
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd
from sqlalchemy import create_engine,text
import numpy as np
import os

from app import app
from apps import estadisticas, conoce_proyecto, conoce_equipo
                
#colors
color_1_green_ryb = '#75B620'
color_2_cafe_back = '#8F7167'
color_3_peach_puff = '#E5CAB1'
color_4_negro_text = '#353535'
color_5_table_resuelve='#6AB187'
color_5_table_resuelve='#A6EDB8'

##########################
## AWS CONECTTION     ####
##########################
#conecta con base de datos
engine = create_engine('postgresql://postgres:LFnnLUQZQMJ9@db-test2.cxqola6hllvk.us-east-2.rds.amazonaws.com/t96_dev')


#####################################################################
##                  Function definition    ####
#####################################################################

##### funciones para grupo familiar (fila-2)
def html_family(df_prueba):
    fila_2_obj = []
    max_group = df_prueba['grupo'].max()
    for group in range(1, max_group + 1):
        max_person = int(df_prueba[df_prueba['grupo'] == group]['n_persona'].max())
        titular_asociado = df_prueba[(df_prueba['grupo'] == group) & (df_prueba['n_persona'] == 1)]
        for person in range(1, max_person + 1):
            df_person = df_prueba[(df_prueba['grupo'] == group) & (df_prueba['n_persona'] == person)]
            # print(df_person['name'].tolist()[0], '\t persona', person, '\t from group:', group)
            fila_2_obj = fila_2_obj + (html_person(df_person, titular_asociado))
            if int(df_person['n_persona']) == max_person:
                fila_2_obj = fila_2_obj[:-1] + [html.Hr(className='line_in_group_fin')]
    fila_2_obj = fila_2_obj + [html.Br()]
    return fila_2_obj

def html_person(df_person, titular_asociado):
    answer = False
    if df_person['n_persona'].tolist()[0] == 1:
        answer = html_person_titular(df_person)
    else:
        answer = html_person_other(df_person, titular_asociado)
    return answer

def html_person_titular(df_person):
    answer = [
        html.P('GRUPO ' + str(df_person['grupo'].to_list()[0]), className='form_group_t'),
        html.P(' Titular del Proceso', className='form_group'),
        html.P('Nombre:', className='form_control'),
        html.P(df_person['name'].to_list()[0], className='form_answer'),
        html.Div(className='n_values', children=[
            html.Div(children=[
                html.P('Tipo de Documento:', className='form_control_inline'),
                html.P('-', className='form_answer_inline')
            ]),
            html.Div(children=[
                html.P('Número de documento:', className='form_control_inline'),
                html.P(str(df_person['cedula'].to_list()[0]), className='form_answer_inline')
            ]),
            html.Div(children=[
                html.P('Género:', className='form_control_inline'),
                html.P('-', className='form_answer_inline'),
            ]),
            html.Div(children=[
                html.P('Rol:', className='form_control_inline'),
                html.P('Titular', className='form_answer_inline')
            ]),
        ]),
        html.Div(className='n_values', children=[
            html.Div(children=[
                html.P('Calidad jurídica:', className='form_control_inline'),
                html.P('-----', className='form_answer_inline')
            ]),
            html.Div(children=[
                html.P('Sentido de la decisión:', className='form_control_inline'),
                html.P('-----', className='form_answer_inline')
            ]),
            html.Div(children=[
                html.P('Enfoque diferencial:', className='form_control_inline'),
                html.P('-----', className='form_answer_inline')
            ]),
        ]),
        html.Hr(className='line_in_group')
        ]
    return answer

def html_person_other(df_person, titular_asociado):
    answer = [html.P('GRUPO ' + str(df_person['grupo'].to_list()[0]) + ' - Beneficiario #' + str(df_person['n_persona'].to_list()[0]-1) + ' del proceso', className='form_group'),
              html.Div(className='n_values', children=[
                html.Div(children=[
                    html.P('Nombre:', className='form_control_inline'),
                    html.P(df_person['name'].to_list()[0], className='form_answer_inline')
                ]),
                html.Div(children=[
                    html.P('Número de documento:', className='form_control_inline'),
                    html.P(str(df_person['cedula'].to_list()[0]), className='form_answer_inline')
                ]),
                html.Div(children=[
                    html.P('Género:', className='form_control_inline'),
                    html.P('-', className='form_answer_inline'),
                ])
              ]),
              html.Div(className='n_values', children=[
                html.Div(children=[
                    html.P('Rol:', className='form_control_inline'),
                    html.P('Beneficiario', className='form_answer_inline')
                ]),
                html.Div(children=[
                    html.P('Parentesco:', className='form_control_inline'),
                    html.P('-', className='form_answer_inline')
                ]),
                html.Div(children=[
                    html.P('Titular asociado:', className='form_control_inline'),
                    html.P(titular_asociado['name'], className='form_answer_inline')
                ])
              ]),
              html.Hr(className='line_in_group_2')
             ]
    return answer


def paginas_a_hojas(Npages):
    if Npages == 1:
        Nhojas = 1
    else:
        Nhojas = int(np.round(Npages/2))
    return Nhojas

### valid URL for URT judgment ###
def valid_url(judgment):
    url_error = "http://190.217.24.108/restituciontierras/views/old/http://190.217.24.108/restituciontierras/views/old/"
    url_base = "http://190.217.24.108/restituciontierras/views/old/"
    ref_link=query_join('mt_sentencia','','certificado',judgment)[['descargar','paginas']]
    ref_link=ref_link[ref_link.paginas == ref_link.paginas.max()].iloc[0]['descargar'].replace(url_error,url_base).replace(' ','%20')
    return(ref_link)


### (ONE COLUMN) return unic value or append if are more than one in a list ###
def append_output(lista):
    text=list(dict.fromkeys(lista))
    if len(text)>1:
        text=' / '.join(text)
    else:
        text=''.join(text)
    if text=='':
        text='-----'
    return(text)    

### (MULTIPLE COLUMN) return unic value or append if are more than one in a list ###
def append_output_M(table):
    table.loc[:,~table.columns.duplicated()]
    table.drop_duplicates() 
    dim=table.shape
    if dim[0]==1:
        lista=list(table.iloc[0])
        text=list(dict.fromkeys(lista))
        if len(text)>1:
            text=', '.join(text)
        else:
            text=''.join(text)
    elif dim[0]>1 and dim[1]>1:
        lista = table.values.tolist() 
        lista = [', '.join(x) for x in lista]
        text=append_output(lista)
    elif dim[0]>1 and dim[1]==1:
        text=append_output(list(table))
    else:
        text='-----'
    return(text)    




### query SQL define variables, key where variable, value and rename variable list ###
def query_connection(table,variables,key,value,rename):
    if len(variables)==0:
        var='*'
    else:
        var=','.join(variables).rstrip(',')
    if value=='':
        subquery0=''
    else:
        subquery0=' WHERE ' + key + '=' + "'" + value + "'"
    
    Query = pd.read_sql_query('SELECT ' + var + ' FROM ' + table + subquery0   , engine)
    df = pd.DataFrame(Query)
    if len(rename)==0:     
        df_out=df
    else:
        df_out = df
        df_out.columns=rename
      
    return(df_out)


### query SQL define variables value and rename variable list ###
def query_connection2(table,variables,value,rename):
    if len(variables)==0:
        var='*'
    else:
        var=','.join(variables).rstrip(',')
    if value=='':
        subquery0=''
        Query = pd.read_sql_query('SELECT ' + var + ' FROM ' + table + subquery0   , engine)
    else:
        if len(value)==29:
            subquery0=' WHERE ' + 'radicacion' + '=' + "'" + value + "'"
            Query = pd.read_sql_query('SELECT ' + var + ' FROM ' + table + subquery0   , engine)
        elif len(value)==67:
            try:
                subquery0=' WHERE ' + 'certificado' + '=' + "'" + value + "'"
                Query = pd.read_sql_query('SELECT ' + var + ' FROM ' + table + subquery0   , engine)
            except:
                subquery0=' WHERE ' + 'key' + '=' + "'" + value + "'"
                Query = pd.read_sql_query('SELECT ' + var + ' FROM ' + table + subquery0   , engine)
     
    df = pd.DataFrame(Query)
    if len(rename)==0:     
        df_out=df
    else:
        df_out = df
        df_out.columns=rename
      
    return(df_out)

### Query SQL join  whit master tables###
def query_join(table,variables,key,value):
    query0='SELECT tr.radicacion ,ms.certificado, c.'  
    query1=' FROM mt_sentencia ms LEFT OUTER JOIN tt_radicado tr ON tr.certificado = ms.certificado JOIN ' 
    if len(variables)==0:
        var='*'
    else:
        var=','.join(variables).rstrip(',')

    subquery= query0 + var + query1 + table +' c ON c.'  + key + '= ms.certificado  WHERE ms.certificado =' +"'"+ value  + "'"+  ' OR  tr.radicacion = ' + "'"+ value +"'"    
    Query_join = pd.read_sql_query(subquery, engine)
           
    df = pd.DataFrame(Query_join) 
    df = df.loc[:,~df.columns.duplicated()]    ## remove duplicate columns
    df = df.drop_duplicates()  ## remove duplicate rows
    return(df)




################################
## Visual layout    ####
################################

nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Inicio", href="/", style = {'text-decoration': 'none', 'font-weight': 'bold', 'font-size': '16px', 'border-right':'solid 1.5px #c6ccd2'}, id="page-1-link")),
        dbc.NavItem(dbc.NavLink("Exploración", href="/apps/estadisticas", style = {'text-decoration': 'none', 'font-weight': 'bold', 'font-size': '16px','border-left':'solid 1.5px #c6ccd2', 'border-right':'solid 1.5px #c6ccd2'}, id="page-2-link")),
        dbc.NavItem(dbc.NavLink("Conoce el proyecto", href="/apps/conoce_proyecto", style = {'text-decoration': 'none',  'font-weight': 'bold', 'font-size': '16px', 'border-left':'solid 1.5px #c6ccd2', 'border-right':'solid 1.5px #c6ccd2'}, id="page-3-link")),
        dbc.NavItem(dbc.NavLink("Conoce al equipo", href="/apps/conoce_equipo", style = {'text-decoration': 'none', 'font-weight': 'bold', 'font-size': '16px', 'border-left':'solid 1.5px #c6ccd2', }, id="page-4-link")),
    ],
    pills= True,
    fill=True,
    justified=True
)


app.layout = html.Div([
    html.Div([
       
        html.Div([
        html.A(html.Img(src='https://www.restituciondetierras.gov.co/image/layout_set_logo?img_id=633248&t=1602383466096', style = {'marginTop':'5px'}
                       ), href='https://www.restituciondetierras.gov.co', target='web_restitucion')
        ], style={'width': '32%', 'display': 'inline-block', 'textAlign':'center'}),
        
        html.Div([
        html.Img(src='https://bootcamp14.s3.us-east-2.amazonaws.com/Logo1_Montserrat.svg', style={'width': '65%'}) 
        ], style={'width': '35%', 'verticalAlign': 'middle', 'display': 'inline-block', 'textAlign':'center'}),

        html.Div([
        html.A(html.Img(src="https://www.restituciondetierras.gov.co/documents/20124/35185/logo+minagricultura.png/4ca0b50a-4be6-4687-4a53-5c94d40ffb03?t=1599778084030"), 
               href='https://www.minagricultura.gov.co', target='web_restitucion')
        ], style={'width': '32%', 'display': 'inline-block',  'marginTop':'20px',  'verticalAlign': 'top', 'textAlign':'center'})      
    ], style={'height':'130px',  'textAlign':'center'}),
    
    nav,
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children = []),
])

index_layout = html.Div([
    
    html.Div([
        html.Div([
        html.H1("Digitalización de sentencias", style={'fontSize': '45px', 'color':'#8F5440', 'marginTop':'30px'}),
        html.P("Obtén información relevante para monitorear los juicios de restitución de tierras", style={'fontSize': '20px', 'color':'#8F5440'}),
        ])  
    ],style={'height':'180px', 'background-color': '#ECE3DF',  'textAlign':'center', 'borderTop':'solid 1px #ECE3DF'}),
    
    html.Div([
        html.Div([
        html.H2(html.B("Buscar sentencias: ", style = {'color':'#8F5440'})),
        ], style={'textAlign':'center', 'marginTop':'22px'}),
        html.Div([
        dcc.Input(id="id_sentencia", type="search", placeholder="Ingresa el número de radicado o el código de certificado", value='', minLength=1, maxLength=80, autoComplete='on', debounce= True, n_submit=0, style= {'width': '625px', 'height':'40px', 'border': '3px solid #ECE3DF', 'display': 'inline-block',  'borderRadius': '10px'}),  
        dbc.Button('BUSCAR', id = 'btn-sentencia',  n_clicks=0, style= { 'width': '120px', 'height':'40px', 'display': 'inline-block', 'font-weight': 'bold', 'background-color': '#8F5440', 'marginLeft':'40px', 'font-size': '13px', 'color':'white', 'cursor': 'pointer', 'border': '2px solid #724333', 'border-radius': '10px'}),
        dbc.Alert("La sentencia no existe, verifica el código digitado",id="alert-auto", is_open=False, duration=3000, style = { 'font-weight': 'bold', 'background-color': '#D32D41', 'display': 'inline-block', 'marginLeft':'40px', 'color':'white', 'border-radius': '5px'}),
        html.Br(),
        html.Br(),
        dbc.Button(
          "Ejemplos de digitación", id="positioned-toast-toggle", color='success', style = {'background-color': '#75b620', 'border': '1px solid #69A31C', 'border-radius': '10px'}
        ),
        dbc.Toast( 
            [html.P("¿Novato en Ground Truth? Prueba la herramienta con uno de estos códigos: "),
            html.P("Certificado: 47A1EC64E482B312 BD3EC81DA998F7C3 C4745A492A5BD9BB 4E11500DB377B7CD"),
            html.P("Radicado: 76001-31-21-002-2016-00039-00")],
            id="positioned-toast",
            is_open=False,
            dismissable=True,
            style={'display': 'inline-flex', 'marginLeft': '40px', 'text-align': 'left'},
        ),  
        html.Br(),
        html.Br(),
        dbc.Alert([
        html.H4(html.B("Advertencia")),
        html.P( 
            "Este documento puede tener mala calidad, se recomienda validar la información extraída. Es posible que no sea una sentencia"
        )], id="alert-quality", color= 'warning', is_open=False, style = {'color':'#8F5440', 'border-radius': '5px'}),
        dbc.Spinner(html.Div(id="loading-output"),color="success"),
        ], style={'textAlign':'center', 'marginTop':'20px'})       
    ]),
    
    html.Div([
          ### tablas de consulta ####    
        html.Br(),
        html.Br(),
        html.Div(id='table0',children=[    ]),
        html.Br(),
        html.Div(id='descargar',children=[    ]),
        html.Br(),
        html.Div(id='formulario', children=[  ] ),
        html.Br(),
        html.Div(id='table2',children=[    ]),
        html.Br(),
        html.Br()
    ],style={'textAlign':'Left', 'marginTop':'20px'}),
], style={'border':'solid 1px #EDF0F4'})


################################
## CALLBACKS    ####
################################

# Update the index
@app.callback(Output(component_id= 'page-content', component_property= 'children'),
              [Input(component_id= 'url', component_property= 'pathname')],
              prevent_initial_call=True)
def display_page(pathname):
    if pathname == '/apps/estadisticas':
        return estadisticas.layout
    elif pathname == '/apps/conoce_proyecto':
        return conoce_proyecto.layout
    elif pathname == '/apps/conoce_equipo':
        return conoce_equipo.layout
    else:
        return index_layout
    
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
    prevent_initial_call=True
)
def toggle_active_links(pathname):
    if pathname == "/":
        return True, False, False, False
    elif pathname == "/apps/estadisticas":
        return False, True, False, False
    elif pathname == "/apps/conoce_proyecto":
        return False, False, True, False
    elif pathname == "/apps/conoce_equipo":
        return False, False, False, True

### Show tables ###
@app.callback(
    [Output(component_id='table0', component_property='children'),
     Output(component_id='descargar', component_property='children'),
    Output(component_id='formulario', component_property='children'),
    Output(component_id='table2', component_property='children')],

    [Input(component_id='id_sentencia', component_property='value'),
     Input(component_id='id_sentencia', component_property='n_submit'),
     Input(component_id='btn-sentencia', component_property='n_clicks')],
    
    prevent_initial_call=True
)
def update_output(value, n_submit, n_clicks):
    conn = engine.connect()

    if value!='' and (len(value)==29 or len(value)==67):
        coincidence =query_join('mt_sentencia','','certificado',value)[['certificado','radicacion']]
        exist=len(coincidence)
        url_download=valid_url(value)
    else:
        exist=0
    
    if (n_clicks or n_submit) is None and value=='':
        raise PreventUpdate
    elif exist>0 and len(value) in [29,67]  and (n_clicks or n_submit):

        ### table 0 (Más de un certificado por radicado?) ####
        lista_certificado=query_join('tt_radicado','','certificado',value)[['nombre_predio','certificado','fecha_providencia']]
        lista_certificado['nombre_predio2']=np.where(lista_certificado['nombre_predio']!= 'ADICIONA/COMPLEMENTA', 'CERTIFICADO ', 'ADICIONA/COMPLEMENTA ')
        lista_certificado['fecha']=pd.to_datetime(lista_certificado['fecha_providencia']).dt.date
        lista_certificado=lista_certificado.sort_values('fecha')
        lista_certificado['new_index']=lista_certificado['nombre_predio2'] + '(' + lista_certificado['fecha'].apply(str) + ')'
        lista_certificado=lista_certificado.drop(['nombre_predio'],axis=1).drop_duplicates()
        #lista_certificado=lista_certificado.drop_duplicates()
        lista_certificado.set_index('new_index', inplace=True)
        lista_certificado=lista_certificado[['certificado']]
        lista_certificado=lista_certificado.transpose()
        lista_certificado = dbc.Table.from_dataframe(lista_certificado, striped=True, bordered=True, hover=True)

        salida0=[lista_certificado]
        salida_descargar=html.A(dbc.Button("Descargar PDF", id="b_download", className="mr-1",block=True,
             style= {  'height':'40px', 'font-weight': 'bold', 'background-color': '#8F5440', 'font-size': '13px', 'color':'white', 'cursor': 'pointer', 'border': '2px solid #724333', 'border-radius': '10px'}), href=url_download),
        

        ##############################################################################
        ###                       QUERYS                                        #####
        ##############################################################################
        ### radicado ###
        form_radicado=list(query_join('mt_sentencia','','certificado',value)['radicacion'])
        form_radicado=append_output(form_radicado)
        form_radicado
        
        ### Territorial responsable ##
        #form_territorial=query_join('tt_localizacion','','certificado',value)[['departamento','municipio','corregimiento','vereda']]
        #form_territorial=append_output_M(form_territorial)
        #if form_territorial=='':
        form_territorial=pd.DataFrame(query_join('tt_radicado','','certificado',value))['municipio_vereda']
        form_territorial=[x for x in form_territorial if x!='ADICIONA/COMPLEMENTA']
        form_territorial=append_output(form_territorial)
        
        ### Fecha de expedición ###
        form_date=query_join('tt_radicado','','certificado',value)
        form_date=form_date[form_date['municipio_vereda']!='ADICIONA/COMPLEMENTA']['fecha_providencia']
        #query_join('tt_encabezado','','key',value)
        form_date=append_output(form_date)

        ### Juzgado / Tribunal ###
        form_judge=query_join('tt_encabezado','','key',value)['clase']
        form_judge=append_output(form_judge)
        
        ### Juzgado / Tribunal ###
        form_magistrado=query_join('tt_juez_magristrado','','key',value)['nombre_jm']
        form_magistrado=append_output(form_judge)


        ### Tipo Sentencia ###
        form_tipo_sentencia=query_join('vw_tipo_sentencia_grupo','','key',value)['tipo']
        form_tipo_sentencia=append_output(form_tipo_sentencia)

        ### area (pesima extracción!) ###
        form_area=query_join('tt_area','','key',value)['area']
        form_area=append_output(form_area)
        
        ### Depto /Mpio ###
        form_depto=query_join('mt_sentencia','','certificado',value)['ciudad']
        form_depto=append_output(form_depto)

        ### No folios (N. Paginas) ###
        form_folios=query_join('mt_sentencia','','certificado',value)['paginas']
        if len(form_folios)>0 :
            form_folios=max(form_folios)
            if form_folios==0 or form_folios=='':
                form_folios=='----'
        else:
            form_folios='-----'
        form_folios='-----'
        
        form_folios=query_join('mt_sentencia','','certificado',value)['paginas']
        if len(form_folios)>0 :
            form_folios=int(max(form_folios))
        if form_folios==0 or form_folios=='':
            form_folios=='----'
        form_folios=paginas_a_hojas(form_folios)

        ##############################################################################
        
        ### 'Nombre del predio ####
        form_name_predio=query_join('tt_radicado','','certificado',value)
        form_name_predio=form_name_predio[form_name_predio['municipio_vereda']!='ADICIONA/COMPLEMENTA']['nombre_predio']
        form_name_predio=append_output(form_name_predio)

        ### Depto doc ####
        form_depto_doc=query_join('tt_localizacion','','certificado',value)['departamento']
        form_depto_doc=append_output(form_depto_doc)

        ### COD Depto doc ####
        form_CODdepto_doc=query_join('tt_localizacion','','certificado',value)['codigo_departamento']
        form_CODdepto_doc=append_output(form_CODdepto_doc)

        ### Mpio doc ####
        form_mpio_doc=query_join('tt_localizacion','','certificado',value)['municipio']
        form_mpio_doc=append_output(form_mpio_doc)

        ### COD Mpio doc ####
        form_CODmpio_doc=query_join('tt_localizacion','','certificado',value)['codigo_municipio']
        form_CODmpio_doc=append_output(form_CODmpio_doc)

        ### corregimiento doc ####
        form_corregimiento_doc=query_join('tt_localizacion','','certificado',value)['corregimiento']
        form_corregimiento_doc=append_output(form_corregimiento_doc)

        ### COD corregimiento doc ####
        form_CODcorregimiento_doc=query_join('tt_localizacion','','certificado',value)['codigo_corregimiento']
        form_CODcorregimiento_doc=append_output(form_CODcorregimiento_doc)

        ### Zona doc ####
        form_zona=query_join('vw_tipo_zona','','certificado',value)['tipo']
        form_zona=append_output(form_zona)

        ### Vereda doc ####
        form_vereda=query_join('tt_localizacion','','certificado',value)['vereda']
        form_vereda=append_output(form_vereda)

        ### COD Vereda doc ####
        form_CODvereda=query_join('tt_localizacion','','certificado',value)['codigo_vereda']
        form_CODvereda=append_output(form_CODvereda)

        ### CC Catastral doc ####
        form_cc_catastral=query_join('tt_cedula_catastral','','key',value)['cedula_catastral']
        form_cc_catastral=append_output(form_cc_catastral)

        ### Matricula Inmoviliaria ####
        form_matricula=query_join('tt_matricula_inmobiliaria','','key',value)['matricula_inmobiliaria']
        form_matricula=append_output(form_matricula)


        ##############################################################################
        df_family=query_join('tt_grupo_familiar','','key',value).drop(['radicacion','certificado'],axis=1) 
        df_family['grupo']=df_family['grupo'].astype('int64')
        df_family['n_persona']=df_family['n_persona'].astype('int64')
        df_family=df_family.drop_duplicates()

        if len(df_family)>0:
            extract_family=html_family(df_family)
        else:
            extract_family=[]
        ##############################################################################
        #close connection 
        conn.close()
        engine.dispose()
        ##############################################################################

        
        ## form presentation
        salida_formulario = html.Div(id='principal', children=[
        html.Div(id='Cabezote', className="fila", children=[
            html.Div(className="logo", children=[
                html.Img(src='https://bootcamp14.s3.us-east-2.amazonaws.com/Logo1_Montserrat.svg')
            ]),
            html.Div(className='Titulo', children=[
                html.Div(className='vl'),
                html.H1('Smart Scan')
            ])
        ]),
        html.Div(id='fila-1', className="fila", children=[
            html.Div(id='formulario-1', className='columna_left', children=[
                html.H2('1. Datos de Sentencia', className='form_title'),
                html.P('Radicado:', className='form_control'),
                html.P(form_radicado, className='form_answer'),
                html.P('Territorial Responsable:', className='form_control'),
                html.P(form_territorial, className='form_answer'),
                html.P('Fecha de expedición:', className='form_control'),
                html.P(form_date, className='form_answer'),
                html.P('Juzgado/tribunal:', className='form_control'),
                html.P(form_judge, className='form_answer'),
                html.P('Juez/magistrado:', className='form_control'),
                html.P(form_magistrado, className='form_answer'),

                html.P('Tipo de sentencia:', className='form_control'),
                html.P(form_tipo_sentencia, className='form_answer'),
                html.P('Área total (Posibles áreas encontradas):', className='form_control'),
                html.P(form_area, className='form_answer'),
                html.P('Tipología pérdida bien:', className='form_control'),
                html.P('-----', className='form_answer'),
                html.P('Departamento/ciudad:', className='form_control'),
                html.P(form_depto, className='form_answer'),
                html.P('No. Folios:', className='form_control'),
                html.P(form_folios, className='form_answer')
            ]),
            html.Div(id='formulario-2', className='columna_right', children=[
                html.H2(['3. Información de Restitución : Gestión de Predio'], className='form_title'),
                html.P(['Nombre del predio:'], className='form_control_inline'),
                html.P(form_name_predio, className='form_answer_inline'),
                html.P('Departamento:', className='form_control'),
                html.P(form_depto_doc, className='form_answer'),
                html.P('Código departamento:', className='form_control_inline'),
                html.P(form_CODdepto_doc, className='form_answer_inline'),
                html.P('Municipio:', className='form_control'),
                html.P(form_mpio_doc, className='form_answer'),
                html.P('Código Municipio:', className='form_control_inline'),
                html.P(form_CODmpio_doc, className='form_answer_inline'),
                html.P('Corregimiento:', className='form_control'),
                html.P(form_corregimiento_doc, className='form_answer'),
                html.P('Código corregimiento:', className='form_control_inline'),
                html.P(form_CODcorregimiento_doc, className='form_answer_inline'),
                html.P('Zona:', className='form_control'),
                html.P(form_zona, className='form_answer'),
                html.P('Inspección:', className='form_control_inline'),
                html.P('-----', className='form_answer_inline'),
                html.P('Vereda:', className='form_control'),
                html.P(form_vereda, className='form_answer'),
                html.P('Código vereda:', className='form_control_inline'),
                html.P(form_CODvereda, className='form_answer_inline'),
                html.P('Barrio:', className='form_control'),
                html.P('-----', className='form_answer'),
                html.P('Cédula catastral:', className='form_control_inline'),
                html.P(form_cc_catastral, className='form_answer_inline'),
                html.P('Matrícula inmobiliaria:', className='form_control'),
                html.P(form_matricula, className='form_answer')
            ])
        ]),
        html.Div(id='fila-2', children =
            [html.Br(), html.H2(['3. Información de Restitución : Gestión de Beneficiarios'], className='form_title')] +
            extract_family
        )
])

        
        ########################################################################
        ###                     Tables output by button
       ######################################################################### 
        conn = engine.connect()

        ### Model resuelve  ###
        table_resuelve=query_join('tt_resuelve','','certificado',value).drop(['resuelve','radicado'],axis=1)  
        table_resuelve.transpose()
        table_resuelve = table_resuelve.melt(id_vars=['radicacion','certificado'], var_name='Tipo Sentencia', value_name='Resuelve')
        table_resuelve['Tipo Sentencia']=table_resuelve['Tipo Sentencia'].str.replace('_',' ').str.upper()
        dup_valida=table_resuelve[['radicacion','certificado']].drop_duplicates()
        if len(dup_valida)==1:
            table_resuelve=table_resuelve.drop(['radicacion','certificado'],axis=1)  
        table_resuelve = dbc.Table.from_dataframe(table_resuelve, striped=True, bordered=True, hover=True,style={'background-color': '#A6EDB8'})

        ### Index "Resulve" extraction ###
        table_ordena_text=query_join('tt_resuelve_text','','key',value).drop(['key','radicacion','certificado'],axis=1)
        table_ordena_text=table_ordena_text.sort_values('contador').drop_duplicates()
        
        table_ordena_text = dbc.Table.from_dataframe(table_ordena_text, striped=True, bordered=True, hover=True,style={'background-color':   '#E5CAB1'})

        #table_index=query_join('tt_indice_sentencia','','key',value).drop(['radicacion','certificado','key','tipo'],axis=1)  
        #table_index=table_index.sort_values('numeral')
        #table_index = dbc.Table.from_dataframe(table_index, striped=True, bordered=True, hover=True,style={'background-color':       '#E5CAB1'})
  
    
        ### GEO referenciación ###
        table_geo=query_join('tt_sentencia_geo','','key',value)[['latitud','longitud']].drop_duplicates()
        table_geo = dbc.Table.from_dataframe(table_geo, striped=True, bordered=True, hover=True,style={'background-color':       '#E5CAB1'})
        
        #DF_tt_sentencia_geo = pd.read_sql("SELECT * from tt_sentencia_geo", engine.connect())
        DF_tt_sentencia_geo = query_join('tt_sentencia_geo','','key',value)
        df_coords = DF_tt_sentencia_geo[DF_tt_sentencia_geo['latitud'] != 'Not Found'].reset_index()
        df_coords['latitud'] = pd.to_numeric(df_coords['latitud'])
        df_coords['longitud'] = pd.to_numeric(df_coords['longitud'])
        
        df_coords_f = df_coords
        df_coords_f['color'] = ''
        fig = px.scatter_mapbox(df_coords_f,
                            lat    = "latitud",
                            lon    = "longitud",
                            zoom   = 5,
                            color_discrete_sequence = ["red", "green"],
                            hover_data = {"color": False})
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      showlegend=False)

        
        mapa= dbc.Card([dbc.CardHeader("Mapa de las coordenadas del predio"),
              dbc.CardBody(dcc.Graph( figure = fig ))  ],
            color="light")


        

        ### extraction resuelve (oredena) text ###      
        table_text_resuelve=query_join('tt_resuelve',['resuelve'],'certificado',value)['resuelve']
        try: 
            table_text_resuelve = list(table_text_resuelve)[0]
        except:
            table_text_resuelve = 'Not Found'
        
            
        ##############################################################################
        #close connection 
        conn.close()
        engine.dispose()
        ##############################################################################
         
        ########################################################################################
                #### botones unica celda
        ########################################################################################

        salida2=[html.Div([
        dbc.Button(
            "Modelo Resuelve", color="success", id="b_modelo", className="mr-1",n_clicks=0,
            style= { 'width': '300px', 'height':'50px', 'display': 'inline-block', 'font-weight': 'bold', 'background-color': '#75b620', 'marginLeft':'30px', 'font-size': '13px', 'color':'black', 'cursor': 'pointer', 'border': '2px solid #69A31C', 'border-radius': '10px'}),
        dbc.Button(
            "Indice Resuelve", id="b_left", className="mr-1",n_clicks=0,
            style= { 'width': '300px', 'height':'50px', 'display': 'inline-block', 'font-weight': 'bold', 'background-color': '#8F5440', 'marginLeft':'30px', 'font-size': '13px', 'color':'white', 'cursor': 'pointer', 'border': '2px solid #724333', 'border-radius': '10px'}),
        dbc.Button(
            "Coordenadas", id="b_center", className="mr-1",n_clicks=0,
            style= { 'width': '300px', 'height':'50px', 'display': 'inline-block', 'font-weight': 'bold', 'background-color': '#8F5440', 'marginLeft':'30px', 'font-size': '13px', 'color':'white', 'cursor': 'pointer', 'border': '2px solid #724333', 'border-radius': '10px'}),
        dbc.Button("Extracción Resuelve", id="b_right", className="mr-1",n_clicks=0,
             style= { 'width': '300px', 'height':'50px', 'display': 'inline-block', 'font-weight': 'bold', 'background-color': '#8F5440', 'marginLeft':'30px', 'font-size': '13px', 'color':'white', 'cursor': 'pointer', 'border': '2px solid #724333', 'border-radius': '10px'}),
        html.Br(),
         dbc.Collapse(
            html.Div(id='inside_collapse1',children=[  table_resuelve  ]),
            id="collapse1",
         ),
            dbc.Collapse(
            html.Div(id='inside_collapse2',children=[  table_ordena_text  ]),
            id="collapse2",
         ),
        dbc.Collapse(
            html.Div(id='inside_collapse3',children=[  table_geo  ,mapa]),
            id="collapse3",
         ),
        dbc.Collapse(
            html.Div(id='inside_collapse4',children=[  html.Br() ,dcc.Textarea(value=table_text_resuelve,readOnly='readonly',wrap='True',style={'width': '90%', 'height': 300,'textAlign':'left','verticalAlign': 'middle','marginLeft':'30px'},)  ]),
            id="collapse4",
         )

    ])
,]

        
        return salida0,salida_descargar,salida_formulario,salida2
    else:
        message=list( np.repeat('',4))
        return [*message]

### Toast ###
@app.callback(
    Output("positioned-toast", "is_open"),
    [Input("positioned-toast-toggle", "n_clicks")],
)
def open_toast(n):
    if n:
        return True
    return False        
    
### Alert ###    
@app.callback(
    [Output("alert-auto", "is_open"),
     Output("alert-quality", "is_open")],
    [Input(component_id='id_sentencia', component_property='value'),
     Input(component_id='id_sentencia', component_property='n_submit'),
     Input(component_id='btn-sentencia', component_property='n_clicks')],
    prevent_initial_call= True)

def toggle_alert(value, n_submit, n_clicks):
    if value!='' and (len(value)==29 or len(value)==67):
        certificado =query_connection('tt_radicado',['Certificado'],'Certificado',value,'')
        radicado =query_connection('tt_radicado',['radicacion'],'radicacion',value,'')
        table_low_quality = query_join('tt_carga_pdf',['low_quality'],'key',value)
        if len(table_low_quality)==0:
            low_quality=''
        else:
            low_quality= table_low_quality = query_join('tt_carga_pdf',['low_quality'],'key',value)['low_quality'][0]
        exist=len(certificado)+len(radicado)
    else:
        exist=0
    
    if exist and (n_clicks or n_submit) and low_quality == 'false':
        return False, False
    elif exist and (n_clicks or n_submit) and low_quality == 'true':
        return False, True
    elif  exist==0 and (n_clicks or n_submit):
        return True, False
    else:
        raise dash.exceptions.PreventUpdate
    return False, False   



### Spinner #####

@app.callback(
    Output("loading-output", "children"), 
     [Input(component_id='id_sentencia', component_property='value'),
     Input(component_id='id_sentencia', component_property='n_submit'),
     Input(component_id='btn-sentencia', component_property='n_clicks')],
)   
def load_output(value, n_submit, n_clicks):
    if (n_clicks or n_submit) and (len(value)==29 or len(value)==67):
        time.sleep(2)

########### Collapse modelo #######
@app.callback(
    Output("collapse1", "is_open"),
    [Input("b_modelo", "n_clicks")]
)
def toggle_collapse(n_click1 ):
    if n_click1 % 2 != 0 :
        return True
    elif n_click1 % 2 == 0:
        return False
        
        
########### Collapse b_left #######
@app.callback(
    Output("collapse2", "is_open"),
    [Input("b_left", "n_clicks")]
)
def toggle_collapse(n_click1 ):
    if n_click1 % 2 != 0 :
        return True
    elif n_click1 % 2 == 0:
        return False

    
    
########### Collapse b_center #######
@app.callback(
    Output("collapse3", "is_open"),
    [Input("b_center", "n_clicks")])
def toggle_collapse(n_click1 ):
    if n_click1 % 2 != 0 :
        return True
    elif n_click1 % 2 == 0:
        return False

########### Collapse b_right #######
@app.callback(
    Output("collapse4", "is_open"),
    [Input("b_right", "n_clicks")]
)
def toggle_collapse(n_click1 ):
    if n_click1 % 2 != 0 : 
        return True
    elif n_click1 % 2 == 0:
        return False

    
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port= '8080')
