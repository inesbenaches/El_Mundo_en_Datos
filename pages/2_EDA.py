import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

###---------------DATA----------------------------------------------------------------------------------------------------------------------------------------------
File = pd.ExcelFile('data/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx')
#escogemos la que vamosa utilizar y la guardamos en la variable df
df = File.parse('Estimates', skiprows = 16, index_col = 0)

###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
prim_color='#FFA726'
sec_color='#E91E63'
dark_color = '#212121'
light_color = '#D7CCC8'

###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------
st.markdown("# EDA: Análisis Exploratorio de los Datos")

#--- sidebar--------------------------------
st.sidebar.markdown("# Análisis Exploratorio de los Datos")
st.sidebar.markdown("# EDA")
st.header('Visualización Inicial')
st.write(df.tail())

st.write('El DataFrame, es decir, la base de datos, se compone de ' +str(df.shape[1])+ ' columnas y '+str(df.shape[0])+' filas' )
with st.expander('Tratamiento de datos nulos', expanded=False):
    st.header('Tratamiento de datos nulos')
    st.write('Vamos a observar si hay datos nulos y en que columnas:')
    st.code('''
for col in df.columns:
    if df[col].isnull().sum() != 0:
        print(str(col) + ': ' + str(df[col].isnull().sum())))''', language='python')
    for col in df.columns:
        if df[col].isnull().sum() != 0:
            st.write('--  ' + str(col) + ': ' + str(df[col].isnull().sum()))
    df['SDMX code**'] = df['SDMX code**'].fillna(-8)
    st.write('Vemos los datos faltantes relativos a Year:')
    st.write(df[df['Year'].isnull()])
    st.write('como se trata de filas separadoras del excel, las eliminamos')
    st.code('''df.drop([73,650,1155,1588], axis = 0, inplace = True)''', language='python')
    df.drop([73,650,1155,1588], axis = 0, inplace = True)
    st.write('tratamos los valores nulos en SDMX Code')
    st.code('''df['SDMX code**'] = df['SDMX code**'].fillna(-8)''', language='python')
    df['SDMX code**'] = df['SDMX code**'].fillna(-8)
    st.write('los demás datos nulos son, segun la documentación, areas diferentes que no responden a un pais, pero observamos que Namibia tiene como ISO2 "NA" que a la hora de leerlo de un excel nos da error, así que lo modificamos como sigue')
    st.code('''df[df['Region, subregion, country or area *']=='Namibia'] =df[df['Region, subregion, country or area *']=='Namibia'].fillna({'ISO2 Alpha-code': 'NA'})''', language='python')
    df[df['Region, subregion, country or area *']=='Namibia'] =df[df['Region, subregion, country or area *']=='Namibia'].fillna({'ISO2 Alpha-code': 'NA'})
with st.expander('Conversión de tipos', expanded=False):
    st.header('Conversión de tipos')
    st.write('Después de echarle un vistazo a los datos, cambiamos a tipo numérico si es posible. Si hay datos faltantes "..." lo reemplazamos con un -8')
    st.code('''
    for col in df.columns[10:]:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                df[col] = df[col].replace('...','-8')
                df[col] = pd.to_numeric(df[col], errors='raise')
    ''', language='python')
    for col in df.columns[10:]:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                df[col] = df[col].replace('...','-8')
                df[col] = pd.to_numeric(df[col], errors='raise')
    st.write('convertimos a float todas las variables de tipo int y mostramos los tipos de datos que tenemos')
    st.code('''df.loc[:,df.select_dtypes(include=np.number).columns] = (df.select_dtypes(include=np.number)).astype(float)''', language='python')
    df.loc[:,df.select_dtypes(include=np.number).columns] = (df.select_dtypes(include=np.number)).astype(float)
    st.write(df.dtypes.value_counts())
