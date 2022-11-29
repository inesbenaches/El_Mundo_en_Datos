import streamlit as st
import numpy as np
import pandas as pd
#Gráficos
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
###---------------DATA----------------------------------------------------------------------------------------------------------------------------------------------
data = pd.read_csv('data/df_axw.csv',
                      na_values = "NA",
                      sep=",", index_col=0)
df = pd.DataFrame(data[data['Tipo']=='World'].set_index('Año')['Pob Total (k)'])

df.plot(figsize=(15, 4))

###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
prim_color='#FFA726'
sec_color='#E91E63'
dark_color = '#212121'
light_color = '#D7CCC8'
bg_color = '#424242'


###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------


#--- sidebar--------------------------------

st.sidebar.markdown("# Implementacion ARIMA")

#--- content--------------------------------
# Leemos datos y dibujamos
col1, col2 = st.columns((4,2), gap = 'large')
with col1:
    st.markdown("# ARIMA")
    st.markdown('El modelo Arima es una metodología econométrica basada en modelos dinámicos que utiliza datos de series temporales.')
    st.markdown('Para trabajar con modelos ARIMA es necesario tener en cuenta una serie de conceptos básicos tales como: proceso estocástico, ruido blanco, sendero aleatorio y estacionariedad.')
    st.markdown('Un <b>proceso estocástico</b> es una sucesión de variables aleatorias ({Yt}, t = -∞,...-1, 0, 1,..., ∞) que dependen de un parámetro, en el caso de las series temporales este parámetro es el tiempo.', unsafe_allow_html=True)
    st.markdown('Llamamos <b>ruido blanco</b> a una sucesión de variables aleatorias que se caracterizan por tener una esperanza constante e igual a cero, igual varianza, y además, son independientes a lo largo del tiempo (covarianza es cero)', unsafe_allow_html=True)
    st.markdown('Un <b>sendero aleatorio</b> es un proceso estocástico que se caracteriza porque su primera diferencia es un ruido blanco, que no es nuestro caso', unsafe_allow_html=True)
    st.markdown('Un proceso estocástico es débilmente <b>estacionario</b> o estacionario en un sentido amplio, si se cumple que su media y su varianza son constantes para cualquier período de tiempo y las covarianzas entre dos variables solo dependen del lapso de tiempo que transcurre entre ellas.', unsafe_allow_html=True)
    st.markdown('### Identificación')
    st.markdown('Para identificar cual es el proceso <b>ARIMA</b> que ha generado una determinada serie temporal es necesario que los datos sean estacionarios, es decir, no pueden presentar tendencia creciente o decreciente', unsafe_allow_html=True)
    # Creamos gráfico
    f = plt.figure(figsize=(15, 4), dpi=80)
    # Preparamos primer componente
    ax1 = f.add_subplot(131)
    ax1.set_title('Serie original')
    ax1.plot(df.values)
    # Preparamos segundo componente
    ax2 = f.add_subplot(132)
    plot_acf(df.values, ax=ax2)
    # Preparamos tercer componente
    ax3 = f.add_subplot(133)
    plot_pacf(df.values, ax=ax3)
    st.pyplot(f)
    
    # Creamos gráfico
    f = plt.figure(figsize=(15, 4), dpi=80)
    # Preparamos primer componente
    ax1 = f.add_subplot(131)
    ax1.set_title('Diferenciación cuarto orden')
    ax1.plot(df.diff().diff().diff().diff().values)
    # Preparamos segundo componente
    ax2 = f.add_subplot(132)
    plot_acf(df.diff().diff().diff().diff().dropna(), ax=ax2)
    # Preparamos tercer componente
    ax3 = f.add_subplot(133)
    plot_pacf(df.diff().diff().diff().diff().dropna(), ax=ax3)
    st.pyplot(f)
    st.markdown('Ejecutamos el modelo con los valores observados y buscamos aquellos con menor AIC y BIC, que son métricas de error', unsafe_allow_html=True)
    st.code('''# Librerías
from statsmodels.tsa.arima.model import ARIMA

# Ajustamos modelo a datos
model = ARIMA(df.values, order=(2,4,2))
model_fit = model.fit()
# Resumen del entrenamiento
print(model_fit.summary())
model_fit.plot_diagnostics()
    ''')
    model = ARIMA(df.values, order=(2,4,1))
    model_fit = model.fit()
    print(model_fit.summary())
    plot1 = model_fit.plot_diagnostics()
    st.write('AIC: '+ f'{model_fit.aic:.2f}' + ' \n\nBIC: ' + f'{model_fit.bic:.2f}')
