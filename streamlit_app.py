import streamlit as st
from general import cargar_datos, obtener_clubes_y_nacionalidades, datosJugador, metricasJugador, metricas_avanzadas_jugador, comparar_metricas, mostrar_tops, seccion_faq, seccion_curiosidades
from utils.graficas import seccion_graficas
from utils.trayetoria import seccion_trayectoria

st.set_page_config(page_title="FIFA App", page_icon="⚽")

# Sidebar de navegación
st.sidebar.title("Navegación")
seccion = st.sidebar.selectbox("Ir a sección:", ["Inicio", "Jugador", "Trayectoria", "Comparador", "Top Jugadores", "Gráficos", "Curiosidades", "Preguntas (FAQ)",])

# --- Secciones ---
if seccion == "Inicio":
    st.title("⚽ FIFA Player Dashboard")
    st.markdown("""
    Bienvenido al panel de análisis de jugadores de FIFA.
    
    Usa el menú de la izquierda para navegar entre:
    - Jugador individual
    - Comparador
    - Top Jugadores
    - Preguntas
    - Gráficos interactivos
    """)

elif seccion == "Jugador":

    st.subheader("🎮 Jugador Individual")

    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    col1, col2 = st.columns(2)
    year = col1.selectbox("Selecciona un año:", years)

    df = cargar_datos(year)
    clubes_disponibles, nacionalidades_disponibles = obtener_clubes_y_nacionalidades(df)

    if 'jugador_actual_index' not in st.session_state:
        st.session_state['jugador_actual_index'] = 0
    if 'limit' not in st.session_state or st.session_state['limit'] != len(df):
        st.session_state['limit'] = len(df)

    # Filtros
    filter1, filter2 = st.columns(2)
    club = filter1.selectbox("Filtrar por club:", ["Todos"] + clubes_disponibles)
    nacion = filter2.selectbox("Filtrar por nacionalidad:", ["Todos"] + nacionalidades_disponibles)

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
    st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="{player['player_face_url']}" width="300">
        <p><em>Fotografía del Jugador</em></p>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        datosJugador(player)
    with col2:
        metricasJugador(player)
    st.divider()
    metricas_avanzadas_jugador(player)

elif seccion == "Trayectoria":
    st.subheader("Trayecoria de Messi y Cristiano")

    # Llamas a la sección cuando sea la pestaña activa
    seccion_trayectoria()

elif seccion == "Comparador":
    st.subheader("🔍 Comparador de Jugadores")
    st.caption("Aquí podrás comparar varios jugadores entre sí.")

    # Filtrar por Año el DataFrame
    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    col1, col2 = st.columns(2)
    year = col1.selectbox("Selecciona un año:", years)
    df = cargar_datos(year)

    name_1, name_2 = st.columns(2)
    nombre_1 = name_1.text_input("Jugador 1")
    nombre_2 = name_2.text_input("Jugador 2")
    jugador_1 = df[df["long_name"].str.contains(nombre_1, case=False, na=False)].iloc[0] if nombre_1 and not df[df["long_name"].str.contains(nombre_1, case=False, na=False)].empty else None
    jugador_2 = df[df["long_name"].str.contains(nombre_2, case=False, na=False)].iloc[0] if nombre_2 and not df[df["long_name"].str.contains(nombre_2, case=False, na=False)].empty else None
    
    if jugador_1 is not None and jugador_2 is not None:
        comparar_metricas(jugador_1, jugador_2)
    else:
        st.info("Introduce los nombres de dos jugadores válidos para comparar.")

elif seccion == "Top Jugadores":
    st.subheader("🏆 Mejores Jugadores por Métrica")
    st.caption("Ranking de Mejores Jugadores por Métrica.")

    # Filtrar por Año el DataFrame
    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    col1, col2 = st.columns(2)
    year = col1.selectbox("Selecciona un año:", years)
    df = cargar_datos(year)

    mostrar_tops(df)

elif seccion == "Gráficos":
    st.title("📊 Gráficos Interactivos")
    st.caption("Visualizaciones interactivas de estadísticas de jugadores.")

    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    col1, col2 = st.columns(2)
    year = col1.selectbox("Selecciona un año:", years)
    df = cargar_datos(year)

    # Funcion englobando los graficos
    seccion_graficas(df)

elif seccion == "Curiosidades":
    st.header("📊 Curiosidades sobre los jugadores")
    # Filtrar por Año el DataFrame
    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    col1, col2 = st.columns(2)
    year = col1.selectbox("Selecciona un año:", years)
    df = cargar_datos(year)

    seccion_curiosidades(df)

elif seccion == "Preguntas (FAQ)":
    st.header("❓ Preguntas")
    st.info("Respuestas basadas en el dataset.")
    seccion_faq()