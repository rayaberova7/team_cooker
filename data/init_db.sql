-- ==============================
--  Table joueur
-- ==============================
CREATE TABLE foot.joueur (
    id_joueur      SERIAL PRIMARY KEY,
    nom            VARCHAR(50) NOT NULL,
    prenom         VARCHAR(50) NOT NULL,
    telephone      NUMERIC(10) NOT NULL,
    malus          NUMERIC,
    team_conj      BOOLEAN,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================
--  Table note
-- ==============================
CREATE TABLE foot.note (
    id_joueur             INT NOT NULL,
    gardien               INT NOT NULL CHECK (gardien BETWEEN 0 AND 10),
    defenseur_lateral     INT NOT NULL CHECK (defenseur_lateral BETWEEN 0 AND 10),
    defenseur_central     INT NOT NULL CHECK (defenseur_central BETWEEN 0 AND 10),
    milieu_defensif       INT NOT NULL CHECK (milieu_defensif BETWEEN 0 AND 10),
    ailier                INT NOT NULL CHECK (ailier BETWEEN 0 AND 10),
    meneur                INT NOT NULL CHECK (meneur BETWEEN 0 AND 10),
    attaquant             INT NOT NULL CHECK (attaquant BETWEEN 0 AND 10),
    FOREIGN KEY (id_joueur) REFERENCES foot.joueur(id_joueur)
);
