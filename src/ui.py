# pip install streamlit requests pandas

import streamlit as st
import requests
import pandas as pd

BASE_URL = "https://team-cooker.lab.sspcloud.fr"


def fetch_players():
    try:
        response = requests.get(f"{BASE_URL}/equipes")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des joueurs: {e}")
        return []

def get_top_positions(notes, top_n=3):
    note_items = {k: v for k, v in notes.items() if k != "id_joueur"}
    sorted_notes = sorted(note_items.items(), key=lambda x: x[1], reverse=True)
    return sorted_notes[:top_n]


# Couleurs par poste (en RGB)
POSTE_COLORS = {
    "gardien": None,                # pas de couleur
    "defenseur_central": (255, 255, 0),  # jaune
    "defenseur_lateral": (255, 165, 0),  # orange
    "milieu_defensif": (50, 205, 50),    # vert
    "meneur": (50, 205, 50),             # vert
    "ailier": (0, 0, 255),               # bleu
    "attaquant": (0, 0, 255),            # bleu
}

st.set_page_config(page_title="Team Cooker - Joueurs et Postes", layout="wide")
st.title("Team Cooker - Les joueurs et leurs top postes")

players = fetch_players()

# Préparer les données
table_data = []
for player in players:
    top_positions = get_top_positions(player["notes"])
    row = {
        "ID": player["id_joueur"],
        "Prénom": player["prenom"],
        "Nom": player["nom"]
    }
    for i, (poste, note) in enumerate(top_positions, start=1):
        row[f"Top {i} poste"] = f"{poste} ({note}/10)"
    table_data.append(row)

df = pd.DataFrame(table_data)

# Fonction pour colorer les cellules selon le poste et la note
def color_postes(val):
    if isinstance(val, str):
        for poste, rgb in POSTE_COLORS.items():
            if val.startswith(poste) and rgb is not None:
                try:
                    note = int(val.split("(")[1].split("/")[0])
                    alpha = 0.3 + 0.7 * (note / 10)
                except:
                    alpha = 0.5
                r, g, b = rgb
                return f"background-color: rgba({r},{g},{b},{alpha}); color: white;"
    return ""


# Appliquer le style sur les colonnes Top postes
styler = df.style
for col in ["Top 1 poste", "Top 2 poste", "Top 3 poste"]:
    styler = styler.map(color_postes, subset=[col])

st.dataframe(styler, use_container_width=True)
