import osmnx as ox
import geopandas as gpd

# --- 1. Define the Place ---
address_name = "Praça dos Três Poderes, Brasília, Brazil"
map_distance = 1500 # Distance in meters (1.5 km)
output_filename = "roads_with_tags.geojson"

print(f"Downloading street network data for the area around {address_name}...")

# --- 2. Download the Street Network Data ---
try:
    graph = ox.graph_from_address(address_name, dist=map_distance, network_type='all')
    print("Download complete.")

    # --- 3. Convert Graph to GeoDataFrame ---
    # We convert the graph edges (the roads) to a GeoDataFrame.
    # Each row represents a road segment, and the 'geometry' column holds the LineString.
    print("Converting graph to GeoDataFrame...")
    gdf_edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # --- 4. Add Required OSM Tags ---
    # We add new columns to the GeoDataFrame. Each column represents an OSM tag.
    # All roads in this file will be assigned these same values.
    print("Adding required OSM tags...")
    gdf_edges['highway'] = 'track'
    gdf_edges['maxspeed'] = '50'
    gdf_edges['name'] = 'estrada'
    gdf_edges['surface'] = 'unpaved'
    gdf_edges['tracktype'] = 'grade2'

    # --- 5. Save to GeoJSON ---
    # The to_file method saves the GeoDataFrame to a file.
    # We specify the 'GeoJSON' driver to ensure the correct format.
    # The resulting file will contain LineString geometries and the specified properties.
    print(f"Saving data to '{output_filename}'...")
    
    # We select only the geometry and the new tag columns for a clean output file.
    columns_to_save = ['geometry', 'highway', 'maxspeed', 'name', 'surface', 'tracktype']
    gdf_edges[columns_to_save].to_file(output_filename, driver='GeoJSON')
    
    print(f"Successfully saved GeoJSON file to '{output_filename}'.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection and that the address is correct.")
    print("You may also need to install the required libraries: pip install osmnx geopandas")