import streamlit as st
import pandas as pd

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
        df["año"] = list(range(2015, 2023))

    columnas_utiles = [
         "age", "value_eur", "wage_eur", "overall", "potential", 
         "pace", "shooting", "passing", "dribbling", "defending", "physic"
    ]

    traduccion_metricas = {
        "age": "Edad",
        "value_eur": "Valor (€)",
        "wage_eur": "Salario Anual (€)",
        "overall": "Media General",
        "potential": "Potencial",
        "pace": "Ritmo",
        "shooting": "Disparo",
        "passing": "Pase",
        "dribbling": "Regate",
        "defending": "Defensa",
        "physic": "Físico"
    }

    # Validar columnas existentes
    columnas_existentes = [col for col in columnas_utiles if col in df.columns]
    df_filtrado = df[["año"] + columnas_existentes].copy()

    # Formatear monetarios
    if "value_eur" in df_filtrado.columns:
        df_filtrado["value_eur"] = df_filtrado["value_eur"].apply(lambda x: formato(x, is_wage=False))
    if "wage_eur" in df_filtrado.columns:
        df_filtrado["wage_eur"] = df_filtrado["wage_eur"].apply(lambda x: formato(x, is_wage=True))

    # Redondear a enteros los demás datos numéricos
    for col in columnas_existentes:
        if col not in ["value_eur", "wage_eur"]:
            df_filtrado[col] = df_filtrado[col].apply(lambda x: int(x) if pd.notna(x) else x)

    # Establecer años como columnas
    df_filtrado.set_index("año", inplace=True)
    tabla = df_filtrado.T  # transponer: métricas = filas, columnas = años

    # Traducir nombres de métricas
    tabla.index = [traduccion_metricas.get(metric, metric) for metric in tabla.index]

    return tabla

def seccion_trayectoria(jugador_seleccionado):
    # 1. Obtener dataframe según jugador - Preprocesamiento previo con pandas
    df_messi = pd.read_csv("messi_trayectoria.csv")
    df_cristiano = pd.read_csv("cristiano_trayectoria.csv")
    df = df_messi if jugador_seleccionado == "L. Messi" else df_cristiano

    # 2. Mostrar tabla resumen
    st.subheader("Resumen de Métricas por Año")
    tabla = obtener_tabla_resumen(df)
    st.dataframe(tabla)

# Este archivo debe usarse dentro del contexto del selectbox y los datos ya procesados
# Supone que df_jugador es el DataFrame del jugador seleccionado (Messi o Cristiano)

def graficas_evolucion(nombre_jugador):
    st.subheader(f"Gráficas de Trayectoria")

    tabs = st.tabs(["Evolución General", "Valor Económico", "Técnicas Año a Año", "Radar (próximamente)"])

    df_messi = pd.read_csv("messi_trayectoria.csv")
    df_cristiano = pd.read_csv("cristiano_trayectoria.csv")
    df_jugador = df_messi if nombre_jugador == "L. Messi" else df_cristiano

    df_jugador["año"] = list(range(2015, 2023))
    df_jugador = df_jugador.set_index("año")

    # --- Tab 1: Evolución General ---
    with tabs[0]:
        st.markdown("### Evolución General")
        metricas_disponibles = ["overall", "potential", "pace", "shooting", "passing", "dribbling", "defending", "physic"]
        seleccionadas = st.multiselect("Selecciona las métricas a visualizar:", options=metricas_disponibles, default=["overall", "potential"])

        if seleccionadas:
            st.line_chart(df_jugador[seleccionadas])

    # --- Tab 2: Valor Económico ---
    with tabs[1]:
        st.markdown("### Valor Económico")
        valores = df_jugador[["value_eur", "wage_eur"]]
        st.line_chart(valores)

    # --- Tab 3: Técnicas Año a Año ---
    with tabs[2]:
        st.markdown("### Atributos Técnicos")
        mostrar_tecnicos = st.checkbox("Mostrar atributos técnicos", value=True)

        if mostrar_tecnicos:
            metricas_tecnicas = ["pace", "shooting", "passing", "dribbling", "defending", "physic"]
            st.line_chart(df_jugador[metricas_tecnicas])

    # --- Tab 4: Radar Chart (placeholder) ---
    with tabs[3]:
        st.info("Gráfico radar en desarrollo. Estará disponible próximamente.")
