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
