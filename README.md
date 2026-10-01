# Sistema de Riego - UNRC

Sistema web para gestionar el riego de calles de tierra en las vecinales de
Río Cuarto. Permite a los empleados de la Municipalidad ver el progreso de los
camiones regadores: recorridos, porcentaje de cumplimiento por calle, estado de
la flota y estadísticas.

Proyecto de extensión de la Universidad Nacional de Río Cuarto (UNRC), junto con
la Municipalidad de Río Cuarto.

## Estructura

- `base_datos/`: script SQL, `docker-compose.yml` y diagramas (DER Chen,
  Crow's Foot y de clases).

## Levantar la base de datos

Requiere Docker. Desde la carpeta `base_datos/`:

    docker compose up -d

La base queda disponible en `127.0.0.1:3307` (usuario `riego`, base `riego`).
Más detalle en la documentación del equipo.
