# landuse_monitoring_project
Projet python pour la monté en compétence sur la création d'un pipeline géospatiale
Le dépôt est structuré de la manière suivante :

Structure du pipeline
├── data/
│   ├── archive/     # Contient les fichiers de l'hérodatage des résultats de chaque exécution
│   ├── input/       # Fichiers sources (Fichier Excel de la population (RGPH-5 -2022)
│   └── output/      # Résultats générés (Cartes PNG, et Rapports PDF)
├── geo/             # Environnement virtuel Python
├── logs/            # Fichiers de suivi de l'exécution et des erreurs
├── scripts/
│   └── main.py      # Script principal du pipeline pour l'exécution
├── config.json      # Fichier de configuration du projet
├── environment.yml  # Dépendances et bibliothèques à installer
└── run.bat          # Script d'exécution automatique sous Windows
