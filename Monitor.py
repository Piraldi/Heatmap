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

# Funzione per aggiornare la colonna 'Copie Prelevate' nel dataframe 'Totale Ubicazioni'
def update_copie_prelevate(totale_ubicazioni_df, pivot_df):
    updated_copie_prelevate = []
    for ubicazione in totale_ubicazioni_df['Ubicazione']:
        if ubicazione in pivot_df.index:
            updated_copie_prelevate.append(pivot_df.loc[ubicazione, 'QTA PRELEVATA'])
        else:
            # Se l'ubicazione non è trovata nella tabella pivot, imposta 'Copie Prelevate' a 0
            updated_copie_prelevate.append(0)
    totale_ubicazioni_df['Copie Prelevate'] = updated_copie_prelevate
    return totale_ubicazioni_df

def heatmap_Area100(df):
    Area100_df = df[df['Area'] == 'Area100']
    
    # Raggruppa per 'Ubicazione' e somma le copie prelevate
    Area100_df = Area100_df.groupby('Ubicazione')['Copie Prelevate'].sum().reset_index()
    
    #creo fila e colonna
    Area100_df['Fila'] = Area100_df['Ubicazione'].str[:3]
    Area100_df['Colonna'] = Area100_df['Ubicazione'].str[4:7]
   
    #creo array x e y (valori corsia e campata unici e ordinati)
    sorted_df = Area100_df.sort_values(by='Fila')
    x = sorted_df['Fila'].unique()
    sorted_df = Area100_df.sort_values(by='Colonna')
    y = sorted_df['Colonna'].unique()
    
    
    # Crea un array vuoto delle dimensioni appropriate per la heatmap
    heatmap_data = np.zeros((len(y), len(x)))
    
    # Riempimento dell'array con i valori delle 'Copie Prelevate'
    for i, colonna in enumerate(y):
        for j, fila in enumerate(x):
            selected_row = Area100_df[(Area100_df['Colonna'] == colonna) & (Area100_df['Fila'] == fila)]
            if not selected_row.empty:
                heatmap_data[i][j] = selected_row['Copie Prelevate'].iloc[0]
    
    # Creazione della heatmap utilizzando Plotly Express
    fig = px.imshow(
        heatmap_data,
        x=x,
        y=y,
        color_continuous_scale=[
            [0.0, 'rgb(100, 150, 50)'],
            [0.2, 'yellow'],
            [0.6, 'orange'],
            [0.8, 'red'],
            [1.0, 'red']
        ]
    )
    
    # Personalizzazione del layout della heatmap
    fig.update_layout(
        xaxis_title="Fila",
        yaxis_title="Colonna",
        xaxis_side="top"  # Posiziona l'asse x in alto
    )
    # Personalizza il testo del cursore
    fig.update_traces(hovertemplate="Fila: %{x}<br>Colonna: %{y}<br>Copie Prelevate: %{z}")
    # Mostra la figura Plotly utilizzando Streamlit
    st.plotly_chart(fig)
    
    #totale prelievi di area
    totale_prelievi_Area100 = np.sum(heatmap_data)
   
    return totale_prelievi_Area100  


def heatmap_Area200(df):
    Area200_df = df[df['Area'] == 'Area200']
    
    # Raggruppa per 'Ubicazione' e somma le copie prelevate
    Area200_df = Area200_df.groupby('Ubicazione')['Copie Prelevate'].sum().reset_index()
    
    #creo fila e colonna
    Area200_df['Fila'] = Area200_df['Ubicazione'].str[:3]
    Area200_df['Colonna'] = Area200_df['Ubicazione'].str[4:7]
   
    #creo array x e y (valori corsia e campata unici e ordinati)
    sorted_df = Area200_df.sort_values(by='Fila')
    x = sorted_df['Fila'].unique()
    sorted_df = Area200_df.sort_values(by='Colonna')
    y = sorted_df['Colonna'].unique()
    
    
    # Crea un array vuoto delle dimensioni appropriate per la heatmap
    heatmap_data = np.zeros((len(y), len(x)))
    
    # Riempimento dell'array con i valori delle 'Copie Prelevate'
    for i, colonna in enumerate(y):
        for j, fila in enumerate(x):
            selected_row = Area200_df[(Area200_df['Colonna'] == colonna) & (Area200_df['Fila'] == fila)]
            if not selected_row.empty:
                heatmap_data[i][j] = selected_row['Copie Prelevate'].iloc[0]
    
    # Creazione della heatmap utilizzando Plotly Express
    fig = px.imshow(
        heatmap_data,
        x=x,
        y=y,
        color_continuous_scale=[
            [0.0, 'rgb(100, 150, 50)'],
            [0.2, 'yellow'],
            [0.6, 'orange'],
            [0.8, 'red'],
            [1.0, 'red']
        ]
    )
    
    # Personalizzazione del layout della heatmap
    fig.update_layout(
        xaxis_title="Fila",
        yaxis_title="Colonna",
        xaxis_side="top"  # Posiziona l'asse x in alto
    )
    # Personalizza il testo del cursore
    fig.update_traces(hovertemplate="Fila: %{x}<br>Colonna: %{y}<br>Copie Prelevate: %{z}")
    # Mostra la figura Plotly utilizzando Streamlit
    st.plotly_chart(fig)
    
    #totale prelievi di area
    totale_prelievi_Area200 = np.sum(heatmap_data)
   
    return totale_prelievi_Area200  

