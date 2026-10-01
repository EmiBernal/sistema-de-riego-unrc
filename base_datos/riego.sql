DROP DATABASE IF EXISTS riego;
CREATE DATABASE riego CHARACTER SET utf8mb4;
USE riego;

DROP TABLE IF EXISTS vecinal;
CREATE TABLE vecinal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_alta DATE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    rol ENUM('SUPERUSUARIO','REGADOR') NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS geocerca;
CREATE TABLE geocerca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_vsat INT NOT NULL UNIQUE,
    nombre VARCHAR(255) NOT NULL,
    min_x      DOUBLE NOT NULL,
    max_x      DOUBLE NOT NULL,
    min_y      DOUBLE NOT NULL,
    max_y      DOUBLE NOT NULL,
    vecinal_id INT NOT NULL UNIQUE, -- es una relacion 1:1
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id)
);

DROP TABLE IF EXISTS coordenada;
CREATE TABLE coordenada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    longitud DOUBLE NOT NULL,
    latitud DOUBLE NOT NULL,
    orden INT NOT NULL,
    geocerca_id INT NOT NULL, -- es una relacion 1:N. Siempre se pone del lado de N
    FOREIGN KEY (geocerca_id) REFERENCES geocerca(id)
);

DROP TABLE IF EXISTS calle;
CREATE TABLE calle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipo ENUM('TIERRA','PAVIMENTADA','SIN_CLASIFICAR') NOT NULL DEFAULT 'SIN_CLASIFICAR',
    pasa_colectivo BOOL NOT NULL DEFAULT FALSE,
    vecinal_id INT NOT NULL, -- es una relacion 1:N. Siempre se pone del lado de N
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id)
);

DROP TABLE IF EXISTS camion;
CREATE TABLE camion (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    id_vsat            INT NOT NULL UNIQUE,
    patente            VARCHAR(10) NOT NULL UNIQUE,
    vtv_venc           DATE,
    estado_luces       BOOLEAN NOT NULL DEFAULT TRUE, -- verificar si el estado es un boolean
    estado_frenos      BOOLEAN NOT NULL DEFAULT TRUE,
    estado_direccion   BOOLEAN NOT NULL DEFAULT TRUE,
    seguro             BOOLEAN NOT NULL DEFAULT TRUE,
    poliza             VARCHAR(100),
    condicion_mecanica VARCHAR(255),
    vecinal_id         INT NOT NULL,
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id)
);

DROP TABLE IF EXISTS superusuario;
CREATE TABLE superusuario (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES usuario(id)
);

DROP TABLE IF EXISTS regador;
CREATE TABLE regador (
  usuario_id      INT PRIMARY KEY,
  dni             VARCHAR(10) NOT NULL UNIQUE,
  telefono        VARCHAR(20),
  carnet_conducir VARCHAR(255),
  info_seguro     VARCHAR(255),
  FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

DROP TABLE IF EXISTS regadorvecinal;
CREATE TABLE regadorvecinal (
    regador_id INT NOT NULL,
    vecinal_id INT NOT NULL,
    PRIMARY KEY (regador_id, vecinal_id),
    FOREIGN KEY (regador_id) REFERENCES regador(usuario_id),
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id)
);

DROP TABLE IF EXISTS deshabilitacion;
CREATE TABLE deshabilitacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_inicio DATE,
    fecha_fin DATE,
    motivo VARCHAR(255) NOT NULL,
    camion_id INT NOT NULL,
    FOREIGN KEY (camion_id) REFERENCES camion(id)
);

DROP TABLE IF EXISTS asignacioncamion;
CREATE TABLE asignacioncamion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_desde DATE,
    fecha_hasta DATE,
    id_regador INT NOT NULL,
    id_camion INT NOT NULL,
    FOREIGN KEY (id_regador) REFERENCES regador(usuario_id),
    FOREIGN KEY (id_camion) REFERENCES camion(id)
);

DROP TABLE IF EXISTS recorrido;
CREATE TABLE recorrido (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE,
    hora_inicio DATETIME,
    hora_fin DATETIME,
    distancia_total DOUBLE,
    camion_id INT NOT NULL,
    regador_id INT, -- puede ser NULL por ahora (participacion parcial en conduce)
    FOREIGN KEY (camion_id) REFERENCES camion(id),
    FOREIGN KEY (regador_id) REFERENCES regador(usuario_id)
);

DROP TABLE IF EXISTS pasoporcalle;
CREATE TABLE pasoporcalle (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora_que_paso DATETIME,
    duracion_en_calle DOUBLE,
    recorrido_id INT NOT NULL,
    calle_id INT NOT NULL,
    FOREIGN KEY (recorrido_id) REFERENCES recorrido(id),
    FOREIGN KEY (calle_id) REFERENCES calle(id)
);
