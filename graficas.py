import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

@st.cache_data
def distribucion_edad(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["age"], bins=20, kde=True, color="skyblue", ax=ax)
    ax.set_title("Distribución de Edades")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Número de Jugadores")
    return fig

@st.cache_data
def jugadores_por_posicion(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    orden = df["player_positions"].value_counts().head(10)
    sns.barplot(x=orden.index, y=orden.values, palette="viridis", ax=ax)
    ax.set_title("Top Posiciones Más Comunes")
    ax.set_xlabel("Posición")
    ax.set_ylabel("Cantidad de Jugadores")
    plt.xticks(rotation=45)
    return fig

@st.cache_data
def correlacion_estadisticas(df):
    cols = ["pace", "shooting", "passing", "dribbling", "defending", "physic", "overall", "potential"]
    df_corr = df[cols].dropna()
    corr = df_corr.corr()
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlación entre Métricas")
    return fig

@st.cache_data
def dispersion_valor_vs_edad(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x="age", y="value_eur", data=df, hue="club_name", legend=False, palette="tab10", ax=ax)
    ax.set_title("Valor de Mercado vs Edad")
    ax.set_xlabel("Edad")
    ax.set_ylabel("Valor de Mercado (€)")
    return fig

def seccion_graficas(df):
    tabs = st.tabs(["Barras", "Dispersión", "Correlación"])

    with tabs[0]:  # Barras
        st.subheader("Distribución de Edades")
        fig1 = distribucion_edad(df)
        st.pyplot(fig1)

        st.subheader("Jugadores por Posición")
        fig2 = jugadores_por_posicion(df)
        st.pyplot(fig2)

    with tabs[1]:  # Dispersión
        st.subheader("Valor de Mercado vs Edad")
        fig3 = dispersion_valor_vs_edad(df)
        st.pyplot(fig3)

    with tabs[2]:  # Correlación
        st.subheader("Correlación entre Estadísticas")
        fig4 = correlacion_estadisticas(df)
        st.pyplot(fig4)