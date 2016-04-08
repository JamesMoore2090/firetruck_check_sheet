DROP DATABASE IF EXISTS truckcheck;
CREATE DATABASE  truckcheck;
\c truckcheck;
CREATE EXTENSION pgcrypto;


-- Table trucks
--------------------------------------------------------

CREATE TABLE IF NOT EXISTS truck(
  truck_id serial NOT NULL,
  truck text NOT NULL,
  PRIMARY KEY(truck_id)
);

INSERT INTO truck (truck) VALUES ('Rescue Engine 8');
INSERT INTO truck (truck) VALUES ('Engine 8');
INSERT INTO truck (truck) VALUES ('Brush 8');
INSERT INTO truck (truck) VALUES ('Tanker 8');
-- -----------------------------------------------------
-- Table usertype
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS usertype (
  usertype_id serial NOT NULL ,
  usertype text NULL,
  PRIMARY KEY (usertype_id)
);

INSERT INTO usertype (usertype) VALUES ('Driver');              -- 1
INSERT INTO usertype (usertype) VALUES ('Driver/EMT');          -- 2
INSERT INTO usertype (usertype) VALUES ('Driver/Lead FF');      -- 3
INSERT INTO usertype (usertype) VALUES ('Driver/Lead FF/EMT');  -- 4
INSERT INTO usertype (usertype) VALUES ('Driver/Officer');      -- 5
INSERT INTO usertype (usertype) VALUES ('Driver/Officer/EMT');  -- 6
INSERT INTO usertype (usertype) VALUES ('Officer');             -- 7
INSERT INTO usertype (usertype) VALUES ('Officer/EMT');         -- 8
INSERT INTO usertype (usertype) VALUES ('Firefighter');         -- 9  
INSERT INTO usertype (usertype) VALUES ('Firefighter/EMT');     -- 10
INSERT INTO usertype (usertype) VALUES ('Lead Firefighter');    -- 11
INSERT INTO usertype (usertype) VALUES ('Lead Firefighter/EMT');-- 12
INSERT INTO usertype (usertype) VALUES ('EMT/MEDIC');           -- 13
INSERT INTO usertype (usertype) VALUES ('Probie');              -- 14

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
INSERT INTO users (username, password, userType) VALUES ('officer', crypt('password', gen_salt('bf')),7);
INSERT INTO users (username, password, userType) VALUES ('Jonathan Begeant', crypt('password', gen_salt('bf')),6);
INSERT INTO users (username, password, userType) VALUES ('Mike Huffman', crypt('capt', gen_salt('bf')),6);
INSERT INTO users (username, password, userType) VALUES ('Eric McDonnel', crypt('lt', gen_salt('bf')),6);
INSERT INTO users (username, password, userType) VALUES ('John Tenda', crypt('lt', gen_salt('bf')),6);
INSERT INTO users (username, password, userType) VALUES ('Brian Wery', crypt('driver', gen_salt('bf')),3);
INSERT INTO users (username, password, userType) VALUES ('Doug McNeil', crypt('driver', gen_salt('bf')),1);
INSERT INTO users (username, password, userType) VALUES ('James Moore', crypt('password', gen_salt('bf')),4);
INSERT INTO users (username, password, userType) VALUES ('Mike ONeil', crypt('driver', gen_salt('bf')),3);
INSERT INTO users (username, password, userType) VALUES ('Tom Vickers', crypt('safety', gen_salt('bf')),6);
INSERT INTO users (username, password, userType) VALUES ('Brian Mackey', crypt('firefighter', gen_salt('bf')),12);
INSERT INTO users (username, password, userType) VALUES ('Chris Dodd', crypt('driver', gen_salt('bf')),3);
INSERT INTO users (username, password, userType) VALUES ('David Hipkins', crypt('driver', gen_salt('bf')),4);
INSERT INTO users (username, password, userType) VALUES ('Elizabeth Vickers', crypt('emt', gen_salt('bf')),13);
INSERT INTO users (username, password, userType) VALUES ('Jon Young', crypt('firefighter', gen_salt('bf')),12);
INSERT INTO users (username, password, userType) VALUES ('Kim Moore', crypt('emt', gen_salt('bf')),13);
INSERT INTO users (username, password, userType) VALUES ('Marc Smith', crypt('password', gen_salt('bf')),9);
INSERT INTO users (username, password, userType) VALUES ('Michele Walker-Reaves', crypt('firefighter', gen_salt('bf')),12);
INSERT INTO users (username, password, userType) VALUES ('Shawn Nunez', crypt('probie', gen_salt('bf')),14);
INSERT INTO users (username, password, userType) VALUES ('Brian Bethea', crypt('firefighter', gen_salt('bf')),9);
INSERT INTO users (username, password, userType) VALUES ('Bryan Houff', crypt('firefighter', gen_salt('bf')),11);
INSERT INTO users (username, password, userType) VALUES ('Ryan Harper', crypt('firefighter', gen_salt('bf')),11);
INSERT INTO users (username, password, userType) VALUES ('Ryan Parent', crypt('firefighter', gen_salt('bf')),11);
INSERT INTO users (username, password, userType) VALUES ('Chris Rezendes', crypt('probie', gen_salt('bf')),14);
-- -----------------------------------------------------
-- Table brush_truck
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS brush_truck (
  brush_truck_id serial NOT NULL ,
  truck INT NOT NULL,
  check_date DATE NULL,
  driver INT NOT NULL,
  officer INT NOT NULL,
  miles INT NOT NULL,
  fuel text NULL,
  hours text NULL,
  
  mapbook BOOLEAN NULL,
  headlights BOOLEAN NULL,
  turnsignals BOOLEAN NULL,
  portableradio text NULL,
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
  
  PRIMARY KEY (brush_truck_id),
    FOREIGN KEY (driver) REFERENCES Users (user_id),
    FOREIGN KEY (truck) REFERENCES truck (truck_id)
);





-- -----------------------------------------------------
-- Table engine
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS engine (
  engine_id serial NOT NULL ,
  truck INT NOT NULL,
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
    FOREIGN KEY (officer) REFERENCES Users (user_id),
    FOREIGN KEY (truck) REFERENCES truck (truck_id)
);


-- -----------------------------------------------------
-- Table checksheet
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS checksheet (
  check_id serial NOT NULL ,
  user_id INT NOT NULL,
  officerApproval BOOLEAN NULL,
  engine_id INT NULL,
  brush_id INT NULL,
  truck INT NULL,
  PRIMARY KEY (check_id),
    FOREIGN KEY (brush_id) REFERENCES brush_truck (brush_truck_id),
    FOREIGN KEY (engine_id) REFERENCES engine (engine_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (truck) REFERENCES truck (truck_id)
);

