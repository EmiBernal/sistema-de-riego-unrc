from app.models import User, db
from werkzeug.security import check_password_hash

def test_register_exitoso(client, app):
    response = client.post("/auth/register", data={
        "nombre": "Ana",
        "apellido": "Perez",
        "email": "ana@gmail.com",
        "password": "Clave123!",
        "confirmar": "Clave123!",
        "submit": "Crear cuenta"
    }, follow_redirects = True)

    assert response.status_code == 200

    with app.app_context():
        user = db.session.execute(
            db.select(User).filter_by(email="ana@gmail.com")
        ).scalar_one_or_none()

        assert user is not None
        assert user.nombre == "Ana"
        assert user.apellido == "Perez"
        assert check_password_hash(user.password_hash, "Clave123!")


def test_register_passwords_no_coinciden(client):
    response = client.post("/auth/register", data={
        "nombre": "Maria",
        "apellido": "Lopez",
        "email": "maria@gmail.com",
        "password": "Clave123!",
        "confirmar": "OtraClave456!",
        "submit": "Crear cuenta"
    })

    assert response.status_code == 400
    assert response.data == "Formulario inválido".encode("utf-8")

def test_register_email_invalido(client, app):
    user1 = {
        "nombre": "Pedro",
        "apellido": "Gonzalez",
        "email": "pedro@example.com",
        "password": "Anio2026!!",
        "confirmar": "Anio2026!!",
        "submit": "Crear cuenta"
    }

    # Registra un usuario con email incorrecto: debe fallar
    response = client.post("/auth/register", data=user1)

    assert response.status_code == 400
    # assert "Ese email ya está registrado" in response.data.decode("utf-8") -> usar cuando se renderiza

    with app.app_context():
        usuarios = db.session.execute(db.select(User)).scalars().all()
        assert len(usuarios) == 0


def test_register_email_duplicado(client, app):
    user1 = {
        "nombre": "Ana",
        "apellido": "Perez",
        "email": "evaGomez@yahoo.com",
        "password": "Clave123!",
        "confirmar": "Clave123!",
        "submit": "Crear cuenta"
    }

    user2 = {
        "nombre": "Eva",
        "apellido": "Gomez",
        "email": "evaGomez@yahoo.com",
        "password": "Clave123!",
        "confirmar": "Clave123!",
        "submit": "Crear cuenta"
    }

    # Primer registro: se crea el usuario
    client.post("/auth/register", data=user1)

    # Segundo registro con el mismo email: debe rechazarse
    response = client.post("/auth/register", data=user2)

    assert response.status_code == 400

    with app.app_context():
        usuarios = db.session.execute(
            db.select(User).filter_by(email="evaGomez@yahoo.com")
        ).scalars().all()

        assert len(usuarios) == 1


# password demasiado corta o sin los requisitos que pidas
def test_register_password_invalidas(client):
    user1 = {
        "nombre": "Ana",
        "apellido": "Gomez",
        "email": "ana@gmail.com",
        "password": "nosirve",
        "confirmar": "nosirve",
        "submit": "Crear cuenta"
    }

    response = client.post("auth/register", data=user1)

    assert response.status_code == 400
    assert response.data == "Formulario inválido".encode("utf-8")

#campos vacíos (nombre, apellido, email, etc.)
def test_register_campos_vacios(client):
    response = client.post("/auth/register", data = {
        "nombre" : "Ana",
        "apellido" : "",
        "email" : "anaSan@gmail.com",
        "password" : "Clave123!!",
        "confirmar" : "Clave123!!",
        "submit": "Crear cuenta"
    })

    assert response.status_code == 400
    assert response.data == "Formulario inválido".encode("utf-8")

#campos con espacios o mayúsculas en el email, si normalizás