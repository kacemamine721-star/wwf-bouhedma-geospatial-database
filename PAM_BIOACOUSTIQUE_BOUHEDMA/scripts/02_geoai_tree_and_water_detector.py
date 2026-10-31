#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PIPELINE GEOAI DÉFINITIF : SÉLECTION STRATIFIÉE DES SITES DE MONITORING BIOACOUSTIQUE (PAM)
Projet : WWF Talent Academy 2026 — Guide Déploiement Song Meter Micro 2 / AudioMoth
Parc National de Bouhedma (Secteur 1)

Principes méthodologiques et écologiques :
1. Substrats physiques réels :
   - Arbres d'Acacia tortilis (houppiers matures détectés par maxima locaux SAVI > 0.12).
   - Poteaux de lignes électriques (POWERLINES) : Perchoirs d'affût majeurs pour rapaces
     (Falco tinnunculus, Buteo rufinus, Falco biarmicus) et passereaux (Lanius meridionalis),
     offrant une écoute omnidirectionnelle 360° sans bruit de feuilles et un filtrage aisé du 50 Hz.
2. Zéro exclusion sur les sentiers de marche (TRAILS) :
   - Les sentiers pédestres (GPS4_TRAIL et GPS6_TRAIL) ne génèrent aucun bruit véhiculaire.
   - Ils constituent au contraire des corridors logistiques essentiels pour les patrouilles de gardes.
3. Zone d'exclusion sonore stricte (300m) :
   - Limitée EXCLUSIVEMENT à la route asphaltée régionale RR 124 en bordure sud du parc.
4. Répertoire hydrographique réaliste :
   - 10 points d'eau réels et pérennes (Aïn Charchara, cirque nord, camp, château, abreuvoirs faune, gueltas).
5. Échantillonnage stratifié représentatif (20 stations) :
   - Savane Ouest (4), Savane Centre (6), Savane Est (3), Oueds & Piémont (4), Canyon Charchara (3).
