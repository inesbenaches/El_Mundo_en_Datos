import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from matplotlib import cm
from plotly import colors

###---------------DATA----------------------------------------------------------------------------------------------------------------------------------------------
df = pd.read_csv('data/df_axw.csv', index_col = 0)


###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
prim_color='#FFA726'
sec_color='#E91E63'
dark_color = '#212121'
light_color = '#D7CCC8'
bg_color = '#424242'



###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------
#--- sidebar-------------------------------- 
st.sidebar.markdown("# Análisis por Grupos")



regiones = pd.unique(df['Tipo'].sort_values())
region = st.sidebar.selectbox(
    'Selecciona una opción',
    regiones, index = 2
)
#una vez seleccionado el tipo hacemos la escala de color dependiendo de la longitud de la lista
n_colors = len(pd.unique(df[df['Tipo']== region]['Nombre']))
colorines = px.colors.sample_colorscale('turbo_r', [n/(n_colors-1) for n in range(n_colors)])

nombres = pd.unique(df[df['Tipo']==region]['Nombre'].sort_values(ascending = False))
nombre = st.sidebar.multiselect(
    'Selecciona los subgrupos a visualizar',
    nombres,
    default = nombres
)
#--- CABECERA ------------------------------------------------------------------------------------------------------------
st.header('Análisis por Grupos de observación')
st.write('---')
col1, col2, col3= st.columns ((1,1,1,))

subset = df[(df['Nombre']== nombre[0]) & (df['Año']==2021)]
for x in nombre[1:]:
    subset = pd.merge(subset, df[(df['Nombre']== x) & (df['Año']==2021)], how = 'outer')
st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 30px;
}
</style>
""",
    unsafe_allow_html=True,
)

with col1:
    esp_max = subset['Esperanza Vida al nacer'].max()
    esp_max_nom = subset['Esperanza Vida al nacer'].idxmax()
    esp_max_nom = subset.loc[esp_max_nom]['Nombre']
    esp_min = subset['Esperanza Vida al nacer'].min()
    esp_min_nom = subset['Esperanza Vida al nacer'].idxmin()
    esp_min_nom = subset.loc[esp_min_nom]['Nombre']
    st.metric('Esperanza de vida al nacer',f'{int(esp_max):,} en {esp_max_nom}', f'{esp_max - esp_min:.2f} más que en {esp_min_nom}',help= 'Años, En 2021')
with col3:
    nac_max = subset['Nacimientos por mujer'].max()
    nac_max_nom = subset['Nacimientos por mujer'].idxmax()
    nac_max_nom = subset.loc[nac_max_nom]['Nombre']
    nac_min = subset['Nacimientos por mujer'].min()
    nac_min_nom = subset['Nacimientos por mujer'].idxmin()
    nac_min_nom = subset.loc[nac_min_nom]['Nombre']
    st.metric('Tasa fecundidad',f'{int(nac_max):.2f} en {nac_max_nom}', f'{nac_max - nac_min:.2f} más que en {nac_min_nom}',help= 'Partos por mujer, En 2021')
with col2:
    ed_max = subset['Mediana Edad'].max()
    ed_max_nom = subset['Mediana Edad'].idxmax()
    ed_max_nom = subset.loc[ed_max_nom]['Nombre']
    ed_min = subset['Mediana Edad'].min()
    ed_min_nom = subset['Mediana Edad'].idxmin()
    ed_min_nom = subset.loc[ed_min_nom]['Nombre']
    st.metric('Mediana de Edad',f'{int(ed_max):,} en {ed_max_nom}', f'{ed_max - ed_min:.2f} más que en {ed_min_nom}',help= 'Años, En 2021')

#--- MÉTRICAS ------------------------------------------------------------------------------------------------------------

st.write('---')


#--- GRÁFICO 2 ---------------------------------------------------------------------------------------------------
fig2 = go.Figure()
config = {'displayModeBar': False}
i = 0
for regs, grupo in df[df['Tipo']== region].groupby('Nombre'):
    if regs in nombre:
        fig2.add_trace(
            go.Scatter(
                x = grupo['Año'], 
                y = grupo['Pob Total (k)'], 
                name = regs,
                fill='tonexty',
                opacity = 0.5,
                line = dict(
                    color = colorines[i], 
                    width = 0.1                            
                    ),
                stackgroup='one',  
                )
            )
    i = i+1
    
fig2.update_layout(
    xaxis_title="<i>Año</i>",
    yaxis_title="<i>Personas</i>",
    hovermode="x",
    hoverlabel=dict(
        font = dict(
            size = 16,
        ),
    ),
    title = dict(
        text = '<b>Total de la Población en miles de personas</b>', 
        y= 0.97,
        x=0.97,
        xanchor= 'right',
        yanchor= 'top'
        ), 
    showlegend=True,
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(0,0,0,0)',
        font=dict(
            size=12,
        ),
    ),
    height= 600,
    width= 1400,
    font=dict(
        size=14,
        color=light_color),
    margin=dict(l=30, r=10, t=10, b=30),
    plot_bgcolor= 'rgba(0,0,0,0)',
)
fig2.update_traces(hovertemplate = '%{y:,.0f} mil personas')
fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(gridcolor=dark_color)
#---DISPLAY GRAFICOS ---------------------------------------------------------------------------------------------------
st.plotly_chart(fig2,config=config)
