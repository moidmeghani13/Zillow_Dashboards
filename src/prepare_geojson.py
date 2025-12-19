import geopandas as gpd

SHAPEFILE_PATH = "Data/Geo/cb_2020_us_zcta520_500k.zip"
OUTPUT_GEOJSON = "Data/Geo/us_zipcodes.geojson"

gdf = gpd.read_file(SHAPEFILE_PATH)
gdf = gdf[["ZCTA5CE20", "geometry"]]

gdf = gdf.rename(columns={"ZCTA5CE20": "zip"})

gdf["zip"] = gdf["zip"].astype(str)

gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

print("GeoJSON saved to:", OUTPUT_GEOJSON)