with st.expander('Limpieza de columnas', expanded=False):
    st.header('Limpieza de columnas')
    st.write('Eliminamos las columnas 0, 2, 3, 4, 5, 6 8, que contienen etiquetas descriptivas que no interfieren con nuestro análisis, así como otras variables que representan el mismo dato de manera diferente.')
    df_w =  df
    df_w = df_w.drop(columns =['Variant', 'Notes', 'Location code', 'ISO3 Alpha-code', 'ISO2 Alpha-code', 'SDMX code**', 'Parent code'])
    df_w = df_w.drop(columns =['Total Population, as of 1 January (thousands)'])
    df_w = df_w.drop(columns=[
    'Male Population, as of 1 July (thousands)', 'Female Population, as of 1 July (thousands)', # representan lo mismo que 'Population Sex Ratio, as of 1 July (males per 100 females)'
    'Natural Change, Births minus Deaths (thousands)', # = que 'Rate of Natural Change (per 1,000 population)'
    'Population Change (thousands)',  # = 'Population Growth Rate (percentage)'
    'Births (thousands)', # = 'Crude Birth Rate (births per 1,000 population)',
    'Total Deaths (thousands)', # = 'Crude Death Rate (deaths per 1,000 population)'
    'Male Deaths (thousands)', # = 'Total Deaths (thousands)' - 'Female Deaths (thousands)'
    'Male Life Expectancy at Birth (years)', # = 'Life Expectancy at Birth, both sexes (years)' - 'Female Life Expectancy at Birth (years)'
    'Male Life Expectancy at Age 15 (years)', # = 'Life Expectancy at Age 15, both sexes (years)' - 'Female Life Expectancy at Age 15 (years)'
    'Male Life Expectancy at Age 65 (years)', # = 'Life Expectancy at Age 65, both sexes (years)', - 'Female Life Expectancy at Age 65 (years)',
    'Male Life Expectancy at Age 80 (years)', # = 'Life Expectancy at Age 80, both sexes (years)' - 
    'Infant Deaths, under age 1 (thousands)', # = 'Infant Mortality Rate (infant deaths per 1,000 live births)', 'Female Life Expectancy at Age 80 (years)',
    'Live Births Surviving to Age 1 (thousands)',
    'Under-Five Deaths, under age 5 (thousands)', # ='Under-Five Mortality (deaths under age 5 per 1,000 live births)',
    'Male Mortality before Age 40 (deaths under age 40 per 1,000 male live births)', # = 'Mortality before Age 40, both sexes (deaths under age 40 per 1,000 live births)' - Female Mortality before Age 40 (deaths under age 40 per 1,000 female live births)',
    'Male Mortality before Age 60 (deaths under age 60 per 1,000 male live births)', # 'Mortality before Age 60, both sexes (deaths under age 60 per 1,000 live births)' - 'Female Mortality before Age 60 (deaths under age 60 per 1,000 female live births)'
    'Male Mortality between Age 15 and 50 (deaths under age 50 per 1,000 males alive at age 15)', # = 'Mortality between Age 15 and 50, both sexes (deaths under age 50 per 1,000 alive at age 15)' - 'Female Mortality between Age 15 and 50 (deaths under age 50 per 1,000 females alive at age 15)',
    'Male Mortality between Age 15 and 60 (deaths under age 60 per 1,000 males alive at age 15)', # = 'Mortality between Age 15 and 60, both sexes (deaths under age 60 per 1,000 alive at age 15)' - 'Female Mortality between Age 15 and 60 (deaths under age 60 per 1,000 females alive at age 15)'
    'Net Number of Migrants (thousands)'# = 'Net Migration Rate (per 1,000 population)'
    ])
    st.write('Aún así el DataFrame se compone de ' +str(df_w.shape[1])+ ' columnas y '+str(df_w.shape[0])+' filas' )
