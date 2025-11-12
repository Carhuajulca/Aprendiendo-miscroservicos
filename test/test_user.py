


def test_crear_usuario(client):
    data = {
        "nombre": "Juan",
        "email": "juan@example.com",
        "edad": 25,
        "password": "123456"
    }

    response = client.post("/users/", json=data)
    assert response.status_code == 200  # o 201 si lo configuraste así
    body = response.json()
    assert body["nombre"] == "Juan"
    assert body["email"] == "juan@example.com"


def test_listar_usuarios(client):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