with col2:
    st.markdown('### Visualizacion de datos iniciales')
    st.line_chart(df , use_container_width=True)
    st.write('---')
    st.write('Como nuestros datos presentan tendencia, hemos de diferenciar la serie hasta que lo sea.')
    st.markdown('para identificar cuantas diferencias son necesarias para alcanzar la estacionariedad, utilizaremos la prueba de <i>Dickey-Fuller</i>', unsafe_allow_html=True)
    st.code('''
    from statsmodels.tsa.stattools import adfuller
    ''')
    st.write(f"p-valor diferenciación orden cero: {adfuller(df)[1]:.3f}")
    st.write(f"p-valor diferenciación orden uno: {adfuller(df.diff().dropna())[1]:.3f}")
    st.write(f"p-valor diferenciación orden dos: {adfuller(df.diff().diff().dropna())[1]:.3f}")
    st.write(f"p-valor diferenciación orden tres: {adfuller(df.diff().diff().diff().dropna())[1]:.3f}")
    st.write(f"p-valor diferenciación orden cuatro: {adfuller(df.diff().diff().diff().diff().dropna())[1]:.3f}")
    st.write('---')
    st.markdown('En los modelos ARIMA(p,d,q), <b>p</b> representa el orden del proceso autorregresivo, <b>d</b> el número de diferencias que son necesarias para que el proceso sea estacionario y <b>q</b> representa el orden del proceso de medias móviles.', unsafe_allow_html=True)
    st.write('---')
    st.markdown('Metricas Arima sobre la serie diferenciada:')
    st.pyplot(plot1)

st.write('---')

col1, col2 = st.columns((2,4), gap = 'large')
with col1:    
    p = 2 # Coeficientes de autoregresión
    d = 4 # Orden de diferenciación
    q = 1 # Ajuste media móvil
    n = 79 # número de predicciones

    # para poder mostrar la serie original
    df_3 = df.values 

    for _ in range(n):
        model3 = ARIMA(df_3, order=(p,d,q))
        model_fit3 = model3.fit()
        preds3 = model_fit3.predict()
        df_3 = np.append(df_3, model_fit3.forecast()[0], axis=None)
        preds3 = np.append(preds3, model_fit3.forecast()[0], axis=None)

    # Mostramos los datos
    fig3, ax3 = plt.subplots()
    ax3.plot(df.index, df.values, 'b-')
    ax3.plot(range(df.index.min()+d-1,df.index.max()+n), preds3[d:], 'r--')
    plt.legend(['Serie temporal', 'Predicciones'])
    plt.title('ARIMA (2,4,1)')
    st.pyplot(fig3)

    p4 = 2 # Coeficientes de autoregresión
    d4 = 3 # Orden de diferenciación
    q4 = 1 # Ajuste media móvil
    n4 = 79 # número de predicciones

    # para poder mostrar la serie original
    df_4 = df.values 

    for _ in range(n4):
        model4 = ARIMA(df_4, order=(p4,d4,q4))
        model_fit4 = model4.fit()
        preds4 = model_fit4.predict()
        df_4 = np.append(df_4, model_fit4.forecast()[0], axis=None)
        preds4 = np.append(preds4, model_fit4.forecast()[0], axis=None)

    # Mostramos los datos
    fig4, ax4 = plt.subplots()
    ax4.plot(df.index, df.values, 'b-')
    ax4.plot(range(df.index.min()+d-1,df.index.max()+n), preds4[d:], 'r--')
    plt.legend(['Serie temporal', 'Predicciones'])
    plt.title('ARIMA (2,3,1)')
    st.write('hemos ploteado la gráfica con orden de diferenciación 3, por si está sobrediferenciada')
    st.pyplot(fig4)

with col2:
    st.markdown("### Ajustamos el modelo a Datos y observamos al predicción")
    st.code('''
p = 2 # Coeficientes de autoregresión
d = 4 # Orden de diferenciación
q = 1 # Ajuste media móvil
n = 79 # número de predicciones

# para poder mostrar la serie original
df_2 = df.values 

# vamos cambiando el tamaño de la serie segun añadimos predicciones
for _ in range(n):
    model = ARIMA(df_2, order=(p,d,q))
    model_fit = model.fit()
    preds = model_fit.predict()
    df_2 = np.append(df_2, model_fit.forecast()[0], axis=None)
    preds = np.append(preds, model_fit.forecast()[0], axis=None)

# Mostramos los datos
fig, ax = plt.subplots()
ax.plot(df.index, df.values, 'b-')
ax.plot(range(df.index.min()+d-1,df.index.max()+n), preds[d:], 'r--')
plt.legend(['Serie temporal', 'Predicciones'])
    ''')
    st.caption('http://enrdados.net/post/series-temporales-con-arima-i/')

    
