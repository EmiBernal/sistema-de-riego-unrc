import os
import requests
from shapely.geometry import Polygon
from geoalchemy2.shape import from_shape


class VSATError(Exception):
    pass


def _get(path, mensaje_error):
    base_url = os.getenv("VSAT_BASE_URL", "https://vsateq.com.ar/vsat/api/v.1")
    token = os.getenv("VSAT_TOKEN")
    app_id = os.getenv("VSAT_APP_ID")

    if not token or not app_id:
        raise VSATError("Faltan configurar los datos de VSAT en el .env")

    url = f"{base_url}/applications/{app_id}/{path}"
    headers = {"Authorization": token, "Accept": "application/json"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            raise VSATError("Token de VSAT inválido o vencido.") from e
        raise VSATError(mensaje_error) from e
    except (requests.RequestException, ValueError) as e:
        raise VSATError(mensaje_error) from e


def obtener_geocercas_vsat():
    data = _get("geofences", "No se pudo conectar con la API de VSAT.")
    return [g for g in data if g.get("shapeType") == "Polygon"]


def obtener_geocerca_por_id(geofence_id):
    return _get(f"geofences/{geofence_id}", "No se pudo traer la geocerca seleccionada desde VSAT.")


def vertices_a_postgis(geocerca_json):
    vertices = geocerca_json.get("polygonShape", {}).get("vertices", [])
    if len(vertices) < 3:
        raise VSATError("La geocerca no tiene suficientes puntos para armar un polígono.")

    coords = [(v["longitude"], v["latitude"]) for v in vertices]
    if coords[0] != coords[-1]:
        coords.append(coords[0])

    poligono = Polygon(coords)
    if not poligono.is_valid:
        raise VSATError("La geometría de la geocerca es inválida.")

    return from_shape(poligono, srid=4326)