import osmnx as ox
import matplotlib.pyplot as plt

# --- 1. Define the Place using Coordinates ---
center_point = (-15.7998, -47.8645) # Coordinates for Praça dos Três Poderes
map_distance = 500 # Distance is now 500 meters

print(f"Downloading street network data for the area around {center_point}...")

# --- 2. Download the Street Network Data ---
try:
    graph = ox.graph_from_point(center_point, dist=map_distance, network_type='all')
    print("Download complete.")

    # --- 3. Plot Edges with OSMnx ---
    print("Plotting the map edges with OSMnx...")
    # First, plot the graph with invisible nodes to draw only the edges.
    fig, ax = ox.plot_graph(
        graph,
        node_size=0,           # Make nodes invisible
        edge_color='gray',
        edge_linewidth=0.8,
        bgcolor='white',
        show=False,
        close=False
    )

    # --- 4. Plot Nodes with Matplotlib ---
    print("Plotting the nodes with Matplotlib...")
    
    # Get the nodes as a GeoDataFrame to easily access their coordinates
    nodes_gdf = ox.graph_to_gdfs(graph, edges=False)
    
    # Use ax.scatter() to plot the nodes directly
    ax.scatter(
        nodes_gdf['x'], 
        nodes_gdf['y'],
        s=30,                  # Size of the nodes
        c='skyblue',           # Color of the nodes
        edgecolor='black',     # Color of the node's stroke
        linewidths=1.0,        # Width of the node's stroke
        zorder=2               # Ensure nodes are drawn on top of edges
    )
    
    # --- 5. Customize and Show the Plot ---
    ax.set_title(f"Street Network around {center_point}", fontsize=14)
    plt.show()
    print("Plot displayed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection.")
    print("You may also need to install the required libraries: pip install osmnx matplotlib geopandas")