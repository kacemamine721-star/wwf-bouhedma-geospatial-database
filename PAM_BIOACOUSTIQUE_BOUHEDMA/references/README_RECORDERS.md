# Boîte à Outils Bioacoustique : Parc National de Bouhedma (GeoAI + QGIS)

Ce dossier regroupe l'ensemble des scripts, tables de référence et couches spatiales validées pour le déploiement des 20 enregistreurs bioacoustiques passifs (**Song Meter Micro 2 / AudioMoth**) dans le Secteur 1 du Parc National de Bouhedma.

---

## 📁 Arborescence Définitive et Épurée

```
bouhedma_recorders/
├── scripts/
│   ├── 01_gee_stack.js                     # Script GEE : Export du stack 10m Sentinel-2 + MNT SRTM (SCL clear mask)
│   ├── 02_geoai_tree_and_water_detector.py # Script Python Maître : 10 vrais points d'eau, 2 substrats, exclusion RR124 seule
│   └── _archive_v1/                        # Anciens scripts v1 archivés (K-Means, AHP pixel, clôtures)
├── tables/
│   ├── candidate_sites_field_sheet.csv    # FICHE DE TERRAIN : 20 sites retenus (GPS WGS84, substrat, Alt, Eau, Instructions)
│   ├── species_guilds.csv                  # 33 espèces confirmées réparties en 4 guildes trophiques
│   ├── parameters.csv                      # Seuils biophysiques, substrats candidats et quotas stratifiés
│   └── strata_legend.csv                   # Légende descriptive des écosystèmes
├── project/
│   ├── bouhedma_pam_final_sites.qml        # Style QGIS pour les 20 sites (couleur par écozone + icône substrat)
│   ├── bouhedma_water_sources.qml          # Style QGIS pour les 10 vrais points d'eau (symboles bleus étiquetés)
│   └── road_exclusion_buffer.qml           # Style QGIS pour visualiser la zone tampon d'exclusion RR124
├── data/
│   ├── gee/
│   │   └── bouhedma_stack_10m.tif          # 12 bandes (SAVI, NDMI, BSI, Amplitude, Texture, SRTM, Pente, TPI)
│   └── qgis/outputs/                       # Couches géographiques finales prêtes pour QGIS
│       ├── bouhedma_pam_final_trees_utm.geojson        # LES 20 SITES DÉFINITIFS (EPSG:32632)
│       ├── bouhedma_pam_final_sites_utm.geojson        # Alias identique (WGS 84)
│       ├── bouhedma_pam_final_trees.geojson            # LES 20 SITES DÉFINITIFS (WGS 84)
│       ├── bouhedma_water_sources_validated_utm.geojson # LES 10 VRAIS POINTS D'EAU VALIDÉS
│       └── road_exclusion_buffer_utm.geojson           # Zone de dérangement acoustique RR124 (300m, sud uniquement)
└── METHODOLOGY_EXPLANATION.md              # Fondements scientifiques et références bibliographiques
```

---

## 🎯 Les 5 Piliers Méthodologiques Validés (Version Finale)

1. **Deux Substrats Physiques Réels (Zéro Fantôme)** :
   * **Arbres** : Chaque site arboricole est ancré sur un houppier d'*Acacia tortilis* détecté par maximum local spectral SAVI (`savi_dry > 0.12`, pente ≤ 25°). Boîtier fixé à **1.8–2.0 m** sur branche maîtresse.
   * **Poteaux électriques** : Les 15 pylons de la ligne BT traversant le Secteur 1 (OSM) sont des **candidats valides**. Ce sont les perchoirs d'affût naturels des rapaces (*Falco tinnunculus*, *Buteo rufinus*, *Lanius meridionalis*). Vue acoustique omnidirectionnelle 360°. Fixation à **2.5–3.0 m** avec sangle UV. Filtre passe-haut 500 Hz recommandé.
   * Aucune clôture virtuelle.

2. **Sentiers GPS = Zéro Exclusion** :
   * `GPS4_TRAIL_OBSERVATION_DAY2` et `GPS6_TRAIL_OBSERVATION_DAY3` sont des **sentiers de marche pédestre** (GPS rennommés de `ROAD` → `TRAIL`). Zéro bruit moteur. Aucun buffer appliqué.
   * Ces sentiers sont au contraire des **corridors logistiques prioritaires** pour accéder aux sites PAM en patrouille.

