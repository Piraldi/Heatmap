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
    # Converti la colonna 'DATA PRELIEVO' in tipo datetime se non lo è già
    df['DATA PRELIEVO'] = pd.to_datetime(df['DATA PRELIEVO'], format='%d/%m/%Y')
    # Converti la colonna 'ORARIO' in tipo datetime
    df['ORA PRELIEVO'] = pd.to_datetime(df['ORA PRELIEVO'], format='%H:%M:%S')
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

#funzione produttività per ordine
def calculate_productivity_per_order(df):
    
    
    # Conversione della colonna 'ORA PRELIEVO' in formato datetime
    df['ORA PRELIEVO'] = pd.to_datetime(df['ORA PRELIEVO'], format='%H.%M.%S', errors='coerce')
    
    # Assicurati che 'Quantità Movimentata' sia in formato numerico
    df['QTA PRELEVATA'] = pd.to_numeric(df['QTA PRELEVATA'], errors='coerce')
    
    # Rimuovi le righe con valori NaN nella colonna 'Quantità Movimentata'
    df = df.dropna(subset=['QTA PRELEVATA'])

    # Raggruppa per ordine, utente,data, tipo cliente e tipo prelievo
    productivity_df_per_order = df.groupby([' ORDINE','UTENTE PRELIEVO', 'DATA PRELIEVO','TIPO SCATOLA','UB']).agg({
        'QTA PRELEVATA': 'sum',
        'ARTICOLO': 'size',# Conteggio delle righe per ogni gruppo
        'ORA PRELIEVO': lambda x: (x.max() - x.min()).total_seconds() / 3600,
        }).reset_index()

    # Calcola la produttività (quantità movimentata per ora)
    productivity_df_per_order['Produttività'] = productivity_df_per_order['QTA PRELEVATA'] / productivity_df_per_order['ORA PRELIEVO']
    # Rinomina le colonne
    productivity_df_per_order.rename(columns={
        'QTA PRELEVATA': 'Q tot',
        'ARTICOLO': 'Righe tot',
        'ORA PRELIEVO': 'Ore tot',
        'Produttività': 'Produttività tot'
    }, inplace=True)
    
    
    return productivity_df_per_order

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data


# Funzione principale dell'applicazione Streamlit
def main():
    st.title("Monitor Education")

    missioni = st.file_uploader("Carica il file 'Missioni' CSV", type=["csv"])


    if missioni:
        
        totale_ubicazioni_df = pd.read_csv('totale_ubicazioni.csv', sep=";")
       
        #st.write("Contenuto del file 'Missioni':")
        missioni_df = load_data(missioni)
        missioni_df = missioni_df.rename(columns={"QTA' PRELEVATA": 'QTA PRELEVATA'})
        # Trasforma la colonna desiderata in stringa
        missioni_df['ARTICOLO'] = missioni_df['ARTICOLO'].astype(str)
        missioni_df[' ORDINE'] = missioni_df[' ORDINE'].astype(str)
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


        # Chiama la funzione per calcolare la produttività per ordine
        productivity_df_per_order = calculate_productivity_per_order(filtered_df)
        st.header("Productivity Per Order")
        # Crea una tabella interattiva per visualizzare i risultati
        st.dataframe(productivity_df_per_order)
        # Bottone di download
        tab_1 = to_excel(productivity_df_per_order)
        st.download_button(label='📥 Download tabella',
                           data=tab_1,
                           file_name='dataframe.xlsx',
                           mime='application/vnd.ms-excel')
        st.markdown("---")



if __name__ == "__main__":
    main()
