import pytest
from werkzeug import security
from app.extensions import db

from app.models import User, Regador


@pytest.fixture
def usuario_regador(client):
    user = User(
        nombre="Ana",
        apellido="Perez",
        email="test@gmail.com",
        rol="USUARIO",
        estado="APROBADO",
        password_hash=security.generate_password_hash("Clave123!")
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def usuario_administrador(client):
    user = User(
        nombre="Emi",
        apellido="Bernal",
        email="administrador@example.com",
        rol="ADMINISTRADOR",
        estado="APROBADO",
        password_hash=security.generate_password_hash("1234")
    )
    db.session.add(user)
    db.session.commit()
    return user

def test_lista_regadores_sin_login(client):
    response = client.get("/regadores/")
    assert response.status_code == 401
    assert response.get_data(as_text=True) == "No autorizado"

def test_listar_regadores_como_regador(client, usuario_regador):
    response = client.post("/auth/login", data={
        "email": "test@gmail.com",
        "password": "Clave123!"
    })

    assert response.status_code == 302 #Para chequear si el inicio de sesion fue exitoso

    response = client.get("/regadores/")

    assert response.status_code == 403
    assert response.get_data(as_text=True) == "Acceso restringido"

def test_listar_regadores_como_administrador(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    assert response.status_code == 302 #Para chequear si el inicio de sesion fue exitoso

    response = client.get("/regadores/")

    assert response.status_code == 200 #Chequeamos que devolvio correctamente

def test_crear_regador_sin_login(client):
    response = client.post("/regadores/crear-regador")
    assert response.status_code == 401
    assert response.get_data(as_text=True) == "No autorizado"

def test_crear_regador_como_usuario(client, usuario_regador):
    response = client.post("/auth/login", data={
            "email": "test@gmail.com",
            "password": "Clave123!"
    })
    response = client.post('/regadores/crear-regador')
    assert response.status_code == 403
    assert response.get_data(as_text=True) == "Acceso restringido"

def test_crear_regador_como_administrador(client, usuario_administrador):
    response = client.post("/auth/login", data={
            "email": "administrador@example.com",
            "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@gmail.com",
        "password": "Clave123!",
        "dni": "12345678",
        "telefono": "1234567890"
    })

    assert response.status_code == 201

    datos = response.get_json()
    regador = db.session.get(Regador, datos["id"])

    assert regador is not None
    assert regador.usuario.nombre == "Juan"
    assert regador.dni == "12345678"
    assert regador.usuario.rol == "USUARIO"
    assert regador.usuario.estado == "APROBADO"


def test_crear_regador_dni_repetido(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
           "nombre": "Juan",
           "apellido": "Perez",
           "email": "juan@gmail.com",
           "password": "Clave123!",
           "dni": "12345678",
           "telefono": "1234567890"
    })

    assert response.status_code == 201

    response = client.post('/regadores/crear-regador', data={
               "nombre": "Pepe",
               "apellido": "Dominguez",
               "email": "Pepe@gmail.com",
               "password": "Clave123!",
               "dni": "12345678",
               "telefono": "48394792834"
    })

    assert response.status_code == 409

def test_crear_regador_email_repetido(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
           "nombre": "Juan",
           "apellido": "Perez",
           "email": "juan@gmail.com",
           "password": "Clave123!",
           "dni": "12345678",
           "telefono": "1234567890"
    })

    assert response.status_code == 201

    response = client.post('/regadores/crear-regador', data={
               "nombre": "Pepe",
               "apellido": "Dominguez",
               "email": "juan@gmail.com",
               "password": "Clave123!",
               "dni": "4893084",
               "telefono": "48394792834"
    })

    assert response.status_code == 409

def test_crear_regador_dni_letras(client, usuario_administrador):
    response = client.post("/auth/login", data={
            "email": "administrador@example.com",
            "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@gmail.com",
        "password": "Clave123!",
        "dni": "234kd53d",
        "telefono": "1234567890"
    })

    assert response.status_code == 400

    assert "dni" in response.get_json()

def test_buscar_regador_sin_login(client):
    response = client.get("/regadores/buscar-regador/1")
    assert response.status_code == 401
    assert response.get_data(as_text=True) == "No autorizado"

def test_buscar_regador_como_usuario(client, usuario_regador):
    response = client.post("/auth/login", data={
        "email": "test@gmail.com",
        "password": "Clave123!"
    })
    response = client.get("/regadores/buscar-regador/1")
    assert response.status_code == 403
    assert response.get_data(as_text=True) == "Acceso restringido"

