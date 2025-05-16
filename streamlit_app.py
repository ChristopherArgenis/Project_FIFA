import streamlit as st
import pandas as pd

# Lectura del Dataframe
@st.cache_data
def cargar_datos(year):
    return pd.read_csv(f"df_players_{year}.csv")

# Header
st.title("Panel de Jugadores de la FIFA ⚽")

# Sidebar
st.sidebar.header("Navegación")
years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
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

def main_content(df, indice_actual):
  tab1, tab2, tab3, tab4 = st.tabs(["Jugador", "Comparador", "Tops", "Preguntas"])
  with tab1:
    # search = st.text_input("Buscar jugadores por alias:")
    indice = f"Indice de Jugador: {indice_actual}"
    st.badge(indice)
    data_player, metric_player = st.columns(2)
    with data_player:
        player = df.iloc[indice_actual]
        st.image(player["player_face_url"], width=300, caption="Fotografia del Jugador")
        st.write("Nombre Completo")
        st.subheader(player["long_name"])
        st.write("Alias")
        st.subheader(player["short_name"])
        st.write("Nacionalidad")
        st.subheader(player["nationality_name"])
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("Edad")
            st.subheader(player["age"])
        with col2:
            st.write("Altura (cm)")
            st.subheader(player["height_cm"])
        with col3:
            st.write("Peso (kg)")
            st.subheader(player["weight_kg"])
    with metric_player:
        st.metric("Nombre del Club", value=player["club_name"])
        col1, col2 = st.columns(2)
        col1.metric("Posición", value=player["club_position"])
        col1.metric("Salario Anual", value=int(player["wage_eur"]))
        col2.metric("Número", value=int(player["club_jersey_number"]))
        col2.image(player["club_logo_url"], width=75)
        st.metric("Valuación", value=int(player["value_eur"]))
        st.divider()
        st.button("Anterior Jugador", on_click=anterior_jugador)
        st.button("Siguiente Jugador", on_click=siguiente_jugador)

with st.spinner("Cargando datos..."):
    df = cargar_datos(seleccion)

# Mostrar la información del jugador actual
indice_actual = st.session_state['jugador_actual_index']
main_content(df, indice_actual)
