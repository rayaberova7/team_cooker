import logging
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from service.joueur_service import JoueurService
from service.notes_service import NotesService

from utils.log_init import initialiser_logs


# -------------------------------------------------------
# INITIALISATION
# -------------------------------------------------------

initialiser_logs("Webservice")

app = FastAPI(title="API Foot – Gestion Joueurs et Équipes")

joueur_service = JoueurService()
notes_service = NotesService()


class EquipesModel(BaseModel):
    id_joueurs: List[int]
    taille_equipe: int


class JoueurModel(BaseModel):
    prenom: str
    nom: str
    telephone: str
    malus: int
    team_conj: bool


class NotesModel(BaseModel):
    id_joueur: int
    gardien: int
    defenseur_lateral: int
    defenseur_central: int
    milieu_defensif: int
    ailier: int
    meneur: int
    attaquant: int


# -------------------------------------------------------
# ROUTES EQUIPES
# -------------------------------------------------------

@app.get("/equipes", tags=["Equipes"])
def lister_joueurs():
    joueurs = joueur_service.lister_tous()
    return [j.to_dict() for j in joueurs]


@app.post("/equipes", tags=["Equipes"])
async def creer_equipes(e: EquipesModel):
    joueurs = []

    for id_j in e.id_joueurs:
        j = joueur_service.trouver_par_id(id_j)
        if j is None:
            raise HTTPException(status_code=404, detail=f"Joueur {id_j} introuvable")

        j.notes = notes_service.recuperer_notes(id_j)
        joueurs.append(j)

    equipes = joueur_service.creer_equipes(joueurs, e.taille_equipe)

    return equipes


# -------------------------------------------------------
# ROUTES JOUEURS
# -------------------------------------------------------

@app.get("/joueurs/{id_joueur}", tags=["Joueurs"])
def trouver_joueur(id_joueur: int):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    notes = notes_service.recuperer_notes(id_joueur)
    joueur.notes = notes

    return joueur.to_dict()


@app.post("/joueurs/", tags=["Joueurs"])
async def creer_joueur(j: JoueurModel):
    logging.info("Créer un joueur")

    joueur = joueur_service.creer(
        j.prenom,
        j.nom,
        j.telephone,
        j.malus,
        j.team_conj
    )

    if not joueur:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du joueur")

    return joueur.to_dict()


@app.delete("/joueurs/{id_joueur}", tags=["Joueurs"])
def supprimer_joueur(id_joueur: int):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur:
        joueur_service.supprimer(id_joueur)
        return {"message": "Joueur supprimé"}
    else:
        return {"message": "Joueur non existant"}


# -------------------------------------------------------
# ROUTES NOTES
# -------------------------------------------------------


@app.get("/notes/{id_joueur}", tags=["Notes"])
def visualiser_notes(id_joueur: int):
    notes = notes_service.recuperer_notes(id_joueur)
    if notes is None:
        raise HTTPException(status_code=404, detail="Notes non trouvées")
    return notes.to_dict()


@app.post("/notes/", tags=["Notes"])
async def ajouter_notes(n: NotesModel):
    joueur = joueur_service.trouver_par_id(n.id_joueur)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    notes = notes_service.ajouter_notes(
        n.id_joueur,
        n.gardien,
        n.defenseur_lateral,
        n.defenseur_central,
        n.milieu_defensif,
        n.ailier,
        n.meneur,
        n.attaquant
    )

    if not notes:
        raise HTTPException(status_code=400, detail="Erreur lors de l'ajout des notes")

    return notes


@app.post("/notes/", tags=["Notes"])
async def modifier_notes(n: NotesModel):
    joueur = joueur_service.trouver_par_id(n.id_joueur)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    notes = notes_service.supprimer(n.id_joueur)
    notes = notes_service.ajouter_notes(
        n.id_joueur,
        n.gardien,
        n.defenseur_lateral,
        n.defenseur_central,
        n.milieu_defensif,
        n.ailier,
        n.meneur,
        n.attaquant
    )

    if not notes:
        raise HTTPException(status_code=400, detail="Erreur lors de l'ajout des notes")

    return notes.to_dict()


# -------------------------------------------------------
# DÉMARRAGE UVICORN
# -------------------------------------------------------

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=9876)
#     logging.info("Arrêt du Webservice")
