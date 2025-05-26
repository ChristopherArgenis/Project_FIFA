import streamlit as st
import pandas as pd

@st.cache_data
def f_distribucion_edad(df):
    return df["age"].value_counts().sort_index()

@st.cache_data
def f_altura_promedio(df):
    return df.groupby("club_position")["height_cm"].mean().dropna()

@st.cache_data
def valor_vs_salario(df):
    df_val = df[["short_name", "value_eur", "wage_eur"]].dropna()
    df_val = df_val.sort_values(by="value_eur", ascending=False).head(20)
    df_val["salario_anual"] = df_val["wage_eur"] * 52
    return df_val.set_index("short_name")[["value_eur", "salario_anual"]]

@st.cache_data
def media_metricas_generales(df):
    columnas = ["overall", "potential", "pace", "shooting", "passing", "dribbling", "defending", "physic"]
    return df[columnas].mean().sort_values(ascending=False)

def seccion_graficas(df):
    st.header("📊 Gráficas de Jugadores")

    # Graficas en Expander para mejor visualizazion
    with st.expander("Distribución de Edad", expanded=False):
        distribucion_edad = f_distribucion_edad(df)
        st.bar_chart(distribucion_edad)

    with st.expander("Altura Promedio por Posición", expanded=False):
        altura_promedio = f_altura_promedio(df)
        st.bar_chart(altura_promedio)

    with st.expander("Top 20: Salario Anual vs Valuación", expanded=False):
        valor_salario = valor_vs_salario(df)
        st.line_chart(valor_salario)

    with st.expander("Media de Métricas Generales", expanded=False):
        medias = media_metricas_generales(df)
        st.bar_chart(medias)