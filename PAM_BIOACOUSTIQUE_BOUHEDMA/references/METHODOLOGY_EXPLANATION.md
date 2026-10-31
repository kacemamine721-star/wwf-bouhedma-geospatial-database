# Fondements Scientifiques & Méthodologie — Bouhedma PAM Network (v3)

> **Version :** Finale validée — WWF Talent Academy 2026  
> **Parc :** Parc National de Bouhedma, Secteur 1 (7,9 km E-O × 8,3 km N-S)  
> **Matériel :** Song Meter Micro 2 (Wildlife Acoustics) — 20 stations bioacoustiques passives

---

## 1. Pourquoi cette méthode ? (Le problème fondamental des milieux arides)

Dans la plupart des projets SIG de conservation, les praticiens utilisent soit un indice de végétation générique (NDVI), soit des modèles statistiques de distribution d'espèces (SDM comme **MaxEnt**). À Bouhedma, **ces approches classiques échouent pour trois raisons majeures** :

1. **L'artefact du sol clair en milieu aride :** Le sol minéral de Bouhedma possède un albédo élevé qui fausse le NDVI classique en surestimant le signal de la roche nue et en masquant la signature de la canopée clairsemée d'*Acacia tortilis*.
2. **L'antagonisme écologique des espèces :** Une carte unique d'« adéquation générale » n'a aucun sens biologique. Un rapace (*Aquila fasciata*, *Buteo rufinus*) a besoin d'un perchoir dominant au-dessus d'une plaine **très ouverte**, tandis qu'un insectivore (*Phoenicurus moussieri*, *Turdoides fulva*) exige une canopée fermée et de l'humidité.
3. **La rareté des occurrences géoréférencées :** Entraîner un modèle Machine Learning (MaxEnt) requiert ≥ 50–100 observations fiables par espèce. En leur absence, l'**Évaluation Spatiale Multicritère (SMCE)** avec **Processus Hiérarchique Analytique (AHP)** est la référence académique internationale *(Malczewski, 1999)*.

```
Approches Classiques (Inadaptées)           Notre Approche Spécifique (Bouhedma)
─────────────────────────────────           ────────────────────────────────────
• NDVI générique (trompé par le sol nu)  ─> SAVI (L=0.5) + Amplitude phénologique ΔSAVI
• Modèle unique moyenné                  ─> Score écologique par zone (5 écozones)
• MaxEnt sans données d'occurrence       ─> Sélection substrats réels + inhibition spatiale
```

---

## 2. Détection des Substrats Physiques Réels

### A. Arbres Vachellia tortilis — Maxima Locaux Spectraux (SAVI)

Les houppiers d'acacias sont détectés dans le raster Sentinel-2 (10 m/pixel, saison sèche juillet–septembre) par **filtrage de maxima locaux sur le SAVI** :

$$\text{SAVI} = \frac{(\rho_{\text{NIR}} - \rho_{\text{rouge}}) \times (1 + L)}{\rho_{\text{NIR}} + \rho_{\text{rouge}} + L}, \quad L = 0.5$$

**Seuils appliqués :**
- `SAVI_dry > 0.12` : seuil empirique séparant le sol minéral nu de la canopée pérenne
- `slope ≤ 25°` : stabilité de pose garantie et accès sécurisé
- Maximum local sur fenêtre 3×3 pixels (30 m) : un seul point par houppier

> **Référence :** Huete, A. R. (1988). *A soil-adjusted vegetation index (SAVI)*. Remote Sensing of Environment, 25(3), 295–309.

### B. Poteaux de Lignes Électriques — Perchoirs Naturels à Rapaces

Les 15 pylons de la ligne basse tension traversant le Secteur 1 (source : OpenStreetMap `power=tower/pole`) sont intégrés comme **candidats physiques valides**, au même titre que les acacias, pour les raisons suivantes :

- **Perchoirs d'affût primaires** pour *Falco tinnunculus*, *Buteo rufinus*, *Falco biarmicus*, *Lanius meridionalis* : en savane aride ouverte, les poteaux représentent souvent les seuls points hauts disponibles à des kilomètres.
- **Vue acoustique omnidirectionnelle 360°** sans bruit de feuilles ni occultation du micro par la canopée.
- **Montage standardisé** sur fût métallique à 2.5–3 m avec sangle UV résistante.
- **Fréquence réseau 50 Hz facilement filtrée** (filtre passe-haut 500 Hz recommandé) sans altération des vocalisations aviaires (1 500–8 000 Hz).

