import streamlit as st
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection

#@st.cache_data

conn = st.connection("gsheets",type = GSheetsConnection)
df = conn.read(spreadsheet=st.secrets['spreadsheet'])
df["ingredienti"] = df["ingredienti"].apply(
    lambda x: [i.strip() for i in x.split(",")]
)
df = df[df.disponibile=='S']
df
df['categoria'] = np.where(df.categoria=='C','Caffè',
                np.where(df.categoria=='T','Tisane e Tè',
                np.where(df.categoria=='A','Amari',
                np.where(df.categoria=='B','Bevande fredde',
                df.categoria))))


st.title("☕ Menu Caffetteria")

ingrediente_filtro = st.text_input(
    "🔍 Filtra per ingrediente (es. zenzero)"
)
senza_caffeina = st.toggle('Senza caffeina')

df_filtrato = df.copy()

if ingrediente_filtro:
    df_filtrato = df_filtrato[
        df_filtrato["ingredienti"].apply(
            lambda ingr: ingrediente_filtro.lower() in [i.lower() for i in ingr]
        )
    ]
if senza_caffeina:
    df_filtrato = df_filtrato[df_filtrato["caffeina"]=='N']

categorie = sorted(df["categoria"].unique())


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
            prodotti_categoria["nome"].tolist(),
            label_visibility="collapsed"
        )

        prodotto = prodotti_categoria[
            prodotti_categoria["nome"] == prodotto_selezionato
        ].iloc[0]

        st.divider()
        st.markdown(f"## {prodotto['nome']}")
        st.write(f"**Descrizione:** {prodotto['descrizione']}")
        st.write(f"**Ingredienti:** {', '.join(prodotto['ingredienti'])}")