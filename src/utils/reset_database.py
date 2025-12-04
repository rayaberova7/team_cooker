import os
import logging
import dotenv

from utils.singleton import Singleton
from dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Réinitialisation de la base de données
    """

    def lancer(self):
        """Lancement de la réinitialisation des données.
        """
        pop_data_path = "data/pop_db.sql"

        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        # Création du schema
        create_schema = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        # Lecture des fichiers SQL
        with open("data/init_db.sql", encoding="utf-8") as f:
            init_db_as_string = f.read()

        with open(pop_data_path, encoding="utf-8") as f:
            pop_db_as_string = f.read()

        # Exécution SQL
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(create_schema)
                    cursor.execute(init_db_as_string)
                    cursor.execute(pop_db_as_string)
        except Exception as e:
            logging.info(e)
            raise

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
