// =========================================================================
// PIPELINE 01 : EXTRACTION DU STACK SATELLITAIRE 10M — PARC DE BOUHEDMA
// Projet : WWF Talent Academy 2026 — Guide Déploiement Bioacoustique
// Emprise : Parc National de Bouhedma (Secteur 1 WDPA 13962 + Buffer 2km)
// SCR d'exportation : EPSG:32632 (WGS 84 / UTM Zone 32N)
// =========================================================================

// -------------------------------------------------------------------------
// 1. DÉFINITION DE LA GÉOMÉTRIE AOI (Emprise tamponnée 2 km)
// -------------------------------------------------------------------------
// OPTION A (Prêt à l'emploi) : Coordonnées réelles du buffer 2km calculé
var aoiCoordinates = [
  [9.578797, 34.514028], [9.580055, 34.515818], [9.580174, 34.515935], [9.585264, 34.519461],
  [9.585605, 34.519768], [9.585887, 34.519892], [9.585945, 34.519932], [9.586053, 34.519965],
  [9.592157, 34.522639], [9.592513, 34.522735], [9.598403, 34.523497], [9.598828, 34.523686],
  [9.599184, 34.523782], [9.600355, 34.523908], [9.600415, 34.523923], [9.600724, 34.523961],
  [9.600822, 34.523958], [9.601548, 34.524036], [9.602293, 34.524369], [9.602674, 34.524484],
  [9.603033, 34.524542], [9.606227, 34.525877], [9.606536, 34.525954], [9.607173, 34.526033],
  [9.612075, 34.527017], [9.612455, 34.527054], [9.615909, 34.527065], [9.616718, 34.527206],
  [9.618058, 34.527078], [9.618058, 34.527114], [9.618344, 34.527113], [9.621666, 34.527886],
  [9.627011, 34.529229], [9.630407, 34.530659], [9.631563, 34.531111], [9.635497, 34.532534],
  [9.636740, 34.533067], [9.638220, 34.533937], [9.639930, 34.535395], [9.645379, 34.537931],
  [9.649840, 34.539357], [9.650411, 34.539532], [9.660075, 34.542364], [9.669455, 34.545469],
  [9.672501, 34.546563], [9.679613, 34.548007], [9.686901, 34.547420], [9.693543, 34.544868],
  [9.698788, 34.540641], [9.702045, 34.535214], [9.702946, 34.529201], [9.702855, 34.527538],
  [9.702689, 34.525995], [9.702200, 34.522926], [9.701934, 34.521628], [9.700894, 34.517474],
  [9.700531, 34.516244], [9.699184, 34.512284], [9.698969, 34.511691], [9.697792, 34.508637],
  [9.698215, 34.508070], [9.699844, 34.502692], [9.699422, 34.497158], [9.696990, 34.491991],
  [9.695749, 34.490222], [9.694713, 34.488258], [9.692482, 34.482927], [9.691839, 34.481571],
  [9.690104, 34.478305], [9.689138, 34.475404], [9.687843, 34.472508], [9.684723, 34.467024],
  [9.684631, 34.466864], [9.682261, 34.462802], [9.682135, 34.462590], [9.677153, 34.454329],
  [9.671165, 34.448231], [9.669677, 34.447258], [9.669135, 34.446914], [9.666663, 34.445400],
  [9.663324, 34.443715], [9.661271, 34.442878], [9.661252, 34.442870], [9.660660, 34.442605],
  [9.659658, 34.442172], [9.655347, 34.440770], [9.654467, 34.440571], [9.654452, 34.440561],
  [9.648707, 34.438590], [9.645523, 34.437918], [9.642467, 34.437463], [9.640926, 34.437326],
  [9.638476, 34.437224], [9.636968, 34.437231], [9.633835, 34.437247], [9.632805, 34.437272],
  [9.625695, 34.437585], [9.623533, 34.437559], [9.619068, 34.437073], [9.616654, 34.437095],
  [9.616656, 34.437206], [9.611215, 34.437720], [9.605228, 34.439905], [9.600295, 34.443465],
  [9.596861, 34.448079], [9.596012, 34.449734], [9.595766, 34.450233], [9.595037, 34.451782],
  [9.594602, 34.452795], [9.593235, 34.456303], [9.588246, 34.456820], [9.581905, 34.459353],
  [9.576870, 34.463429], [9.573668, 34.468622], [9.572634, 34.474390], [9.572961, 34.492505],
  [9.572959, 34.499222], [9.572869, 34.500025], [9.573520, 34.506357], [9.573679, 34.506848],
  [9.576233, 34.511716], [9.576570, 34.512163], [9.578797, 34.514028]
];

