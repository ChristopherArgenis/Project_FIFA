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

def traducir_pie_preferente(valor):
    if isinstance(valor, str):
        if valor.lower() == "left":
            return "Izquierda"
        elif valor.lower() == "right":
            return "Derecha"
    return "Desconocido"

# Jugador

def datosJugador(player):
    st.empty()
    st.metric("Nombre Completo", value=player["long_name"])
    st.metric("Alias", value=player["short_name"])
    st.metric("Nacionalidad", value=player["nationality_name"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Edad", value=player["age"])
    col2.metric("Altura (cm)", value=player["height_cm"])
    col3.metric("Peso (kg)", value=player["weight_kg"])

def metricasJugador(player):
    st.metric("Nombre del Club", value=player["club_name"])
    col1, col2 = st.columns(2)
    col1.metric("Posición", value=player["club_position"])
    col1.metric("Salario Anual", value=formato(player["wage_eur"], True))
    col1.metric("Valuación", value=formato(player["value_eur"], False))
    col2.metric("Número", value=int(player["club_jersey_number"]))
    col2.image(player["club_logo_url"], width=75)
    col2.metric("Pie Preferente", value=traducir_pie_preferente(player["preferred_foot"]))

def metricas_avanzadas_jugador(player):
    st.subheader("📊 Métricas Avanzadas")

    col_m1, col_m2 = st.columns(2)

    # --- Métricas Generales ---
    with col_m1:
        st.markdown("**🧠 Métricas Generales**")
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.metric("General", value=is_nulo(player.get("overall"), " "))
            st.metric("Potencial", value=is_nulo(player.get("potential"), " "))
            st.metric("Ritmo", value=is_nulo(player.get("pace"), " "))
            st.metric("Tiro", value=is_nulo(player.get("shooting"), " "))
        with subcol2:
            st.metric("Fisico", value=is_nulo(player.get("physic"), " "))
            st.metric("Pase", value=is_nulo(player.get("passing"), " "))
            st.metric("Regate", value=is_nulo(player.get("dribbling"), " "))
            st.metric("Defensa", value=is_nulo(player.get("defending"), " "))
        st.button("Anterior Jugador", on_click=lambda: cambiar_jugador(-1))
    # --- Habilidades Técnicas ---
    with col_m2:
        st.markdown("**🎯 Habilidades Técnicas**")
        subcol3, subcol4 = st.columns(2)
        with subcol3:
            st.metric("Dribbling", value=player.get("skill_dribbling"))
            st.metric("Efecto", value=player.get("skill_curve"))
            st.metric("Control de Balón", value=player.get("skill_ball_control"))
            st.metric("Agilidad", value=player.get("movement_agility"))
        with subcol4:
            st.metric("Reacciones", value=player.get("movement_reactions"))
            st.metric("Potencia de Tiro", value=player.get("power_shot_power"))
            st.metric("Salto", value=player.get("power_jumping"))
        st.button("Siguiente Jugador", on_click=lambda: cambiar_jugador(1))

# Comparador

def mostrar_jugador_comparador(player):
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="{player['player_face_url']}" width="150">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.subheader(player["long_name"])
    st.caption(player["short_name"])

def comparar_metricas(j1, j2):
    metricas_generales = ["overall", "potential", "pace", "shooting", 
                          "passing", "dribbling", "defending", "physic"]
    metricas_habilidades = ["skill_dribbling", "skill_curve", "skill_ball_control",
                            "movement_agility", "movement_reactions", "power_shot_power", "power_jumping"]
    traduccion = {
    "overall": "General",
    "potential": "Potencial",
    "pace": "Ritmo",
    "shooting": "Tiro",
    "passing": "Pase",
    "dribbling": "Regate",
    "defending": "Defensa",
    "physic": "Físico",
    "skill_dribbling": "Regate (Habilidad)",
    "skill_curve": "Efecto",
    "skill_ball_control": "Control de balón",
    "movement_agility": "Agilidad",
    "movement_reactions": "Reacciones",
    "power_shot_power": "Potencia de tiro",
    "power_jumping": "Salto" }

    col1, col2 = st.columns(2)

    with col1:
        mostrar_jugador_comparador(j1)
    with col2:
        mostrar_jugador_comparador(j2)

    st.markdown("---")
    st.markdown("### Métricas Generales 🧠")

    for metrica in metricas_generales:
        v1 = j1[metrica]
        v2 = j2[metrica]

        col1, col2 = st.columns(2)

        label_es = traduccion.get(metrica, metrica)

        if pd.notna(v1) and pd.notna(v2):
            delta1 = int(v1) - int(v2)
            delta2 = int(v2) - int(v1)

            with col1:
                st.metric(label=label_es, value=int(v1), delta=f"{delta1:+}", delta_color="normal")
            with col2:
                st.metric(label=label_es, value=int(v2), delta=f"{delta2:+}", delta_color="normal")
        else:
            with col1:
                st.metric(label=label_es, value="No aplica")
            with col2:
                st.metric(label=label_es, value="No aplica")

    st.markdown("---")
    st.markdown("### Habilidades Técnicas 🎯")

    for metrica in metricas_habilidades:
        v1 = j1[metrica]
        v2 = j2[metrica]

        col1, col2 = st.columns(2)

        label_es = traduccion.get(metrica, metrica)

        if pd.notna(v1) and pd.notna(v2):
            delta1 = int(v1) - int(v2)
            delta2 = int(v2) - int(v1)

            with col1:
                st.metric(label=label_es, value=int(v1), delta=f"{delta1:+}", delta_color="normal")
            with col2:
                st.metric(label=label_es, value=int(v2), delta=f"{delta2:+}", delta_color="normal")
        else:
            with col1:
                st.metric(label=label_es, value="No aplica")
            with col2:
                st.metric(label=label_es, value="No aplica")

# Tops

def mostrar_tops(df):
    st.divider()

    # --- Filtros ---
    col1, col2, col3 = st.columns(3)

    clubes, nacionalidades = obtener_clubes_y_nacionalidades(df)
    with col1:
        nacionalidad = st.selectbox("Filtrar por Nacionalidad", ["Todas"] + nacionalidades)
    with col2:
        club = st.selectbox("Filtrar por Club", ["Todos"] + clubes)
    with col3:
        posicion = st.selectbox("Filtrar por Posición", ["Todas"] + sorted(df["club_position"].dropna().unique()))

    if nacionalidad != "Todas":
        df = df[df["nationality_name"] == nacionalidad]
    if club != "Todos":
        df = df[df["club_name"] == club]
    if posicion != "Todas":
        df = df[df["club_position"] == posicion]

    # --- Métricas disponibles y traducción ---
    metricas = {
        "overall": "General",
        "potential": "Potencial",
        "pace": "Ritmo",
        "shooting": "Tiro",
        "passing": "Pase",
        "dribbling": "Regate",
        "defending": "Defensa",
        "physic": "Físico",
        "skill_dribbling": "Habilidad Regate",
        "skill_curve": "Efecto",
        "skill_ball_control": "Control de Balón",
        "movement_agility": "Agilidad",
        "movement_reactions": "Reacciones",
        "power_shot_power": "Potencia de Tiro",
        "power_jumping": "Salto",
        "wage_eur": "Salario Anual",
        "value_eur": "Valuación",
        "height_cm": "Altura (cm)"
    }

    metrica_traducida = st.selectbox("Selecciona una métrica para ver el Top", list(metricas.values()))
    metrica_seleccionada = [k for k, v in metricas.items() if v == metrica_traducida][0]

    # Opción de visualización
    vista = st.radio("¿Cómo deseas ver el Top?", ["Tarjetas", "Tabla"], horizontal=True)

    # Cantidad (solo si es tabla)
    cantidad = 10
    if vista == "Tabla":
        cantidad = st.selectbox("Cantidad de jugadores a mostrar", [10, 25, 50, 100])

    # Preparar top
    df_top = df.copy()
    df_top = df_top[df_top[metrica_seleccionada].notna()]
    df_top = df_top.sort_values(by=metrica_seleccionada, ascending=False).head(cantidad)

    # Determinar si se debe aplicar formato
    aplicar_formato = metrica_seleccionada in ["value_eur", "wage_eur"]
    is_wage = metrica_seleccionada == "wage_eur"

    # Visualización seleccionada
    if vista == "Tabla":
        st.subheader("📋 Tabla del Top 10")
        valores = [
            formato(valor, is_wage) if aplicar_formato else int(valor)
            for valor in df_top[metrica_seleccionada]
        ]
        # Nuevo Dataframe formateado
        df_tabla = pd.DataFrame({
            "Nombre": df_top["long_name"],
            "Club": df_top["club_name"],
            "Nacionalidad": df_top["nationality_name"],
            metrica_traducida: valores
        })
        df_tabla.index = range(1, len(df_tabla) + 1)
        st.dataframe(df_tabla, use_container_width=True)
    else:
        st.subheader("📸 Tarjetas de Jugadores")
        for _, jugador in df_top.iterrows():
            valor = jugador[metrica_seleccionada]
            valor_mostrar = formato(valor, is_wage) if aplicar_formato else int(valor)
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(jugador["player_face_url"], width=300)
                with col2:
                    st.subheader(jugador["long_name"])
                    st.caption(f"{jugador['nationality_name']} | {jugador['club_name']} | {jugador['club_position']}")
                    st.metric(label=metrica_traducida, value=valor_mostrar)

def cambiar_jugador(delta):
    st.session_state['jugador_actual_index'] = (st.session_state['jugador_actual_index'] + delta) % st.session_state['limit']