import logging
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection
from business_object.joueur import Notes


class NotesDao(metaclass=Singleton):
    """DAO Notes"""

    @log
    def ajouter(self, notes: Notes) -> bool:
        """Ajouter des notes pour un joueur"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO foot.notes (
                            id_joueur, gardien, defenseur_lateral, defenseur_central,
                            milieu_defensif, ailier, meneur, attaquant
                        ) VALUES (
                            %(id_joueur)s, %(gardien)s, %(defenseur_lateral)s, %(defenseur_central)s,
                            %(milieu_defensif)s, %(ailier)s, %(meneur)s, %(attaquant)s
                        );
                        """,
                        {
                            "id_joueur": notes.id_joueur,
                            "gardien": notes.gardien,
                            "defenseur_lateral": notes.defenseur_lateral,
                            "defenseur_central": notes.defenseur_central,
                            "milieu_defensif": notes.milieu_defensif,
                            "ailier": notes.ailier,
                            "meneur": notes.meneur,
                            "attaquant": notes.attaquant,
                        },
                    )
                    return cursor.rowcount == 1
        except Exception as e:
            logging.info(e)
            return False

    @log
    def trouver_par_id_joueur(self, id_joueur: int) -> Notes | None:
        """Récupérer les notes d’un joueur"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM foot.notes WHERE id_joueur=%(id_joueur)s;",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        if res:
            return Notes(
                id_joueur=res["id_joueur"],
                gardien=res["gardien"],
                defenseur_lateral=res["defenseur_lateral"],
                defenseur_central=res["defenseur_central"],
                milieu_defensif=res["milieu_defensif"],
                ailier=res["ailier"],
                meneur=res["meneur"],
                attaquant=res["attaquant"]
            )
        return None

    @log
    def supprimer(self, id_joueur: int) -> bool:
        """Supprimer les notes d'un joueur"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM foot.notes WHERE id_joueur = %(id_joueur)s;",
                        {"id_joueur": id_joueur},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            raise
