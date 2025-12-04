import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from business_object.joueur import Joueur
from business_object.notes import Notes
from service.joueur_service import JoueurService
from service.notes_service import NotesService

from utils.log_init import initialiser_logs

app = FastAPI(title="Mon webservice")


initialiser_logs("Webservice")

joueur_service = JoueurService()

app = FastAPI(title="API Foot – Gestion Joueurs et Équipes")

joueur_service = JoueurService()
notes_service = NotesService()

# -------------------------------------------------------
# ROUTES JOUEURS
# -------------------------------------------------------

@app.get("/joueurs")
def lister_joueurs():
    joueurs = joueur_service.lister()
    return [j.to_dict() for j in joueurs]


@app.get("/joueurs/{id_joueur}")
def trouver_joueur(id_joueur: int):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    notes = notes_service.trouver_par_id_joueur(id_joueur)
    joueur.notes = notes

    return joueur.to_dict()


@app.post("/joueurs")
def creer_joueur(payload: dict):
    try:
        joueur = Joueur(
            prenom=payload["prenom"],
            nom=payload["nom"],
            telephone=payload.get("telephone"),
            malus=payload.get("malus", 0),
            team_conj=payload.get("team_conj", False),
        )
    except KeyError:
        raise HTTPException(status_code=400, detail="Champs obligatoires manquants")

    res = joueur_service.creer(joueur)
    if not res:
        raise HTTPException(status_code=500, detail="Erreur lors de la création du joueur")

    return joueur.to_dict()


@app.put("/joueurs/{id_joueur}")
def modifier_joueur(id_joueur: int, payload: dict):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur.prenom = payload.get("prenom", joueur.prenom)
    joueur.nom = payload.get("nom", joueur.nom)
    joueur.telephone = payload.get("telephone", joueur.telephone)
    joueur.malus = payload.get("malus", joueur.malus)
    joueur.team_conj = payload.get("team_conj", joueur.team_conj)

    ok = joueur_service.modifier(joueur)
    if not ok:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification")

    return joueur.to_dict()


@app.delete("/joueurs/{id_joueur}")
def supprimer_joueur(id_joueur: int):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    joueur_service.supprimer(joueur)
    return {"message": "Joueur supprimé"}


# -------------------------------------------------------
# ROUTES NOTES
# -------------------------------------------------------

@app.get("/notes/{id_joueur}")
def get_notes(id_joueur: int):
    notes = notes_service.trouver_par_id_joueur(id_joueur)
    if notes is None:
        raise HTTPException(status_code=404, detail="Notes non trouvées pour ce joueur")
    return notes.to_dict()


@app.post("/notes/{id_joueur}")
def ajouter_notes(id_joueur: int, payload: dict):
    joueur = joueur_service.trouver_par_id(id_joueur)
    if joueur is None:
        raise HTTPException(status_code=404, detail="Joueur non trouvé")

    notes = Notes(id_joueur=id_joueur, **payload)
    ok = notes_service.ajouter(notes)

    if not ok:
        raise HTTPException(status_code=500, detail="Erreur lors de l'ajout des notes")

    return notes.to_dict()


@app.put("/notes/{id_joueur}")
def modifier_notes(id_joueur: int, payload: dict):
    notes = notes_service.trouver_par_id_joueur(id_joueur)
    if notes is None:
        raise HTTPException(status_code=404, detail="Notes inexistantes")

    for cle, valeur in payload.items():
        if hasattr(notes, cle):
            setattr(notes, cle, valeur)

    ok = notes_service.modifier(notes)
    if not ok:
        raise HTTPException(status_code=500, detail="Erreur lors de la modification des notes")

    return notes.to_dict()


# -------------------------------------------------------
# ROUTE CRÉATION ÉQUIPES
# -------------------------------------------------------

@app.post("/equipes")
def creer_equipes(payload: dict):
    """
    payload:
    {
        "joueurs": [1,2,3,4,5,6,7,8,9,10],
        "taille_equipe": 5
    }
    """
    try:
        ids = payload["joueurs"]
        taille = payload["taille_equipe"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Champs manquants")

    liste_joueurs = []
    for i in ids:
        j = joueur_service.trouver_par_id(i)
        if j is None:
            raise HTTPException(status_code=404, detail=f"Joueur {i} introuvable")

        j.notes = notes_service.trouver_par_id_joueur(i)
        liste_joueurs.append(j)

    equipes = joueur_service.creer_equipes(liste_joueurs, taille)

    return equipes


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

    logging.info("Arret du Webservice")
