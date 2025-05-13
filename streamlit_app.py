import streamlit as st
import pandas as pd

df_players_15 = pd.read_csv("df_players_15.csv")
nombres_jugadores = df_players_15['short_name'].tolist()

st.title("Panel de Jugadores de la FIFA ⚽")
st.sidebar.header("Navegación")
years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
seleccion = st.sidebar.selectbox("Selecciona un año:", years)

if seleccion == "2015":
  tab1, tab2 = st.tabs(["Jugador", "Comparador", "Tops", "Preguntas"])
  with tab1:
    search = st.text_input("Buscar jugadores por nombre:")
    col1, col2 = st.columns(2)
    col1.image(df_players_15["player_face_url"][0], width=300)
    col1.subheader("Nombre Completo:")
    col1.subheader(df_players_15["long_name"][0])
    col1.divider()
    col1.subheader("Alias:")
    col1.subheader(df_players_15["short_name"][0])
    col2.metric("Valor en Euros", value=int(df_players_15["value_eur"][0]))
