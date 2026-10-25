CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TYPE rol_usuario AS ENUM ('SUPERUSUARIO', 'REGADOR');
CREATE TYPE estado_recorrido AS ENUM ('LLUVIA', 'FERIADO', 'NORMAL');

CREATE TABLE vecinal (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    km INT NOT NULL,
    polinomio GEOMETRY(Polygon, 4326) NOT NULL
);
CREATE INDEX idx_vecinal_polinomio ON vecinal USING GIST (polinomio);

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    fecha_alta DATE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    rol rol_usuario NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE camion (
    id                 SERIAL PRIMARY KEY,
    id_vsat            INT NOT NULL UNIQUE,
    patente            VARCHAR(10) NOT NULL UNIQUE,
    vtv_venc           DATE,
    estado_luces       BOOLEAN NOT NULL DEFAULT TRUE,
    estado_frenos      BOOLEAN NOT NULL DEFAULT TRUE,
    estado_direccion   BOOLEAN NOT NULL DEFAULT TRUE,
    seguro             BOOLEAN NOT NULL DEFAULT TRUE,
    poliza             VARCHAR(100),
    condicion_mecanica VARCHAR(255),
    vecinal_id         INT NOT NULL,
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id)
);

CREATE TABLE superusuario (
    id INT PRIMARY KEY,
    FOREIGN KEY (id) REFERENCES usuario(id)
);

CREATE TABLE regador (
    usuario_id      INT PRIMARY KEY,
    dni             VARCHAR(10) NOT NULL UNIQUE,
    telefono        VARCHAR(20),
    carnet_conducir VARCHAR(255),
    info_seguro     VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

CREATE TABLE regadorvecinal (
    regador_id INT NOT NULL,
    vecinal_id INT NOT NULL,
    PRIMARY KEY (regador_id, vecinal_id),
    FOREIGN KEY (regador_id) REFERENCES regador(usuario_id),
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id)
);

CREATE TABLE deshabilitacion (
    id SERIAL PRIMARY KEY,
    fecha_inicio DATE,
    fecha_fin DATE,
    descripcion VARCHAR(255) NOT NULL,
    camion_id INT NOT NULL,
    FOREIGN KEY (camion_id) REFERENCES camion(id)
);

CREATE TABLE asignacioncamion (
    id SERIAL PRIMARY KEY,
    fecha_desde DATE,
    fecha_hasta DATE,
    id_regador INT NOT NULL,
    id_camion INT NOT NULL,
    FOREIGN KEY (id_regador) REFERENCES regador(usuario_id),
    FOREIGN KEY (id_camion) REFERENCES camion(id)
);

CREATE TABLE recorrido (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    hora_inicio TIMESTAMP,
    hora_fin TIMESTAMP,
    estado estado_recorrido NOT NULL DEFAULT 'NORMAL',
    distancia_total DOUBLE PRECISION,
    camion_id INT NOT NULL,
    regador_id INT, -- puede ser NULL por ahora
    FOREIGN KEY (camion_id) REFERENCES camion(id),
    FOREIGN KEY (regador_id) REFERENCES regador(usuario_id)
);

CREATE TABLE recorre (
    km_recorridos NUMERIC(10, 2) DEFAULT 0.0,
    vecinal_id INT NOT NULL,
    recorrido_id INT NOT NULL,
    PRIMARY KEY (vecinal_id, recorrido_id),
    FOREIGN KEY (vecinal_id) REFERENCES vecinal(id),
    FOREIGN KEY (recorrido_id) REFERENCES recorrido(id)
);