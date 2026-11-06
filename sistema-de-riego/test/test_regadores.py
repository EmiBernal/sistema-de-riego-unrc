import pytest
from werkzeug import security
from app.extensions import db

from app.models import User, Regador


@pytest.fixture
def usuario_regador(client):
    client.post("/auth/register", data={
        "nombre": "Ana", 
        "apellido": "Perez",
        "email": "test@gmail.com",
        "password": "Clave123!",
        "confirmar": "Clave123!",
        "submit": "Crear cuenta",
    })

@pytest.fixture
def usuario_superusuario(client):
    user = User(
        nombre="Emi",
        apellido="Bernal",
        email="superusuario@example.com",
        rol="SUPERUSUARIO",
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

    assert response.status_code == 200 #Para chequear si el inicio de sesion fue exitoso

    response = client.get("/regadores/")

    assert response.status_code == 403
    assert response.get_data(as_text=True) == "Acceso restringido"

def test_listar_regadores_como_superusuario(client, usuario_superusuario):
    response = client.post("/auth/login", data={
        "email": "superusuario@example.com",
        "password": "1234"
    })

    assert response.status_code == 200 #Para chequear si el inicio de sesion fue exitoso

    response = client.get("/regadores/")

    assert response.status_code == 200 #Chequeamos que devolvio correctamente