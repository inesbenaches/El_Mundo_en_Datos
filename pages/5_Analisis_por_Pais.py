import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from plotly import colors
import plotly.graph_objs as go
import matplotlib.colors as clrs

###---------------DATA----------------------------------------------------------------------------------------------------------------------------------------------
banderas = pd.read_csv('data/banderas.csv', index_col = 0)
piramide = pd.read_csv('data/piramide.csv', index_col = 0)
df = pd.read_csv('data/df_axp.csv', index_col = 0)

#https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2022_Life_Table_Complete_Medium_Both_1950-2021.zip
#females
df_edades = pd.read_csv('data/WPP2022_Population1JanuaryByAge5GroupSex_Medium.csv', low_memory=False)

###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
prim_color='#FFA726'
sec_color='#E91E63'
dark_color = '#212121'
light_color = '#D7CCC8'
bg_color = '#424242'


###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------
#--- sidebar-------------------------------- 
st.sidebar.markdown("# Análisis por País")

paises = pd.unique(df['Nombre'].sort_values())
pais = st.sidebar.selectbox(
    'Selecciona un país',
    paises, index = 200
)

annos = pd.unique(df[df['Nombre']==pais]['Año'].sort_values(ascending = False))
anno = st.sidebar.selectbox(
    'Selecciona el año a visualizar',
    annos,
)
if  '-8' in df[df['Nombre']==pais].values: #si faltara algun dato, nos lo mostraria en el sidebar.
    st.sidebar.write('Hay datos incompletas, por loq ue la interpretación puede fallar')

color1_pais =  banderas.loc[banderas['Nombre'] == pais, ['rgb1']].values[0]
color2_pais =  banderas.loc[banderas['Nombre'] == pais, ['rgb2']].values[0]
color3_pais =  banderas.loc[banderas['Nombre'] == pais, ['rgb3']].values[0]
color1_p_rgb = color1_pais[0].replace('a', '').replace(',1)', ')')
color2_p_rgb = color2_pais[0].replace('a', '').replace(',1)', ')')
color3_p_rgb = color3_pais[0].replace('a', '').replace(',1)', ')')

#--- MÉTRICAS ------------------------------------------------------------------------------------------------------------

naci = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Natalidad (x1000)'].values[0]
if anno != 1950:
    anno_ant = anno-1
else:
    anno_ant = anno
naci_ant = df.loc[(df['Nombre']==pais) & (df['Año']==anno_ant),'Natalidad (x1000)'].values[0]
pob = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Pob Total (k)'].values[0]
pob = pob*1000
dif_ant = pob - (df.loc[(df['Nombre']==pais) & (df['Año']==anno_ant),'Pob Total (k)'].values[0])*1000
naci = naci * pob /1000
naci_ant = naci_ant *dif_ant /1000
esp = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Esperanza Vida al nacer'].values[0]
esp_ant = df.loc[(df['Nombre']==pais) & (df['Año']==anno_ant),'Esperanza Vida al nacer'].values[0]
dens = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Densidad (xkm2)'].values[0]
dens_ant = df.loc[(df['Nombre']==pais) & (df['Año']==anno_ant),'Densidad (xkm2)'].values[0]
part = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Nacimientos por mujer'].values[0]
part_ant = df.loc[(df['Nombre']==pais) & (df['Año']==anno_ant),'Nacimientos por mujer'].values[0]
edad = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Mediana Edad'].values[0]
edad_ant = df.loc[(df['Nombre']==pais) & (df['Año']==anno_ant),'Mediana Edad'].values[0]
p_edad = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Mediana edad alumbramiento'].values[0]
p_edad_ant = df.loc[(df['Nombre']==pais) & (df['Año']==anno_ant),'Mediana edad alumbramiento'].values[0]

#--- GRÁFICO PIRÁMIDE ---------------------------------------------------------------------------------------------------
piramide_sub = piramide[(piramide['Nombre']== pais) & (piramide['Año']== anno)]

#definir límites para x and y
y = range(0, piramide_sub.shape[0])
x_male = piramide_sub['PopMale']
x_female = piramide_sub['PopFemale']
if x_male.max() > x_female.max():
    x = range(0, int(x_male.max()+1), int((x_male.max()/6+1)))  # hacerlo en múltiplos de 500
else:
    x = range(0, int(x_female.max()+1),int((x_female.max()/6+1) ))

