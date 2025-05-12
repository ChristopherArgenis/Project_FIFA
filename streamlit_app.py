import streamlit as st
import pandas as pd

df_players_15 = pd.DataFrame("players_15.csv")

st.title("Panel de Jugadores de la FIFA ⚽")
st.sidebar.header("Navegación")
st.dataframe(df_players_15)
