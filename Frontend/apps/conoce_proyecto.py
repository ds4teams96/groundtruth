# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

#from app import app

layout = html.Div([ 
    
    html.Div([
        html.Div([
        html.H1("Nuestra solución: Ground Truth", style={'fontSize': '45px', 'color':'#8F5440'}),
        html.P("Accede al repositorio del proyecto: ", style={'fontSize': '20px', 'color':'#8F5440','display': 'inline'}),
        html.A("github.com/team96_ds4a/ground_truth", href='https://www.github.com/ds4teams96/groundtruth', target='github_proyecto', style={'fontSize': '15px', 'fontWeight': 'bold', 'color':'#8F5440', 'display': 'inline'}),
        html.P("En el siguiente vídeo conocerás todos los detalles de nuestro proyecto: ", style={'fontSize': '20px', 'color':'#8F5440'}),

        ],style={'marginTop':'20px', 'textAlign':'center'})  
    ],style={'height':'180px', 'background-color': '#ECE3DF',  'textAlign':'center', 'borderTop':'solid 1px #ECE3DF'}),
    html.Br(),
    html.Div([
        html.Iframe(src='https://www.youtube.com/embed/NDIXpZrbHSE',
            style={'height':'382px', 'width': '676px', 'frameborder': '0', 'allow': 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen'})
    ], style= {'width':'50%', 'margin': '0 auto'}),
])
