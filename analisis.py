# Importacion de libreria de Pandas
import pandas as pd

# Lectura del .csv
# Con cualquiera que sea solo cambiar "players_<año>.csv"
# players = pd.read_csv("df_players_15.csv")
# Descubrimiento de las columnas:
# Proposito: Filtrar columnas innecesarias para el analisis.
# Code:
# dicc_columns = {"Names": players.columns}
# players_column = pd.DataFrame(dicc_columns)
# print(players_column[n:m])

# Columnas a utilizar.
columns_required = ["sofifa_id","player_url", "short_name", "long_name", "overall", "potential", "value_eur", "wage_eur", "age", "height_cm", "weight_kg",
                    "club_name", "club_position", "club_jersey_number", "nationality_name", "preferred_foot", "pace", "shooting", "passing", "dribbling",
                    "defending", "physic", "skill_dribbling", "skill_curve", "skill_ball_control", "movement_agility", "movement_reactions", "power_shot_power",
                    "power_jumping", "player_face_url", "club_logo_url", "nation_logo_url"]

new_columns_requerid = ["short_name", "long_name", "overall", "potential", "value_eur", "wage_eur", "age", "height_cm", "weight_kg",
                    "club_name", "club_position", "club_jersey_number", "nationality_name", "preferred_foot", "pace", "shooting", "passing", "dribbling",
                    "defending", "physic", "skill_dribbling", "skill_curve", "skill_ball_control", "movement_agility", "movement_reactions", "power_shot_power",
                    "power_jumping", "player_face_url", "club_logo_url"]

# Tablas
Jugador = ["long_name", "short_name", "age", "height_cm", "weight_kg", "player_face_url", "club_jersey_number", "preferred_foot"]
posicion = ["club_position"]
Pais = ["nationality_name"]
club = ["club_name", "club_logo_url"]
Finanzas = ["value_eur", "wage_eur"]
metricas = ["overall", "potential", "pace", "shooting", "passing", "dribbling", "defending", "physic"]
habilidades = ["skill_dribbling", "skill_curve", "skill_ball_control", "movement_agility", "movement_reactions", "power_shot_power", "power_jumping"]

# Formato a Guardar.
# Solo cambiar la parte "df_players_<año>.csv".
# --- players.to_csv("df_players_22.csv", index=False, columns=new_columns_requerid)
# Para procesarlos todos.
# Subir el .csv con las columnas que seran necesarias para el analisis.
# Y metricas a mostrar en la Aplicacion Web usando -> (Streamlit).

# player = players.iloc[4]
# print(player)

# Before : 3.9+ MB - After: 3.6+ MB
def is_nulo(valor, texto_si_nulo=" "):
    if pd.isna(valor):
        return texto_si_nulo
    try:
        return int(valor)
    except:
        return valor
    
nulls_player = ["value_eur", "wage_eur", "club_name", "club_position", "club_jersey_number", "club_logo_url"]
nulls_metric = ["pace", "passing", "dribbling", "defending", "physic"]

# Cargar todos los datasets
players_15 = pd.read_csv("df_players_15.csv")
players_16 = pd.read_csv("df_players_16.csv")
players_17 = pd.read_csv("df_players_17.csv")
players_18 = pd.read_csv("df_players_18.csv")
players_19 = pd.read_csv("df_players_19.csv")
players_20 = pd.read_csv("df_players_20.csv")
players_21 = pd.read_csv("df_players_21.csv")
players_22 = pd.read_csv("df_players_22.csv")

# Empaquetar los datasets con su año correspondiente
datasets = [
    (players_15, 2015),
    (players_16, 2016),
    (players_17, 2017),
    (players_18, 2018),
    (players_19, 2019),
    (players_20, 2020),
    (players_21, 2021),
    (players_22, 2022),
]

# DataFrames acumulativos
messi_rows = []
cristiano_rows = []

for df, year in datasets:
    df["year"] = year  # Agregar año

    messi = df[df["short_name"] == "L. Messi"]
    cristiano = df[df["short_name"] == "Cristiano Ronaldo"]

    messi_rows.append(messi)
    cristiano_rows.append(cristiano)

# Concatenar los años
df_messi = pd.concat(messi_rows, ignore_index=True)
df_cristiano = pd.concat(cristiano_rows, ignore_index=True)

# Guardar si se desea
df_messi.to_csv("trayectoria_messi.csv", index=False)
df_cristiano.to_csv("trayectoria_cristiano.csv", index=False)

print("✅ Listo. Archivos de trayectoria creados.")