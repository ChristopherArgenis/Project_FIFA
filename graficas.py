import streamlit as st
import pandas as pd

@st.cache_data
def f_distribucion_edad(df, column="age"):
    return df[column].value_counts().sort_index()

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
    tabs = st.tabs(["Barras", "Dispersión", "Correlación"])

    # Distribuciones
    with tabs[0]: 
        medidas_list = ["age", "height_cm", "weight_kg", "preferred_foot", "club_position"]
        medida = st.selectbox("Elige la medida", medidas_list)
        st.subheader(f"Distribución de {medida}")
        distribucion_edad = f_distribucion_edad(df, medida)
        st.bar_chart(distribucion_edad)

    with tabs[1]:
        st.subheader("Top 20: Salario Anual vs Valuación")
        valor_salario = valor_vs_salario(df)
        st.line_chart(valor_salario)

    with tabs[2]:
        st.subheader("Media de Métricas Generales")
        medias = media_metricas_generales(df)
        st.bar_chart(medias)