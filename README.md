# WWF Talent Academy 2026 - Base de Données Géospatiale et Écologique du Parc National de Bouhedma
**Bouhedma National Park Geospatial and Biodiversity Monitoring Database**

![wwf_image](wwf_talent_academy_2026.png)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![CRS: EPSG 4326](https://img.shields.io/badge/CRS-EPSG%3A4326%20(WGS%2084)-blue.svg)](https://epsg.io/4326)
[![WDPA ID: 13962](https://img.shields.io/badge/WDPA%20Site-13962-green.svg)](https://www.protectedplanet.net/13962)
[![UNESCO-MAB](https://img.shields.io/badge/UNESCO--MAB-Biosphere%20Reserve-brightgreen.svg)](https://en.unesco.org/mab)

---

## 🇫🇷 Présentation du Projet (Français)

Cette base de données géospatiale compile l'ensemble des données géographiques, écologiques et méthodologiques collectées lors du camp de terrain **WWF Talent Academy 2026** (Session Savane, 14–19 septembre 2026) au **Parc National de Bouhedma** (Tunisie centrale).

Le Parc National de Bouhedma protège l'unique savane pré-saharienne d'Afrique du Nord dominée par ***Vachellia tortilis*** (anciennement *Acacia raddiana*) et constitue un pôle de référence pour la réintroduction et le suivi de la grande faune saharo-sahélienne :
* **Oryx algazelle** (*Oryx dammah* - Code WWF : `ORDA`, Statut UICN : Éteint à l'état sauvage / Réintroduit)
* **Gazelle dorcas** (*Gazella dorcas* - Code WWF : `GADO`, Statut UICN : Vulnérable)
* **Mouflon à manchettes** (*Ammotragus lervia* - Code WWF : `AMLE`, Statut UICN : Vulnérable)
* **Autruche d'Afrique du Nord** (*Struthio camelus* - Code WWF : `STCA`, Réintroduite en enclos)
* **Faune carnivore & nocturne** : Hyène rayée (*Hyaena hyaena*), Loup doré (*Canis lupaster* / *aureus*), Renard roux (*Vulpes vulpes*).

---

## 🇬🇧 Project Overview (English)

This geospatial database compiles all geographic, ecological, and methodological monitoring data collected during the **WWF Talent Academy 2026** field camp (Savanna Session, September 14–19, 2026) in **Bouhedma National Park** (Central Tunisia).

Bouhedma National Park preserves North Africa's last remaining pre-Saharan savanna dominated by ***Vachellia tortilis*** (formerly *Acacia raddiana*) and serves as the flagship reintroduction center for threatened Saharan megafauna (Scimitar-horned Oryx, Dorcas Gazelle, Barbary Sheep, and North African Ostrich).

---

## 👥 Encadrement Scientifique & Experts de Session / Scientific Leadership

| Thématique / Session | Encadrant(s) Scientifique(s) | Institution de rattachement |
| :--- | :--- | :--- |
| **Grands Herbivores & Recensement (J2)** | **Marie Petretto** | Marwell Wildlife |
| **Chiroptères / Chauves-souris (J2)** | **Khaled Ferchichi** | Helmholtz Institute for One Health (HIOH) |
| **Carnivores & Pièges Photographiques (J3)** | **Dr. Haithem El-Farhati & Jamel Jrijer** | WWF Afrique du Nord & Conservation du Parc |
| **Entomologie Nocturne (J3)** | **Wael Ben Aba** | WWF Afrique du Nord |
| **Micro-mammifères, Rongeurs & Transects (J4)**| **Faouz Kilani & Dr. Haithem El-Farhati** | WWF Talent Academy & Experts associés |
| **Phytoécologie & Dendrométrie (J5)** | **Dr. Alaeddine Rouissi** | WWF Afrique du Nord & Enseignant-chercheur |
| **Coordination Générale & Données** | **Zakher Bouragaoui & Intissar Ferjani** | WWF Afrique du Nord |

---

## 📁 Structure du Répertoire / Directory Structure

```
WWF_TALENT_ACADEMY_2026_BOUHEDMA_DATABASE/
├── DAY1_14-09-2026/        # Infrastructures, Zonage WDPA 13962 & Enclos de reproduction
├── DAY2_15-09-2026/        # Route d'excursion, Recensement antilopes/autruches & Filet chiroptères
├── DAY3_16-09-2026/        # Pièges photographiques carnivores & Station lumineuse entomologique
├── DAY4_17-09-2026/        # Cages pièges rongeurs & Transect bio-index synchronisé à 3 personnes
├── DAY5_18-09-2026/        # Phytoécologie, Dendrométrie Vachellia tortilis & Source Ain Charchara
├── Ressources_en_francais/ # Fiches officielles PDF & Tableaux Excel (Métadonnées & Attributs)
└── Resources_in_English/   # Official Metadata Datasheets & Summary Attribute Tables (PDF & Excel)
```

Chaque dossier journalier contient pour chaque couche :
- Le fichier vectoriel **GeoJSON** (`.geojson`) encodé en UTF-8.
- Le fichier vectoriel **ESRI Shapefile** complet (`.shp`, `.shx`, `.dbf`, `.prj`, `.cpg`).
- La fiche de métadonnées **QGIS** officielle (`.qmd`) intégrée aux propriétés de couche.
- La fiche de métadonnées **ISO 19139 / ESRI** (`.shp.xml`).
- Le fichier de métadonnées léger **JSON** (`.meta.json`).

---

## 🌐 Système de Coordonnées & Précision / Spatial Reference System

* **CRS / Système de référence :** WGS 84 (World Geodetic System 1984)
* **Code EPSG :** `EPSG:4326`
* **Unités :** Degrés décimaux (Latitude / Longitude)
* **Emprise Bounding Box :**
  * Ouest (Min X) : `9.2622° E`
  * Est (Max X) : `9.6850° E`
  * Sud (Min Y) : `34.2855° N`
  * Nord (Max Y) : `34.6105° N`

---

## 📜 Licences & Droits d'Utilisation / License

* **Données géospatiales & métadonnées :** [Creative Commons Attribution - Pas d’Utilisation Commerciale - Partage dans les Mêmes Conditions 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).
* **Code source & scripts de traitement :** [MIT License](https://opensource.org/licenses/MIT).

---

## 📖 Citation Recommandée / How to Cite

```bibtex
@dataset{wwf_bouhedma_2026,
  author       = {{WWF Afrique du Nord} and {Direction Générale des Forêts}},
  title        = {Base de données géospatiale et écologique du Parc National de Bouhedma – WWF Talent Academy 2026},
  year         = {2026},
  publisher    = {WWF North Africa},
  address      = {Tunis, Tunisie},
  url          = {https://www.wwfna.org}
}
```

