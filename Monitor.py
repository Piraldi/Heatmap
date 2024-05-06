import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
import plotly.express as px
from io import BytesIO

# Imposta il nome della pagina
st.set_page_config(page_title='Monitor Education')


#funzione per caricare file e scegliere separatore
def load_data(file):
    data = pd.read_csv(file, sep=';')
    return data
            
def filter_dataframe_by_date(df):
    # Seleziona l'intervallo di date in una sidebar (container)
  with st.sidebar:
    st.subheader('Imposta filtro tra date:')
    df['ConfermaNew']=df['Conferma'].str[:8]
    df['Datanew'] = pd.to_datetime(df['ConfermaNew'], format='%d/%m/%y')
    min_date = df['Datanew'].min().date()
    max_date = df['Datanew'].max().date()
    with st.form('filtro'):
      # Crea un widget a scorrimento per selezionare le date
      start_date = st.date_input("Seleziona data inizio", min_date)
      end_date = st.date_input("Seleziona data fine", max_date)
      submit = st.form_submit_button('Filtra')
      if submit:
       # Filtra il dataframe in base all'intervallo di date selezionato dall'utente
       filtered_df = df[(df['Datanew'].dt.date >= start_date) & (df['Datanew'].dt.date <= end_date)]
       return filtered_df 
    return df
     
