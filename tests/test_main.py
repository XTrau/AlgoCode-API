def test_main(client, reset_database):
    response = client.get("/ping")
    data = response.json()
    assert data == {"message": "pong"}
