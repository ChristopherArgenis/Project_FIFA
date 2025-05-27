import streamlit as st

def selector_jugador_trayectoria(jugadores):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        jugador = st.selectbox("Selecciona el Jugador", jugadores, index=0)
    return jugador

def tabla_resumen_anual(df, jugador):
    metricas = ["overall", "potential", "pace", "shooting", "passing", "dribbling", "defending", "physic"]
    
    # Filtrar por jugador
    df_jugador = df[df["short_name"] == jugador].copy()
    
    if df_jugador.empty:
        st.warning("No hay datos disponibles para este jugador.")
        return
    
    # Verificar que 'year' exista
    if "year" not in df_jugador.columns:
        st.error("La columna 'year' no está disponible en el conjunto de datos.")
        return
    
    # Crear tabla pivot
    tabla = df_jugador[["year"] + metricas].set_index("year").T
    tabla.columns = tabla.columns.astype(str)  # Asegura que los años sean string
    
    # Mostrar tabla
    st.subheader("Resumen de métricas por año")
    st.dataframe(tabla.style.format(precision=1))