def test_buscar_regador_como_administrador(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@gmail.com",
        "password": "Clave123!",
        "dni": "12345678",
        "telefono": "1234567890"
    })

    assert response.status_code == 201

    id_regador = response.get_json()["id"]
    response = client.get(f"/regadores/buscar-regador/{id_regador}")

    assert response.status_code == 200

    datos = response.get_json()
    assert datos["nombre"] == "Juan"
    assert datos["dni"] == "12345678"
    assert datos["telefono"] == "1234567890"

def test_buscar_regador_inexistente(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.get("/regadores/buscar-regador/9999")
    assert response.status_code == 404

def test_editar_regador_sin_login(client):
    response = client.post("/regadores/editar-regador/1")
    assert response.status_code == 401
    assert response.get_data(as_text=True) == "No autorizado"

def test_editar_regador_como_usuario(client, usuario_regador):
    response = client.post("/auth/login", data={
        "email": "test@gmail.com",
        "password": "Clave123!"
    })
    response = client.post("/regadores/editar-regador/1")
    assert response.status_code == 403
    assert response.get_data(as_text=True) == "Acceso restringido"

def test_editar_regador_como_administrador(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@gmail.com",
        "password": "Clave123!",
        "dni": "12345678",
        "info_seguro": "Seguro X"
    })

    assert response.status_code == 201

    id_regador = response.get_json()["id"]
    response = client.post(f"/regadores/editar-regador/{id_regador}", data={
        "nombre": "Pedro",
        "telefono": "1234567890"
    })

    assert response.status_code == 200

    regador = db.session.get(Regador, id_regador)

    assert regador.usuario.nombre == "Pedro"
    assert regador.telefono == "1234567890"
    assert regador.usuario.apellido == "Perez"
    assert regador.dni == "12345678"
    assert regador.info_seguro == "Seguro X"

def test_editar_regador_inexistente(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post("/regadores/editar-regador/9999", data={
        "nombre": "Pedro"
    })
    assert response.status_code == 404

def test_editar_regador_dni_letras(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@gmail.com",
        "password": "Clave123!",
        "dni": "12345678"
    })

    assert response.status_code == 201

    id_regador = response.get_json()["id"]
    response = client.post(f"/regadores/editar-regador/{id_regador}", data={
        "dni": "234kd53d"
    })

    assert response.status_code == 400

    assert "dni" in response.get_json()

def test_editar_regador_dni_repetido(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@gmail.com",
        "password": "Clave123!",
        "dni": "12345678"
    })

    assert response.status_code == 201

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Pepe",
        "apellido": "Dominguez",
        "email": "pepe@gmail.com",
        "password": "Clave123!",
        "dni": "4893084"
    })

    assert response.status_code == 201

    id_regador = response.get_json()["id"]
    response = client.post(f"/regadores/editar-regador/{id_regador}", data={
        "dni": "12345678"
    })

    assert response.status_code == 409

def test_eliminar_regador_sin_login(client):
    response = client.post("/regadores/eliminar-regador/1")
    assert response.status_code == 401
    assert response.get_data(as_text=True) == "No autorizado"

def test_eliminar_regador_como_usuario(client, usuario_regador):
    response = client.post("/auth/login", data={
        "email": "test@gmail.com",
        "password": "Clave123!"
    })
    response = client.post("/regadores/eliminar-regador/1")
    assert response.status_code == 403
    assert response.get_data(as_text=True) == "Acceso restringido"

def test_eliminar_regador_como_administrador(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post('/regadores/crear-regador', data={
        "nombre": "Juan",
        "apellido": "Perez",
        "email": "juan@gmail.com",
        "password": "Clave123!",
        "dni": "12345678"
    })

    assert response.status_code == 201

    id_regador = response.get_json()["id"]
    response = client.post(f"/regadores/eliminar-regador/{id_regador}")

    assert response.status_code == 204

    assert db.session.get(Regador, id_regador) is None
    assert db.session.get(User, id_regador) is None 

def test_eliminar_regador_inexistente(client, usuario_administrador):
    response = client.post("/auth/login", data={
        "email": "administrador@example.com",
        "password": "1234"
    })

    response = client.post("/regadores/eliminar-regador/9999")
    assert response.status_code == 404
