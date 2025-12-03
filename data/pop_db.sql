-- ==============================
--  Insertion de joueurs
-- ==============================
INSERT INTO foot.joueur (nom, prenom, numero, malus, team_conj) VALUES
('Dupont', 'Jean', 1, 0, TRUE),
('Martin', 'Paul', 2, 1, FALSE),
('Durand', 'Luc', 3, 0, TRUE),
('Bernard', 'Marc', 4, 2, FALSE),
('Petit', 'Louis', 5, 0, TRUE);

-- ==============================
--  Insertion de notes aléatoires
-- ==============================
INSERT INTO foot.note (id_joueur, gardien, defenseur_lateral, defenseur_central, milieu_defensif, ailier, meneur, attaquant) VALUES
(1, 5, 8, 2, 7, 3, 4, 1),
(2, 9, 7, 8, 1, 7, 2, 7),
(3, 8, 5, 7, 6, 0, 0, 0),
(4, 0, 5, 0, 8, 6, 5, 1),
(5, 8, 0, 0, 0, 0, 1, 0)