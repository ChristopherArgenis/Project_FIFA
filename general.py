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

def seccion_inicio():
    st.title("⚽ Football Analytics Hub")
    st.markdown("---")

    st.markdown("""
    ### Bienvenido al centro definitivo de análisis futbolístico 🎯

    Sumérgete en una experiencia interactiva diseñada para **fanáticos, analistas y amantes del fútbol**.
    Esta plataforma combina estadísticas detalladas, visualizaciones impactantes y comparativas inteligentes 
    para ofrecerte un recorrido completo por el universo del fútbol moderno.

    🔍 **¿Qué puedes hacer aquí?**

    - Explora más de mil jugadores con sus **estadísticas generales, técnicas y económicas**.
    - **Compara cara a cara** a tus futbolistas favoritos y descubre quién domina en cada métrica.
    - Consulta los **Top Rankings** por posición, nacionalidad, club, valor de mercado, salario, altura y mucho más.
    - Participa en **curiosidades, preguntas futboleras** y pronto... ¡en nuestros quizes!
    - Navega por gráficas exclusivas y descubre patrones que van más allá de los números.
    - Sumérgete en la **trayectoria histórica de Messi y Cristiano Ronaldo**, una rivalidad legendaria analizada como nunca antes.

    📊 Cada sección ha sido pensada para **impresionar a los apasionados**, facilitar el análisis a los expertos, 
    y sobre todo, **maravillar a quienes aman este deporte**.

    ---
    """)
    
    st.success("⚠ Consejo: Usa las pestañas, filtros y visualizaciones para personalizar tu experiencia.")
    st.markdown("👉 ¡Comienza a explorar en el menú de la izquierda!")

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

# Curiosidades
def seccion_curiosidades(df):
    with st.expander("Datos interesantes del dataset"):
        st.markdown("- ⚽ ¿Sabías que el jugador más alto mide más de **2 metros**?")
        st.markdown(f"- 💰 El jugador con **mayor valor de mercado** es: **{df.loc[df['value_eur'].idxmax(), 'short_name']}**")
        st.markdown(f"- 👶 El jugador más joven tiene apenas **{df['age'].min()} años**.")
        st.markdown(f"- 🏆 El país con más jugadores registrados es: **England**")
        st.markdown(f"- 🥾 El jugador con mejor 'Regate' es: **{df.loc[df['dribbling'].idxmax(), 'short_name']}** con {int(df['dribbling'].max())} puntos.")
        st.markdown(f"- 🚀 El más veloz tiene **{int(df['pace'].max())}** puntos de velocidad: **{df.loc[df['pace'].idxmax(), 'short_name']}**.")
        st.markdown(f"- 🧱 El defensor con mayor 'Defensa' tiene **{int(df['defending'].max())}**: **{df.loc[df['defending'].idxmax(), 'short_name']}**.")

    st.info("¡Descubre más en la sección de gráficas!")

# Preguntas (FAQ)
def seccion_faq():
    st.subheader("❓ Preguntas Frecuentes")

    with st.expander("¿Qué significa cada tipo de métrica?"):
        st.markdown("#### Métricas Generales")
        st.write("- **General (overall)**: Nivel actual del jugador.")
        st.write("- **Potencial (potential)**: Nivel máximo estimado del jugador.")
        st.write("- **Físico (physic)**: Fuerza y resistencia física.")
        st.write("- **Velocidad (pace)**: Aceleración y velocidad máxima.")

        st.markdown("#### Métricas Técnicas")
        st.write("- **Tiro (shooting)**: Capacidad para disparar a portería.")
        st.write("- **Pase (passing)**: Precisión y capacidad de pase.")
        st.write("- **Defensa (defending)**: Habilidad para recuperar y bloquear.")
        st.write("- **Regate (dribbling)**: Habilidad para controlar el balón en movimiento.")

        st.markdown("#### Métricas de Habilidad")
        st.write("- **Control de balón (skill_ball_control)**: Dominio general del balón.")
        st.write("- **Efecto (skill_curve)**: Precisión al curvar la pelota.")
        st.write("- **Habilidad de Regate (skill_dribbling)**: Capacidad para regatear.")
        st.write("- **Agilidad (movement_agility)**: Rapidez para cambiar de dirección.")
        st.write("- **Reacción (movement_reactions)**: Tiempo de respuesta a jugadas.")
        st.write("- **Potencia de tiro (power_shot_power)**: Fuerza en los disparos.")
        st.write("- **Salto (power_jumping)**: Capacidad para elevarse.")

    with st.expander("¿Qué es el 'Potencial' y cómo se diferencia del 'General'?"):
        st.write(
            "- **General** representa el nivel actual del jugador.\n"
            "- **Potencial** indica el nivel máximo que puede alcanzar, según una estimación."
        )

    with st.expander("¿Por qué algunos jugadores no tienen datos de ciertas métricas?"):
        st.write(
            "Algunas posiciones, como la de portero, no requieren ciertos atributos como "
            "pase, velocidad o regate, por lo que esos valores pueden estar vacíos o no aplican."
        )

    with st.expander("¿Qué representa el valor de mercado (valuación)?"):
        st.write(
            "Es una estimación del valor económico del jugador en el mercado de fichajes, "
            "basado en edad, habilidad y potencial. No es lo mismo que el salario."
        )

    with st.expander("¿Por qué un mismo jugador aparece en varios años?"):
        st.write(
            "Porque los datos corresponden a distintas ediciones, y muestran cómo "
            "evoluciona el rendimiento y el valor de un jugador a lo largo del tiempo."
        )

