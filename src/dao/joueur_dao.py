import logging
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection
from business_object.joueur import Joueur


class JoueurDao(metaclass=Singleton):
    """DAO Joueur"""

    @log
    def creer(self, joueur: Joueur) -> bool:
        """Créer un joueur dans la base"""
        res = None
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO foot.joueur (prenom, nom, telephone, malus, team_conj)
                        VALUES (%(prenom)s, %(nom)s, %(telephone)s, %(malus)s, %(team_conj)s)
                        RETURNING id_joueur;
                        """,
                        {
                            "prenom": joueur.prenom,
                            "nom": joueur.nom,
                            "telephone": joueur.telephone,
                            "malus": joueur.malus,
                            "team_conj": joueur.team_conj,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            return False

        if res:
            joueur.id_joueur = res["id_joueur"]
            return True
        return False

    @log
    def trouver_par_id(self, id_joueur: int) -> Joueur | None:
        """Trouver un joueur par son id"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM foot.joueur WHERE id_joueur = %(id_joueur)s;",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        if res:
            return Joueur(
                id_joueur=res["id_joueur"],
                prenom=res["prenom"],
                nom=res["nom"],
                telephone=res["telephone"],
                malus=res["malus"],
                team_conj=res["team_conj"],
            )
        return None

    @log
    def lister_tous(self) -> list[Joueur]:
        """Lister tous les joueurs"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM foot.joueur;")
                    res = cursor.fetchall()
        except Exception as e:
            logging.info(e)
            raise

        return [
            Joueur(
                id_joueur=row["id_joueur"],
                prenom=row["prenom"],
                nom=row["nom"],
                telephone=row["telephone"],
                malus=row["malus"],
                team_conj=row["team_conj"]
            )
            for row in res
        ]

    @log
    def modifier(self, joueur: Joueur) -> bool:
        """Modifier un joueur existant"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE foot.joueur
                        SET prenom=%(prenom)s,
                            nom=%(nom)s,
                            telephone=%(telephone)s,
                            malus=%(malus)s,
                            team_conj=%(team_conj)s
                        WHERE id_joueur=%(id_joueur)s;
                        """,
                        {
                            "prenom": joueur.prenom,
                            "nom": joueur.nom,
                            "telephone": joueur.telephone,
                            "malus": joueur.malus,
                            "team_conj": joueur.team_conj,
                            "id_joueur": joueur.id_joueur
                        },
                    )
                    return cursor.rowcount == 1
        except Exception as e:
            logging.info(e)
            return False

    @log
    def supprimer(self, id_joueur: int) -> bool:
        """Supprimer un joueur et ses notes (via cascade ou explicitement)"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM foot.joueur WHERE id_joueur = %(id_joueur)s;",
                        {"id_joueur": id_joueur},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.info(e)
            raise
