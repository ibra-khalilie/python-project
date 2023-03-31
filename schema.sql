DROP TABLE IF EXISTS product_command;
DROP TABLE IF EXISTS command;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS product;

CREATE TABLE customer (
  idcustomer INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT  NOT NULL,
  firstname TEXT NOT NULL,
  adress TEXT NOT NULL,
  phone  TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE command (
  idcommand INTEGER PRIMARY KEY AUTOINCREMENT,
  idcustomer INTEGER NOT NULL,
  commanddate DATE NOT NULL,
  FOREIGN KEY (idcustomer) REFERENCES customer (idcustomer)
);

CREATE TABLE product (
  idProduct INTEGER PRIMARY KEY AUTOINCREMENT,
  price DECIMAL NOT NULL,
  libelle TEXT NOT NULL,
  image Text NOT NULL
);

CREATE TABLE product_command (
  idcommand INTEGER,
  idProduct INTEGER,
  quantity INTEGER NOT NULL,
  PRIMARY KEY (idcommand,idProduct),
  FOREIGN KEY (idcommand) REFERENCES command (idcommand),
  FOREIGN KEY (idProduct) REFERENCES product (idProduct)
);


-- insertion of data for the test

INSERT INTO customer (name, firstname, adress, phone, username, password)
VALUES
('Rébecca', 'Armand', '18 rue Federico Garcia, Grenoble', '04349560', 'toule','Toulel97'),
('Issa', 'Fall', '11 Rue Maurice, Lyon', '08223847', 'toule2' ,'Toulel97'),
('Hilaire', 'Savary', '30 Rue Colibris, Paris', '0784048322', 'toule3', 'Toulel97');

INSERT INTO product (price, libelle,image)
VALUES
(10,'Vin','/static/img/1.jpg'),
(50,'Poulet','/static/img/2.jpg'),
(40,'ordiAllumetes','/static/img/3.jpg'),
(2.4,'tarte feuilletée','/static/img/4.jpg'),
(3.4,'fond de champignons','/static/img/5.jpg'),
(1,'haricots verts Bonduelle','/static/img/6.jpg'),
(5,'chocolats Reveillon','/static/img/7.jpg'),
(5,'pops KitKat','/static/img/8.jpg'),
(4,'chips Pringles','/static/img/9.jpg'),
(15,'champagne','/static/img/10.jpg'),
(4,'bonbons Candies & Co','/static/img/11.jpg'),
(1.5,'conconbre de Martinique','/static/img/12.jpg'),
(3,'poireaux Carrefour Bio','/static/img/13.jpg'),
(5,'mini eggs After Eight','/static/img/14.jpg'),
(5,'saucisses Les Occitanes','/static/img/15.jpg');

INSERT INTO command (idcustomer, commanddate)
VALUES
(1,'2021-02-12'),
(2,'2022-01-02'),
(1,'2023-09-02');



