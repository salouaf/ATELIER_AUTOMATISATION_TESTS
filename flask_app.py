from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)

@app.get("/")
def consignes():
     return render_template('consignes.html')


@app.get("/plat")
def plat_aleatoire():
    # Appel de l'API Foodish
    url = "https://foodish-api.com/api/"
    response = requests.get(url)
    
    # Vérifier que la requête a fonctionné
    if response.status_code != 200:
        return "Erreur lors de l'appel à l'API", 500
    
    # Récupérer le JSON
    data = response.json()
    image_url = data.get("image", "")
    
    # Afficher l'image dans le navigateur
    html = f"""
    <h1>Plat aléatoire</h1>
    <img src="{image_url}" alt="Plat" style="max-width:500px;">
    <br><a href='/plat'>Voir un autre plat</a>
    """
    return html

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)
