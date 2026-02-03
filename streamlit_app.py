import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection

@st.cache_data
def load_data():
    conn = st.connection("gsheets",type = GSheetsConnection)
    df = conn.read(spreadsheet=st.secrets['spreadsheet'])
    return df

if st.sidebar.button("🔄 Aggiorna il menu"):
    load_data.clear()
    st.rerun()

df = load_data()
df["ingredienti"] = df["ingredienti"].apply(
    lambda x: [i.strip() for i in x.split(",")]
)
df = df[df.disponibile=='S']


st.title("☕ Menu Caffetteria")

lista_ingredienti_unici = df["ingredienti"].explode().sort_values().unique().tolist()
opzioni_ingredienti = st.multiselect(
    "🔍 Ti piacerebbe sentire qualcosa in particolare?",
    lista_ingredienti_unici,
    placeholder="Scegli i tuoi ingredienti preferiti...",
)
senza_caffeina = st.toggle('Senza caffeina')

df_filtrato = df.copy()
if opzioni_ingredienti:
    df_filtrato = df_filtrato[
        df_filtrato["ingredienti"].apply(
            lambda ingr: all(i in ingr for i in opzioni_ingredienti)
        )
    ]
if senza_caffeina:
    df_filtrato = df_filtrato[df_filtrato["caffeina"]=='N']

categorie = sorted(df_filtrato["categoria"].unique())

try:
    tabs = st.tabs(categorie)
    for tab, categoria in zip(tabs, categorie):
        with tab:
            prodotti_categoria = df_filtrato[
                df_filtrato["categoria"] == categoria
            ]

            if prodotti_categoria.empty:
                st.info("Nessun prodotto disponibile")
                continue

            prodotto_selezionato = st.radio(
                "Seleziona un prodotto",
                sorted(prodotti_categoria["nome"].tolist()),
                label_visibility="collapsed"
            )

            prodotto = prodotti_categoria[
                prodotti_categoria["nome"] == prodotto_selezionato
            ].iloc[0]

            st.divider()
            st.markdown(f"## {prodotto['nome']}")
            st.write(f"**Descrizione:** {prodotto['descrizione']}")
            st.write(f"**Ingredienti:** {', '.join(prodotto['ingredienti'])}")
except:
    st.warning('Non ci sono prodotti disponibili con queste combinazioni di ingredienti! Ritenta :)', icon="⚠️")