import osmnx as ox
import matplotlib.pyplot as plt
import random

# --- 1. Define the Place ---
# Instead of a whole city, we specify a specific address.
# We'll also define a distance (in meters) around this address to create our map.
address_name = "Praça dos Três Poderes, Brasília, Brazil"
map_distance = 1500 # Distance in meters (1.5 km)

print(f"Downloading street network data for the area around {address_name}...")

# --- 2. Download the Street Network Data ---
# Use osmnx to download the street network data for the specified address.
# The 'graph_from_address' function gets the network within a certain distance
# of a specific address.
try:
    graph = ox.graph_from_address(address_name, dist=map_distance, network_type='all')
    print("Download complete.")

    # --- 3. Select and List Random Nodes ---
    # Get a list of all nodes in the graph.
    all_nodes = list(graph.nodes())
    
    # Select 10 random nodes from the list, ensuring we don't select more than exist.
    num_random_nodes = min(10, len(all_nodes))
    random_nodes_to_delete = random.sample(all_nodes, num_random_nodes)
    
    print(f"\nSelected {num_random_nodes} random nodes to delete:")
    for node_id in random_nodes_to_delete:
        print(node_id)
    
    # --- 4. Delete the Nodes from the Graph ---
    # Create a copy of the graph before removing nodes to work with.
    graph_modified = graph.copy()
    graph_modified.remove_nodes_from(random_nodes_to_delete)
    print(f"\nSuccessfully removed {len(random_nodes_to_delete)} nodes from the graph.")


    # --- 5. Plot the Modified Map ---
    # Use the plot_graph function to visualize the modified street network.
    print("\nPlotting the modified map...")
    fig, ax = ox.plot_graph(
        graph_modified,
        node_size=10,              # Show the remaining nodes
        node_color='skyblue',      # Color for the remaining nodes
        edge_linewidth=0.8,        # Set the thickness of the street lines
        edge_color='gray',         # Set the color of the streets
        bgcolor='white',           # Set the background color of the plot
        show=False,                # Don't display the plot immediately
        close=False                # Don't close the plot immediately
    )

    # --- 6. Plot Markers for the Deleted Nodes ---
    # Get the coordinates of the nodes that were deleted from the original graph.
    deleted_node_coords = [
        (graph.nodes[node]['x'], graph.nodes[node]['y']) 
        for node in random_nodes_to_delete
    ]
    
    if deleted_node_coords:
        x_coords, y_coords = zip(*deleted_node_coords)
        # Use scatter to plot red 'x' markers at the locations of the deleted nodes.
        ax.scatter(
            x_coords, y_coords, 
            s=100,              # Size of the marker
            c='red',            # Color of the marker
            marker='x',         # Marker style
            zorder=5,           # Ensure markers are drawn on top
            label='Deleted Nodes' # Label for the legend
        )

    # --- 7. Customize and Show the Plot ---
    # Add a title to the plot using matplotlib functions.
    ax.set_title(f"Street Network around {address_name} (with nodes removed)", fontsize=14)
    ax.legend() # Display the legend

    # Display the plot.
    plt.show()
    print("Plot displayed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection and that the address is correct.")
    print("You may also need to install the required libraries: pip install osmnx matplotlib")