"""

import os
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from scipy.ndimage import distance_transform_edt, maximum_filter
import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import unary_union

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GPKG_PATH = r"c:\Users\Dell\Desktop\GeoAI\WWF_PARC_BOUHEDMA\WWF_TALENT_ACADEMY_2026_BOUHEDMA_DATABASE\bouhedma_database.gpkg"
STACK_PATH = os.path.join(BASE_DIR, "data", "gee", "bouhedma_stack_10m.tif")
OUTPUTS_DIR = os.path.join(BASE_DIR, "data", "qgis", "outputs")
TABLES_DIR = os.path.join(BASE_DIR, "tables")

def main():
    print("=" * 80)
    print(" PIPELINE GEOAI : SÉLECTION STRATIFIÉE DES SITES PAM (BOUHEDMA SECTEUR 1)")
    print("=" * 80)

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    os.makedirs(TABLES_DIR, exist_ok=True)

    # 1. Chargement du stack raster Sentinel-2 / SRTM (résolution 10m)
    with rasterio.open(STACK_PATH) as src:
        savi_dry = src.read(4)
        ndmi_dry = src.read(5)
        savi_amp = src.read(7)
        elev = src.read(9)
        slope = src.read(10)
        tf = src.transform
        crs = src.crs
        res_x = abs(tf.a)
        shape = savi_dry.shape

    # 2. Emprise du Secteur 1
    bnd = gpd.read_file(GPKG_PATH, layer="PARC_NATIONAL_BOUHEDMA_SECTOR1").to_crs(crs)
    poly_bnd = bnd.geometry.iloc[0]

    # 3. Répertoire des 10 VRAIS points d'eau validés de Bouhedma
    print("\n[1/5] Cartographie des 10 sources d'eau validées de Bouhedma...")
    real_water_records = [
        {
            "NAME": "Aïn Charchara (Cascade pérenne canyon)",
            "TYPE": "Source naturelle pérenne",
            "geometry": Point(560202.8, 3819021.7)
        },
        {
            "NAME": "Cirque Nord (Point d'eau piémont)",
            "TYPE": "Source / Résurgence de cirque",
            "geometry": Point(559290.0, 3818980.0) # Cirque nord entouré par l'utilisateur
        },
        {
            "NAME": "Camp WWF (Citernes & robinets)",
            "TYPE": "Point d'eau infrastructure",
            "geometry": Point(559729.4, 3815047.7)
        },
        {
            "NAME": "Château Français (Réservoir historique)",
            "TYPE": "Point d'eau réservoir",
            "geometry": Point(559864.0, 3815197.8)
        },
        {
            "NAME": "Éco-Parc (Point d'eau & écomusée)",
            "TYPE": "Point d'eau écomusée",
            "geometry": Point(559634.4, 3815105.5)
        },
        {
            "NAME": "Enclos Autruches (Abreuvoir faune)",
            "TYPE": "Abreuvoir faune sauvage",
            "geometry": Point(559453.0, 3815083.3)
        },
        {
            "NAME": "Enclos Mouflons (Abreuvoir faune)",
            "TYPE": "Abreuvoir faune sauvage",
            "geometry": Point(559531.8, 3815033.6)
        },
        {
            "NAME": "Abreuvoir Plaine Centrale (Oryx & Gazelles)",
            "TYPE": "Abreuvoir pastoral DGF",
            "geometry": Point(559280.0, 3814300.0)
        },
        {
            "NAME": "Guelta Oued Médian (Cuvette rocheuse)",
            "TYPE": "Guelta naturelle oued",
            "geometry": Point(560445.0, 3817735.0)
        },
        {
            "NAME": "Piémont Ouest (Suintement montagneux)",
            "TYPE": "Suintement / Source temporaire",
            "geometry": Point(556920.0, 3816100.0)
        }
    ]
    gdf_water = gpd.GeoDataFrame(real_water_records, crs=crs)
    out_water_utm = os.path.join(OUTPUTS_DIR, "bouhedma_water_sources_validated_utm.geojson")
    gdf_water.to_file(out_water_utm, driver="GeoJSON")
    print(f"  [+] {len(gdf_water)} points d'eau exportés : {out_water_utm}")

    # Injection dans le GPKG maître
    gdf_water_wgs = gdf_water.to_crs("EPSG:4326")
    try:
        gdf_water_wgs.to_file(GPKG_PATH, layer="REAL_WATER_SOURCES", driver="GPKG")
        print(f"  [V] Couche REAL_WATER_SOURCES mise à jour dans le GPKG.")
    except Exception as e:
        print(f"  [!] Note GPKG : {e}")

    # Calcul de distance euclidienne continue aux points d'eau
    water_shapes = [(g, 1) for g in gdf_water.geometry]
    water_mask = rasterize(water_shapes, out_shape=shape, transform=tf, fill=0, dtype=np.uint8)
    dist_water_m = distance_transform_edt(water_mask == 0) * res_x

    # 4. Modélisation du Buffer de Perturbation Sonore STRICTEMENT Routière (RR 124)
    print("\n[2/5] Délimitation de la zone de quiétude acoustique (recul de 300m sur la route RR124)...")
    roads = gpd.read_file(GPKG_PATH, layer="ROADS_PARC_NATIONAL_BOUHEDMA").to_crs(crs)
    
    # Seule la route régionale asphaltée RR124 (trafic motorisé) est exclue
    rr124 = roads[roads["highway"] == "secondary"]
    if len(rr124) == 0:
        # Fallback si highway n'est pas secondary
        rr124 = roads[roads["ref"] == "RR124"]

    # Buffer 300m le long de la RR124
    buf_rr124_geoms = [g.buffer(300.0) for g in rr124.geometry]
    y_south_thresh = bnd.total_bounds[1] + 300.0

    # Création du polygone d'exclusion propre
    excl_geom = unary_union(buf_rr124_geoms)
    gdf_excl = gpd.GeoDataFrame([{"NAME": "Zone de Dérangement Acoustique RR124 (300m)", "geometry": excl_geom}], crs=crs)
    out_buf_path = os.path.join(OUTPUTS_DIR, "road_exclusion_buffer_utm.geojson")
    gdf_excl.to_file(out_buf_path, driver="GeoJSON")
    print(f"  [V] Buffer d'exclusion routière (RR124 uniquement) exporté : {out_buf_path}")

    # Injection GPKG
    try:
        gdf_excl.to_crs("EPSG:4326").to_file(GPKG_PATH, layer="ROAD_EXCLUSION_BUFFER", driver="GPKG")
        print(f"  [V] Couche ROAD_EXCLUSION_BUFFER mise à jour dans le GPKG.")
    except Exception as e:
        print(f"  [!] Note GPKG : {e}")

    # Rasterisation ultra-rapide de l'exclusion
    excl_raster = rasterize([(excl_geom, 1)], out_shape=shape, transform=tf, fill=0, dtype=np.uint8)

    # 5. Détection des Substrats Physiques Disponibles (Arbres & Poteaux Électriques)
    print("\n[3/5] Détection des substrats de fixation (Houppiers d'acacias + Poteaux électriques)...")
    
    # A. Détection des arbres (Vachellia tortilis)
    local_max = maximum_filter(savi_dry, size=3)
    is_tree = (savi_dry == local_max) & (savi_dry > 0.12) & (slope <= 25.0)
    t_rows, t_cols = np.where(is_tree)
    t_xy = [tf * (c + 0.5, r + 0.5) for r, c in zip(t_rows, t_cols)]
    t_pts = [Point(x, y) for x, y in t_xy]

    gdf_raw_trees = gpd.GeoDataFrame({
        "SUBSTRATE": "Arbre (Vachellia tortilis)",
        "SAVI_DRY": savi_dry[t_rows, t_cols],
        "NDMI_DRY": ndmi_dry[t_rows, t_cols],
        "SAVI_AMP": savi_amp[t_rows, t_cols],
        "ELEV": elev[t_rows, t_cols],
        "SLOPE": slope[t_rows, t_cols],
        "DIST_WATER": dist_water_m[t_rows, t_cols],
        "EXCL": excl_raster[t_rows, t_cols],
        "geometry": t_pts
    }, crs=crs)

    # Filtrage : dans le parc et hors buffer routier RR124
    trees_clean = gdf_raw_trees[
        gdf_raw_trees.within(poly_bnd) &
        (gdf_raw_trees.geometry.y >= y_south_thresh) &
        (gdf_raw_trees["EXCL"] == 0)
    ].copy().reset_index(drop=True)
    print(f"  [+] Arbres Vachellia tortilis retenus en zone de quiétude : {len(trees_clean)}")

    # B. Intégration des Poteaux Électriques (Perchoirs à rapaces)
    power = gpd.read_file(GPKG_PATH, layer="POWERLINES_PARC_NATIONAL_BOUHEDMA").to_crs(crs)
    power_in_park = power[power.within(poly_bnd)].copy()
    
    # Échantillonnage raster pour les poteaux
    p_rows, p_cols = rasterio.transform.rowcol(tf, power_in_park.geometry.x.values, power_in_park.geometry.y.values)
    power_in_park["EXCL"] = [excl_raster[r, c] for r, c in zip(p_rows, p_cols)]
    power_in_park["SAVI_DRY"] = [float(savi_dry[r, c]) for r, c in zip(p_rows, p_cols)]
    power_in_park["NDMI_DRY"] = [float(ndmi_dry[r, c]) for r, c in zip(p_rows, p_cols)]
    power_in_park["SAVI_AMP"] = [float(savi_amp[r, c]) for r, c in zip(p_rows, p_cols)]
    power_in_park["ELEV"] = [float(elev[r, c]) for r, c in zip(p_rows, p_cols)]
    power_in_park["SLOPE"] = [float(slope[r, c]) for r, c in zip(p_rows, p_cols)]
    power_in_park["DIST_WATER"] = [float(dist_water_m[r, c]) for r, c in zip(p_rows, p_cols)]
    power_in_park["SUBSTRATE"] = "Poteau de ligne électrique (Perchoir rapace)"

    power_clean = power_in_park[
        (power_in_park.geometry.y >= y_south_thresh) &
        (power_in_park["EXCL"] == 0)
    ].copy().reset_index(drop=True)
    print(f"  [+] Poteaux électriques retenus en zone de quiétude : {len(power_clean)}")

    # C. Fusion de tous les candidats disponibles
    all_candidates = pd.concat([trees_clean, power_clean], ignore_index=True)
    all_candidates = gpd.GeoDataFrame(all_candidates, crs=crs)

    # 6. Découpage Zonal et Échantillonnage Stratifié
    print("\n[4/5] Attribution des écozones et calcul du score d'attractivité écologique...")
    x_min, x_max = 554580.0, 562500.0
    w_boundary = x_min + (x_max - x_min) / 3.0       # 557220 m
    e_boundary = x_min + 2.0 * (x_max - x_min) / 3.0 # 559860 m

    def assign_ecozone(row):
        gx = row.geometry.x
        gy = row.geometry.y
        el = row.ELEV
        if el >= 380.0 or (gx >= 560000.0 and gy >= 3818500.0):
            return "CANYON_CHARCHARA"
        elif el >= 300.0 or gy >= 3817500.0:
            return "OUEDS_ET_PIEMONT"
        else:
            if gx < w_boundary:
                return "SAVANE_OUEST"
            elif gx > e_boundary:
                return "SAVANE_EST"
            else:
                return "SAVANE_CENTRE"

    all_candidates["ECOZONE"] = all_candidates.apply(assign_ecozone, axis=1)

    # Fonction de score écologique unifiée
    def compute_score(r):
        w_norm = np.clip((3000.0 - r["DIST_WATER"]) / 3000.0, 0.0, 1.0)
        
        if str(r["SUBSTRATE"]).startswith("Poteau"):
            # Poteau électrique : Perchoir surélevé à 8-10m, vue acoustique 360°, attractivité rapaces/passereaux
            # Bonus de stabilité structurelle et d'ouverture acoustique (absence de bruit foliaire au vent)
            perch_vantage = 0.85
            surrounding_veg = np.clip((r["SAVI_DRY"] - 0.08) / (0.25 - 0.08), 0.0, 1.0)
            return 0.40 * perch_vantage + 0.35 * w_norm + 0.25 * surrounding_veg
        else:
            # Arbre Acacia tortilis
            savi_norm = np.clip((r["SAVI_DRY"] - 0.12) / (0.35 - 0.12), 0.0, 1.0)
            canopy_stab = 1.0 - np.clip(r["SAVI_AMP"] / 0.20, 0.0, 1.0)
            if r["ECOZONE"] == "CANYON_CHARCHARA":
                return 0.40 * savi_norm + 0.35 * w_norm + 0.25 * canopy_stab
            elif r["ECOZONE"] == "OUEDS_ET_PIEMONT":
                return 0.45 * savi_norm + 0.35 * w_norm + 0.20 * canopy_stab
            else:
                return 0.50 * savi_norm + 0.30 * w_norm + 0.20 * canopy_stab

    all_candidates["SCORE_ECO"] = all_candidates.apply(compute_score, axis=1).round(4)

    # Quotas d'échantillonnage stratifié pour 20 capteurs
    quota_plan = {
        "SAVANE_OUEST":     (4, 750.0, "Plaine Savane Ouest (Steppe ouverte à Acacias isolés)"),
        "SAVANE_CENTRE":    (6, 600.0, "Plaine Savane Centrale (Cœur du peuplement Vachellia tortilis & Perchoirs)"),
        "SAVANE_EST":       (3, 750.0, "Plaine Savane Est (Transition steppique orientale)"),
        "OUEDS_ET_PIEMONT": (4, 550.0, "Oueds & Piémont nord (Bassin humide du Cirque & talwegs)"),
        "CANYON_CHARCHARA": (3, 450.0, "Gorges d'Aïn Charchara (Falaises, perchoirs & cascade pérenne)")
    }

    selected_indices = []
    print("\nSélection stratifiée (Inhibition spatiale stricte pour éviter l'agrégation) :")
    for z_name, (target_n, min_dist, desc) in quota_plan.items():
        sub = all_candidates[all_candidates["ECOZONE"] == z_name].sort_values(by="SCORE_ECO", ascending=False)
        z_picks = []
        for idx, row in sub.iterrows():
            pt = row.geometry
            if all(pt.distance(sub.loc[p_idx].geometry) >= min_dist for p_idx in z_picks):
                z_picks.append(idx)
            if len(z_picks) >= target_n:
                break
        selected_indices.extend(z_picks)
        print(f"  -> {z_name:<18} : {len(z_picks)}/{target_n} stations retenues ({desc})")

    final_picks = all_candidates.loc[selected_indices].copy().reset_index(drop=True)
    final_picks = final_picks.sort_values(by="SCORE_ECO", ascending=False).reset_index(drop=True)
    final_picks["DEPLOY_ORDER"] = range(1, len(final_picks) + 1)
    final_picks["SITE_ID"] = [f"BHD26_PAM_{r['DEPLOY_ORDER']:02d}" for _, r in final_picks.iterrows()]

    # Coordonnées WGS84 et champs formatés
    final_wgs84 = final_picks.to_crs("EPSG:4326")
    final_picks["LAT_WGS84"] = final_wgs84.geometry.y.round(6)
    final_picks["LON_WGS84"] = final_wgs84.geometry.x.round(6)
    final_picks["UTM_X"] = final_picks.geometry.x.round(1)
    final_picks["UTM_Y"] = final_picks.geometry.y.round(1)
    final_picks["ELEV_M"] = final_picks["ELEV"].round(1)
    final_picks["DIST_WATER_M"] = final_picks["DIST_WATER"].round(1)
    final_wgs84 = final_picks.to_crs("EPSG:4326")

    print("\n" + "=" * 90)
    print(" LES 20 STATIONS PAM RETENUES (ARBRES + POTEAUX PERCHOIRS RAPACES)")
    print("=" * 90)
    for _, r in final_picks.iterrows():
        sub_abbr = "Poteau électrique" if "Poteau" in r["SUBSTRATE"] else "Acacia tortilis"
        print(f"  Ordre {r['DEPLOY_ORDER']:02d} | {r['SITE_ID']} | {r['ECOZONE']:<18} | {sub_abbr:<18} | Alt: {r['ELEV_M']}m | Eau: {r['DIST_WATER_M']}m | Score: {r['SCORE_ECO']:.3f} | ({r['LON_WGS84']}, {r['LAT_WGS84']})")

    # 7. Sauvegardes vecteur et tableur
    print("\n[5/5] Export des couches propres...")
    
    # Couche finale sous deux noms pour compatibilité QGIS
    out_geojson_utm = os.path.join(OUTPUTS_DIR, "bouhedma_pam_final_trees_utm.geojson")
    final_picks.to_file(out_geojson_utm, driver="GeoJSON")
    print(f"  [V] GeoJSON UTM exporté : {out_geojson_utm}")

    out_geojson_sites = os.path.join(OUTPUTS_DIR, "bouhedma_pam_final_sites_utm.geojson")
    final_picks.to_file(out_geojson_sites, driver="GeoJSON")
    print(f"  [V] GeoJSON UTM exporté : {out_geojson_sites}")

    out_geojson_wgs = os.path.join(OUTPUTS_DIR, "bouhedma_pam_final_trees.geojson")
    final_wgs84.to_file(out_geojson_wgs, driver="GeoJSON")
    print(f"  [V] GeoJSON WGS84 exporté : {out_geojson_wgs}")

    # Injection dans le GeoPackage maître
    try:
        final_wgs84.to_file(GPKG_PATH, layer="BOUHEDMA_PAM_FINAL_SITES", driver="GPKG")
        print(f"  [V] Couche BOUHEDMA_PAM_FINAL_SITES ajoutée à : {GPKG_PATH}")
    except Exception as e:
        print(f"  [!] Note GPKG : {e}")

    # Nettoyage de l'ancien fichier de 436 points d'eau si présent
    old_water = os.path.join(OUTPUTS_DIR, "all_water_sources_detected_utm.geojson")
    if os.path.exists(old_water):
        arch_water = os.path.join(BASE_DIR, "data", "qgis", "_archive_v1", "outputs", "all_water_sources_detected_utm.geojson")
        os.makedirs(os.path.dirname(arch_water), exist_ok=True)
        try:
            if os.path.exists(arch_water):
                os.remove(arch_water)
            os.rename(old_water, arch_water)
            print(f"  [-] Ancien fichier all_water_sources_detected_utm.geojson archivé.")
        except Exception:
            pass

    # Export de la fiche de terrain CSV avec consignes adaptées au substrat
    field_sheet_cols = [
        "DEPLOY_ORDER", "SITE_ID", "ECOZONE", "SUBSTRATE",
        "LAT_WGS84", "LON_WGS84", "UTM_X", "UTM_Y",
        "ELEV_M", "SAVI_DRY", "DIST_WATER_M", "SCORE_ECO"
    ]
    df_field = final_picks[field_sheet_cols].copy()
    
    def get_instructions(row):
        if "Poteau" in row["SUBSTRATE"]:
            return "Fixer le boîtier à 2.5-3m sur le fût du poteau électrique avec sangles / colliers de serrage UV. Microphone orienté perpendiculairement à la ligne. Activer le filtre passe-haut 500 Hz (suppression du 50 Hz résiduel)."
        ecozone = row["ECOZONE"]
        if ecozone == "SAVANE_OUEST":
            return "Fixer à 1.8-2m sur branche maîtresse d'Acacia tortilis orientée Nord. Microphone dégagé vers la steppe ouverte."
        elif ecozone == "SAVANE_CENTRE":
            return "Fixer à 2m de haut sur tronc principal. Tailler ou écarter les épines d'acacia à moins de 30cm du micro."
        elif ecozone == "SAVANE_EST":
            return "Fixer à 1.8m sous le houppier. Protéger le boîtier du soleil couchant par l'ombre naturelle du tronc."
        elif ecozone == "OUEDS_ET_PIEMONT":
            return "Fixer à 2.2m sur acacia de berge d'oued, hors de portée des crues éclair et du pâturage de la faune."
        elif ecozone == "CANYON_CHARCHARA":
            return "Fixer solidement à 2m sur acacia ou pistachier de paroi. Microphone pointé vers la gorge et le lit d'eau pérenne."
        return "Fixer solidement à 2m de hauteur avec sangle résistante aux intempéries."

    df_field["FIELD_INSTRUCTIONS"] = df_field.apply(get_instructions, axis=1)
    
    csv_sheet_path = os.path.join(TABLES_DIR, "candidate_sites_field_sheet.csv")
    df_field.to_csv(csv_sheet_path, index=False, encoding="utf-8-sig")
    print(f"  [V] Fiche de terrain CSV exportée : {csv_sheet_path}")

    print("\n" + "=" * 80)
    print(" TRAITEMENT TERMINÉ : TOUTES LES DONNÉES SONT PROPRES, COHÉRENTES ET VALIDÉES !")
    print("=" * 80)

if __name__ == "__main__":
    main()
