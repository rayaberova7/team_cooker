# pip install streamlit requests pandas

import streamlit as st
import requests
import pandas as pd

BASE_URL = "https://team-cooker.lab.sspcloud.fr"


# ------------------------------
# Fonctions API
# ------------------------------
def fetch_players():
    try:
        response = requests.get(f"{BASE_URL}/equipes")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des joueurs: {e}")
        return []


def create_player(prenom, nom, malus, team_conj="true", telephone="0000000000"):
    try:
        payload = {
            "prenom": prenom,
            "nom": nom,
            "telephone": telephone,
            "malus": malus,
            "team_conj": team_conj
        }
        response = requests.post(f"{BASE_URL}/joueurs/", json=payload)
        response.raise_for_status()
        return response.json()  # Doit contenir id_joueur
    except Exception as e:
        st.error(f"Erreur lors de la création du joueur: {e}")
        return None


def set_notes(id_joueur, notes_dict):
    try:
        payload = {"id_joueur": id_joueur, **notes_dict}
        response = requests.post(f"{BASE_URL}/notes/", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur lors de l'ajout des notes: {e}")
        return None


def get_top_positions(notes, top_n=3):
    note_items = {k: v for k, v in notes.items() if k != "id_joueur"}
    sorted_notes = sorted(note_items.items(), key=lambda x: x[1], reverse=True)
    return sorted_notes[:top_n]


# ------------------------------
# Couleurs par poste (FIFA style)
# ------------------------------
POSTE_COLORS = {
    "gardien": None,                # pas de couleur
    "defenseur_central": (255, 255, 0),  # jaune
    "defenseur_lateral": (255, 165, 0),  # orange
    "milieu_defensif": (50, 205, 50),    # vert
    "meneur": (50, 205, 50),             # vert
    "ailier": (0, 0, 255),               # bleu
    "attaquant": (0, 0, 255),            # bleu
}

# ------------------------------
# Interface principale
# ------------------------------
st.set_page_config(page_title="Team Cooker - Joueurs et Postes", layout="wide")
st.title("Team Cooker - Les joueurs et leurs top postes")

players = fetch_players()

# Préparer le tableau
table_data = []
for player in players:
    if player["notes"]:
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


# Fonction de coloration
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


styler = df.style
for col in ["Top 1 poste", "Top 2 poste", "Top 3 poste"]:
    styler = styler.map(color_postes, subset=[col])

st.dataframe(styler, use_container_width=True)

# ------------------------------
# Ajouter un nouveau joueur
# ------------------------------
st.header("Ajouter un nouveau joueur et ses notes")

# Formulaire création joueur
with st.form("nouveau_joueur"):
    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")
    telephone = st.text_input("Téléphone", value="0000000000")
    malus = st.text_input("Malus", value=0)
    team_conj = st.text_input("Team conjoncture", value="false")

    submitted_player = st.form_submit_button("Créer joueur")

if submitted_player:
    new_player = create_player(prenom, nom, malus, team_conj, telephone)
    if new_player:
        id_joueur = new_player.get("id_joueur")
        st.success(f"Joueur créé avec ID: {id_joueur}")

        # Formulaire pour ajouter les notes, **en dehors** du formulaire précédent
        with st.form("ajouter_notes"):
            gardien = st.number_input("Gardien", 0, 10, value=0)
            defenseur_lateral = st.number_input("Défenseur latéral", 0, 10, value=0)
            defenseur_central = st.number_input("Défenseur central", 0, 10, value=0)
            milieu_defensif = st.number_input("Milieu défensif", 0, 10, value=0)
            meneur = st.number_input("Meneur", 0, 10, value=0)
            ailier = st.number_input("Ailier", 0, 10, value=0)
            attaquant = st.number_input("Attaquant", 0, 10, value=0)

            submitted_notes = st.form_submit_button("Ajouter les notes")
            if submitted_notes:
                notes_dict = {
                    "gardien": gardien,
                    "defenseur_lateral": defenseur_lateral,
                    "defenseur_central": defenseur_central,
                    "milieu_defensif": milieu_defensif,
                    "meneur": meneur,
                    "ailier": ailier,
                    "attaquant": attaquant
                }
                result = set_notes(id_joueur, notes_dict)
                if result:
                    st.success("Notes ajoutées avec succès !")