def cambiar_jugador(delta):
    st.session_state['jugador_actual_index'] = (st.session_state['jugador_actual_index'] + delta) % st.session_state['limit']

# Acerca de...
def seccion_acerca():
    st.header("📘 Acerca de esta Aplicación")
    st.markdown("---")
    st.markdown("""
    En esta sección encontrarás la **documentación técnica y explicativa** de todo el proceso detrás de esta plataforma. 
    Desde el análisis y transformación de datos hasta cómo se visualiza cada apartado.
    
    Cada expander a continuación detalla el **trabajo realizado en cada sección** de la app.
    """)

    with st.expander("📂 1. Carga y Preparación de Datos"):
        st.markdown("""
        - **Análisis:** Se recolectaron datasets desde FIFA 15 hasta FIFA 22, centrando el análisis en jugadores con información suficiente.
        - **Transformación:** 
            - Se estandarizaron nombres, posiciones y columnas relevantes.
            - Se unieron múltiples CSVs en estructuras por jugador o año para trayectorias.
            - Se tradujeron métricas y se normalizaron datos monetarios (salario y valuación).
        - **Resultado:** Se obtuvo un dataframe limpio y estructurado, con columnas clave como estadísticas generales, técnicas, económicas y físicas.
        """)

    with st.expander("👤 2. Sección: Jugador"):
        st.markdown("""
        - **Funcionalidad:** Búsqueda por nombre y despliegue de información detallada.
        - **Visualización:** Imagen, nombre, métricas generales, técnicas y económicas.
        - **Transformaciones aplicadas:** 
            - Formateo personalizado para salarios y valores.
            - Traducción de columnas (ej. `preferred_foot` a "Izquierda"/"Derecha").
        - **Resultado:** Vista centrada y visualmente ordenada del rendimiento e información del jugador.
        """)

    with st.expander("🤜🤛 3. Sección: Comparador"):
        st.markdown("""
        - **Funcionalidad:** Comparar dos jugadores por nombre.
        - **Visualización:** Imagen, nombre y métricas enfrentadas.
        - **Lógica especial:** 
            - Se usaron `st.metric` con flechas verde/roja/gris según quién supera en cada métrica.
            - Se controló que no se comparen métricas inexistentes (como porteros en velocidad).
        - **Resultado:** Comparaciones intuitivas y útiles para elegir entre dos talentos.
        """)

    with st.expander("📊 4. Sección: Tops"):
        st.markdown("""
        - **Funcionalidad:** Mostrar rankings por métrica seleccionada.
        - **Filtros:** Nacionalidad, posición, club.
        - **Visualización:** Tarjetas o tabla según preferencia del usuario.
        - **Transformaciones destacadas:** 
            - Formateo monetario con función `formato()`.
            - Traducción de métricas.
            - Tablas ordenadas con índice que inicia en 1.
        - **Resultado:** Rankings dinámicos, claros y visualmente atractivos.
        """)

    with st.expander("🧠 5. Sección: Preguntas & Curiosidades"):
        st.markdown("""
        - **Objetivo:** Educar y entretener al usuario con contenido futbolero.
        - **Contenido:** 
            - FAQ (significado de métricas, conceptos como potencial y general).
            - Curiosidades (top clubes con más jugadores, nacionalidades dominantes).
        - **Resultado:** Una sección educativa que enriquece el análisis con contexto.
        """)

    with st.expander("📈 6. Sección: Gráficas"):
        st.markdown("""
        - **Gráficos incluidos:** Barras, dispersión, histogramas y pronto radar.
        - **Opciones del usuario:** 
            - Elegir qué métrica graficar.
            - Filtros avanzados.
        - **Cálculos cacheados:** Optimización mediante funciones decoradas con `@st.cache`.
        - **Resultado:** Visualización rica en insights sobre la distribución y relaciones de los datos.
        """)

    with st.expander("📆 7. Sección: Trayectoria"):
        st.markdown("""
        - **Jugadores:** Messi y Cristiano Ronaldo entre 2015 y 2022.
        - **Análisis:** 
            - Se preprocesaron y unieron los datos por año.
            - Se construyó una tabla resumen (años como columnas, métricas como filas).
            - Visualizaciones de evolución por año, valor económico, técnica y progresión/regresión.
        - **Resultado:** Un seguimiento histórico y visualmente atractivo de dos leyendas del fútbol.
        """)

    st.info("📌 Cada sección ha sido cuidadosamente diseñada para balancear análisis técnico, estética y utilidad práctica.")
