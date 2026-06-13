#imports des scripts
from collect import collect_donnees
from process import process_data
from analyze import traitement_geo, jointure_data_population, generate_carte, graphique_population
from report import rapport_geo
from archive import archivage
import logging
import json

# Charger la config
with open("config.json", encoding="utf-8") as f: 
    config = json.load(f)

# Logger
logging.basicConfig(
    filename=config["log_file"],
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger()

# Exécution
try:
    logger.info("Script start")

    logger.info("Début collect des données")
    collect_donnees(INPUT_DIR= config["INPUT_DIR"])

    logger.info("Début processing des données")
    process_data(INPUT_DIR= config["INPUT_DIR"], OUTPUT_DIR= config["OUTPUT_DIR"], epsg_target = config["epsg_target"])

    logger.info("Début traitement des données")
    traitement_geo(OUTPUT_DIR= config["OUTPUT_DIR"])

    logger.info("Début jointure des données")
    jointure_data_population(INPUT_DIR= config["INPUT_DIR"], OUTPUT_DIR= config["OUTPUT_DIR"], filter = config["filter"])

    logger.info("Début de génération de carte par région de la population masculine")
    generate_carte(
        OUTPUT_DIR= config["OUTPUT_DIR"],
        colonne="Masculin",
        titre="Population Masculine par Région en 2022",
        chemin_sortie= config["CARTE_DIR_MALE"]
        )
    generate_carte(
        OUTPUT_DIR= config["OUTPUT_DIR"],
        colonne="Féminin",
        titre="Population Féminine par Région en 2022",
        chemin_sortie= config["CARTE_DIR_FEMALE"]
        )
    
    logger.info("Début génération des graphiques")
    graphique_population(
        col_pop= "Total",
        col_name= "name",
        titre= "Population par Région en 2022",
        OUTPUT_DIR= config["OUTPUT_DIR"],
        chemin_sortie = config["OUTPUT_GRAPHIQUE"]
    )

    logger.info("Début génération automatique du rapport pdf")
    rapport_geo(config["OUTPUT_DIR"]
    )

    logger.info("Début de l'archivage des données")
    archivage(
        config["OUTPUT_DIR"],
        config["ARCHIVE_DIR"]
    )

    logger.info("Script OK")

except Exception as e:
    logger.exception("Script FAILED")
    raise