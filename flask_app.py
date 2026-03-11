from flask import Flask, render_template, jsonify
import requests
import time
import sqlite3
from datetime import datetime

app = Flask(__name__)

# -----------------------------
# CONFIGURATION
# -----------------------------

API_URL = "https://foodish-api.com/api/"
DB = "runs.db"


# -----------------------------
# INITIALISATION BASE SQLITE
# -----------------------------

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        passed INTEGER,
        failed INTEGER,
        avg_latency REAL
    )
    """)

    conn.commit()
    conn.close()


init_db()


# -----------------------------
# FONCTION APPEL API
# -----------------------------

def call_api():
    start = time.time()

    response = requests.get(API_URL, timeout=3)

    latency = (time.time() - start) * 1000

    return response, latency


# -----------------------------
# PAGE CONSIGNES
# -----------------------------

@app.get("/")
def consignes():
    return render_template('consignes.html')


# -----------------------------
# PAGE PLAT ALEATOIRE
# -----------------------------

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

    <br>

    <a href="/dashboard">Voir le dashboard</a>
    """

    return html


# -----------------------------
# TESTS API (Testing as Code)
# -----------------------------

def test_status_code():

    r, latency = call_api()

    assert r.status_code == 200

    return {
        "name": "status code",
        "status": "PASS",
        "latency": latency
    }


def test_content_type():

    r, latency = call_api()

    assert "application/json" in r.headers["Content-Type"]

    return {
        "name": "content type json",
        "status": "PASS",
        "latency": latency
    }


def test_json_valid():

    r, latency = call_api()

    data = r.json()

    assert isinstance(data, dict)

    return {
        "name": "json valid",
        "status": "PASS",
        "latency": latency
    }


def test_image_field():

    r, latency = call_api()

    data = r.json()

    assert "image" in data

    return {
        "name": "image field present",
        "status": "PASS",
        "latency": latency
    }


def test_image_type():

    r, latency = call_api()

    data = r.json()

    assert isinstance(data["image"], str)

    return {
        "name": "image type string",
        "status": "PASS",
        "latency": latency
    }


def test_latency():

    r, latency = call_api()

    assert latency < 3000

    return {
        "name": "latency < 3s",
        "status": "PASS",
        "latency": latency
    }


# -----------------------------
# LANCER LES TESTS
# -----------------------------

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

    latencies = []

    for t in tests:

        try:

            res = t()

            results.append(res)

            passed += 1

            latencies.append(res["latency"])

        except Exception as e:

            results.append({
                "name": t.__name__,
                "status": "FAIL",
                "details": str(e)
            })

            failed += 1

    avg_latency = 0

    if latencies:
        avg_latency = sum(latencies) / len(latencies)

    # -----------------------------
    # SAUVEGARDE DANS SQLITE
    # -----------------------------

    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "INSERT INTO runs (timestamp, passed, failed, avg_latency) VALUES (?, ?, ?, ?)",
        (datetime.now().isoformat(), passed, failed, avg_latency)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "passed": passed,
        "failed": failed,
        "avg_latency": avg_latency,
        "tests": results
    })


# -----------------------------
# DASHBOARD
# -----------------------------

@app.get("/dashboard")
def dashboard():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM runs ORDER BY id DESC LIMIT 20")
    rows = c.fetchall()
    conn.close()
    # Récupérer image du dernier test ou mettre image par défaut
    last_image = rows[0][5] if rows and len(rows[0])>5 else "https://foodish-api.com/images/pizza/pizza18.jpg"
    return render_template("dashboard.html", runs=rows, last_image=last_image)

# -----------------------------
# LANCER FLASK
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
