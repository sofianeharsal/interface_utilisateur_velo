# Interface Utilisateur Vélo

## Description

Ce projet vise à développer une interface interactive qui intègre les données des stations de vélos partagés de Nancy via l'API de JCDecaux. L'application permet de visualiser les stations surchargées ou sous-alimentées en vélo et indiquera aux utilisateurs à déplacer les vélos en fonction des besoins.

## Fonctionnalités

- Affichage des données en temps réel des stations (nombre de vélos, nombre de place libre)
- Affichage du chemin le plus court entre 2 stations à rééquilibrer en vélo

## Technologies Utilisées

- HTML
- CSS
- JavaScript
- Bibliothèques Python requests, folium, osmnx, networkx, geopy

## Installation

Pour exécuter ce projet localement, suivez les étapes ci-dessous :

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/sofianeharsal/interface_utilisateur_velo.git](https://github.com/sofianeharsal/interface_utilisateur_velo.git

2. Installez les dépendances nécessaires :
   pip install (requests, osmnx, netwrokx, folium, geopy)

## Utilisation

Excécutez le script main.py
Le programme ouvrira une page HTML contenant la carte de Nancy et les différentes stations de vélo. 
Le nombre de vélo disponble et le nombre de place de vélo est indiqué pour chaque station. 
Le programme détectera automatiquement la station de vélo la plus rempli et indiquera le chemin le plus court pour se rendre à la station ayant le plus besoin de vélo afin de rééquilibrer la distribution des vélos dans la ville.
