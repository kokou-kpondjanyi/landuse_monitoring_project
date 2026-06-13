# imports des bibliothèques
import json
import logging
import time
from pathlib import Path
import requests


def collect_donnees(INPUT_DIR):

    """configuration des logs"""
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")

    logging.info("Début du script")
    # Lien de l'API
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    # Entête
    headers = {
        "User-Agent": "FormationPythonSIG_Lome (osm_togo@gmail.com)",
        "Referer": "https://geodonnee.ca",
        "Accept": "application/json",
    }
    
    # les régions du Togo
    region_togo = [
        "Région Maritime, Togo",
        "Région des Plateaux, Togo",
        "Région Centrale, Togo",
        "Région de la Kara, Togo",
        "Région des savanes, Togo",
    ]
    logging.info("collecte des données des régions renvoyées par l'API") 
    # collecte de tous les régions renvoyées par l'api
    geojson_output = {"type": "FeatureCollection", "features": []}

    for zone in region_togo:
        print(f"Recherche de : {zone}")

        # paramètres de la requête
        params = {
            "q": zone,
            "format": "geojson",
            "polygon_geojson": 1,
            "limit": 1,
        }

        time.sleep(2)

        try:
            response = requests.get(
                BASE_URL, params=params, headers=headers, timeout=15
            )
            # vérification du statut de la réponse
            response.raise_for_status()
            logging.info("Conversion de la requete en dictionnaire") 
            # conversion de la requête en dictionnaire
            data = response.json()

            logging.info("vérification de la clé feature") 
            # vérification de la clé features
            features = data.get("features", [])

            # compile des arrondissememnts
            if not features:
                print(f"Aucun contour trouvé pour : {zone}")
            else:
                feature = features[0]
                feature["properties"]["nom_propre"] = zone.split(",")[0]
                geojson_output["features"].append(feature)

        except Exception as e:
            print(f"Erreur pour {zone} : {e}")

    # Dossier de destination
    dossier = Path("data/input")
    # Vérification de l'existence du dossier
    logging.info("Vérification de l'existence du dossier") 
    dossier.mkdir(parents=True, exist_ok=True)

    # Chemin du fichier
    chemin = Path(INPUT_DIR) / "region_polygon.geojson" 

    logging.info("Début sauvegarde des données")
    # Sauvegarde des données
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(geojson_output, f, ensure_ascii=False, indent=2)

    print(f"Fichier sauvegardé avec succès dans {chemin}")

    logging.info("Fin du script")
    return chemin