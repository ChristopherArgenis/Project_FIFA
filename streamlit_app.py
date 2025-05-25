import streamlit as st

st.set_page_config(page_title="FIFA App", page_icon="⚽")

st.title("⚽ FIFA Player Dashboard")
st.markdown("""
Bienvenido al panel de análisis de jugadores de FIFA.

Usa el menú de la izquierda para navegar entre secciones:
- Jugador individual
- Comparador
- Rankings (Tops)
- Respuestas a preguntas frecuentes
- Gráficos interactivos
""")

st.page_link("pages/Jugador.py", label="Jugador", icon="🎮")