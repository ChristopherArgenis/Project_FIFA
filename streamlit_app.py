import streamlit as st
import pandas as pd

# Mejor uso solo en Ordenador o Laptop
# st.set_page_config(layout="wide")

# Lectura del Dataframe
@st.cache_data
def cargar_datos(year):
    return pd.read_csv(f"df_players_{year[2:]}.csv")

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
    limit = st.session_state['limit']
    st.session_state['jugador_actual_index'] += 1
    if st.session_state['jugador_actual_index'] >= limit:
        st.session_state['jugador_actual_index'] = 0  # Volver al inicio

# Función para avanzar al siguiente jugador
def anterior_jugador():
    if st.session_state['jugador_actual_index'] > 0:
        st.session_state['jugador_actual_index'] -= 1
    else:
        st.session_state['jugador_actual_index'] = st.session_state['limit'] - 1  # Último jugador

def formato(valor, is_wage):
    valor_numerico = str(int(valor * 52)) if is_wage else str(int(valor))
    if len(valor_numerico) > 6:
        return f"{numerico[:3]} M"
    else:
        return f"{numerico[:3]} mil"

def Jugador(df, indice):
    player = df.iloc[indice_actual]
    # search = st.text_input("Buscar jugadores por alias:")
    indice = f"Indice de Jugador: {indice_actual}"
    st.badge(indice)
    data_player, metric_player = st.columns(2)
    with data_player:
        st.image(player["player_face_url"], width=300, caption="Fotografia del Jugador")
        st.write("Nombre Completo")
        st.subheader(player["long_name"])
        st.metric("Alias", value=player["short_name"])
        st.metric("Nacionalidad", value=player["nationality_name"])
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Edad", value=player["age"])
        with col2:
            st.metric("Altura (cm)", value=player["height_cm"])
        with col3:
            st.metric("Peso (kg)", value=player["weight_kg"])
        st.divider()
        st.button("Anterior Jugador", on_click=anterior_jugador)
    with metric_player:
        st.metric("Nombre del Club", value=player["club_name"])
        col1, col2 = st.columns(2)
        col1.metric("Posición", value=player["club_position"])
        col1.metric("Salario Anual", value=formato(player["wage_eur"], True))
        col2.metric("Número", value=int(player["club_jersey_number"]))
        col2.image(player["club_logo_url"], width=75)
        st.metric("Valuación", value=formato(player["value_eur"], False))
        st.divider()
        skill, potential = st.columns(2)
        with skill:
            st.metric("Habilidad General", value=int(player["overall"]))
            st.metric("Pie Preferente", value=player["preferred_foot"])
        with potential:
            st.metric("Potencial", value=int(player["potential"]))
            st.metric("Nivel Fisico", value=int(player["physic"]))
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tiro", value=int(player["shooting"]))
        with col2:
            st.metric("Pase", value=int(player["passing"]))
        with col3:
            st.metric("Defensa", value=int(player["defending"]))
        st.divider()
        st.button("Siguiente Jugador", on_click=siguiente_jugador)

def main_content(df, indice_actual):
  jugador, comparador, tops, preguntas, graficos = st.tabs(["Jugador", "Comparador", "Tops", "Preguntas", "Graficos"])
  with jugador:
    Jugador(df, indice_actual)
  with comparador:
    st.write("Comparador")
  with tops:
    st.write("Tops")
  with preguntas:
    st.write("Preguntas")
  with graficos:
    st.write("Graficos")

df = cargar_datos(seleccion)

# Validar el límite y el índice
if 'limit' not in st.session_state or st.session_state['limit'] != len(df):
    st.session_state['limit'] = len(df)
    st.session_state['jugador_actual_index'] = 0  # Reiniciar el índice si cambió el límite
    
# Mostrar la información del jugador actual
indice_actual = st.session_state['jugador_actual_index']
main_content(df, indice_actual)
