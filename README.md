# Sistema de Riego - UNRC

Sistema web para gestionar el riego de calles de tierra en las vecinales de
Río Cuarto. Permite a los empleados de la Municipalidad ver el progreso de los
camiones regadores: recorridos, porcentaje de cumplimiento por calle, estado de
la flota y estadísticas.

Proyecto de extensión de la Universidad Nacional de Río Cuarto (UNRC), junto con
la Municipalidad de Río Cuarto.

## Estructura

- `backend/`: aplicación Flask (`app.py`), `Dockerfile` y `requirements.txt`.
- `frontend/`: plantillas Jinja2 (`templates/`) y archivos estáticos (`static/`).
- `database/`: script SQL de inicialización (`init.sql`).
- `docker-compose.yml`: define los servicios `db` y `web`.
- `.env.example`: plantilla de variables de entorno.

## Requisitos

- Docker y Docker Compose.

## Ejecucion del sistema

1. Copiar la plantilla de variables de entorno:

   cp .env.example .env

2. Levantar el proyecto desde la raíz:

   docker compose up --build o docker-compose up --build

3. Abrir http://localhost:5000.

Las siguientes veces alcanza con `docker compose up` o `docker-compose up`. Solo hace falta `--build` cuando cambian `requirements.txt` o el `Dockerfile`.

## Base de datos

- Motor: PostgreSQL 16 con PostGIS.
- El esquema se crea automáticamente la primera vez desde
  `database/init.sql`.

Los datos persisten en el volumen `sistema_riego_data`.

- Para consultar las tablas:
  docker compose exec db psql -U app -d app_db -c "\dt"

## Comandos útiles

| Acción                        | Comando                                                     |
| ----------------------------- | ----------------------------------------------------------- |
| Levantar                      | `docker compose up` o `docker-compose up`                   |
| Levantar en segundo plano     | `docker compose up -d` o `docker-compose up -d`             |
| Apagar (conserva los datos)   | `docker compose down` o `docker-compose down`               |
| Ver logs de la app            | `docker compose logs -f web` o `docker-compose logs -f web` |
| Borrar todo, incluida la base | `docker compose down -v` o `docker-compose down -v`         |

## Diagramas

Los diagramas se encuentran en
`docs/diagrama_clases/diagrama`>. Más detalle en la documentación del equipo.