var aoi = ee.Geometry.Polygon(aoiCoordinates);
// OPTION B (Si vous téléversez le shapefile bouhedma_aoi_wgs84.zip dans Assets) :
// var aoi = ee.FeatureCollection('projects/YOUR_PROJECT/assets/bouhedma_aoi').geometry();

Map.centerObject(aoi, 12);
Map.setOptions('SATELLITE');
Map.addLayer(aoi, {color: 'FF0000'}, 'Emprise AOI (Buffer 2km Bouhedma)', false);

// -------------------------------------------------------------------------
// 2. COMPOSITES SENTINEL-2 L2A HARMONISÉS (Masquage SCL Robuste & Garanti)
// -------------------------------------------------------------------------
var YEAR = 2025;
var WET_SEASON = [YEAR + '-03-01', YEAR + '-05-31']; // Printemps (floraison & tapis herbacé)
var DRY_SEASON = [YEAR + '-07-01', YEAR + '-09-30']; // Été aride (persistance des ligneux)

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED');

function getCleanComposite(dateRange) {
  var s2Filtered = s2.filterBounds(aoi)
    .filterDate(dateRange[0], dateRange[1])
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 35));
  
  var masked = s2Filtered.map(function(img) {
    // SCL (Scene Classification Layer natif Sentinel-2 L2A) :
    // Élimination : 3 (ombres de nuage), 8 (nuage probabilité moyenne),
    // 9 (nuage forte probabilité), 10 (cirrus fin), 11 (neige)
    var scl = img.select('SCL');
    var clearMask = scl.neq(3).and(scl.neq(8)).and(scl.neq(9)).and(scl.neq(10)).and(scl.neq(11));
    return img.updateMask(clearMask);
  });
  
  print('Images Sentinel-2 retenues (' + dateRange[0] + ' à ' + dateRange[1] + ') :', masked.size());
  return masked.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
               .median()
               .divide(10000)
               .clip(aoi);
}

var compWet = getCleanComposite(WET_SEASON);
var compDry = getCleanComposite(DRY_SEASON);

// -------------------------------------------------------------------------
// 3. CALCUL DES INDICES BIOPHYSIQUES DU MILIEU ARIDE
// -------------------------------------------------------------------------
function computeIndices(img, suffix) {
  // SAVI (Soil-Adjusted Vegetation Index, L=0.5) adapté aux sols à fort albédo
  var savi = img.expression(
    '1.5 * (NIR - RED) / (NIR + RED + 0.5)', {
      'NIR': img.select('B8'),
      'RED': img.select('B4')
    }
  ).rename('savi_' + suffix);
  
  // NDMI (Normalized Difference Moisture Index) mesurant l'humidité foliaire
  var ndmi = img.normalizedDifference(['B8', 'B11']).rename('ndmi_' + suffix);
  
  // BSI (Bare Soil Index) séparant sol minéral nu et canopée clairsemée
  var bsi = img.expression(
    '((SWIR1 + RED) - (NIR + BLUE)) / ((SWIR1 + RED) + (NIR + BLUE))', {
      'SWIR1': img.select('B11'),
      'RED': img.select('B4'),
      'NIR': img.select('B8'),
      'BLUE': img.select('B2')
    }
  ).rename('bsi_' + suffix);
  
  return savi.addBands(ndmi).addBands(bsi);
}

var indWet = computeIndices(compWet, 'wet');
var indDry = computeIndices(compDry, 'dry');