**Score composite des poteaux :**

$$\text{Score}_{\text{poteau}} = 0.40 \times P_{\text{vue}} + 0.35 \times W_{\text{norm}} + 0.25 \times V_{\text{surr}}$$

où $P_{\text{vue}} = 0.85$ (bonus fixe de vue panoramique), $W_{\text{norm}}$ = proximité eau normalisée sur 3 000 m, $V_{\text{surr}}$ = végétation environnante (SAVI local).

---

## 3. Modélisation Hydrologique — Les 10 Sources d'Eau Validées

### Pourquoi écarter le NDMI spectral ?

La première tentative automatique basée sur le **NDMI** (Normalized Difference Moisture Index) a produit **436 points aberrants** — essentiellement des ombres de parois rocheuses et des buissons humides — qui ne correspondent à aucune source accessible à la faune. Ces points ont été archivés dans `data/qgis/_archive_v1/`.

### Les 10 sources réelles validées sur le terrain

Le gradient de distance aux points d'eau est calculé par **transformée de distance euclidienne** (EDT) sur un raster binaire des 10 sources, normalisé sur 3 000 m (rayon de vol quotidien des gangas au lever du soleil) :

$$W_{\text{norm}} = \text{clip}\left(\frac{3000 - d_{\text{eau}}}{3000}, 0, 1\right)$$

| # | Nom | Type | Coordonnées UTM |
|---|-----|------|-----------------|
| 1 | Aïn Charchara | Source naturelle pérenne (cascade) | (560203, 3819022) |
| 2 | Cirque Nord | Résurgence de cirque (piémont) | (559290, 3818980) |
| 3 | Camp WWF | Citernes & robinets infrastructure | (559729, 3815048) |
| 4 | Château Français | Réservoir historique | (559864, 3815198) |
| 5 | Éco-Parc | Point d'eau écomusée | (559634, 3815106) |
| 6 | Enclos Autruches | Abreuvoir faune sauvage | (559453, 3815083) |
| 7 | Enclos Mouflons | Abreuvoir faune sauvage | (559532, 3815034) |
| 8 | Abreuvoir Plaine | Abreuvoir Oryx & Gazelles (DGF) | (559280, 3814300) |
| 9 | Guelta Oued Médian | Cuvette rocheuse pérenne | (560445, 3817735) |
| 10 | Piémont Ouest | Suintement montagneux temporaire | (556920, 3816100) |

> **Référence :** Gao, B. C. (1996). *NDMI: A normalized difference water index for remote sensing of vegetation liquid water from space*. Remote Sensing of Environment, 58(3), 257–266.

---

## 4. Définition des Zones d'Exclusion Acoustique

### Règle unique : Route Régionale RR 124 (300 m)

**La seule exclusion dure** appliquée est un recul de **300 m** de la route asphaltée régionale **RR 124** longeant la bordure sud du parc. Cette route supporte un trafic motorisé régulier susceptible de :
- Saturer le microphone par des bruits impulsifs de véhicules (dépassement du seuil de clippage)
- Créer des masques acoustiques sur la bande 500–2 000 Hz couvrant les chants de Ptéroclidés et Passereaux

### Ce qui n'est PAS exclu (corrections v3)

| Élément | Décision | Justification |
|---------|----------|---------------|
| Sentiers pédestres GPS4 & GPS6 (`TRAILS`) | ✅ **Aucune exclusion** | Zéro bruit moteur. Corridors logistiques ranger essentiels. |
| Pistes `track`/`service` OSM internes | ✅ **Aucune exclusion** | Trafic très rare, bruit < 40 dB à 50 m (Darras et al., 2019). |
| Lignes électriques | ✅ **Candidats positifs** | Perchoirs d'affût — voir §2.B. |

> **Note historique :** Les couches GPS4 et GPS6 avaient été initialement nommées `ROAD_OBSERVATION` dans le GeoPackage, entraînant par erreur leur exclusion à 20–50 m. Ces couches ont été renommées `TRAIL_OBSERVATION` dans la version finale. La RR 124 et les pistes carrossables internes proviennent d'OpenStreetMap (import `DAY1_14-09-2026`).

