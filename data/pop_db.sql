-- =================================
--  Insertion de joueurs
-- =================================
INSERT INTO foot.joueur (nom, prenom, telephone, malus, team_conj) VALUES
('Dupont', 'Jean', '0600000000', 0, TRUE),
('Martin', 'Paul', '0600000000', 1, FALSE),
('Durand', 'Luc', '0600000000', 0, TRUE),
('Bernard', 'Marc', '0600000000', 2, FALSE),
('Petit', 'Louis', '0600000000', 0, TRUE);

-- ==================================
--  Insertion de notes entre 0 et 10
-- ==================================
INSERT INTO foot.notes (id_joueur, gardien, defenseur_lateral, defenseur_central, milieu_defensif, ailier, meneur, attaquant) VALUES
(1, 5, 8, 2, 7, 3, 4, 1),
(2, 9, 7, 8, 1, 7, 2, 7),
(3, 8, 5, 7, 6, 0, 0, 0),
(4, 0, 5, 0, 8, 6, 5, 1),
(5, 8, 0, 0, 0, 0, 1, 0)
