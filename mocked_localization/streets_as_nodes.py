import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Define the Place & Parameters ---
center_point = (-15.7998, -47.8645) # Coordinates for Praça dos Três Poderes
map_distance = 500 # Using the 500 meter distance
sampling_distance = 10 # Denser sampling: a new point every 5 meters

print(f"Downloading street network data for the area around {center_point}...")

# --- 2. Download and Project the Graph ---
try:
    # Download the graph in the default coordinate system (degrees)
    graph = ox.graph_from_point(center_point, dist=map_distance, network_type='all')

    # FIXED: Project the graph to a local UTM CRS (uses meters)
    print("Projecting graph to a local CRS...")
    graph_proj = ox.project_graph(graph)

    print("Download and projection complete.")

    # --- 3. Plot the Edges ---
    print("Plotting the map edges...")
    # Use the projected graph for all plotting and analysis
    fig, ax = ox.plot_graph(
        graph_proj,
        node_size=0,
        edge_linewidth=0.8,
        edge_color='gray',
        bgcolor='white',
        show=False,
        close=False
    )

    # --- 4. Plot the Original Nodes ---
    print("Plotting the original intersection nodes...")
    # Get nodes from the projected graph
    nodes_proj = ox.graph_to_gdfs(graph_proj, edges=False)
    ax.scatter(
        nodes_proj['x'],
        nodes_proj['y'],
        s=30,
        c='skyblue',
        edgecolor='black',
        linewidths=1.0,
        zorder=3
    )

    # --- 5. Sample and Plot New Nodes on Edges ---
    print("Sampling and plotting new nodes along edges...")
    # Get edges from the projected graph
    edges_proj = ox.graph_to_gdfs(graph_proj, nodes=False)

    new_nodes_x = []
    new_nodes_y = []

    # This loop will now work correctly because lengths and distances are in meters
    for geom in edges_proj['geometry']:
        length = geom.length
        for distance in np.arange(0, length, sampling_distance):
            point = geom.interpolate(distance)
            new_nodes_x.append(point.x)
            new_nodes_y.append(point.y)

    # Plot the new sampled nodes
    ax.scatter(
        new_nodes_x,
        new_nodes_y,
        s=15,
        c='purple',
        edgecolor='none',
        alpha=0.5,
        zorder=2
    )

    # --- 6. Customize and Show the Plot ---
    ax.set_title(f"Street Network Nodes around {center_point}", fontsize=14)
    plt.show()
    print("Plot displayed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection.")
    print("You may also need to install the required libraries: pip install osmnx matplotlib geopandas numpy")