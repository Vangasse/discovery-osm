import osmnx as ox
import matplotlib.pyplot as plt
import contextily as ctx

# --- 1. Define the Place ---
# Specify the name of the place you want to get the map for.
address_name = "Praça dos Três Poderes, Brasília, Brazil"
map_distance = 1500 # Distance in meters (1.5 km)

print(f"Downloading street network data for the area around {address_name}...")

# --- 2. Download the Street Network Data ---
# Use osmnx to download the street network data for the specified address.
try:
    # Download the original graph
    graph = ox.graph_from_address(address_name, dist=map_distance, network_type='all')
    print("Download complete.")

    # --- 3. Project the Graph ---
    # Project the graph from its original CRS (WGS84) to the Web Mercator CRS (EPSG:3857)
    # This is necessary for compatibility with most web map tile services.
    graph_proj = ox.project_graph(graph, to_crs='epsg:3857')

    # --- 4. Plot the Map with Aerial Imagery ---
    print("\nPlotting the map...")
    # Plot the projected graph. We set a visible edge color and make the background transparent.
    fig, ax = ox.plot_graph(
        graph_proj,
        node_size=0,               # Hide the nodes
        edge_linewidth=1,          # Set the thickness of the street lines
        edge_color='white',        # White is often visible on satellite images
        edge_alpha=0.8,            # Make lines slightly transparent
        bgcolor='none',            # Make the plot background transparent to see the basemap
        show=False,
        close=False
    )

    # --- 5. Add the Aerial Basemap ---
    # Use contextily to add a satellite imagery basemap to the axes.
    # The source is Esri's World Imagery service.
    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, zoom='auto')
    
    # --- 6. Customize and Show the Plot ---
    # Remove the axis labels for a cleaner look
    ax.set_axis_off()
    ax.set_title(f"Street Network around {address_name}", fontsize=14, color='black')


    # Display the plot.
    plt.show()
    print("Plot displayed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection and that the address is correct.")
    print("You may also need to install the required libraries: pip install osmnx matplotlib contextily")

