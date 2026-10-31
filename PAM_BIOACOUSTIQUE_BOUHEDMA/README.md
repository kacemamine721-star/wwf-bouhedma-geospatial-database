# PAM Bioacoustique Bouhedma — Monitoring Passif de l'Avifaune

**Projet :** WWF Talent Academy 2026 — Déploiement des enregistreurs bioacoustiques passifs  
**Parc :** Parc National de Bouhedma, Secteur 1  
**Matériel :** Song Meter Micro 2 (Wildlife Acoustics) — **20 stations PAM**

---

## 📁 Arborescence

```
PAM_BIOACOUSTIQUE_BOUHEDMA/
│
├── scripts/
│   ├── 01_gee_stack.js                          # Google Earth Engine : export du stack Sentinel-2 + SRTM 10m
│   └── 02_geoai_tree_and_water_detector.py      # Pipeline GeoAI principal : détection acacias + pylônes, sélection 20 stations
│
├── data/
│   ├── aoi/PARC_NATIONAL_BOUHEDMA_SECTOR1_AOI_2KM_WGS84.geojson # Zone d'étude étendue
│   ├── gee_stack/
│   │   └── bouhedma_stack_10m.tif               # ENTRÉE : raster 12 bandes (SAVI, NDMI, Texture, SRTM, Pente...)
│   ├── outputs_vectors/
│   │   ├── bouhedma_pam_final_trees_utm.geojson # SORTIE PRINCIPALE : 20 stations PAM (EPSG:32632)
│   │   ├── bouhedma_pam_final_trees.geojson     # SORTIE PRINCIPALE : 20 stations PAM (WGS84)
│   │   ├── bouhedma_pam_final_sites_utm.geojson # Alias identique (UTM)
│   │   ├── bouhedma_water_sources_validated_utm.geojson  # 10 sources d'eau validées terrain
│   │   ├── road_exclusion_buffer_utm.geojson    # Zone d'exclusion acoustique RR124 (300m, sud)
│   │   └── PARC_NATIONAL_BOUHEDMA_SECTOR1_*    # Limites du Secteur 1 (shapefile + GeoJSON, UTM + WGS84)
│   └── outputs_tables/
│       ├── candidate_sites_field_sheet.csv      # FICHE DE TERRAIN : GPS + substrat + instructions de pose
│       ├── parameters.csv                       # Tous les seuils et paramètres du pipeline
│       ├── species_guilds.csv                   # 33 espèces de Bouhedma classées en 4 guildes
│       └── strata_legend.csv                    # Description des 5 écozones
│
├── project/
│   └── qml_styles/
│       ├── bouhedma_pam_final_sites.qml         # Style QGIS : vert=arbre / orange=poteau ; étiquette SITE_ID
│       ├── bouhedma_water_sources.qml           # Style QGIS : points d'eau bleus étiquetés
│       └── road_exclusion_buffer.qml            # Style QGIS : zone tampon RR124 (rouge semi-transparent)
│
└── references/
    ├── METHODOLOGY_EXPLANATION.md              # Fondements scientifiques complets (SAVI, NDMI, AHP, inhibition spatiale)
    └── README_RECORDERS.md                    # Guide opérationnel QGIS et protocole de déploiement terrain
```

---

## 🗺️ Couches Clés dans `bouhedma_database.gpkg`

Le GeoPackage maître (à la racine de ce dossier) contient également ces couches issues du pipeline PAM :

| Couche GPKG | Description |
|-------------|-------------|
| `BOUHEDMA_PAM_FINAL_SITES` | 20 stations PAM finales (WGS84) |
| `REAL_WATER_SOURCES` | 10 sources d'eau validées (WGS84) |
| `ROAD_EXCLUSION_BUFFER` | Tampon 300m RR124 (WGS84) |
| `POWERLINES_PARC_NATIONAL_BOUHEDMA` | 15 pylônes électriques OSM (candidats perchoirs) |
| `ROADS_PARC_NATIONAL_BOUHEDMA` | Routes OSM (dont RR124 ref=secondaire) |
| `GPS4_TRAIL_OBSERVATION_DAY2` | Sentier pédestre Jour 2 (anciennement ROAD) |
| `GPS6_TRAIL_OBSERVATION_DAY3` | Sentier pédestre Jour 3 (anciennement ROAD) |

---

## ⚡ Démarrage Rapide

### Relancer le pipeline complet
```bash
python scripts/02_geoai_tree_and_water_detector.py
```
Outputs générés dans `data/outputs_vectors/` et `data/outputs_tables/`.

### Charger dans QGIS
1. Ouvrir QGIS en **EPSG:32632** (UTM Zone 32N)
2. Glisser `data/outputs_vectors/bouhedma_pam_final_trees_utm.geojson`
3. Clic droit → Style → Charger le style → `project/qml_styles/bouhedma_pam_final_sites.qml`
4. Répéter pour les points d'eau et le buffer RR124

---

## 📍 Les 20 Stations PAM — Résumé

| Écozone | Sites | Score moyen | Substrat dominant |
|---------|-------|-------------|-------------------|
| Canyon Charchara | 3 | 0.847 | Acacia de paroi |
| Oueds & Piémont | 4 | 0.901 | Acacia de berge |
| Savane Centre | 6 | 0.912 | Acacia tortilis dense |
| Savane Est | 3 | 0.900 | Acacia + pylônes OSM |
| Savane Ouest | 4 | 0.559 | Acacia steppe (zone pauvre) |

> **Note terrain :** PAM_20 (Savane Ouest, score 0.479) est le site le plus marginal. Si l'arbre est mort ou inaccessible, remplacer par le pylône électrique `osm_id=2334542306` (257m plus au nord-est).

---

*Généré le 2026-10-31 — WWF Talent Academy 2026 / GeoAI Module*

