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

    # --- 3. Select Random Nodes to Move ---
    # Get a list of all nodes in the graph.
    all_nodes = list(graph.nodes())
    
    # Select 10 random nodes from the list, ensuring we don't select more than exist.
    num_random_nodes = min(10, len(all_nodes))
    nodes_to_move = random.sample(all_nodes, num_random_nodes)
    
    print(f"\nSelected {num_random_nodes} random nodes to move.")
    
    # --- 4. Create a Modified Graph with Moved Nodes ---
    graph_modified = graph.copy()
    original_coords = {}
    new_coords = {}
    
    # Define how much to move the nodes (a small offset in degrees)
    offset_magnitude = 0.0003 

    for node in nodes_to_move:
        # Store original coordinates
        original_x = graph.nodes[node]['x']
        original_y = graph.nodes[node]['y']
        original_coords[node] = (original_x, original_y)

        # Calculate a random offset and apply it
        offset_x = (random.random() - 0.5) * 2 * offset_magnitude
        offset_y = (random.random() - 0.5) * 2 * offset_magnitude
        new_x = original_x + offset_x
        new_y = original_y + offset_y

        # Update the node's coordinates in the modified graph
        graph_modified.nodes[node]['x'] = new_x
        graph_modified.nodes[node]['y'] = new_y
        new_coords[node] = (new_x, new_y)

    print(f"\nSlightly moved {len(nodes_to_move)} nodes.")


    # --- 5. Plot the Base Map ---
    # Plot the street network from the modified graph. We make the nodes invisible
    # here because we will plot custom markers for them later.
    print("\nPlotting the map...")
    fig, ax = ox.plot_graph(
        graph_modified,
        node_size=0,               # Hide the default nodes
        edge_linewidth=0.8,        # Set the thickness of the street lines
        edge_color='gray',         # Set the color of the streets
        bgcolor='white',           # Set the background color of the plot
        show=False,                # Don't display the plot immediately
        close=False                # Don't close the plot immediately
    )

    # --- 6. Plot Markers for Original and New Node Positions ---
    # Get lists of original and new coordinates for plotting.
    orig_x, orig_y = zip(*original_coords.values())
    new_x, new_y = zip(*new_coords.values())

    # Plot original positions as blue squares
    ax.scatter(orig_x, orig_y, s=100, marker='s', facecolors='none', edgecolors='blue', zorder=5, label='Original Position')
    
    # Plot new positions as red circles
    ax.scatter(new_x, new_y, s=100, marker='o', facecolors='none', edgecolors='red', zorder=5, label='New Position')

    # --- 7. Customize and Show the Plot ---
    # Add a title and legend.
    ax.set_title(f"Street Network with Moved Nodes around {address_name}", fontsize=14)
    ax.legend()

    # Display the plot.
    plt.show()
    print("Plot displayed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection and that the address is correct.")
    print("You may also need to install the required libraries: pip install osmnx matplotlib")

