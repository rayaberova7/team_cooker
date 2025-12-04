from utils.log_decorator import log
from business_object.notes import Notes
from dao.notes_dao import NotesDao


class NotesService:
    """Méthodes de service pour gérer les notes des joueurs"""

    @log
    def ajouter_notes(self, notes: Notes) -> bool:
        return NotesDao().ajouter(notes)

    @log
    def modifier_notes(self, notes: Notes) -> bool:
        return NotesDao().modifier(notes)

    @log
    def recuperer_notes(self, id_joueur: int) -> Notes | None:
        return NotesDao().trouver_par_id_joueur(id_joueur)

    @log
    def supprimer_notes(self, id_joueur: int) -> bool:
        return NotesDao().supprimer_par_joueur(id_joueur)
