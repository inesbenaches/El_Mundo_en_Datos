import streamlit as st
import numpy as np
import pandas as pd
#Gráficos
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
#para paleta color personalizada
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


###---------------DATA----------------------------------------------------------------------------------------------------------------------------------------------

df = pd.read_csv('https://datahub.io/core/population-global-historical/r/population.csv')
edades = pd.read_csv('data/edades.csv', index_col=0)

#####------- GRAFICO 1
#limites del gráfico
xlim1= -15000
xlim2= int(df.Year.max())
x_total = list(range(xlim1,xlim2,500))
ylim1= 0
ylim2 = int(df.Average.max())
# etiquetas para hovertext
hovertext = []
for x in df['Year']:
    index = df.index[df['Year']==x].tolist()
    #hovertext.append(list())
    if x > 0:
        ht_anno = str(x)+' E.C'
    elif x < 0:
        ht_anno = str(x)+' A.E.C'
    else:
        ht_anno = 'Inicio Era Común'
    y = df.loc[index[0],'Average'] 
    if y < 100:
        ht_pop = str(int(y*1000)) + ' miles de personas'
    else:
        ht_pop = str(int(y)) + ' millones de personas'
    hovertext.append('{} : {}'.format(ht_anno, ht_pop))

###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
prim_color='#FFA726'
sec_color='#E91E63'
dark_color = '#212121'
light_color = '#D7CCC8'
#####------- GRAFICO 1
# paleta color personalizada- desde Paleta 'Dark2'

cmap_by_ages = cm.get_cmap('Set2_r')

###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("# Histórico Mundial")

#--- sidebar--------------------------------
values = df['Year'].values.tolist()
st.sidebar.markdown("# Histórico \nPoblación Mundial")
xlim1, xlim2 = st.sidebar.select_slider(
    'Selecciona el rango de años a visualizar',
    options =  values,
    value= (values[3], values[-1])
)
#--- content--------------------------------
st.caption('A.E.C.: Antes de la Era común \n\n E.C.: Era Común')
#--- GRAFICO 1
fig = go.Figure()
#quita la barra de configuracion del gráfico
config = {'displayModeBar': False} 

#colors = cmap.colors
colors = []
ages = edades['Ages'].unique()
for i in range(len(ages)):
    edades_len = edades[edades['Ages']==ages[i]].shape[0]
    x = list(cmap_by_ages.colors[i])
    #creamos 5 subcolores para cada color
    vals = np.ones((5,3))# el AGE con más edades es 5 
    vals[:, 0] = np.linspace(x[0]*255, x[0]*255/2, 5)
    vals[:, 1] = np.linspace(x[1]*255, x[1]*255/2, 5)
    vals[:, 2] = np.linspace(x[2]*255, x[2]*255/2, 5)
    for c in range(edades_len):
        colors.append('rgb'+ str(tuple(vals[c])))

#Formas para Eras
for i in range(len(edades.index)):
    x1 = edades.iloc[i,0]
    x2 = edades.iloc[i,1]

    fig.add_trace(go.Scatter(   x=[x1, x1, x2, x2],  # coordenadas x para rectángulo
                                y=[0,df.Average.max(), df.Average.max(),0], # coordenadas y para rectángulo
                                fill='toself', 
                                fillcolor=colors[i],
                                #hoveron = 'fills', # select where hover is active
                                line_width=0,
                                text = f' {edades.Ages[i]} ',
                                opacity= 0.6,
                                name= edades.index.values[i],
                                mode = 'none',
                            )
    )
#grafico de lineas
data = fig.add_trace(go.Line(x=df['Year'], 
                        y = df['Average'], 
                        line = dict(
                                    color = prim_color, 
                                    width = 3
                                    ),
                        hoverinfo='text',
                        text=hovertext,

))
fig.update_layout(
    #límites interactivos slidebar
    xaxis_range = [xlim1,xlim2], 
    yaxis_range = [ylim1,df[df['Year']==xlim2].Average.max()], 
    xaxis_title="<em>Año</em>",
    yaxis_title="<em>Población</em><i> en Millones de Personas</i>",
    hovermode="x",
    hoverlabel=dict(
        font = dict(
            size = 16,
        ),
    ),  
    showlegend=False,
    height= 700,
    width= 1200,
    font=dict(
        size=14,
        color=light_color),
    margin=dict(l=30, r=10, t=10, b=30),
    xaxis = dict(# cambiamos los tics para que muestren AC o DC
        tickmode = 'array',
        tickvals = x_total,
        ticktext = [str(i).replace('-','') +' A.E.C' if i < 0 else  'Inicio Era Común' if i == 0 else str(i)+' E.C' for i in x_total]
    )
)
fig.update_xaxes(showgrid=False)
st.plotly_chart(fig, config=config, use_container_width=True)
