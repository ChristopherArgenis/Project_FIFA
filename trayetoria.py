import streamlit as st
import pandas as pd

def seleccionar_jugador():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        jugador = st.selectbox("Selecciona el Jugador", ["L. Messi", "Cristiano Ronaldo"])
    return jugador

def formato(valor, is_wage):
    if pd.isna(valor):
        return " "
    else:
        valor_numerico = str(int(valor * 52)) if is_wage else str(int(valor))
        match len(valor_numerico):
            case 9: return f"{valor_numerico[:3]} M"
            case 8: return f"{valor_numerico[:2]} M"
            case 7: return f"{valor_numerico[0]} M"
            case 6: return f"{valor_numerico[:3]} mil"
            case 5: return f"{valor_numerico[:2]} mil"
            case 4: return f"{valor_numerico[0]} mil"
            case _:  return valor_numerico

def obtener_tabla_resumen(df):
    # Agregar columna de año si no existe
    if "año" not in df.columns:
        df["año"] = list(range(2015, 2023))  # solo si ya se estableció como índice externo

    columnas_utiles = [
        "overall", "potential", "pace", "shooting", "passing", "dribbling",
        "defending", "physic", "value_eur", "wage_eur", "age", "height_cm", "weight_kg"
    ]

    # Validar columnas existentes
    columnas_existentes = [col for col in columnas_utiles if col in df.columns]

    # Solo columnas válidas + año
    df_filtrado = df[["año"] + columnas_existentes].copy()

    # Formatear valores monetarios
    if "value_eur" in df_filtrado.columns:
        df_filtrado["value_eur"] = df_filtrado["value_eur"].apply(lambda x: formato(x, is_wage=False))
    if "wage_eur" in df_filtrado.columns:
        df_filtrado["wage_eur"] = df_filtrado["wage_eur"].apply(lambda x: formato(x, is_wage=True))

    # Poner años como columnas
    df_filtrado.set_index("año", inplace=True)
    tabla = df_filtrado.T  # Transponer para que las métricas sean el índice

    return tabla

def seccion_trayectoria():
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