> **Référence :** Darras, K., et al. (2019). *Comparing the sampling performance of sound recorders versus point counts in bird monitoring*. Methods in Ecology and Evolution, 10(9), 1407–1419.

---

## 5. Score Écologique et Échantillonnage Stratifié

### Fonction de score unifiée (par site candidat)

$$\text{Score}_{\text{arbre}} = \alpha \cdot S_{\text{SAVI}} + \beta \cdot W_{\text{norm}} + \gamma \cdot (1 - A_{\text{SAVI}})$$

Les poids $(\alpha, \beta, \gamma)$ varient selon l'écozone :

| Écozone | $\alpha$ (Végétation) | $\beta$ (Eau) | $\gamma$ (Stabilité canopée) |
|---------|----------------------|---------------|------------------------------|
| CANYON_CHARCHARA | 0.40 | 0.35 | 0.25 |
| OUEDS_ET_PIEMONT | 0.45 | 0.35 | 0.20 |
| SAVANE_* | 0.50 | 0.30 | 0.20 |

où $S_{\text{SAVI}} = \text{clip}\left(\frac{\text{SAVI}_{\text{dry}} - 0.12}{0.35 - 0.12}, 0, 1\right)$ et $A_{\text{SAVI}} = \text{clip}\left(\frac{\text{SAVI}_{\text{amp}}}{0.20}, 0, 1\right)$.

### Algorithme d'Inhibition Spatiale (anti-pseudoréplication)

Sélectionner uniquement les pixels au score maximal concentrerait tous les enregistreurs dans un même bosquet d'acacias dense. Pour éviter cette **pseudo-réplication spatiale**, un algorithme d'**inhibition spatiale à rayon dur** (processus de Matérn de type II) est appliqué par écozone :

1. Sélection du candidat au score le plus élevé dans la zone.
2. Émission d'un cercle d'exclusion de $d_{\min}$ autour de ce point.
3. Sélection du meilleur candidat restant hors de tous les cercles.
4. Répétition jusqu'à atteindre le quota zonal.

| Écozone | Quota | $d_{\min}$ |
|---------|-------|-----------|
| SAVANE_OUEST | 4 | 750 m |
| SAVANE_CENTRE | 6 | 600 m |
| SAVANE_EST | 3 | 750 m |
| OUEDS_ET_PIEMONT | 4 | 550 m |
| CANYON_CHARCHARA | 3 | 450 m |
| **Total** | **20** | — |

> **Référence statistique :** Diggle, P. J. (1983). *Statistical Analysis of Spatial Point Patterns*. Academic Press, London. *(Processus ponctuels de Matérn de type II — inhibition à distance minimale stricte.)*

---

## 6. Analyse de la Couverture Spatiale des 20 Sites

### Distribution et espacement

