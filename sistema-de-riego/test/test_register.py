from app.models import User, db
from werkzeug.security import check_password_hash

def test_register_exitoso(client, app):
    response = client.post("/auth/register", data={
        "nombre": "Ana",
        "apellido": "Perez",
        "email": "ana@example.com",
        "password": "Clave123!",
        "confirmar": "Clave123!",
        "submit": "Crear cuenta"
    }, follow_redirects = True)

    assert response.status_code == 200

    with app.app_context():
        user = db.session.execute(
            db.select(User).filter_by(email="ana@example.com")
        ).scalar_one_or_none()

        assert user is not None
        assert user.nombre == "Ana"
        assert user.apellido == "Perez"
        assert check_password_hash(user.password_hash, "Clave123!")


def test_register_passwords_no_coinciden(client):
    response = client.post("/auth/register", data={
        "nombre": "Maria",
        "apellido": "Lopez",
        "email": "maria@example.com",
        "password": "Clave123!",
        "confirmar": "OtraClave456!",
        "submit": "Crear cuenta"
    })

    assert response.status_code == 400
    assert response.data == "Formulario inválido".encode("utf-8")
   