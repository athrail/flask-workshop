DELETE FROM clients;
INSERT INTO clients (full_name, email, phone) VALUES
  ('Christian Slater', 'mail@slater.com', 12312323),
  ('Grzegorz Brzęczyszczykiewicz', 'grzech@wp.pl', 12312324);

DELETE FROM makers;
INSERT INTO makers (name) VALUES ('FSO'), ('Skoda'), ('Ford'), ('Opel');

DELETE FROM models;
INSERT INTO models (name, production_start, production_end, maker_id) VALUES
  ('Warszawa', 1951, 1973, 1),
  ('Syrena', 1952, 1972, 1),
  ('Polonez', 1978, 2003, 1),
  ('Daewoo Lanos', 2004, 2008, 1),
  ('Scala', 2008, 2025, 2);

DELETE FROM cars;
INSERT INTO cars (plate, owner_id, maker_id, model_id) VALUES
  ('GA 411HU', 1, 2, 5),
  ('SK 1234', 2, 1, 1);
