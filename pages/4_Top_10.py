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
banderas = pd.read_csv('data/banderas.csv', index_col = 0)
df_total = pd.read_csv('data/df_top10_total.csv', index_col = 0)
tf = open('resources/color_top10_pais.json','r')
color_pais = json.load(tf)
#####------- GRAFICO 1

###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
prim_color='#FFA726'
sec_color='#E91E63'
dark_color = '#212121'
light_color = '#D7CCC8'
bg_color = '#424242'

###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------

#--- GRAFICO Top10
config = {'displayModeBar': False}
fig2 = px.bar(
    df_total.sort_values('Población', ascending = False), x="Población", y="Año", color="País", 
    text_auto=False, 
    height=600, 
    width= 1400,
    color_discrete_map=color_pais,
    opacity = 0.8,
    
)
fig2.update_traces(
    orientation='h',

)
fig2.update_layout(
    bargap=0,
    xaxis=dict(
        categoryorder='total ascending',
        visible = False,
        showticklabels = False,
    ),
    yaxis=dict(
        visible = False,
        showticklabels = False,
    ),
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor=bg_color,
    plot_bgcolor=bg_color,
    geo_bgcolor = bg_color,
    title = dict(
        font_color = light_color,
        text = 'desde <b>1950</b><br> hasta <b>2021</b>',
        font_size = 30,
        y = 0.9,
        x = 0.9,
        ),
    showlegend = False,
    hoverlabel=dict(
        font = dict(
            size = 12,
        ),
    ),
)
fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(showgrid=False)
fig2['layout']['yaxis']['autorange'] = "reversed" # gracias vestland  https://stackoverflow.com/questions/59100115/plotly-how-to-reverse-axes

#--- sidebar-------------------------------- 
st.sidebar.header('Top 10 países más poblados del Planeta')
st.sidebar.caption('Desde 1950 hasta 2021')
#--- content--------------------------------
st.header('Top 10 países más poblados')
col1, col2 = st.columns((1,23), gap = 'medium')
with col1:
    pais = list(color_pais.keys())
    for i in range(len(color_pais)):
        bandera = banderas.loc[banderas['Nombre'] == pais[i], ['flag']].values[0]
        response = requests.get(bandera[0])
        img = Image.open(BytesIO(response.content))
        col1.image(img, use_column_width='always')
with col2:        
    st.plotly_chart(fig2, config=config)




