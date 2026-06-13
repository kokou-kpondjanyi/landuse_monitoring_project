# imports des bibliothèques
import logging
import geopandas as gpd
from pathlib import Path
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt



def traitement_geo (OUTPUT_DIR):
    """ Fonction pour: création du champs area_m2, calcule de la surface totale et création des centroides """
    # configuration des logs
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")
    logging.info("Début du script")
    chemin_gdf = Path(OUTPUT_DIR) / "region_polygon_utm.geojson"
    gdf = gpd.read_file(chemin_gdf)

    logging.info("Vérification du CRS de la couche")
    #vérification du crs
    print(f"Le CRS de la couche est: {gdf.crs}")

    logging.info("Création du champs area_km2 et code et calcule de la surface en Km²")
    #Calcule de la surface en kilomètre 2
    gdf["area_km2"] = gdf.geometry.area/1000000
    # copie de la colonne name vers le nouveau champs code
    gdf["code"] = gdf["name"]

    logging.info("Aperçu des collones de la couche")
    #Aperçu des colonnes
    print(f"L'entête des colonnes: {gdf.head()}")

    #export des données avec les nouvelles colonnes
    resultat_analyse = Path(OUTPUT_DIR) / "region_polygon_analyse.geojson"
    gdf.to_file(resultat_analyse)
    print("Données exporter avec succès")

    logging.info("Création des centroides pour les régions")
    #création de la géometrie
    gdf["centroid_geom"] = gdf.geometry.centroid

    logging.info("Export des centroides")
    #Export des centroides
    region_centroid = gdf.set_geometry("centroid_geom")[["centroid_geom","name"]]
    resultat_centroid = Path(OUTPUT_DIR) / "region_centroid.geojson"
    region_centroid.to_file(resultat_centroid)
    print("Centroïde exporter avec succès")
    logging.info("Export des données ")

    return resultat_analyse

def jointure_data_population(INPUT_DIR, OUTPUT_DIR, filter):

    """ Fonction pour la jointure attributaire des données excel au fichier geojson en utm """

    # configuration des logs
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")
    logging.info("Début du script")

    #Préparation pour la jointure
    logging.info("Chargement du fichier excel")
    #chargement des fichiers excel et geojson
    xlsx = Path(INPUT_DIR) / "repartition_population_par_region.xlsx" 
    pop_region = Path(OUTPUT_DIR) / "region_polygon_analyse.geojson"
    geojson = gpd.read_file(pop_region)

    #lecture du fichier excel
    logging.info("Lecture du fichier excel")
    df = pd.read_excel(xlsx)
    #affichage de l'entête
    print(df.head())

    logging.info("Début de la vérification")
    #vérification de la présence du champs "code"
    cle = filter

    #vérification du champs dans la couche geojson
    if cle in geojson.columns:
        print(f"Le champs {cle} est présent dans la couche geojson")
    else:
        print(f"Erreur le champs {cle} est absent du geojson")

    #vérification du champs dans la couche excel  
    if cle in df.columns:
        print(f"Le champs {cle} est présent dans la couche Excel")
    else:
        print(f"Erreur le champs {cle} est absent du Excel")

    logging.info("Fin de la vérification")

    logging.info("Affichage d l'aperçu de la clé dans les couches")
    #Aperçu des valeurs de la CLE
    print(f"Valeurs Geojson: {geojson[cle].unique()[:5]}")
    print(f"Valeurs Excel: {df[cle].unique()[:5]}")


    #Réalisation de la jointure proprement dite
    logging.info("Jointure de la couche excel au geosjon")
    #Jointure
    geojson_joint = geojson.merge(df, on="code", how="left")
    #affichage des colonnes àprès la jointure
    print(f"Liste des colonnes {geojson_joint.columns}")

    logging.info("Export des données après jointures")
    #Vérification de l'existence du dossier
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    #export des données après jointures
    chemin_pop = Path(OUTPUT_DIR) / "region_population_joint.geojson"
    geojson_joint.to_file(chemin_pop)
    print("Export effectuer avec succès")
    logging.info("Export des données après jointures effectuer avec succès")
    logging.info("Fin du script")

    return geojson_joint

def generate_carte(OUTPUT_DIR, colonne:str, titre: str, chemin_sortie:Path):
    """Produition des graphiques""" 
        # configuration des logs
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")
    logging.info("Début du script")

    logging.info("Génération des graphiques")
    chemin_gdf = Path(OUTPUT_DIR) / "region_population_joint.geojson"
    gdf = gpd.read_file(chemin_gdf)

    #création de la figure matplotlib
    fig, ax = plt.subplots(figsize = (12,8))
   
    #carte théamtique
    gdf.plot(
        column= colonne,
        cmap= "YlOrRd",
        legend= True,
        legend_kwds= {"label":"Population", "shrink":0.6},
        edgecolor= "black",
        linewidth= 0.4,
        ax = ax
    )

    #Génération du centroide pour l'affichage des nom de régions sur la carte
    logging.info("Affichage des noms des cinqs régions")
    for idx, row in gdf.iterrows():
        centroid = row.geometry.centroid
        #affichage de l'ettiquete
        ax.annotate(
            text=row["Région"],
            xy=(centroid.x, centroid.y),
            xytext=(0, 0),
            textcoords="offset points",
            fontsize=9, 
            fontweight="normal",
            color="black",    
            ha="center",          
            va="center"      
        )

    #titre et mise en page
    ax.set_title(titre,
                fontsize = 14,
                fontweight = "bold",
                pad = 15
                )
    ax.set_axis_off()
    plt.tight_layout()

    logging.info("Début export de la carte")
    #Export de la carte
    fig.savefig(chemin_sortie, dpi = 300, bbox_inches= "tight")
    plt.close(fig)
    print(f"carte exporter dans {chemin_sortie}")

def graphique_population(col_pop: str,
                         col_name: str,
                         titre: str, 
                         OUTPUT_DIR: str, 
                         chemin_sortie: str):
    """Graphique par population"""

    # configuration des logs
    logging.basicConfig(filename="log.file", level=logging.INFO, encoding="utf-8")
    logging.info("Début du script")
    chemin_data = Path(OUTPUT_DIR) / "region_population_joint.geojson"
    gdf_graphe = gpd.read_file(chemin_data)
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.bar(
    gdf_graphe[col_name],
    gdf_graphe[col_pop],
    color="#2E8B57",
    edgecolor="white",
    width=0.7
    )

    #titre et étiquettes des axes
    ax.set_title(titre, fontsize=20, fontweight = "bold" , pad=15)
    ax.set_xlabel("\n Régions", fontsize = 15, fontweight = "bold")
    ax.set_ylabel("Population", fontsize = 15, fontweight = "bold")

    # Grille legère en arriere-plan
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)
    plt.tight_layout()

    fig.savefig(chemin_sortie, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logging.info("Fin de l'export du graphique")
    print(f"Graphique exporter : {chemin_sortie}")
