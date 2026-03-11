import requests

# Test 1 : Vérifier le statut HTTP
def test_status_http():
    url = "https://foodish-api.com/api/"
    response = requests.get(url)
    assert response.status_code == 200  # la requête doit réussir

# Test 2 : Vérifier que le JSON contient le champ 'image'
def test_json_et_champ_image():
    url = "https://foodish-api.com/api/"
    response = requests.get(url)
    data = response.json()  # transforme la réponse en dictionnaire
    assert "image" in data        # le champ 'image' existe
    assert isinstance(data["image"], str)  # c’est une chaîne
