import streamlit as st
import pandas as pd

def seleccionar_jugador():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        jugador = st.selectbox("Selecciona el Jugador", ["L. Messi", "Cristiano Ronaldo"])
    return jugador

def obtener_tabla_resumen(df):
    # Filtrar columnas numéricas útiles para el resumen
    columnas_utiles = [
        "overall", "potential", "pace", "shooting", "passing", "dribbling", "defending", "physic",
        "value_eur", "wage_eur", "age", "height_cm", "weight_kg"
    ]
    
    # Verificamos qué columnas existen realmente
    columnas_existentes = [col for col in columnas_utiles if col in df.columns]

    # Añadir la columna de año como index si no está
    if "año" in df.columns:
        df.set_index("año", inplace=True)

    # Transponer: índice = métricas, columnas = años
    tabla = df[columnas_existentes].T
    return tabla

def seccion_trayectoria():
    st.title("📈 Trayectoria del Jugador")

    # 1. Selección
    jugador_seleccionado = seleccionar_jugador()

    # 2. Obtener dataframe según jugador - Preprocesamiento previo con pandas
    df_messi = pd.read_csv("messi_trayectoria.csv")
    df_cristiano = pd.read_csv("cristiano_trayectoria.csv")
    df = df_messi if jugador_seleccionado == "L. Messi" else df_cristiano

    # 3. Mostrar tabla resumen
    st.subheader("Resumen de Métricas por Año")
    tabla = obtener_tabla_resumen(df)
    st.dataframe(tabla)