3. **Zone de Silence Acoustique Stricte : RR 124 uniquement (300 m)** :
   * La **seule** exclusion dure est le recul de 300 m de la Route Régionale asphaltée RR 124 le long de la bordure sud du parc.
   * Les pistes carrossables internes (`track`, `service`) et les lignes électriques **ne sont plus exclus** : ce sont des éléments du paysage sonore naturel de référence dans une zone protégée.

4. **Les 10 Sources d'Eau Validées sur le Terrain** :
   * Remplacement des 436 points NDMI spectraux erronés (ombres de rochers + buissons humides) par les **10 points d'eau réels** :
     1. `Aïn Charchara` — Cascade pérenne du canyon
     2. `Cirque Nord` — Source / résurgence au pied du Djebel
     3. `Camp WWF` — Citernes & robinets
     4. `Château Français` — Réservoir historique
     5. `Éco-Parc` — Point d'eau de l'écomusée
     6. `Enclos Autruches` — Abreuvoir faune sauvage
     7. `Enclos Mouflons` — Abreuvoir faune sauvage
     8. `Abreuvoir Plaine` — Abreuvoir central Oryx & Gazelles DGF
     9. `Guelta Oued Médian` — Cuvette rocheuse pérenne
     10. `Piémont Ouest` — Suintement montagneux temporaire

5. **Échantillonnage Stratifié Équilibré (20 Enregistreurs, 5 Écozones)** :
   * **Savane Centre** (6 sites) : Cœur du peuplement *Vachellia tortilis* & pylons perchoirs rapaces.
   * **Savane Ouest** (4 sites) : Plaine ouverte (Outarde houbara, Courvite isabelle, Sirli du désert).
   * **Savane Est** (3 sites) : Transition steppique orientale le long du transect de pylons.
   * **Oueds & Piémont** (4 sites) : Confluences boisées, cirque nord et suintements.
   * **Canyon d'Aïn Charchara** (3 sites) : Falaises, perchoirs rupestres et cascade pérenne.

---

## 🚀 Utilisation Immédiate dans QGIS

1. Ouvrez votre projet QGIS sur Bouhedma (en **EPSG:32632**).
2. Chargez les couches depuis `data/qgis/outputs/` :
   * `bouhedma_pam_final_trees_utm.geojson` (Style : `project/bouhedma_pam_final_sites.qml`) — distingue arbres (cercle vert) et poteaux (carré orange).
   * `bouhedma_water_sources_validated_utm.geojson` (Style : `project/bouhedma_water_sources.qml`).
   * `road_exclusion_buffer_utm.geojson` (Style : `project/road_exclusion_buffer.qml`) — maintenant uniquement la bande sud de 300m le long de la RR124.
3. Consultez la fiche de terrain [`tables/candidate_sites_field_sheet.csv`](file:///c:/Users/Dell/Desktop/GeoAI/WWF_PARC_BOUHEDMA/bouhedma_recorders/tables/candidate_sites_field_sheet.csv) pour les coordonnées GPS et instructions de pose adaptées au substrat.

---

## ⚠️ Note d'Analyse Spatiale — Limite identifiée

L'analyse de position des 20 sites révèle **un point d'attention** :

- **SAVANE_OUEST** : les 4 sites (PAM_16, 18, 19, 20) sont concentrés entre X=556 295 m et X=556 765 m. La bande X < 556 000 m (~1,7 km vers l'ouest) est sans couverture car le SAVI détecte peu d'acacias dans cette zone de steppe minérale ouverte.
- **PAM_20** a le score le plus bas du réseau (0.479) et se trouve à 264 m d'altitude sur la bordure du piémont.
- **Solution terrain** : si la reconnaissance confirme l'absence d'acacias dans l'extrême ouest, PAM_20 peut être remplacé par le poteau électrique `osm_id=2334542306` (X=560 397 m, score 0.574) ou tout piquet de clôture / abreuvoir découvert lors de la visite.
- **PAM_07 ↔ PAM_08** sont espacés de seulement **200 m** dans la gorge d'Aïn Charchara — espacement volontaire (couloir acoustique étroit) mais à confirmer si la mémoire des cartes SD est limitée.
