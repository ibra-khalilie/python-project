DROP TABLE IF EXISTS produit_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS produit;

CREATE TABLE client (
  idclient INTEGER PRIMARY KEY AUTOINCREMENT,
  nom TEXT  NOT NULL,
  prenom TEXT NOT NULL,
  adresse TEXT NOT NULL,
  tel  TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE commande (
  idCommande INTEGER PRIMARY KEY AUTOINCREMENT,
  idclient INTEGER NOT NULL,
  dateComande DATE NOT NULL,
  FOREIGN KEY (idclient) REFERENCES client (idclient)
);

CREATE TABLE produit (
  idProduit INTEGER PRIMARY KEY AUTOINCREMENT,
  prixUnitaire DECIMAL NOT NULL,
  libelle TEXT NOT NULL,
  image Text NOT NULL
);

CREATE TABLE produit_commande (
  idCommande INTEGER,
  idProduit INTEGER,
  quantite INTEGER NOT NULL,
  PRIMARY KEY (idCommande,idProduit),
  FOREIGN KEY (idCommande) REFERENCES commande (idCommande),
  FOREIGN KEY (idProduit) REFERENCES produit (idProduit)
);


-- insertion of data for the test

INSERT INTO client (nom, prenom, adresse, tel, username, password)
VALUES
('Rébecca', 'Armand', '18 rue Federico Garcia, Grenoble', '04349560', 'toule','Toulel97'),
('Issa', 'Fall', '11 Rue Maurice, Lyon', '08223847', 'toule2' ,'Toulel97'),
('Hilaire', 'Savary', '30 Rue Colibris, Paris', '0784048322', 'toule3', 'Toulel97');

INSERT INTO produit (prixUnitaire, libelle,image)
VALUES
(10,'chemise','/static/img/1.jpg'),
(20,'montre','/static/img/2.jpg'),
(10.4,'ordinateur','/static/img/3.jpg'),
(10.4,'robe','/static/img/4.jpg'),
(10.4,'trotinette','/static/img/5.jpg');

INSERT INTO commande (idclient, dateComande)
VALUES
(1,'2021-02-12'),
(2,'2022-01-02'),
(1,'2023-09-02');

INSERT INTO produit_commande (idCommande,idProduit,quantite)
VALUES
(1,2,2),
(2,1,10),
(3,3,8);