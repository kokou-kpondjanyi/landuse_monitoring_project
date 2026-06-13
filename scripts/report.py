# imports
import logging
from weasyprint import HTML 
from  pathlib  import Path



def rapport_geo(OUTPUT_DIR):
    """configuration des logs"""
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")
    logging.info("Début du script") 

    html = """
    <style>
        /* Configuration de la page A4 et de ses marges */
        @page {
            size: A4;
            margin: 1.5cm;
        }
        h1 {
            color: #083D44;
        }
        
        /* Conteneur pour forcer les images à rester ensemble ou bien dimensionnées */
        .galerie-cartes {
            text-align: center;
        }
        .carte-img {
            max-width: 85%;    /* Empêche l'image de déborder de la page */
            height: auto;      /* Garde les proportions de la carte */
            margin-bottom: 5px; /* Espace léger entre les visuels */
        }
    </style>

    <h1> Rapport automatisé </h1>
    <p> Rapport de la population togolaise par région en 2022</p>

    <div class="galerie-cartes">
        <img src="carte_pop_feminine.png" class="carte-img">
        <img src="carte_pop_masculine.png" class="carte-img">
        <img src="graphique_population.png" class="carte-img">
    </div>

    <p>Rapport généré automatiquement avec python. </p>
    """

    base_path = Path(OUTPUT_DIR)
    chemin_pdf = base_path / "rapport_population.pdf"

    HTML(
        string=html,
        base_url=str(base_path)
    ).write_pdf(chemin_pdf )
    logging.info("PDF généré avec succès")
    logging.info("Fin du script")


