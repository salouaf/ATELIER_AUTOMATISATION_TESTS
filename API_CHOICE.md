# API Choice

- Étudiant : Saloua FLORAND
- API choisie : Foodish
- URL base : https://foodish-api.com/
- Documentation officielle / README : https://github.com/surhud004/Foodish?utm_source=chatgpt.com
- Auth : None / API Key / OAuth : None
- Endpoints testés :
  - GET /api/ → image aléatoire
  - GET /api/images/{food} → image d’une catégorie spécifique (ex: pizza, burger)
    
- Hypothèses de contrat (champs attendus, types, codes) :
    Réponse JSON :
  {
    "image": "URL de l'image"
  }
  Champs : image → string (URL de l’image)

  Codes HTTP :

  200 → OK, image renvoyée

  404 → catégorie non trouvée

  500 → erreur serveur
- Limites / rate limiting connu : Pas de limite documentée, API simple et publique
- Risques (instabilité, downtime, CORS, etc.) :
Peut être indisponible si le serveur GitHub Pages est down

Pas de contrôle sur le contenu des images

CORS possible si utilisé côté navigateur directement
