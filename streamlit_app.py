import streamlit as st
import pandas as pd

df_players_15 = pd.read_csv("df_players_15.csv")
nombres_jugadores = df_players_15['short_name'].tolist()

st.title("Panel de Jugadores de la FIFA ⚽")
st.sidebar.header("Navegación")
years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
seleccion = st.sidebar.selectbox("Selecciona un año:", years)

# Inicializar el contador del índice del jugador en la sesión
if 'jugador_actual_index' not in st.session_state:
    st.session_state['jugador_actual_index'] = 0

# Función para avanzar al siguiente jugador
def siguiente_jugador():
    st.session_state['jugador_actual_index'] += 1
    if st.session_state['jugador_actual_index'] >= len(df_players_15):
        st.session_state['jugador_actual_index'] = 0  # Volver al inicio

# Mostrar la información del jugador actual
indice_actual = st.session_state['jugador_actual_index']

if seleccion == "2015":
  tab1, tab2, tab3, tab4 = st.tabs(["Jugador", "Comparador", "Tops", "Preguntas"])
  with tab1:
    search = st.text_input("Buscar jugadores por nombre:")
    col1, col2 = st.columns(2)
    col1.image(df_players_15["player_face_url"][indice_actual], width=300)
    col1.subheader("Nombre Completo:")
    col1.subheader(df_players_15["long_name"][indice_actual])
    col1.divider()
    col1.subheader("Alias:")
    col1.subheader(df_players_15["short_name"][indice_actual])
    col2.metric("Valor en Euros", value=int(df_players_15["value_eur"][indice_actual]))
    col2.button("Siguiente Jugador", on_click=siguiente_jugador)
