import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import json
import plotly.graph_objects as go

from app import app

engine = create_engine('postgresql://postgres:LFnnLUQZQMJ9@db-test2.cxqola6hllvk.us-east-2.rds.amazonaws.com/t96_dev')
DF = pd.read_sql("SELECT * from tt_localizacion", engine.connect())
Dane = pd.read_sql("SELECT * from mt_dane_geo", engine.connect())
DF_tt_radicado = pd.read_sql("SELECT * from tt_radicado", engine.connect())
DF_tt_sentencia_geo = pd.read_sql("SELECT * from tt_sentencia_geo", engine.connect())
DF_tt_grupo_familiar = pd.read_sql("SELECT * from tt_grupo_familiar", engine.connect())
DF_tt_resuelve = pd.read_sql("SELECT * from tt_resuelve", engine.connect())

dane = Dane[['codigo_dep','nombre_dep']]
dane = dane.drop_duplicates(subset = ["codigo_dep"])
dane.reset_index(drop=True,inplace=True)

coords_dep = Dane.groupby(['nombre_dep']).agg({'longitud':'mean','latitud':'mean'}).reset_index()

daneM = Dane[['codigo_dep','nombre_dep','codigo_mun','nombre_mun']]
daneM = daneM.drop_duplicates(subset = ["codigo_mun"])
daneM.reset_index(drop=True,inplace=True)

df_map1 = DF.groupby(['codigo_departamento']).size().reset_index().rename(columns={0:'Conteo'})
df_map1 = df_map1.rename(columns={'codigo_departamento':'DPTO'})
df_map1['DPTO'] = df_map1['DPTO'].apply(lambda x: x.zfill(2))
df_map1 = df_map1.merge(dane, how="right", left_on="DPTO", right_on="codigo_dep")
df_map1.drop(['DPTO'],axis=1, inplace=True)

df_coords = DF_tt_sentencia_geo[DF_tt_sentencia_geo['latitud'] != 'Not Found'].reset_index()
#df_coords.dtypes
df_coords['latitud'] = pd.to_numeric(df_coords['latitud'])
df_coords['longitud'] = pd.to_numeric(df_coords['longitud'])

cols_dd = list(df_map1.nombre_dep[df_map1.Conteo > 0])

with open('./datasets/Colombia.geo.json',"r",encoding='utf-8') as f:
    departamentos = json.load(f)
    
with open('./datasets/municipios.geojson',"r",encoding='utf-8') as f:
    municipios = json.load(f)
    
map1 = px.choropleth_mapbox(df_map1,
                           geojson=departamentos,
                           color="Conteo",
                           color_continuous_scale="brwnyl",
                           locations="codigo_dep", 
                           featureidkey="properties.DPTO",
                           mapbox_style="carto-positron", 
                           zoom=4,
                           center={"lat": 4.6004294, "lon": -74.0762067},
                           hover_name="nombre_dep",
                           hover_data={"codigo_dep": False},
                           labels={"Conteo": "Número de <br> sentencias"})
map1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
map1.update_layout(
    autosize=True,
    hoverlabel=dict(
        bgcolor="#EDEAE8",
        font_size=16,
        font_color = '#1B1B1B'
    )
)
    
df_map2 = DF.groupby(['codigo_departamento','codigo_municipio']).size().reset_index().rename(columns={0:'Conteo'})
df_map2 = df_map2.rename(columns={'codigo_departamento':'DPTO'})
df_map2['DPTO'] = df_map2['DPTO'].apply(lambda x: x.zfill(2))
df_map2['codigo_municipio'] = df_map2['codigo_municipio'].apply(lambda x: x.zfill(5))
df_map2 = df_map2.merge(daneM, how="right", left_on=["DPTO",'codigo_municipio'], right_on=["codigo_dep",'codigo_mun'])
df_map2.drop(['DPTO'],axis=1, inplace=True)
df_map2.drop(['codigo_municipio'],axis=1, inplace=True)