def heatmap_Area400(df):
    Area400_df = df[df['Area'] == 'Area400']
    
    # Raggruppa per 'Ubicazione' e somma le copie prelevate
    Area400_df = Area400_df.groupby('Ubicazione')['Copie Prelevate'].sum().reset_index()
    
    #creo fila e colonna
    Area400_df['Fila'] = Area400_df['Ubicazione'].str[:3]
    Area400_df['Colonna'] = Area400_df['Ubicazione'].str[4:7]
   
    #creo array x e y (valori corsia e campata unici e ordinati)
    sorted_df = Area400_df.sort_values(by='Fila')
    x = sorted_df['Fila'].unique()
    sorted_df = Area400_df.sort_values(by='Colonna')
    y = sorted_df['Colonna'].unique()
    
    
    # Crea un array vuoto delle dimensioni appropriate per la heatmap
    heatmap_data = np.zeros((len(y), len(x)))
    
    # Riempimento dell'array con i valori delle 'Copie Prelevate'
    for i, colonna in enumerate(y):
        for j, fila in enumerate(x):
            selected_row = Area400_df[(Area400_df['Colonna'] == colonna) & (Area400_df['Fila'] == fila)]
            if not selected_row.empty:
                heatmap_data[i][j] = selected_row['Copie Prelevate'].iloc[0]
    
    # Creazione della heatmap utilizzando Plotly Express
    fig = px.imshow(
        heatmap_data,
        x=x,
        y=y,
        color_continuous_scale=[
            [0.0, 'rgb(100, 150, 50)'],
            [0.2, 'yellow'],
            [0.6, 'orange'],
            [0.8, 'red'],
            [1.0, 'red']
        ]
    )
    
    # Personalizzazione del layout della heatmap
    fig.update_layout(
        xaxis_title="Fila",
        yaxis_title="Colonna",
        xaxis_side="top"  # Posiziona l'asse x in alto
    )
    # Personalizza il testo del cursore
    fig.update_traces(hovertemplate="Fila: %{x}<br>Colonna: %{y}<br>Copie Prelevate: %{z}")
    # Mostra la figura Plotly utilizzando Streamlit
    st.plotly_chart(fig)
    
    #totale prelievi di area
    totale_prelievi_Area400 = np.sum(heatmap_data)
   
    return totale_prelievi_Area400  

