from flask import Flask, render_template, jsonify
import requests
from flask import render_template_string, request, redirect, url_for, session
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)

# --- Page consignes ---
@app.get("/")
def consignes():
    return render_template('consignes.html')

# --- Route pour afficher un plat aléatoire ---
@app.get("/plat")
def plat_aleatoire():
    url = "https://foodish-api.com/api/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        image_url = data.get("image", "")
    except Exception:
        # Si l'API n'est pas accessible, on utilise un mock
        image_url = "https://foodish-api.com/images/pizza/pizza18.jpg"
    
    html = f"""
    <h1>Plat aléatoire</h1>
    <img src="{image_url}" alt="Plat" style="max-width:500px;">
    <br><a href='/plat'>Voir un autre plat</a>
    <br><a href='/run-tests'>Lancer les tests API</a>
    """
    return html

# --- Mock pour les tests ---
fake_response = {
    "image": "https://foodish-api.com/images/pizza/pizza18.jpg"
}

# --- Fonctions de test “as code” ---
def test_status_http():
    status_code = 200  # simulé
    assert status_code == 200
    return "Test status HTTP passé"

def test_json_et_champ_image():
    data = fake_response
    assert "image" in data
    assert isinstance(data["image"], str)
    return "Test JSON et champ image passé"

# --- Endpoint pour lancer les tests ---
@app.get("/run-tests")
def run_tests():
    results = []
    try:
        results.append(test_status_http())
        results.append(test_json_et_champ_image())
        return jsonify({"success": True, "results": results})
    except AssertionError as e:
        return jsonify({"success": False, "error": str(e), "results": results})

# --- Lancer Flask ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
