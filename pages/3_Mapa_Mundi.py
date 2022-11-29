# Contents of ~/my_app/pages/page_3.py
import streamlit as st
import plotly.express as px
import numpy as np
import json
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

###---------------DATA----------------------------------------------------------------------------------------------------------------------------------------------
with open('resources/countries.geojson') as file:
    data = json.load(file)
df_pop = pd.read_csv('data/df_pop.csv')
df_dens = pd.read_csv('data/df_dens.csv')

#####------- GRAFICO 1

###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
prim_color='#FFA726'
sec_color='#E91E63'
dark_color = '#212121'
light_color = '#D7CCC8'
bg_color = '#424242'

#####------- GRAFICO 1
color_scale = px.colors.make_colorscale([dark_color,'#170E62','#75157F', sec_color,'#FF8900', prim_color, '#F8FE45'])

###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------


#--- content--------------------------------

#--- GRAFICO 1
def grafico_mapamundi(df, coletilla):
    min = df[anno].min()
    if coletilla == 'personas por km<sup>2</sup>':
        max = df[anno].quantile(0.9)
    else:
        max = df[anno].max()

    
    fig = px.choropleth(
        df, geojson=data, color=anno,
        featureidkey="properties.ISO_A3", locations='ISO3',
        color_continuous_scale=color_scale,
        range_color=(min, max),
        labels={anno:coletilla, 'ISO3':'IS0-3'},
        hover_name = 'Nombre',
        width=1200,
        height=600,
    
    )
    fig.update_geos(
        showocean = True,
        showframe = False,
        showlakes =  False,
        oceancolor=bg_color,
        resolution = 110,
        landcolor = dark_color,
        projection_type = 'equirectangular',
        projection_scale = 1.1,
        fitbounds = 'locations',
        framecolor = bg_color,
        framewidth = 0.5,
        countrywidth = 0.5,
    )
    fig.update_layout(
        coloraxis = dict(
            colorbar = dict(
                len = 0.8,
                tickcolor = light_color,
                tickfont_color = light_color,
                orientation = 'h',
                y = -0.15,
                x = 0.942,
                xanchor = 'right',
                title = dict(
                    font_color = light_color,
                    text = coletilla+' en <b>'+ anno,
                    font_size = 20,
                ),
                #tickvals = [df[anno].quantile(0.1), df[anno].quantile(0.25), df[anno].quantile(0.5), df[anno].quantile(0.75), df[anno].quantile(0.9),max ]
            ),
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        geo_bgcolor = bg_color,
    )
    fig.update_coloraxes(cmin = 20, cmid = max/4, cmax = max)
    return fig

#--- sidebar--------------------------------
st.sidebar.markdown("# Mapa Mundi")

estadistica = st.sidebar.radio(
    'Seleccione el tipo de estadística a representar',
    ('Densidad de Población', 'Población Total'),
    horizontal = True, )
if estadistica == 'Población Total':
    annos = df_pop.columns
else:
    annos = df_dens.columns


anno = st.sidebar.selectbox(
    'Selecciona el año a visualizar',
    annos[3:],
)
#--- content--------------------------------
if estadistica == 'Densidad de Población':
    st.plotly_chart(grafico_mapamundi(df_dens, 'personas por km<sup>2</sup>'), use_container_width=True)
else:
    st.plotly_chart(grafico_mapamundi(df_pop, 'personas'))






