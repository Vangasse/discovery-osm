import geopandas as gpd
import matplotlib.pyplot as plt

# --- 1. Define the Filename ---
input_filename = "roads_with_tags.geojson"

print(f"Loading GeoJSON file: '{input_filename}'...")

# --- 2. Load the GeoJSON File ---
# Use a try-except block to handle cases where the file doesn't exist.
try:
    # geopandas.read_file can directly read a GeoJSON file into a GeoDataFrame.
    gdf = gpd.read_file(input_filename)
    print("File loaded successfully.")

    # --- 3. Plot the Roads ---
    # The .plot() method on a GeoDataFrame will render its geometries.
    print("Plotting the roads...")
    fig, ax = plt.subplots(figsize=(10, 10)) # Create a figure and axes for plotting

    gdf.plot(
        ax=ax,              # Specify the axes to draw on
        color='#5a7d60',    # Color for the roads (can be any color)
        linewidth=1.5       # Thickness of the road lines
    )

    # --- 4. Customize and Show the Plot ---
    ax.set_title("Roads Loaded from GeoJSON File", fontsize=14)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_aspect('equal', adjustable='box') # Ensure correct aspect ratio
    plt.grid(True) # Add a grid for better visualization
    plt.show()
    print("Plot displayed.")

except FileNotFoundError:
    print(f"Error: The file '{input_filename}' was not found.")
    print("Please make sure this script is in the same directory as the GeoJSON file, or provide the full path.")
except Exception as e:
    print(f"An error occurred: {e}")