- **Emprise couverte :** 4,4 km E-O × 5,8 km N-S sur les 7,9 × 8,3 km du Secteur 1
- **Espacement global moyen :** ~3 030 m entre toute paire de sites
- **Espacement minimum global :** 200 m (PAM_07 ↔ PAM_08, gorge d'Aïn Charchara — voulu, car la gorge est un couloir étroit)

### Points forts de la sélection

- Les 6 sites de `SAVANE_CENTRE` couvrent la bande d'acacias dense de 559 000 à 560 000 m E, le cœur de l'habitat de la savane.
- Les 4 sites de `OUEDS_ET_PIEMONT` intègrent correctement le cirque nord et la guelta, maximisant la détection des espèces liées à l'eau.
- Les 3 sites du `CANYON_CHARCHARA` sont regroupés dans le couloir étroit de la gorge — densité justifiée par la richesse spécifique rupestre.

### Limite identifiée — Savane Ouest

Les 4 sites de `SAVANE_OUEST` sont concentrés dans un rayon de 3 km autour de X = 556 500 m E (entre 556 295 et 556 765 m E), laissant la zone X < 556 000 m E (~1,7 km depuis le bord ouest du parc) **sans couverture**. Cette zone est de steppe minérale ouverte à faible richesse arboricole — l'absence d'acacias au SAVI > 0.12 explique qu'aucun substrat n'y a été détecté. Si un accès terrain confirme la présence de piémont végétalisé à l'extrême ouest, un 21ème site pourrait y être ajouté (ou remplacer PAM_20 dont le score est le plus bas, 0.479).

---

## 7. Protocole de Déploiement Terrain

### Fixation sur Acacia tortilis
- Hauteur : **1.8–2.0 m** sur branche maîtresse horizontale
- Orientation du microphone : dégagée vers l'espace ouvert (éviter les branches frottantes)
- Tailler ou écarter les épines d'acacia à moins de 30 cm du microphone
- Attaches : sangle nylon UV résistante + fil de fer inoxydable de sécurité

### Fixation sur Poteau Électrique (Perchoir rapace)
- Hauteur : **2.5–3.0 m** sur le fût métallique
- Fixation : colliers de serrage inox + sangle UV 25 mm
- Activer le **filtre passe-haut 500 Hz** dans Song Meter (élimine le 50 Hz résiduel de la ligne BT)
- Microphone perpendiculaire au fil de la ligne (évite le soufflement du vent le long du câble)

### Paramètres d'enregistrement recommandés (Song Meter Micro 2)
| Paramètre | Valeur | Justification |
|-----------|--------|---------------|
| Fréquence d'échantillonnage | 32 000 Hz | Nyquist 16 kHz → 100% couverture avifaune |
| Profondeur de bits | 16 bits | Rapport signal/bruit suffisant en milieu calme |
| Plage horaire | Aube –30 min → +90 min ; Crépuscule –30 → +30 min | Pic d'activité vocale des passereaux et rapaces |
| Filtre passe-haut (poteaux) | 500 Hz | Suppression du 50 Hz des lignes BT |
| Format | WAV PCM | Compatible BirdNET, Kaleidoscope Pro |

---

## 8. Références Bibliographiques Complètes

| Référence | Usage dans la méthode |
|-----------|----------------------|
| Huete, A. R. (1988). *Remote Sensing of Environment*, 25(3), 295–309. | Formule SAVI, facteur L=0.5 pour sol aride |
| Gao, B. C. (1996). *Remote Sensing of Environment*, 58(3), 257–266. | NDMI et gradient hydrique |
| Saaty, T. L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill. | Fondement AHP / pondération par paires |
| Malczewski, J. (1999). *GIS and Multicriteria Decision Analysis*. Wiley. | Cadre SMCE général |
| Diggle, P. J. (1983). *Statistical Analysis of Spatial Point Patterns*. Academic Press. | Inhibition spatiale Matérn type II |
| Darras, K. et al. (2019). *Methods in Ecology and Evolution*, 10(9), 1407–1419. | Comparaison PAM vs points d'écoute, seuils de bruit |
| Isenmann, P., Maurin, G. & DGF (2005). *Oiseaux de Tunisie*. SEOF, Paris. | Écologie des espèces détectables à Bouhedma |
| Wildlife Acoustics (2024). *Song Meter Micro 2 User Guide*. | Paramètres matériels de déploiement |


## 8. Références Bibliographiques Complètes

| Référence | Usage dans la méthode |
|-----------|----------------------|
| Huete, A. R. (1988). *Remote Sensing of Environment*, 25(3), 295–309. | Formule SAVI, facteur L=0.5 pour sol aride |
| Gao, B. C. (1996). *Remote Sensing of Environment*, 58(3), 257–266. | NDMI et gradient hydrique |
| Saaty, T. L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill. | Fondement AHP / pondération par paires |
| Malczewski, J. (1999). *GIS and Multicriteria Decision Analysis*. Wiley. | Cadre SMCE général |
| Diggle, P. J. (1983). *Statistical Analysis of Spatial Point Patterns*. Academic Press. | Inhibition spatiale Matérn type II |
| Darras, K. et al. (2019). *Methods in Ecology and Evolution*, 10(9), 1407–1419. | Comparaison PAM vs points d'écoute, seuils de bruit |
| Isenmann, P., Maurin, G. & DGF (2005). *Oiseaux de Tunisie*. SEOF, Paris. | Écologie des espèces détectables à Bouhedma |
| Wildlife Acoustics (2024). *Song Meter Micro 2 User Guide*. | Paramètres matériels de déploiement |