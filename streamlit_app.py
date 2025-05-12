import streamlit as st
import pandas as pd

st.title("Panel de Jugadores de la FIFA ⚽")
st.sidebar.header("Navegación")
opcion = st.sidebar.radio(
    "Selecciona una año:",
    ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
)
