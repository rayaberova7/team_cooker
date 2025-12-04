from utils.log_decorator import log
from business_object.notes import Notes
from dao.notes_dao import NotesDao


class NotesService:
    """Méthodes de service pour gérer les notes des joueurs"""

    @log
    def ajouter_notes(
        self,
        id_joueur,
        gardien,
        defenseur_lateral,
        defenseur_central,
        milieu_defensif,
        ailier,
        meneur,
        attaquant
    ) -> bool:
        notes = Notes(
            id_joueur=id_joueur,
            gardien=gardien,
            defenseur_lateral=defenseur_lateral,
            defenseur_central=defenseur_central,
            milieu_defensif=milieu_defensif,
            ailier=ailier,
            meneur=meneur,
            attaquant=attaquant
        )

        return NotesDao().ajouter(notes)

    @log
    def recuperer_notes(self, id_joueur: int) -> Notes | None:
        return NotesDao().trouver_par_id_joueur(id_joueur)

    @log
    def supprimer(self, id_joueur: int) -> bool:
        return NotesDao().supprimer(id_joueur)
