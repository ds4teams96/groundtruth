# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import base64

#from app import app

image_carolina = 'images/Foto_Carolina.png' 
image_javier = 'images/Foto_Javier.png' 
image_jorge = 'images/Foto_Jorge.png' 
image_juan = 'images/Foto_Juan_David.png' 
image_gabriel = 'images/Foto_Gabriel.png' 
image_nelson = 'images/Foto_Nelson.png' 
image_ricardo = 'images/Foto_Ricardo.png' 


encoded_image_carolina = base64.b64encode(open(image_carolina, 'rb').read())
encoded_image_javier = base64.b64encode(open(image_javier, 'rb').read())
encoded_image_jorge = base64.b64encode(open(image_jorge, 'rb').read())
encoded_image_juan = base64.b64encode(open(image_juan, 'rb').read())
encoded_image_gabriel = base64.b64encode(open(image_gabriel, 'rb').read())
encoded_image_nelson = base64.b64encode(open(image_nelson, 'rb').read())
encoded_image_ricardo = base64.b64encode(open(image_ricardo, 'rb').read())

top_card_carolina = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_carolina.decode()), top=True, className = 'card_image'),
        html.Hr(),
        dbc.CardBody(
            html.P("Ingeniera en Electrónica y Telecomunicaciones, Magíster y Doctorado(c) en Ingeniería Telemática de la Universidad del Cauca. " 
                   "Experiencia en proyectos de analítica de datos aplicados al sector legal y de salud.", className="card_text"), style={'height':'230px'}
        ),
    ]

top_card_javier = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_javier.decode()), top=True, className = 'card_image'),
        html.Hr(),
        dbc.CardBody(
            html.P(" Estadístico de la Universidad Nacional de Colombia. "
                   " Magíster en economía aplicada de la Universidad de los Andes. "
                   " Nueve años de experiencia participando en proyectos de investigación económica/social. ", className="card_text"), style={'height':'230px'}
        ),
    ]


top_card_jorge = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_jorge.decode()), top=True, className = 'card_image'),
        html.Hr(),
        dbc.CardBody(
            html.P("Estadístico de la Universidad Nacional de Colombia. "
                   "Tres años de experiencia en el área de investigación de mercado de medios.", className="card_text"), style={'height':'230px'}
        ),
    ]


top_card_juan = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_juan.decode()), top=True, className = 'card_image'),
        html.Hr(),
        dbc.CardBody(
            html.P("Estadístico de la Universidad Nacional de Colombia Sede Medellín. "
                   "Experiencia relacionada con analítica y procesamiento de datos", className="card_text"), style={'height':'230px'}
        ),
    ]


top_card_gabriel = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_gabriel.decode()), top=True, className = 'card_image'),
        html.Hr(),
        dbc.CardBody(
            html.P("Ingeniero electrónico de la Universidad de los Llanos. "
                   "Un año de experiencia en el desarrollo de hardware y software embebido.", className="card_text"), style={'height':'230px'}
        ),
    ]


top_card_nelson = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_nelson.decode()), top=True, className = 'card_image'),
        html.Hr(),
        dbc.CardBody(
            html.P("Ingeniero electrónico, maestrando en Ingeniería de la Universidad del Magdalena. "
                   "Tres años de experiencia profesional en la industria y la academia", className="card_text"), style={'height':'230px'}
        ),
    ]


top_card_ricardo = [
        dbc.CardImg(src='data:image/png;base64,{}'.format(encoded_image_ricardo.decode()), top=True, className = 'card_image'),
        html.Hr(),
        dbc.CardBody(
            html.P("Ingeniero de Sistemas de la Universidad Nacional de Colombia, "
                   "maestrando en Ingeniería de la Información de la Universidad de los Andes. "
                   "Quince años de experiencia en sector privado. ", className="card_text"), style={'height':'230px'}
        ),
    ]

layout = html.Div([ 
    
    html.Div([
        html.Div([
        html.H1("¿Quiénes somos?", style={'fontSize': '45px', 'color':'#8F5440'}),
        html.P(" Somos un equipo multidisciplinario integrado por profesionales en estadística e ingeniería. Nuestros perfiles: ", style={'fontSize': '20px', 'color':'#8F5440'}),
             ],style={'marginTop':'33px', 'textAlign':'center'})  
        
    ],style={'height':'180px', 'background-color': '#ECE3DF', 'borderTop':'solid 1px #ECE3DF'}),
        html.Br(),
        html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(top_card_carolina, color = "light"), width=3),
                dbc.Col(dbc.Card(top_card_javier, color = "light"), width=3),
                dbc.Col(dbc.Card(top_card_jorge, color = "light"), width=3),
                dbc.Col(dbc.Card(top_card_juan, color ="light"), width=3),
            ],
        ),
        
        ], style= {'width':'80%', 'margin': '0 auto'}),
        html.Br(),
        html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(top_card_gabriel,  color = "light"), width={"size": 3, "offset": 2}),
                dbc.Col(dbc.Card(top_card_nelson,   color="light"), width=3),
                dbc.Col(dbc.Card(top_card_ricardo,  color = "light"), width=3),
            ], 
        ),
    ], style= {'width':'80%', 'margin': '0 auto'})
    
])
