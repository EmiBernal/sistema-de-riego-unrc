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
