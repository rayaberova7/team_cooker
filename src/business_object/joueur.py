from business_object.notes import Notes


class Joueur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant du joueur
    prenom : str
        prénom du joueur
    nom : str
        nom du joueur
    telephone : str
        numéro de téléphone du joueur
    malus : int
        malus attribué entre 0 et 10
    team_conj : bool
        le joueur fait parti de la team conj ou non
    notes : Notes | None
        objet Notes associé au joueur (peut être None)
    """

    def __init__(
        self,
        prenom: str,
        nom: str,
        telephone: str,
        malus: int,
        team_conj: bool,
        id_joueur: int = None,
        notes: Notes = None
    ):
        self.id_joueur = id_joueur
        self.prenom = prenom
        self.nom = nom
        self.telephone = telephone
        self.malus = malus
        self.team_conj = team_conj
        self.notes = notes  # attribut de type Notes

    def __str__(self):
        return f"Joueur({self.prenom} {self.nom}, notes={self.notes})"
