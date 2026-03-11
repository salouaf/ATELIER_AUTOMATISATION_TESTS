from flask import Flask, render_template, jsonify
import requests
from flask import render_template_string, request, redirect, url_for, session
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
import requests
import time

app = Flask(__name__)

# URL de l'API choisie
API_URL = "https://foodish-api.com/api/"


# Fonction pour appeler l'API et mesurer la latence
def call_api():
    start = time.time()
    response = requests.get(API_URL, timeout=3)
    latency = (time.time() - start) * 1000
    return response, latency


# Page consignes
@app.get("/")
def consignes():
    return render_template('consignes.html')


# Route pour afficher un plat aléatoire
@app.get("/plat")
def plat_aleatoire():
    try:
        response = requests.get(API_URL, timeout=3)
        data = response.json()
        image_url = data.get("image", "")
    except Exception:
        image_url = "https://foodish-api.com/images/pizza/pizza18.jpg"

    html = f"""
    <h1>Plat aléatoire</h1>
    <img src="{image_url}" style="max-width:500px;">
    <br><br>
    <a href="/plat">Voir un autre plat</a>
    <br>
    <a href="/run-tests">Lancer les tests API</a>
    """

    return html


# ------------------------
# TESTS API (Testing as Code)
# ------------------------

def test_status_code():
    r, latency = call_api()
    assert r.status_code == 200
    return {"name": "status code", "status": "PASS", "latency": latency}


def test_content_type():
    r, latency = call_api()
    assert "application/json" in r.headers["Content-Type"]
    return {"name": "content type json", "status": "PASS", "latency": latency}


def test_json_valid():
    r, latency = call_api()
    data = r.json()
    assert isinstance(data, dict)
    return {"name": "json valid", "status": "PASS", "latency": latency}


def test_image_field():
    r, latency = call_api()
    data = r.json()
    assert "image" in data
    return {"name": "image field present", "status": "PASS", "latency": latency}


def test_image_type():
    r, latency = call_api()
    data = r.json()
    assert isinstance(data["image"], str)
    return {"name": "image type string", "status": "PASS", "latency": latency}


def test_latency():
    r, latency = call_api()
    assert latency < 3000
    return {"name": "latency < 3s", "status": "PASS", "latency": latency}


# ------------------------
# Endpoint pour lancer les tests
# ------------------------

@app.get("/run-tests")
def run_tests():

    tests = [
        test_status_code,
        test_content_type,
        test_json_valid,
        test_image_field,
        test_image_type,
        test_latency
    ]

    results = []
    passed = 0
    failed = 0

    for t in tests:
        try:
            res = t()
            results.append(res)
            passed += 1
        except Exception as e:
            results.append({
                "name": t.__name__,
                "status": "FAIL",
                "details": str(e)
            })
            failed += 1

    return jsonify({
        "passed": passed,
        "failed": failed,
        "tests": results
    })


# Lancer Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