with st.expander('Test de normalidad', expanded=False):
    st.header('Test de normalidad')
    st.write('Veamos si nuestra variable objetivo (Poblacion Total) es normal')
    st.code('''
from scipy.stats import shapiro
stat, p = shapiro(df_w['Total Population, as of 1 July (thousands)'])
print('stat=%.3f, p = %.3f' %(stat, p))
if p > 0.05:
    print('No podemos rechazar que siga una distribución normal')
else:
    print('Sigue una distribución normal')
    ''', language='python')
    from scipy.stats import shapiro
    stat, p = shapiro(df_w['Total Population, as of 1 July (thousands)'])
    st.write('stat=%.3f, p = %.3f' %(stat, p))
    if p > 0.05:
        st.write('No podemos rechazar que siga una distribución normal')
    else:
        st.write('Sigue una distribución normal')
with st.expander('Test de correlación', expanded=False):
    st.header('Test de correlación')
    st.write('Como sigue una gausiana, utilizaremos pearson. Además, vamos a eliminar del modelo variables que aporten una información linealmente similar al mismo. La lógica será la siguiente:')
    st.write('1.   Analizamos de la matriz de correlación en busca de valores que sean superior a un cierto *threshold* (en nuestro caso, .95)')
    st.write('2.   De entre ambas variables con un índice de correlación tan alto, eliminamos aquella que tenga menor corficiente de correlación con la variable respuesta.')
    st.code('''
import plotly.express as px
corr = df_w.corr(method = 'pearson').sort_values(by = 'Total Population, as of 1 July (thousands)', axis = 0, ascending = False).sort_values(by = 'Total Population, as of 1 July (thousands)', axis = 1, ascending = False)
threshold = .95
var_out = [corr.columns[col] if ((corr.iloc[idx,col]>threshold) & (corr.iloc[idx,0]>corr.iloc[0,col])) else corr.index[idx] if ((corr.iloc[idx,col]>threshold) & (corr.iloc[idx,0]<corr.iloc[0,col])) else 0 for idx in range(1,corr.shape[0]) for col in range(idx+1,corr.shape[1])]
var_out = [var for var in var_out if var!=0]
    ''', language='python')
    import plotly.express as px
    corr = df_w.corr(method = 'pearson').sort_values(by = 'Total Population, as of 1 July (thousands)', axis = 0, ascending = False).sort_values(by = 'Total Population, as of 1 July (thousands)', axis = 1, ascending = False)
    threshold = .95
    var_out = [corr.columns[col] if ((corr.iloc[idx,col]>threshold) & (corr.iloc[idx,0]>corr.iloc[0,col])) else corr.index[idx] if ((corr.iloc[idx,col]>threshold) & (corr.iloc[idx,0]<corr.iloc[0,col])) else 0 for idx in range(1,corr.shape[0]) for col in range(idx+1,corr.shape[1])]
    var_out = [var for var in var_out if var!=0]
    df_w = df_w.drop(var_out, axis = 1)
    corr = df_w.corr(method = 'pearson').sort_values(by = 'Total Population, as of 1 July (thousands)', axis = 0, ascending = False).sort_values(by = 'Total Population, as of 1 July (thousands)', axis = 1, ascending = False)
    st.write('creamos un mapa de correlación de variables para ver ')

    fig = px.imshow(corr.iloc[0:,0:],  x = corr.iloc[0:,0:].index, y = corr.iloc[0:,0:].index,
                color_continuous_scale="RdBu", title = 'Heatmap corr marca ACME', template = 'plotly_dark', height = 1000)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("De aqui podemos obtener varias conclusiones: (comentaremos las 6 menos obvias)\n 1. **Population Sex Ratio'** no interfiere en ninguna otra variable\n 2. La **'Median Age'** esta alta y negativamente correlacionada con el **'Rate Natural Change'** y con **'Crude Birth Rate'**\n 3. El **'Mean Age Childbearing'** esta correlacionada con **'Sex ratio at birth'** \n 4. **'Births by women aged 15 to 19'** está altamente correlacionada con **'Female Deaths'** y **'Total Population'**\n 5. **'Year'** esta negativa y moderadamente correlacionado con **'Infant Mortality Rate'** \n 6. **'Population Density'** no está correlacionada con ninguna otra variable")
