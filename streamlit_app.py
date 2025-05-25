import streamlit as st
from utils import cargar_datos, obtener_clubes_y_nacionalidades, datosJugador, metricasJugador, metricas_avanzadas_jugador

st.set_page_config(page_title="FIFA App", page_icon="⚽")

# Sidebar de navegación
st.sidebar.title("Navegación")
seccion = st.sidebar.selectbox("Ir a sección:", ["Inicio", "Jugador", "Comparador", "Tops", "Preguntas", "Gráficos"])

# --- Secciones ---
if seccion == "Inicio":
    st.title("⚽ FIFA Player Dashboard")
    st.markdown("""
    Bienvenido al panel de análisis de jugadores de FIFA.
    
    Usa el menú de la izquierda para navegar entre:
    - Jugador individual
    - Comparador
    - Tops
    - Preguntas
    - Gráficos interactivos
    """)

elif seccion == "Jugador":

    st.title("🎮 Jugador Individual")

    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    year = st.selectbox("Selecciona un año:", years)

    df = cargar_datos(year)
    clubes_disponibles, nacionalidades_disponibles = obtener_clubes_y_nacionalidades(df)

    if 'jugador_actual_index' not in st.session_state:
        st.session_state['jugador_actual_index'] = 0
    if 'limit' not in st.session_state or st.session_state['limit'] != len(df):
        st.session_state['limit'] = len(df)

    # Filtros
    club = st.selectbox("Filtrar por club:", ["Todos"] + clubes_disponibles)
    nacion = st.selectbox("Filtrar por nacionalidad:", ["Todos"] + nacionalidades_disponibles)

    if club != "Todos":
        df = df[df["club_name"] == club]
    if nacion != "Todos":
        df = df[df["nationality_name"] == nacion]

    # Reiniciar índice si cambian los filtros
    if 'club_anterior' not in st.session_state: st.session_state['club_anterior'] = ""
    if 'nacion_anterior' not in st.session_state: st.session_state['nacion_anterior'] = ""
    if club != st.session_state['club_anterior'] or nacion != st.session_state['nacion_anterior']:
        st.session_state['jugador_actual_index'] = 0
        st.session_state['club_anterior'] = club
        st.session_state['nacion_anterior'] = nacion

    # Búsqueda
    busqueda = st.text_input("🔍 Buscar jugador por nombre o alias:")
    if busqueda:
        resultados = df[df["long_name"].str.contains(busqueda, case=False, na=False) |
                    df["short_name"].str.contains(busqueda, case=False, na=False)]
        if not resultados.empty:
            player = resultados.iloc[0]
            st.success(f"Jugador encontrado: {player['long_name']}")
        else:
            st.warning("No se encontró ningún jugador.")
            st.stop()
    else:
        if df.empty:
            st.warning("No hay jugadores para mostrar.")
            st.stop()
        player = df.iloc[st.session_state['jugador_actual_index'] % len(df)]
        st.badge(f"Índice actual: {st.session_state['jugador_actual_index'] % len(df)}")

    # Mostrar
    st.image(player["player_face_url"], width=300, caption="Fotografia del Jugador")
    col1, col2 = st.columns(2)
    with col1:
        datosJugador(player)
    with col2:
        metricasJugador(player)
    metricas_avanzadas_jugador(player)

elif seccion == "Comparador":
    st.title("🔍 Comparador de Jugadores")
    st.info("Aquí podrás comparar varios jugadores entre sí (en construcción).")

elif seccion == "Tops":
    st.title("🏆 Top Jugadores")
    st.info("Ranking de mejores jugadores por posición o atributo.")

elif seccion == "Preguntas":
    st.title("❓ Preguntas Frecuentes")
    st.info("Respuestas automáticas basadas en el dataset.")

elif seccion == "Gráficos":
    st.title("📊 Gráficos Interactivos")
    st.info("Visualizaciones interactivas de estadísticas de jugadores.")