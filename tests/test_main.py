def test_main(client, reset_backend):
    response = client.get("/ping")
    data = response.json()
    assert data == {"message": "pong"}
