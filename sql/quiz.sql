DROP DATABASE IF EXISTS quiz;
CREATE DATABASE  quiz;
\c quiz;
CREATE EXTENSION pgcrypto;

-- -----------------------------------------------------
-- Table userstype
-- -----------------------------------------------------
DROP TABLE IF EXISTS userstype ;

CREATE TABLE IF NOT EXISTS userstype (
  id serial NOT NULL ,
  userstype text NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO userstype (usersType) VALUES ('admin'),('users');

-- -----------------------------------------------------
-- Table class
-- -----------------------------------------------------
DROP TABLE IF EXISTS class ;

CREATE TABLE IF NOT EXISTS class (
  id_class serial NOT NULL ,
  class text NOT NULL,
  PRIMARY KEY (id_class)
);


-- -----------------------------------------------------
-- Table users
-- -----------------------------------------------------
DROP TABLE IF EXISTS users ;

CREATE TABLE IF NOT EXISTS users (
  id_users serial NOT NULL ,
  usersname text NOT NULL,
  password text NOT NULL,
  userstype INT NOT NULL DEFAULT 2,
  class INT NULL,
  PRIMARY KEY (id_users),
    FOREIGN KEY (class) REFERENCES class (id_class),
    FOREIGN KEY (userstype) REFERENCES userstype (id)
);

INSERT INTO users (usersname , password,userstype) VALUES
('admin', crypt('password', gen_salt('bf')),1),
('user', crypt('password', gen_salt('bf')),2);

-- -----------------------------------------------------
-- Table book
-- -----------------------------------------------------
DROP TABLE IF EXISTS book ;

CREATE TABLE IF NOT EXISTS book (
  id_book serial NOT NULL ,
  book text NOT NULL,
  class INT NOT NULL,
  PRIMARY KEY (id_book),
    FOREIGN KEY (class)REFERENCES class (id_class)
);


-- -----------------------------------------------------
-- Table chapter
-- -----------------------------------------------------
DROP TABLE IF EXISTS chapter ;

CREATE TABLE IF NOT EXISTS chapter (
  id_chapter serial NOT NULL ,
  chapter text NOT NULL,
  book INT NOT NULL,
  PRIMARY KEY (id_chapter),
    FOREIGN KEY (book) REFERENCES book (id_book)
);


-- -----------------------------------------------------
-- Table question
-- -----------------------------------------------------
DROP TABLE IF EXISTS question ;

CREATE TABLE IF NOT EXISTS question (
  id_question serial NOT NULL ,
  question text NOT NULL,
  chapter INT NOT NULL,
  PRIMARY KEY (id_question),
    FOREIGN KEY (chapter) REFERENCES chapter (id_chapter)
);

-- -----------------------------------------------------
-- Table answer
-- -----------------------------------------------------
DROP TABLE IF EXISTS answer ;

CREATE TABLE IF NOT EXISTS answer (
  id_answer serial NOT NULL ,
  answer text NOT NULL,
  correct boolean NOT NULL,
  question INT NOT NULL,
  PRIMARY KEY (id_answer),
    FOREIGN KEY (question) REFERENCES question (id_question)
);

-- -----------------------------------------------------
-- Table answer
-- -----------------------------------------------------
DROP TABLE IF EXISTS test ;

CREATE TABLE IF NOT EXISTS test (
  id_test serial NOT NULL ,
  question1 int NULL,
  correct boolean NOT NULL,
  question INT NOT NULL,
  PRIMARY KEY (id_test),
    FOREIGN KEY (question1) REFERENCES question (id_question)
);
