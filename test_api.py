import requests

def test_status_http():
    url = "https://foodish-api.com/api/"  # URL complète de Foodish
    response = requests.get(url)
    assert response.status_code == 200

def test_json_et_champ_image():
    url = "https://foodish-api.com/api/"
    response = requests.get(url)
    data = response.json()
    assert "image" in data
    assert isinstance(data["image"], str)
