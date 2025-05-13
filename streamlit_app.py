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

# Función para avanzar al siguiente jugador
def anterior_jugador():
    st.session_state['jugador_actual_index'] -= 1
    if st.session_state['jugador_actual_index'] < 0:
        st.session_state['jugador_actual_index'] = 0  # Volver al inicio

# Mostrar la información del jugador actual
indice_actual = st.session_state['jugador_actual_index']

if seleccion == "2015":
  tab1, tab2, tab3, tab4 = st.tabs(["Jugador", "Comparador", "Tops", "Preguntas"])
  with tab1:
    search = st.text_input("Buscar jugadores por alias:")
    data_player, metric_player = st.columns(2)
    with data_player:
        st.image(df_players_15["player_face_url"][indice_actual], width=300, caption="Fotografia del Jugador")
        st.write("Nombre Completo")
        st.subheader(df_players_15["long_name"][indice_actual])
        st.write("Alias")
        st.subheader(df_players_15["short_name"][indice_actual])
        st.write("Nacionalidad")
        st.subheader(df_players_15["nationality_name"][indice_actual])
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Edad")
            st.subheader(df_players_15["age"][indice_actual])
        with col2:
            st.write("Altura (cm)")
            st.subheader(df_players_15["height_cm"][indice_actual])
        with col3:
            st.write("Peso (kg)")
            st.subheader(df_players_15["weight_kg"][indice_actual])
    with metric_player:
        st.metric("Valuación", value=int(df_players_15["value_eur"][indice_actual]))
        st.metric("Salario Anual", value=int(df_players_15["wage_eur"][indice_actual]))
        st.button("Anterior Jugador", on_click=anterior_jugador)
        st.button("Siguiente Jugador", on_click=siguiente_jugador)
