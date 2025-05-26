import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def radar_chart_jugador(player):
    st.markdown("## 🕸️ Perfil de Habilidades del Jugador")

    # Definir métricas a comparar
    categorias = ["pace", "shooting", "passing", "dribbling", "defending", "physic"]
    etiquetas = ["Ritmo", "Tiro", "Pase", "Regate", "Defensa", "Físico"]

    # Extraer los valores del jugador
    valores = [player[c] if not pd.isna(player[c]) else 0 for c in categorias]

    # Cerrar el círculo del radar
    valores += valores[:1]
    etiquetas += etiquetas[:1]

    # Ángulos para el radar
    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    angulos += angulos[:1]

    # Estilo del gráfico
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores, color='blue', linewidth=2)
    ax.fill(angulos, valores, color='blue', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas)
    ax.set_title(player["short_name"], size=16, weight='bold', y=1.1)

    st.pyplot(fig)

def filtrar_jugador_por_nombre(df, nombre):
    return df[df["short_name"].str.lower().str.contains(nombre.lower())]

def jugador_valido_para_radar(player):
    metricas = ["pace", "shooting", "passing", "dribbling", "defending", "physic"]
    return all(m in player and not pd.isna(player[m]) for m in metricas)

def mostrar_radar_para_jugador(df, nombre_jugador):
    if not nombre_jugador:
        return

    jugadores_filtrados = filtrar_jugador_por_nombre(df, nombre_jugador)

    if jugadores_filtrados.empty:
        st.error("No se encontró ningún jugador con ese nombre.")
        return

    player = jugadores_filtrados.iloc[0]

    if jugador_valido_para_radar(player):
        radar_chart_jugador(player)
    else:
        st.warning("Este jugador no tiene suficientes datos para mostrar el gráfico radar.")