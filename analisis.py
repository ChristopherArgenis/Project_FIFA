# Importacion de libreria de Pandas
import pandas as pd

# Lectura del .csv
# Con cualquiera que sea solo cambiar "players_<año>.csv"
players = pd.read_csv("df_players_15.csv")
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
# --- players.to_csv("df_players_22.csv", index=False, columns=columns_required) ---
# Para procesarlos todos.
# Subir el .csv con las columnas que seran necesarias para el analisis.
# Y metricas a mostrar en la Aplicacion Web usando -> (Streamlit).

# player = players.iloc[0]
# print(player)

estadisticas = players[["skill_dribbling", "dribbling", "skill_curve", "skill_ball_control", 
                        "movement_agility", "movement_reactions", "power_shot_power", "power_jumping"]]

print(estadisticas.head(10))