layout = html.Div([
    html.Div([
        html.Div([
        html.H1("Ficha departamental", style={'fontSize': '45px', 'color':'#8F5440'}),
        html.P("Obtén estadísticas relevantes para monitorear las sentencias sobre restitución de tierras", style={'fontSize': '20px', 'color':'#8F5440'}),
        ],style={'marginTop':'33px', 'textAlign':'center'})  
    ],style={'height':'180px', 'background-color': '#ECE3DF',  'textAlign':'center', 'border-top':'solid 1px #ECE3DF'}),
    
    html.Br(),
    
    html.Div([
            html.Div([
                    html.H3(html.B("Selecciona un departamento: "))],
                    style={'height': '50px', 'color':'#8F5440', 'textAlign':'center'}),

            html.Div([dcc.Dropdown(
                    id = 'dep_select',
                    options = [{'label': k, 'value': k} for k in cols_dd],
                    value=cols_dd[0])], style={'width': '300px', 'margin': '0 auto'})
            ], style={'height':'120px', 'textAlign':'center'}),
    
    html.Div([
            dbc.Row([
                    dbc.Col(dbc.Card([dbc.CardHeader("Departamentos de Colombia con procesos de restitución de tierras"),
                                     dbc.CardBody( html.Div([dcc.Graph( figure = map1 )], style = {'border':'solid 1px #ECE3DF'}) )], color="light")),
                    dbc.Col(dbc.Card([dbc.CardHeader("Municipios con procesos de restitución de tierras del departamento seleccionado"),
                                     dbc.CardBody( html.Div(id='map2p', className="two columns", style = {'border':'solid 1px #ECE3DF'}) )], color="light"))])
    ]),
    
    html.Br(),
    dbc.Card([dbc.CardHeader("Órdenes de los jueces"),
              dbc.CardBody(html.Div(id='modelco'))], color="light"),
    html.Br(),          
    html.Div([
            dbc.Row([
                    dbc.Col(dbc.Card([dbc.CardHeader("Número de sentencias por año para el departamento seleccionado"),
                                     dbc.CardBody(html.Div(id='timeline', className="two columns"))], color="light")),
                    dbc.Col(dbc.Card([dbc.CardHeader("Familias y personas"),
                                     dbc.CardBody(dcc.Markdown(id ='text01'))], color="light"))])
    ]),
    
   ])

@app.callback(
    Output(component_id='map2p', component_property='children'),
    [Input('dep_select', 'value')])
def update_map2p(dep_select_value):
    df_map2a = df_map2[df_map2['nombre_dep']==dep_select_value]
    coords_dep_f = coords_dep[coords_dep['nombre_dep']==dep_select_value].reset_index()
    map2 = px.choropleth_mapbox(df_map2a,
                           geojson=municipios,
                           color="Conteo",
                           color_continuous_scale="brwnyl",
                           locations="codigo_mun", 
                           featureidkey="properties.MPIO_CCNCT",
                           mapbox_style="carto-positron", 
                           zoom=7,
                           center={"lat": coords_dep_f.latitud[0], "lon": coords_dep_f.longitud[0]},
                           hover_name="nombre_mun",
                           hover_data={"codigo_dep": False,
                                       "codigo_mun": False},
                           labels={"Conteo": "Número de <br> sentencias"})
    map2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    map2.update_layout(
            autosize=True,
            hoverlabel=dict(
                    bgcolor="#EDEAE8",
                    font_size=16,
                    font_color = '#1B1B1B')
                    )
    return [
            dcc.Graph( figure = map2 )
    ]

@app.callback(
    Output(component_id='timeline', component_property='children'),
    [Input('dep_select', 'value')])
def update_graph_timeline(dep_select_value):
    df_tla = DF[DF['departamento']==dep_select_value]
    vector_certificado = df_tla['certificado'].unique()
    df_tlb = DF_tt_radicado[DF_tt_radicado['certificado'].isin(vector_certificado.tolist()) == True]
    df_tlc = df_tlb.groupby(['anio']).size().reset_index().rename(columns={0:'Conteo'})
    df_tlc = df_tlc.astype({'anio': 'int32'})
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = df_tlc['anio'],
                             y = df_tlc['Conteo'],
                             mode = 'lines+markers',
                             line = dict(color='royalblue',
                                         width=2)))
    
    fig.update_layout(
            title='',
            xaxis_title='Año',
            yaxis_title='Cantidad de sentencias',
            xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    linecolor='#1B1B1B',
                    linewidth=3,
                    ticks='outside',
                    tickfont=dict(
                            size=13,
                            color='#1B1B1B',
                            )
                        ),
            yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    showline=True,
                    showticklabels=True,
                    linecolor='#1B1B1B',
                    linewidth=3,
                    ticks='outside',
                    tickfont=dict(
                            size=13,
                            color='#1B1B1B',
                            )
                    ),
    autosize=True,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=False,
    plot_bgcolor='white'
    )
    
    return [
        dcc.Graph(
            figure=fig
        )
    ]
    
