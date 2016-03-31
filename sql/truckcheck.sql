DROP DATABASE IF EXISTS truckcheck;
CREATE DATABASE  truckcheck;
\c truckcheck;
CREATE EXTENSION pgcrypto;

-- -----------------------------------------------------
-- Table usertype
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usertype (
  usertype_id serial NOT NULL ,
  usertype text NULL,
  PRIMARY KEY (usertype_id)
);

INSERT INTO usertype (usertype) VALUES ('Driver');
INSERT INTO usertype (usertype) VALUES ('Driver/Officer');
INSERT INTO usertype (usertype) VALUES ('Officer');
INSERT INTO usertype (usertype) VALUES ('Firefighter');
INSERT INTO usertype (usertype) VALUES ('Probie');

-- -----------------------------------------------------
-- Table .Users
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Users (
  user_id serial NOT NULL ,
  username text NOT NULL,
  password text NOT NULL,
  userType INT NOT NULL,
  PRIMARY KEY (user_id),
    FOREIGN KEY (userType) REFERENCES usertype (usertype_id)
);

INSERT INTO users (username, password, userType) VALUES ('driver', crypt('password', gen_salt('bf')),1);
INSERT INTO users (username, password, userType) VALUES ('officer', crypt('password', gen_salt('bf')),3);

-- -----------------------------------------------------
-- Table brush_truck
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS brush_truck (
  brush_truck_id serial NOT NULL ,
  driver INT NOT NULL,
  miles INT NOT NULL,
  fuel text NULL,
  mapbook text NULL,
  headlights BOOLEAN NULL,
  turnsignals BOOLEAN NULL,
  radiocheck BOOLEAN NULL,
  portableradio BOOLEAN NULL,
  emlights BOOLEAN NULL,
  spotlight BOOLEAN NULL,
  waterLevel text NULL,
  foamlevel text NULL,
  hoses BOOLEAN NULL,
  pumpOperation BOOLEAN NULL,
  handtools BOOLEAN NULL,
  chainsaw BOOLEAN NULL,
  wench BOOLEAN NULL,
  Notes text NULL,
  check_date DATE NULL,
  PRIMARY KEY (brush_truck_id),
    FOREIGN KEY (driver) REFERENCES Users (user_id)
);





-- -----------------------------------------------------
-- Table engine
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS engine (
  engine_id serial NOT NULL ,
  truck text NOT NULL,
  check_date DATE NULL,
  driver INT NOT NULL,
  officer INT NOT NULL,
  miles text NULL,
  hours text NULL,
  fuel text NULL,
  
  fuelcard BOOLEAN NULL,
  headlights BOOLEAN NULL,
  turnsignals BOOLEAN NULL,
  markerlights BOOLEAN NULL,
  warninglights BOOLEAN NULL,
  sirens BOOLEAN NULL,
  airhorn BOOLEAN NULL,
  tires BOOLEAN NULL,
  
  pumpOperation BOOLEAN NULL,
  waterlevel text NULL,
  foamlevel text NULL,
  generator BOOLEAN NULL,
  scenelights BOOLEAN NULL,
  
  helmetmarkers BOOLEAN NULL,
  portableradio text NULL,
  passport BOOLEAN NULL,
  commandboard BOOLEAN NULL,
  erg BOOLEAN NULL,
  mapbook BOOLEAN NULL,
  headsets BOOLEAN NULL,
  forms BOOLEAN NULL,
  
  thermalimager BOOLEAN NULL,
  paktracker BOOLEAN NULL,
  ladders BOOLEAN NULL,
  gasmonitor text NULL,
  handlights text NULL,
  binoculars BOOLEAN NULL,
  smokedetectors text NULL,
  batteries text NULL,
  SCBA text NULL,
  ritpack BOOLEAN NULL,
  roadflares text NULL,
  eroadflares text NULL,
  hoses BOOLEAN NULL,
  appliances BOOLEAN NULL,
  roadsign BOOLEAN NULL,
  absorbant BOOLEAN NULL,
  handtools BOOLEAN NULL,
  sawzall BOOLEAN NULL,
  chimneykit BOOLEAN NULL,
  saws BOOLEAN NULL,
  extinguishers BOOLEAN NULL,
  fans BOOLEAN NULL,
  spillcont BOOLEAN NULL,
  salvage BOOLEAN NULL,
  lifeline BOOLEAN NULL,
  utilityrope BOOLEAN NULL,
  rigging BOOLEAN NULL,
  pikepoles BOOLEAN NULL,
  electicalequip BOOLEAN NULL,
  hondalight BOOLEAN NULL,
  cribbing BOOLEAN NULL,
  spreaders BOOLEAN NULL,
  ocutters BOOLEAN NULL,
  hydropump BOOLEAN NULL,
  paratech BOOLEAN NULL,
  lchannel BOOLEAN NULL,
  portaPump BOOLEAN NULL,
  airbagcontroler BOOLEAN NULL,
  airbags BOOLEAN NULL,
  
  jumpbag BOOLEAN NULL,
  o2level text NULL,
  spareo2 BOOLEAN NULL,
  collarbag BOOLEAN NULL,
  gloves BOOLEAN NULL,
  clipboard BOOLEAN NULL,
  suckunit BOOLEAN NULL,
  triagebag BOOLEAN NULL,
  lifepak text NULL,
  toughbook BOOLEAN NULL,
  
  notes text NULL,

  PRIMARY KEY (engine_id),
    FOREIGN KEY (driver) REFERENCES Users (user_id),
    FOREIGN KEY (officer) REFERENCES Users (user_id)
);


-- -----------------------------------------------------
-- Table checksheet
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS checksheet (
  check_id serial NOT NULL ,
  user_id INT NOT NULL,
  officerApproval BOOLEAN NULL,
  engine INT NULL,
  brush INT NULL,
  PRIMARY KEY (check_id),
    FOREIGN KEY (brush) REFERENCES brush_truck (brush_truck_id),
    FOREIGN KEY (engine) REFERENCES engine (engine_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