#define los parámetros de la trama
fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(6, 6))

#especifique el color de fondo y el título de la trama
plt.rcParams['axes.facecolor'] = clrs.to_rgba([0,0,0,0])
plt.figtext(0.53,1,
    'Pirámide Poblacional', 
    fontsize=15, 
    ha='center', 
    fontdict = dict(
        color=light_color,
        weight = 'bold',
    )
)
    
#definir barras masculinas y femeninas
axes[0].barh(
    y, 
    x_male, 
    align='center', 
    color=colors.validate_colors(color2_pais)
)
axes[0].set_title('Hombres (miles)', color=light_color)
axes[1].barh(
    y, 
    x_female, 
    align='center', 
    color=colors.validate_colors(color1_pais)
)
plt.xticks(np.arange(min(x), max(x)+1, 1.0))
axes[1].set_title('Mujeres (miles)', color=light_color)

# ajuste los parámetros de la cuadrícula y especifique etiquetas para el eje y
axes[0].set(yticks=y, yticklabels=piramide_sub['AgeGrp'])
axes[0].set(xticks=x, xticklabels=x)
axes[1].set(xticks=x, xticklabels=x)
axes[0].tick_params(axis='y', colors=light_color, direction = 'in', labelright = True, right = True, left = False, labelleft = False, pad = 15, width = 0)
axes[1].tick_params(axis='y', colors=light_color, direction = 'in', width = 0)
axes[0].tick_params(axis='x',colors=light_color)
axes[1].tick_params(axis='x', colors=light_color)
axes[0].invert_xaxis()
axes[0].spines['right'].set_visible(False)
axes[0].spines['top'].set_visible(False)
axes[0].spines['bottom'].set_visible(False)
axes[0].spines['left'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].spines['top'].set_visible(False)
axes[1].spines['bottom'].set_visible(False)
axes[1].spines['left'].set_visible(False)
plt.tight_layout()
fig.patch.set_facecolor('blue')
fig.patch.set_alpha(0)
#--- GRÁFICO Crecimiento total de la población ---------------------------------------------------------------------------------------------------
fig2 = go.Figure()
config = {'displayModeBar': False}

fig2.add_trace(go.Scatter(
    x =df[df['Nombre']==pais]['Año'], 
    y = df[df['Nombre']==pais]['Natalidad (x1000)']*pob/1000,
    fill='tozeroy',
    name = 'Nacimientos', 
    opacity = 0.5,
    line = dict(
        color = color1_p_rgb, 
        width = 0.1                            
        ),
    ),
) 

fig2.add_trace(go.Scatter(
    x =df[df['Nombre']==pais]['Año'], 
    y = -df[df['Nombre']==pais]['Mortalidad (x1000)']*pob/1000, 
    fill='tozeroy',
    name = 'Muertes', 
    opacity = 0.5,
    line = dict(
        color = color3_p_rgb, 
        width = 0.1                            
        ),
    ),
)

fig2.add_trace(go.Scatter(
    x =df[df['Nombre']==pais]['Año'], 
    y =df[df['Nombre']==pais]['Migracion(x1000)']*pob/1000, 
    fill='tozeroy',
    name = 'Migración', 
    opacity = 0.5,
    line = dict(
        color = color2_p_rgb, 
        width = 0.1                           
        ),
    ),
    
)

