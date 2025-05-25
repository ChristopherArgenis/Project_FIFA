import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos(year):
    return pd.read_csv(f"df_players_{year[2:]}.csv")

@st.cache_data
def obtener_clubes_y_nacionalidades(df):
    clubes = sorted(df["club_name"].dropna().unique())
    nacionalidades = sorted(df["nationality_name"].dropna().unique())
    return clubes, nacionalidades

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

def is_nulo(valor, texto_si_nulo=" "):
    if pd.isna(valor):
        return texto_si_nulo
    return int(valor)

def datosJugador(player):
    st.subheader(player["long_name"])
    st.metric("Alias", value=player["short_name"])
    st.metric("Nacionalidad", value=player["nationality_name"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Edad", value=player["age"])
    col2.metric("Altura (cm)", value=player["height_cm"])
    col3.metric("Peso (kg)", value=player["weight_kg"])
    st.button("Anterior Jugador", on_click=lambda: cambiar_jugador(-1))

def metricasJugador(player):
    st.metric("Nombre del Club", value=player["club_name"])
    col1, col2 = st.columns(2)
    col1.metric("Posición", value=player["club_position"])
    col1.metric("Salario Anual", value=formato(player["wage_eur"], True))
    col1.metric("Valuación", value=formato(player["value_eur"], False))
    col2.metric("Número", value=int(player["club_jersey_number"]))
    col2.image(player["club_logo_url"], width=75)
    col2.metric("Pie Preferente", value=player["preferred_foot"])
    st.button("Siguiente Jugador", on_click=lambda: cambiar_jugador(1))

def metricas_avanzadas_jugador(player):
    st.subheader("📊 Métricas Avanzadas")

    metricas = [
        "overall", "potential", "pace", "shooting", 
        "passing", "dribbling", "defending", "physic"
    ]
    habilidades = [
        "skill_dribbling", "skill_curve", "skill_ball_control",
        "movement_agility", "movement_reactions", 
        "power_shot_power", "power_jumping"
    ]

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.markdown("**🧠 Métricas Generales**")
            for m in metricas[:len(metricas)//2]:
                valor = is_nulo(player.get(m), texto_si_nulo="No disponible")
                st.metric(label=m.replace("_", " ").capitalize(), value=valor)
        with subcol2:
            for m in metricas[len(metricas)//2:]:
                valor = is_nulo(player.get(m), texto_si_nulo="No disponible")
                st.metric(label=m.replace("_", " ").capitalize(), value=valor)

    with col_m2:
        subcol3, subcol4 = st.columns(2)
        with subcol3:
            st.markdown("**🎯 Habilidades Técnicas**")
            for h in habilidades[:len(habilidades)//2]:
                valor = is_nulo(player.get(h), texto_si_nulo="No disponible")
                st.metric(label=h.replace("_", " ").capitalize(), value=valor)
        with subcol4:
            for h in habilidades[len(habilidades)//2:]:
                valor = is_nulo(player.get(h), texto_si_nulo="No disponible")
                st.metric(label=h.replace("_", " ").capitalize(), value=valor)


def cambiar_jugador(delta):
    st.session_state['jugador_actual_index'] = (st.session_state['jugador_actual_index'] + delta) % st.session_state['limit']