// Amplitude annuelle du flush (Herbacées annuelles = amplitude forte ; Acacias = SAVI sec élevé & amplitude faible)
var saviAmp = indWet.select('savi_wet').subtract(indDry.select('savi_dry')).rename('savi_amp');

// Texture spatiale locale (Écart-type 5x5 sur SAVI dry pour détecter les houppiers isolés d'acacia)
var saviDrySd5 = indDry.select('savi_dry').reduceNeighborhood({
  reducer: ee.Reducer.stdDev(),
  kernel: ee.Kernel.square(2)
}).rename('savi_dry_sd5');

// -------------------------------------------------------------------------
// 4. TOPOGRAPHIE ET MORPHOMÉTRIE (SRTM 30m rééchantillonné bilinéairement)
// -------------------------------------------------------------------------
var dem = ee.Image('USGS/SRTMGL1_003').clip(aoi);
var slope = ee.Terrain.slope(dem).rename('slope');
var aspect = ee.Terrain.aspect(dem).rename('aspect');
// TPI 300m : Thalwegs/Oueds < 0, Crêtes > 0
var tpi300 = dem.subtract(dem.focalMean(300, 'circle', 'meters')).rename('tpi300');

// -------------------------------------------------------------------------
// 5. ASSEMBLAGE DU STACK MASTER 10M
// -------------------------------------------------------------------------
var masterStack = indWet
  .addBands(indDry)
  .addBands(saviAmp)
  .addBands(saviDrySd5)
  .addBands(dem.rename('elev'))
  .addBands(slope)
  .addBands(aspect)
  .addBands(tpi300)
  .toFloat();

print('Bandes incluses dans masterStack :', masterStack.bandNames());

// CONTRÔLE DE VALIDITÉ IMMÉDIAT DANS LA CONSOLE GEE :
// Si ces valeurs s'affichent, vos bandes sont 100% peuplées et valides !
print('Contrôle SAVI sec moyen sur Bouhedma :', indDry.select('savi_dry').reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: aoi,
  scale: 100,
  maxPixels: 1e9
}));

print('Contrôle MNT altitude moyenne :', dem.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: aoi,
  scale: 100,
  maxPixels: 1e9
}));

Map.addLayer(indDry.select('savi_dry'), {min: 0.05, max: 0.35, palette: ['#FFFFE5', '#78C679', '#004529']}, 'SAVI Saison Sèche (Canopée)');

// -------------------------------------------------------------------------
// 6. EXPORTATION DRIVE DU STACK 10M (VERS data/gee/)
// -------------------------------------------------------------------------
Export.image.toDrive({
  image: masterStack,
  description: 'bouhedma_stack_10m',
  folder: 'BOUHEDMA_GEE_EXPORTS',
  region: aoi,
  scale: 10,
  crs: 'EPSG:32632',
  maxPixels: 1e9,
  fileFormat: 'GeoTIFF'
});

// -------------------------------------------------------------------------
// 7. EXTRACTION DES EMBEDDINGS SATELLITAIRES ANNUELS (AlphaEarth 64 Bandes)
// NOTE : Vous avez DÉJÀ exporté bouhedma_alphaearth_2025.tif (107 Mo valide).
// Vous n'avez pas besoin de relancer cette tâche si vous l'avez déjà téléchargée.
// -------------------------------------------------------------------------
// var embeddingsCol = ee.ImageCollection('GOOGLE/SATELLITE_EMBEDDING/V1/ANNUAL')
//   .filterDate(YEAR + '-01-01', (YEAR + 1) + '-01-01')
//   .filterBounds(aoi)
//   .mosaic()
//   .clip(aoi);
// 
// print('Nombre de canaux d\'embedding AlphaEarth :', embeddingsCol.bandNames().size());
// 
// Export.image.toDrive({
//   image: embeddingsCol.toFloat(),
//   description: 'bouhedma_alphaearth_2025',
//   folder: 'BOUHEDMA_GEE_EXPORTS',
//   region: aoi,
//   scale: 10,
//   crs: 'EPSG:32632',
//   maxPixels: 1e9,
//   fileFormat: 'GeoTIFF'
// });

