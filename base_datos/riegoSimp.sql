DROP DATABASE IF EXISTS riego;
CREATE DATABASE riego CHARACTER SET utf8mb4;
USE riego;

DROP TABLE IF EXISTS vecinal;
CREATE TABLE vecinal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    km INT NOT NULL,
    polinomio POLYGON NOT NULL SRID 4326,
    SPATIAL INDEX (polinomio) --vamos viendo
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
    descripcion VARCHAR(255) NOT NULL,
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
    estado ENUM('LLUVIA','FERIADO','NORMAL') NOT NULL DEFAULT 'NORMAL',
    distancia_total DOUBLE,
    camion_id INT NOT NULL,
    regador_id INT, -- puede ser NULL por ahora (participacion parcial en conduce)
    FOREIGN KEY (camion_id) REFERENCES camion(id),
    FOREIGN KEY (regador_id) REFERENCES regador(usuario_id)
);

DROP TABLE IF EXISTS recorre;
CREATE TABLE recorre (
    km_recorridos DECIMAL DEFAULT 0.0,
    vecinal_id INT NOT NULL,
    recorrido_id INT NOT NULL,
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id),
    FOREIGN KEY (recorrido_id) REFERENCES recorrido(id)
);