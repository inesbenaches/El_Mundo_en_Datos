# Contents of ~/my_app/main_page.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

###---------------STYLE----------------------------------------------------------------------------------------------------------------------------------------------

# paleta https://colorhunt.co/palette/2c3333395b64a5c9cae7f6f2
#2C3333
#395B64
#A5C9CA
#E7F6F2

###---------------DATA----------------------------------------------------------------------------------------------------------------------------------------------



#####------- GRAFICO 1

###---------------STYLING----------------------------------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title='El Mundo en Datos', page_icon='resources/world.png', layout='wide',  initial_sidebar_state="expanded")

###---------------PAGE----------------------------------------------------------------------------------------------------------------------------------------------

#--- sidebar
st.sidebar.markdown('El matemático **Andrejs Dunkels** es famoso por dos frases que pronunció muy seguidas. \n\n *“Es fácil mentir con estadísticas”* \n\n *“Es difícil decir la verdad sin ellas”*')

#--- content

st.image('resources/wordcloud.png')
st.caption('Source info: https://population.un.org')
#--- GRAFICO 1