def heatmap_Area300(df, piano):
    Area300_df = df[(df['Area'] == 'Area300') & (df['ripiano'] == piano)]
    
    # Raggruppa per 'Ubicazione' e somma le copie prelevate
    Area300_df = Area300_df.groupby('Ubicazione')['Copie Prelevate'].sum().reset_index()
    
    #creo fila e colonna
    Area300_df['Fila'] = Area300_df['Ubicazione'].str[:3]
    Area300_df['Colonna'] = Area300_df['Ubicazione'].str[4:7]
   
    #creo array x e y (valori corsia e campata unici e ordinati)
    sorted_df = Area300_df.sort_values(by='Fila')
    x = sorted_df['Fila'].unique()
    sorted_df = Area300_df.sort_values(by='Colonna')
    y = sorted_df['Colonna'].unique()
    
    
    # Crea un array vuoto delle dimensioni appropriate per la heatmap
    heatmap_data = np.zeros((len(y), len(x)))
    
    # Riempimento dell'array con i valori delle 'Copie Prelevate'
    for i, colonna in enumerate(y):
        for j, fila in enumerate(x):
            selected_row = Area300_df[(Area300_df['Colonna'] == colonna) & (Area300_df['Fila'] == fila)]
            if not selected_row.empty:
                heatmap_data[i][j] = selected_row['Copie Prelevate'].iloc[0]
    
    # Creazione della heatmap utilizzando Plotly Express
    fig = px.imshow(
        heatmap_data,
        x=x,
        y=y,
        color_continuous_scale=[
            [0.0, 'rgb(100, 150, 50)'],
            [0.2, 'yellow'],
            [0.6, 'orange'],
            [0.8, 'red'],
            [1.0, 'red']
        ]
    )
    
    # Personalizzazione del layout della heatmap
    fig.update_layout(
        xaxis_title="Fila",
        yaxis_title="Colonna",
        xaxis_side="top"  # Posiziona l'asse x in alto
    )
    # Personalizza il testo del cursore
    fig.update_traces(hovertemplate="Fila: %{x}<br>Colonna: %{y}<br>Copie Prelevate: %{z}")
    # Mostra la figura Plotly utilizzando Streamlit
    st.plotly_chart(fig)
    
    #totale prelievi di area
    totale_prelievi_Area300 = np.sum(heatmap_data)
   
    return totale_prelievi_Area300  
   
   
    
