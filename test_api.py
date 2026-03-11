import requests


/On va créer une fonction de test pour vérifier le statut http et que l’API répond bien avec le code 200.
def test_status_http():
    url = "https://foodish-api.com/api/"  # endpoint aléatoire
    response = requests.get(url)           # on envoie la requête GET
    
    # Vérifier le statut HTTP
    assert response.status_code == 200


/vérifier que la réponse est bien du JSON et contient le champ image
def test_json_et_champ_image():
    url = "https://foodish-api.com/api/"  # endpoint aléatoire
    response = requests.get(url)
    
    # Vérifier que la réponse est du JSON
    data = response.json()  # convertit la réponse en dictionnaire Python
    
    # Vérifier que le champ 'image' existe
    assert "image" in data
    
    # Vérifier que le champ 'image' est une chaîne de caractères
    assert isinstance(data["image"], str)
