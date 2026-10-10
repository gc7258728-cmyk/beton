# BETON INSIGHT PRO

Application Streamlit pour analyser des résultats d'essais de résistance du béton à 28 jours.

## Fonctions

- Import de fichiers CSV et Excel (.xlsx).
- Détection des résistances manquantes, illisibles, nulles ou négatives.
- Repérage des lignes entièrement dupliquées.
- Indicateurs : moyenne, médiane, écart-type, coefficient de variation, minimum, maximum et taux au-dessus du seuil choisi.
- Comparaison des lots avec un graphique.
- Export du rapport texte, des essais analysés et du contrôle qualité en CSV.
- Jeu de démonstration fictif disponible à l'ouverture.

Les fichiers importés ne sont pas enregistrés par l'application. Les données de démonstration sont fictives. Le seuil de conformité est configurable et doit correspondre aux spécifications du projet.

## Lancer en local sous Windows

Dans PowerShell, depuis le dossier du projet :

~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
~~~

## Déployer sur Render

Créer un Web Service connecté au dépôt, puis utiliser :

- Branch : main
- Root Directory : laisser vide
- Build Command : pip install -r requirements.txt
- Start Command : streamlit run app.py --server.address 0.0.0.0 --server.port $PORT

## Déployer sur Streamlit Community Cloud

Créer une application depuis le dépôt GitHub, avec :

- Branch : main
- Main file path : app.py

Le fichier requirements.txt à la racine déclare les dépendances Python.