#funzione produttività per ordine a pallet
def calculate_productivity_per_order_pallet(df):
    df = df[df['TIPO SCATOLA'] == 'BANC']
    
    # Conversione della colonna 'ORA PRELIEVO' in formato datetime
    df['ORA PRELIEVO'] = pd.to_datetime(df['ORA PRELIEVO'], format='%H.%M.%S', errors='coerce')
    
    # Assicurati che 'Quantità Movimentata' sia in formato numerico
    df['QTA PRELEVATA'] = pd.to_numeric(df['QTA PRELEVATA'], errors='coerce')
    
    # Rimuovi le righe con valori NaN nella colonna 'Quantità Movimentata'
    df = df.dropna(subset=['QTA PRELEVATA'])

    # Raggruppa per ordine, utente,data, tipo cliente e tipo prelievo
    productivity_df_per_order = df.groupby([' ORDINE','UTENTE PRELIEVO', 'DATA PRELIEVO','TIPO SCATOLA']).agg({
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

#funzione produttività per ordine pick&pack
def calculate_productivity_per_order_pickpack(df):
    df = df[df['TIPO SCATOLA'] != 'BANC']
    
    # Conversione della colonna 'ORA PRELIEVO' in formato datetime
    df['ORA PRELIEVO'] = pd.to_datetime(df['ORA PRELIEVO'], format='%H.%M.%S', errors='coerce')
    
    # Assicurati che 'Quantità Movimentata' sia in formato numerico
    df['QTA PRELEVATA'] = pd.to_numeric(df['QTA PRELEVATA'], errors='coerce')
    
    # Rimuovi le righe con valori NaN nella colonna 'Quantità Movimentata'
    df = df.dropna(subset=['QTA PRELEVATA'])

    # Raggruppa per ordine, utente,data, tipo cliente e tipo prelievo
    productivity_df_per_order = df.groupby(['DATA PRELIEVO','UTENTE PRELIEVO', 'N. PIANO','GIRO', 'ROLL']).agg({
        'QTA PRELEVATA': 'sum',
        'ARTICOLO': 'size',# Conteggio delle righe per ogni gruppo
        'ORA PRELIEVO': lambda x: (x.max() - x.min()).total_seconds() / 3600,
        'CASSETTO': pd.Series.nunique,  # Conteggio dei valori unici nella colonna 'CASSETTO'
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
    # Creazione del sommario delle heatmap nella sidebar
    st.sidebar.title("Sommario Heatmap")
    st.sidebar.markdown("""
    - [Heatmap Area100](#heatmap-Area100)
    - [Heatmap Area200](#heatmap-Area200)
    - [Heatmap Area300](#heatmap-Area300)
    - [Heatmap Area400](#heatmap-Area400)
    """, unsafe_allow_html=True)
    
    st.title("Monitor Education")

    missioni = st.file_uploader("Carica il file 'Missioni' CSV", type=["csv"])


    if missioni:
        
        totale_ubicazioni_df = pd.read_csv('totale_ubicazioni.csv', sep=";")
        # Rimuovi i duplicati nella colonna 'Ubicazione' (alcune ubicazioni hanno frazionati diversi)
        totale_ubicazioni_df.drop_duplicates(subset=['Ubicazione'], inplace=True)
       
       
        missioni_df = load_data(missioni)
        
        # Trasforma la colonna desiderata in stringa
        missioni_df['ARTICOLO'] = missioni_df['ARTICOLO'].astype(str)
        missioni_df[' ORDINE'] = missioni_df[' ORDINE'].astype(str)

        # Formatta i numeri nella colonna per avere tre cifre
        missioni_df['FILA'] = missioni_df['FILA'].astype(str).str.zfill(3)
        missioni_df['COLONNA'] = missioni_df['COLONNA'].astype(str).str.zfill(3)
        missioni_df['RIPIANO'] = missioni_df['RIPIANO'].astype(str).str.zfill(3)
        
        
        
        # Crea una nuova colonna 'ubicazione nel formato 'fila.colonna.rip.fraz'
        missioni_df['UBICAZIONE'] = missioni_df['FILA'] + '.' + missioni_df['COLONNA'] + '.' + missioni_df['RIPIANO']
        st.write("Contenuto del file:")
        st.dataframe(missioni_df)
        
        # Filtrare le righe con NaN o valori non validi
        righe_nan = missioni_df[missioni_df['QTA PRELEVATA'].isna()]

        # Rimuovere le righe con NaN o valori non validi
        missioni_df = missioni_df.dropna(subset=['QTA PRELEVATA'])

        # Convertire la colonna 'Quantità Movimentata' in tipo int
        missioni_df['QTA PRELEVATA'] = missioni_df['QTA PRELEVATA'].astype(int)
        
        
        #filtro le missioni in base alle date
        filtered_df = filter_dataframe_by_date(missioni_df)
        #st.write("Database filtrato per data")
        #st.dataframe(filtered_df)

        pivot_missioni = filtered_df.pivot_table(index='UBICAZIONE', values='QTA PRELEVATA', aggfunc='sum')
        
        updated_totale_ubicazioni_df = update_copie_prelevate(totale_ubicazioni_df, pivot_missioni)
        
       
        
        st.markdown("---")
        totale_prelievi_nel_periodo = int(filtered_df['QTA PRELEVATA'].sum())

        # Istogramma copie per area
        # Calcolo delle somme per ogni area
        area_sums = updated_totale_ubicazioni_df.groupby('Area')['Copie Prelevate'].sum().reset_index()

        # Calcolo della percentuale per ogni area rispetto al totale
        area_sums['Percentuale'] = (area_sums['Copie Prelevate'] / area_sums['Copie Prelevate'].sum()) * 100

        # Creazione dell'istogramma con le percentuali
        fig = px.bar(area_sums, x='Area', y='Copie Prelevate', text='Percentuale', title='Copie Prelevate per Area (%)')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

        # Aggiunta del grafico a Streamlit
        st.plotly_chart(fig)
        # Calcolo del totale delle copie prelevate
        totale_copie_prelevate = area_sums['Copie Prelevate'].sum()

        # Aggiunta del valore totale sotto al grafico
        st.write(f"Totale copie prelevate: {totale_copie_prelevate}")
        st.markdown("---")

        #Istogramma ME
        filtered_df_ME = filtered_df[filtered_df['SOC'] == 'ME']
        pivot_missioni_ME = filtered_df_ME.pivot_table(index='UBICAZIONE', values='QTA PRELEVATA', aggfunc='sum')
        #st.write("Tabella Pivot 'Missioni ME':")
        #st.dataframe(pivot_missioni_ME)
        
        updated_totale_ubicazioni_df_ME = update_copie_prelevate(totale_ubicazioni_df, pivot_missioni_ME)
        #st.write("totale ubicazioni ME:")
        #st.dataframe(updated_totale_ubicazioni_df_ME)
        
        st.markdown("---")
        totale_prelievi_nel_periodo_ME = int(filtered_df_ME['QTA PRELEVATA'].sum())

        # Istogramma copie per area
        # Calcolo delle somme per ogni area
        area_sums_ME = updated_totale_ubicazioni_df_ME.groupby('Area')['Copie Prelevate'].sum().reset_index()

        # Calcolo della percentuale per ogni area rispetto al totale
        area_sums_ME['Percentuale'] = (area_sums_ME['Copie Prelevate'] / area_sums_ME['Copie Prelevate'].sum()) * 100

        # Creazione dell'istogramma con le percentuali
        fig = px.bar(area_sums_ME, x='Area', y='Copie Prelevate', text='Percentuale', title='ME Copie Prelevate per Area (%)')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

        # Aggiunta del grafico a Streamlit
        st.plotly_chart(fig)
        # Calcolo del totale delle copie prelevate
        totale_copie_prelevate_ME = area_sums_ME['Copie Prelevate'].sum()

        # Aggiunta del valore totale sotto al grafico
        st.write(f"Totale copie prelevate ME: {totale_copie_prelevate_ME}")
        st.markdown("---")

        #Istogramma RE
        filtered_df_RE = filtered_df[filtered_df['SOC'] == 'RE']
        pivot_missioni_RE = filtered_df_RE.pivot_table(index='UBICAZIONE', values='QTA PRELEVATA', aggfunc='sum')
        #st.write("Tabella Pivot 'Missioni RE':")
        #st.dataframe(pivot_missioni_RE)
        
        updated_totale_ubicazioni_df_RE = update_copie_prelevate(totale_ubicazioni_df, pivot_missioni_RE)
        #st.write("totale ubicazioni RE:")
        #st.dataframe(updated_totale_ubicazioni_df_RE)
        
        st.markdown("---")
        totale_prelievi_nel_periodo_RE = int(filtered_df_RE['QTA PRELEVATA'].sum())

        # Istogramma copie per area
        # Calcolo delle somme per ogni area
        area_sums_RE = updated_totale_ubicazioni_df_RE.groupby('Area')['Copie Prelevate'].sum().reset_index()

        # Calcolo della percentuale per ogni area rispetto al totale
        area_sums_RE['Percentuale'] = (area_sums_RE['Copie Prelevate'] / area_sums_RE['Copie Prelevate'].sum()) * 100

        # Creazione dell'istogramma con le percentuali
        fig = px.bar(area_sums_RE, x='Area', y='Copie Prelevate', text='Percentuale', title='RE Copie Prelevate per Area (%)')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

        # Aggiunta del grafico a Streamlit
        st.plotly_chart(fig)
        # Calcolo del totale delle copie prelevate
        totale_copie_prelevate_RE = area_sums_RE['Copie Prelevate'].sum()

        # Aggiunta del valore totale sotto al grafico
        st.write(f"Totale copie prelevate RE: {totale_copie_prelevate_RE}")
        st.markdown("---")

        #Istogramma DA
        filtered_df_DA = filtered_df[filtered_df['SOC'] == 'DA']
        pivot_missioni_DA = filtered_df_DA.pivot_table(index='UBICAZIONE', values='QTA PRELEVATA', aggfunc='sum')
        #st.write("Tabella Pivot 'Missioni DA':")
        #st.dataframe(pivot_missioni_DA)
        
        updated_totale_ubicazioni_df_DA = update_copie_prelevate(totale_ubicazioni_df, pivot_missioni_DA)
        #st.write("totale ubicazioni DA:")
        #st.dataframe(updated_totale_ubicazioni_df_DA)
        
        st.markdown("---")
        totale_prelievi_nel_periodo_DA = int(filtered_df_DA['QTA PRELEVATA'].sum())

        # Istogramma copie per area
        # Calcolo delle somme per ogni area
        area_sums_DA = updated_totale_ubicazioni_df_DA.groupby('Area')['Copie Prelevate'].sum().reset_index()

        # Calcolo della percentuale per ogni area rispetto al totale
        area_sums_DA['Percentuale'] = (area_sums_DA['Copie Prelevate'] / area_sums_DA['Copie Prelevate'].sum()) * 100

        # Creazione dell'istogramma con le percentuali
        fig = px.bar(area_sums_DA, x='Area', y='Copie Prelevate', text='Percentuale', title='DA Copie Prelevate per Area (%)')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

        # Aggiunta del grafico a Streamlit
        st.plotly_chart(fig)
        # Calcolo del totale delle copie prelevate
        totale_copie_prelevate_DA = area_sums_DA['Copie Prelevate'].sum()

        # Aggiunta del valore totale sotto al grafico
        st.write(f"Totale copie prelevate DA: {totale_copie_prelevate_DA}")
        st.markdown("---")

       

        #Heatmap Area 100
        st.markdown("<a name='heatmap-Area100'></a>", unsafe_allow_html=True) #link per facilitare lo scorrimento
        st.header('Heatmap Area 100')
        totale_prelievi_Area100_nel_periodo = int(heatmap_Area100(updated_totale_ubicazioni_df))
        st.subheader(f"Totale prelievi Area 100: {totale_prelievi_Area100_nel_periodo}" )
        percentuale =  (totale_prelievi_Area100_nel_periodo/totale_prelievi_nel_periodo)*100
        st.subheader(f"% sul totale magazzino: {percentuale:.2f}%")
        st.markdown("---")

        #Heatmap Area 200
        st.markdown("<a name='heatmap-Area200'></a>", unsafe_allow_html=True) #link per facilitare lo scorrimento
        st.header('Heatmap Area 200')
        totale_prelievi_Area200_nel_periodo = int(heatmap_Area200(updated_totale_ubicazioni_df))
        st.subheader(f"Totale prelievi Area 200: {totale_prelievi_Area200_nel_periodo}" )
        percentuale =  (totale_prelievi_Area200_nel_periodo/totale_prelievi_nel_periodo)*100
        st.subheader(f"% sul totale magazzino: {percentuale:.2f}%")
        st.markdown("---")

        #Heatmap Area 300 piano 1
        st.markdown("<a name='heatmap-Area300'></a>", unsafe_allow_html=True) #link per facilitare lo scorrimento
        st.header('Heatmap Area 300')
        totale_prelievi_Area300_nel_periodo = int(heatmap_Area300(updated_totale_ubicazioni_df,1))
        st.subheader(f"Totale prelievi Area 300 piano 1: {totale_prelievi_Area300_nel_periodo}" )
        percentuale =  (totale_prelievi_Area300_nel_periodo/totale_prelievi_nel_periodo)*100
        st.subheader(f"% sul totale magazzino: {percentuale:.2f}%")
        st.markdown("---")


         #Heatmap Area 400
        st.markdown("<a name='heatmap-Area400'></a>", unsafe_allow_html=True) #link per facilitare lo scorrimento
        st.header('Heatmap Area 400')
        totale_prelievi_Area400_nel_periodo = int(heatmap_Area400(updated_totale_ubicazioni_df))
        st.subheader(f"Totale prelievi Area 400: {totale_prelievi_Area400_nel_periodo}" )
        percentuale =  (totale_prelievi_Area400_nel_periodo/totale_prelievi_nel_periodo)*100
        st.subheader(f"% sul totale magazzino: {percentuale:.2f}%")
        st.markdown("---")
        
        # Chiama la funzione per calcolare la produttività per ordine a pallet
        productivity_df_per_order_pallet = calculate_productivity_per_order_pallet(filtered_df)
        st.header("Productivity Pallet")
        # Crea una tabella interattiva per visualizzare i risultati
        st.dataframe(productivity_df_per_order_pallet)
        # Bottone di download
        tab_1 = to_excel(productivity_df_per_order_pallet)
        st.download_button(label='📥 Download tabella',
                           data=tab_1,
                           file_name='dataframe.xlsx',
                           mime='application/vnd.ms-excel')
        st.markdown("---")
        
        # Chiama la funzione per calcolare la produttività per pick&pack
        productivity_df_per_order_pickpack = calculate_productivity_per_order_pickpack(filtered_df)
        st.header("Productivity Pick&pack")
        # Crea una tabella interattiva per visualizzare i risultati
        st.dataframe(productivity_df_per_order_pickpack)
        # Bottone di download
        tab_2 = to_excel(productivity_df_per_order_pickpack)
        st.download_button(label='📥 Download tabella',
                           data=tab_2,
                           file_name='dataframe.xlsx',
                           mime='application/vnd.ms-excel')
        st.markdown("---")





if __name__ == "__main__":
    main()
