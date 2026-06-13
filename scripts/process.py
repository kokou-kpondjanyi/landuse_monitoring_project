# imports des bibliothèques
import logging
import geopandas as gpd
from pathlib import Path






def process_data(INPUT_DIR, OUTPUT_DIR, epsg_target):
    """ Fonction pour charger les données, le nettoyage des colonnes et la projection en EPSG:32631 """

    # configuration des logs
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")
    logging.info("Début du script") 

    logging.info("Données chargées avec succès")
    #Lecture des données geojson
    chemin = Path(INPUT_DIR) / "region_polygon.geojson"
    region_polygon = gpd.read_file(chemin)

    logging.info("Affiche de la liste des attributs de la couche")
    #affiche de la liste des champs de la couche geojson
    print(region_polygon.columns.tolist())

    logging.info("Nettoyage des attributs et colonnes inutiles")
    #filtrage des colonnes utiles
    colonne = ['name', 'geometry']
    region_polygon_flitrer = region_polygon[colonne] 

    logging.info("Reprojection  de la couche")
    region_polygon_utm = region_polygon_flitrer.to_crs(epsg_target)

    logging.info("Sauvegarde des données reprojecter")
    #Sauvegarde des données
    region_polygon_utm.to_file(Path(OUTPUT_DIR) / "region_polygon_utm.geojson")

    logging.info("Fin du script")
    return region_polygon_utm