@app.callback(
    Output(component_id='text01', component_property='children'),
    [Input('dep_select', 'value')])
def callback_text(dep_select_value):
    df_tla = DF[DF['departamento']==dep_select_value]
    vector_certificado = df_tla['certificado'].unique()
    df_tlb = DF_tt_grupo_familiar[DF_tt_grupo_familiar['key'].isin(vector_certificado.tolist()) == True]
    df_tlc = df_tlb.groupby(['key', 'grupo']).size().reset_index(name='Freq')
    investor_str = ''' Para el departamento de **{0}** las sentencias del juez actuaron sobre **{1}** personas, 
    en **{2}** familias que en promedio tienen **{3}** personas por familia'''.format(
            dep_select_value,
            df_tlc.Freq.sum(),
            df_tlc.key.count(),
            round(df_tlc.Freq.mean(),1))
    return investor_str

@app.callback(
    Output(component_id='modelco', component_property='children'),
    [Input('dep_select', 'value')])
def update_graph_model(dep_select_value):
    df_tla = DF[DF['departamento']==dep_select_value]
    vector_certificado = df_tla['certificado'].unique()
    df_tlb = DF_tt_resuelve[DF_tt_resuelve['certificado'].isin(vector_certificado.tolist()) == True]
    vector_columnas = df_tlb.columns[3:(len(df_tlb.columns)-1)].tolist()
    df_to_model = []
    for i in vector_columnas:
        df_temp = df_tlb.groupby([i]).size().reset_index(name='Y')
        df_temp.columns = ['Category','Count']
        df_temp['Variable'] = i 
        df_to_model.append(df_temp)
    df_to_model2 = pd.concat(df_to_model)
    df_to_model2 = df_to_model2.reset_index()
    df_to_model2['Variable'] = df_to_model2['Variable'].str.replace('_',' ')
    df_to_model2['Variable'] = df_to_model2['Variable'].str.capitalize()
    
    df_to_model2['Variable'] = np.where(df_to_model2['Variable']=='Proyectos productivos beneficiarios restitucion', 'Proyectos productivos restitución', df_to_model2['Variable'])
    df_to_model2['Variable'] = np.where(df_to_model2['Variable']=='Administracion proyectos productivos agroindustriales', 'Administración proyectos agroindustriales', df_to_model2['Variable'])
        
    fig = px.bar(df_to_model2, x="Variable", y="Count", color="Category", title="", text='Count',
                 color_discrete_sequence =['#1B1B1B','#75B620'])
    
    fig.update_layout(
            title='',
            xaxis_title='Órdenes de los jueces',
            yaxis_title='Cantidad de órdenes',
            xaxis=dict(
                    showline=True,
                    showgrid=False,
                    showticklabels=True,
                    automargin= True,
                    linecolor='#1B1B1B',
                    linewidth=2,
                    ticks='outside',
                    tickfont=dict(
                            size=13,
                            color='#1B1B1B',
                            )
                        ),
            yaxis=dict(
                    showgrid=False,
                    zeroline=True,
                    showline=True,
                    showticklabels=True,
                    linecolor='#1B1B1B',
                    linewidth=5,
                    ticks='outside',
                    tickfont=dict(
                            size=13,
                            color='#1B1B1B',
                            )
                    ),
    autosize=True,
    margin=dict(
        autoexpand=True,
        l=50,
        r=20,
        t=20,
        b=260
    ),
    showlegend=True,
    plot_bgcolor='white'
    )
    
    return [
        dcc.Graph(
            figure=fig
        )
    ]
