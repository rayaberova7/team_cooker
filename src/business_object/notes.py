class Notes:
    """
    Classe représentant l'ensemble des notes entre 0 et 10 par poste et par joueur

    Attributs
    ----------
    id_joueur : int
        identifiant du joueur
    gardien : int
    defenseur_lateral : int
    defenseur_central : int
    milieu_defensif : int
    ailier : int
    meneur : int
    attaquant : int
    """

    def __init__(
        self,
        gardien,
        defenseur_lateral,
        defenseur_central,
        milieu_defensif,
        ailier,
        meneur,
        attaquant,
        id_joueur=None
    ):
        """Constructeur"""
        self.id_joueur = id_joueur
        self.gardien = gardien
        self.defenseur_lateral = defenseur_lateral
        self.defenseur_central = defenseur_central
        self.milieu_defensif = milieu_defensif
        self.ailier = ailier
        self.meneur = meneur
        self.attaquant = attaquant

    def __str__(self):
        return (
            f"Notes(gardien={self.gardien}, defenseur_lateral={self.defenseur_lateral}, "
            f"defenseur_central={self.defenseur_central}, milieu_defensif={self.milieu_defensif}, "
            f"ailier={self.ailier}, meneur={self.meneur}, attaquant={self.attaquant})"
        )

    def to_dict(self):
        return {
            "id_joueur": self.id_joueur,
            "gardien": self.gardien,
            "defenseur_lateral": self.defenseur_lateral,
            "defenseur_central": self.defenseur_central,
            "milieu_defensif": self.milieu_defensif,
            "ailier": self.ailier,
            "meneur": self.meneur,
            "attaquant": self.attaquant,
        }