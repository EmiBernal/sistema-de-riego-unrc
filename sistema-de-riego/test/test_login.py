import pytest

@pytest.fixture
def usuario(client):
    client.post("/auth/register", data={
        "nombre": "Ana", 
        "apellido": "Perez",
        "email": "test@gmail.com",
        "password": "Clave123!",
        "confirmar": "Clave123!",
        "submit": "Crear cuenta",
    })

def test_login_exitoso(client, usuario):
    response = client.post("/auth/login", data={
        "email": "test@gmail.com",
        "password": "Clave123!",
    })

    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Ok"

def test_login_email_incorrecto(client, usuario):
    response = client.post("auth/login", data = {
        "email": "test1@gmail.com",
        "password": "Clave123!"
    })

    assert response.status_code == 401
    assert response.data == "Email o contraseña incorrecta. Intente nuevamente.".encode("utf-8")

def test_login_password_incorrecto(client, usuario):
    response = client.post("/auth/login", data={
        "email": "test@gmail.com",
        "password": "Clave12!"  
    })

    assert response.status_code == 401
    assert response.data == "Email o contraseña incorrecta. Intente nuevamente.".encode("utf-8")

def test_login_campo_email_vacio(client, usuario): 
    response = client.post("/auth/login", data ={
        "email": "",
        "password": "Clave12!"  
    })

    assert response.status_code == 400
    assert response.data == "Datos incompletos".encode("utf-8")

def test_login_campo_password_vacio(client, usuario):
    response = client.post("/auth/login", data={
        "email": "test@gmail.com",
        "password": ""  
    })

    assert response.status_code == 400
    assert response.data == "Datos incompletos".encode("utf-8")