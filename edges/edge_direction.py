import osmnx as ox
import matplotlib.pyplot as plt

# --- 1. Define the Place & Parameters ---
address_name = "Praça dos Três Poderes, Brasília, Brazil"
map_distance = 1500 # Distance in meters (1.5 km)

# NEW: Parameters to control arrow position and size
# The arrow will be drawn from the point at `start_pos` to the point at `end_pos`
# along the length of the road segment (0.0=start, 1.0=end).
arrow_start_pos = 0.48
arrow_end_pos = 0.52

print(f"Downloading street network data for the area around {address_name}...")

# --- 2. Download the Street Network Data ---
try:
    graph = ox.graph_from_address(address_name, dist=map_distance, network_type='all')
    print("Download complete.")

    # --- 3. Plot the Base Map ---
    print("Plotting the base map...")
    fig, ax = ox.plot_graph(
        graph,
        node_size=0,
        edge_linewidth=0.8,
        edge_color='gray',
        bgcolor='white',
        show=False,
        close=False
    )

    # --- 4. Prepare and Plot Directional Arrows ---
    print("Calculating and plotting directional arrows...")
    x_coords, y_coords, dx_vals, dy_vals = [], [], [], []

    # Iterate over each edge in the graph
    for u, v, data in graph.edges(data=True):
        # For curved roads, use the 'geometry' attribute
        if 'geometry' in data:
            line = data['geometry']
            p1 = line.interpolate(arrow_start_pos, normalized=True)
            p2 = line.interpolate(arrow_end_pos, normalized=True)
        # For straight roads, calculate points from the nodes
        else:
            p1_coords = (graph.nodes[u]['x'], graph.nodes[u]['y'])
            p2_coords = (graph.nodes[v]['x'], graph.nodes[v]['y'])
            
            # Linear interpolation for the two points
            p1 = ( (p1_coords[0] * arrow_end_pos + p2_coords[0] * arrow_start_pos),
                   (p1_coords[1] * arrow_end_pos + p2_coords[1] * arrow_start_pos) )
            p2 = ( (p1_coords[0] * arrow_start_pos + p2_coords[0] * arrow_end_pos),
                   (p1_coords[1] * arrow_start_pos + p2_coords[1] * arrow_end_pos) )
            
            # Convert to a generic object with .x and .y attributes
            class Point:
                def __init__(self, x, y):
                    self.x, self.y = x, y
            p1, p2 = Point(*p1), Point(*p2)

        # The arrow starts at p1
        x_coords.append(p1.x)
        y_coords.append(p1.y)
        # The arrow's direction is the vector from p1 to p2
        dx_vals.append(p2.x - p1.x)
        dy_vals.append(p2.y - p1.y)

    # Use ax.quiver to plot all arrows efficiently
    ax.quiver(
        x_coords,
        y_coords,
        dx_vals,
        dy_vals,
        color='black',
        scale_units='xy',
        angles='xy',
        scale=2,
        width=0.006
    )

    # --- 5. Customize and Show the Plot ---
    ax.set_title(f"Street Network with Directions around {address_name}", fontsize=14)
    plt.show()
    print("Plot displayed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection and that the address is correct.")
    print("You may also need to install the required libraries: pip install osmnx matplotlib")