fig2.add_trace(go.Line(
    x =df[df['Nombre']==pais]['Año'], 
    y = (-df[df['Nombre']==pais]['Mortalidad (x1000)']*pob/1000) + (df[df['Nombre']==pais]['Natalidad (x1000)']*pob/1000) + (df[df['Nombre']==pais]['Migracion(x1000)']*pob/1000), 
    name = 'Crecimiento Total', 
    line = dict(
        color = light_color, 
        width = 3                            
        ),
    ),
)
fig2.update_layout(
    yaxis=dict(tickformat=","),
    #límites interactivos slidebar
    #xaxis_range = [xlim1,xlim2], 
    #yaxis_range = [ylim1,df[df['Year']==xlim2].Average.max()], 
    xaxis_title="<i>Año</i>",
    yaxis_title="<i>Personas</i>",
    hovermode="x",
    hoverlabel=dict(
        font = dict(
            size = 14,
        ),
    ),
    title = dict(
        text = '<b>Crecimiento Total de la Población</b>', 
        y= 0.97,
        x=0.97,
        xanchor= 'right',
        yanchor= 'top'
        ), 
    showlegend=False,
    height= 500,
    width= 850,
    font=dict(
        size=14,
        color=light_color),
    margin=dict(l=30, r=10, t=10, b=30),
    plot_bgcolor= 'rgba(0,0,0,0)',
)
fig2.update_traces(hovertemplate = '%{y:,.0f} personas')
fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(gridcolor=dark_color)
#--- GRÁFICO PIE MORTALIDAD ---------------------------------------------------------------------------------------------------
fig3 = go.Figure()
col_fig3 = colors.n_colors(color1_p_rgb,color2_p_rgb, 4,colortype = 'rgb')
df3 = pd.DataFrame(columns = ['Personas'], index = ['menores de 5 años', 'entre 5 y 40 años', 'entre 40 y 60 años', 'mayores de 60 años'])
df3['Personas'].loc['menores de 5 años'] = (df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Mortalidad <5 (x1000 nac)'].values[0])*naci /1000
df3['Personas'].loc['entre 5 y 40 años'] = (df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Mortalidad <40 (x1000 nac)'].values[0])*naci / 1000 - df3['Personas'].loc['menores de 5 años']
df3['Personas'].loc['entre 40 y 60 años'] = (df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Mortalidad <60 (x1000 nac)'].values[0])*naci / 1000 - df3['Personas'].loc['entre 5 y 40 años']
df3['Personas'].loc['mayores de 60 años'] = (df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Mortalidad (x1000)'].values[0]*pob/1000)-(df3['Personas'].loc['entre 40 y 60 años'])
df3.reset_index(inplace = True)
df3.rename(columns ={'index':'Fallecimientos'}, inplace = True)
fallecimientos = df.loc[(df['Nombre']==pais) & (df['Año']==anno),'Mortalidad (x1000)'].values[0]*pob/1000
fig3 = px.pie(
    df3, values = 'Personas', 
    names = 'Fallecimientos',
    color_discrete_sequence=col_fig3,
    title= 'Total fallecimientos: ' + str(f'{int(fallecimientos):,}') + ' personas',
)
fig3.update_traces(hovertemplate = '%{label}: <br>%{value:,.0f} personas')
fig3.update_layout(showlegend=False)
#--- CABECERA ------------------------------------------------------------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns((0.8,4.2,1,1,1,))
with col1:
    bandera = banderas.loc[banderas['Nombre'] == pais, ['flag']].values[0]
    response = requests.get(bandera[0])
    img = Image.open(BytesIO(response.content))
    col1.image(img, use_column_width='always')
with col2:
    st.header('Análisis de ' + str(pais) + '\n en ' + str(anno)) ## hacerlo en markdown  y  traducir nombres a español?
with col3:
    st.metric('Población Total', f'{int(pob):,}', delta=f'{int(dif_ant):,}', help= 'Frente '+ str(anno-1))   
with col4:
    st.metric('Densidad (personas/km²)',f'{dens:.2f}', f'{dens - dens_ant:.2f}',help= 'Frente '+ str(anno-1))  
with col5:   
    st.metric('Mediana de la Edad',f'{int(edad):,} años', f'{edad - edad_ant:.2f}',help= 'Frente '+ str(anno-1))
st.write('---')

col1, col2, col3  = st.columns((4,2,1), gap = 'large')

#---DISPLAY GRAFICOS ---------------------------------------------------------------------------------------------------
with col1:
    st.plotly_chart(fig2,config=config, use_container_width=True)
with col2:
    tab1, tab2 = st.tabs(['Pirámide población', 'Fallecimientos por rango de edad'])
    with tab1:
        st.pyplot(fig)
    with tab2:
        st.plotly_chart(fig3, use_container_width=True,config=config)
    
with col3:
    st.metric('Esperanza de vida al nacer',f'{int(esp):,} años', f'{esp - esp_ant:.2f}',help= 'Frente '+ str(anno-1))
    st.write('---')
    st.metric('Hijos por mujer',f'{part:.2f}', f'{part - part_ant:.2f}',help= 'Frente '+ str(anno-1))
    st.write('---')
    st.metric('Mediana edad en el parto',f'{p_edad:.0f} años', f'{p_edad - p_edad_ant:.2f}',help= 'Frente '+ str(anno-1))
