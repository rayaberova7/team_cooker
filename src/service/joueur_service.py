# service/joueur_service.py
import random
from tabulate import tabulate

from utils.log_decorator import log
from business_object.joueur import Joueur
from service.notes_service import NotesService
from dao.joueur_dao import JoueurDao


class JoueurService:
    """Classe regroupant les services métier liés aux joueurs"""

    @log
    def creer(self, joueur: Joueur) -> bool:
        return JoueurDao().creer(joueur)

    @log
    def modifier(self, joueur: Joueur) -> bool:
        return JoueurDao().modifier(joueur)

    @log
    def supprimer(self, joueur: Joueur) -> bool:
        return JoueurDao().supprimer(joueur)

    @log
    def trouver_par_id(self, id_joueur: int) -> Joueur | None:
        joueur = JoueurDao().trouver_par_id(id_joueur)
        if joueur:
            joueur.notes = NotesService().recuperer_notes(id_joueur)
        return joueur

    @log
    def lister_tous(self) -> list[Joueur]:
        joueurs = JoueurDao().lister_tous()
        notes_service = NotesService()
        for j in joueurs:
            j.notes = notes_service.recuperer_notes(j.id_joueur)
        return joueurs

    # ---------------------------------------
    # Création d'équipes
    # ---------------------------------------

    @log
    def creer_equipes(self, joueurs: list[Joueur], taille_equipe: int) -> list[list[Joueur]]:
        """
        Créer des équipes équilibrées en fonction des notes.
        Chaque joueur est placé à son meilleur poste.
        """

        if not joueurs:
            raise ValueError("Liste de joueurs vide")

        if taille_equipe < 2:
            raise ValueError("Taille d'équipe invalide")

        # Charger les notes si absentes
        notes_service = NotesService()
        for j in joueurs:
            if not hasattr(j, "notes") or j.notes is None:
                j.notes = notes_service.recuperer_notes(j.id_joueur)

        # Filtrer joueurs sans notes
        joueurs = [j for j in joueurs if j.notes]
        if len(joueurs) < taille_equipe:
            raise ValueError("Pas assez de joueurs pour créer une équipe")

        # 1. Déterminer le meilleur poste pour chaque joueur
        def meilleur_poste(joueur):
            notes = joueur.notes.__dict__.copy()
            notes.pop("id_joueur")
            return max(notes, key=notes.get)

        for j in joueurs:
            j.meilleur_poste = meilleur_poste(j)

        # Mélange aléatoire
        random.shuffle(joueurs)

        # 2. Regrouper les joueurs par poste
        postes = {
            "gardien": [],
            "defenseur_lateral": [],
            "defenseur_central": [],
            "milieu_defensif": [],
            "ailier": [],
            "meneur": [],
            "attaquant": [],
        }

        for j in joueurs:
            postes[j.meilleur_poste].append(j)

        # 3. Construire les équipes équilibrées
        equipes = []
        nb_equipes = len(joueurs) // taille_equipe

        for _ in range(nb_equipes):
            equipe = []

            def piocher(poste):
                if postes[poste]:
                    return postes[poste].pop()
                return None

            # Ordre logique pour une équipe standard
            priorite = [
                "gardien",
                "defenseur_lateral", "defenseur_lateral",
                "defenseur_central", "defenseur_central",
                "milieu_defensif",
                "meneur",
                "ailier", "ailier",
                "attaquant",
            ]

            for p in priorite:
                if len(equipe) >= taille_equipe:
                    break
                joueur = piocher(p)
                if joueur:
                    equipe.append(joueur)

            # Si manque des joueurs → compléter aléatoirement
            if len(equipe) < taille_equipe:
                restants = [j for liste in postes.values() for j in liste]
                random.shuffle(restants)
                equipe += restants[: (taille_equipe - len(equipe))]

                # Enlever les joueurs ajoutés du "ban"
                for j in equipe:
                    for liste in postes.values():
                        if j in liste:
                            liste.remove(j)

            equipes.append(equipe)

        return equipes
