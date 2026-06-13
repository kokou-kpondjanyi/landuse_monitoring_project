# imports
import os
import shutil
from  pathlib  import Path
from datetime import datetime
import logging


def archivage(OUTPUT_DIR, ARCHIVE_DIR):
    """création du dossier d'archive"""
    #configuration des logs
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")


    logging.info("Début du script et vérification de l'existence du dossier d'export")
    #chemin du dossier archive
    archive = ARCHIVE_DIR
    os.makedirs(archive, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d-%H-%M")

    logging.info("Début de l'hérodatage")
    #herodatage
    for f in ["carte_pop_feminine.png", "carte_pop_masculine.png", "graphique_population.png", "rapport_population.pdf"]:
        src = Path(OUTPUT_DIR)/f
        dest = Path(archive) / f"{today}_{f}"
        if os.path.exists(src):
            shutil.copy(src, dest)
            print(f"Archivé avec succès : {f}")
        logging.info("Fin de l'hérodatage")