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
    min_date = df['DATA PRELIEVO'].min().date()
    max_date = df['DATA PRELIEVO'].max().date()
    with st.form('filtro'):
      # Crea un widget a scorrimento per selezionare le date
      start_date = st.date_input("Seleziona data inizio", min_date)
      end_date = st.date_input("Seleziona data fine", max_date)
      submit = st.form_submit_button('Filtra')
      if submit:
       # Filtra il dataframe in base all'intervallo di date selezionato dall'utente
       filtered_df = df[(df['DATA PRELIEVO'].dt.date >= start_date) & (df['DATA PRELIEVO'].dt.date <= end_date)]
       return filtered_df 
    return df
     
# Funzione principale dell'applicazione Streamlit
def main():
    st.title("Monitor Education")

    missioni = st.file_uploader("Carica il file 'Missioni' CSV", type=["csv"])


    if missioni:
        
        totale_ubicazioni_df = pd.read_csv('totale_ubicazioni.csv', sep=";")
       
        #st.write("Contenuto del file 'Missioni':")
        missioni_df = load_data(missioni)
        missioni_df = missioni_df.rename(columns={"QTA' PRELEVATA": 'QTA PRELEVATA'})
        st.write("Contenuto del file 'Missioni':")
        st.dataframe(missioni_df)
    
        
        # Filtrare le righe con NaN o valori non validi
        righe_nan = missioni_df[missioni_df['QTA PRELEVATA'].isna()]

        # Rimuovere le righe con NaN o valori non validi
        missioni_df = missioni_df.dropna(subset=['QTA PRELEVATA'])

        # Convertire la colonna 'Quantità Movimentata' in tipo int
        missioni_df['QTA PRELEVATA'] = missioni_df['QTA PRELEVATA'].astype(int)
        
        
        #filtro le missioni in base alle date
        filtered_df = filter_dataframe_by_date(missioni_df)
        st.write("Database filtrato per data")
        st.dataframe(filtered_df)


if __name__ == "__main__":
    main()
