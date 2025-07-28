import osmnx as ox
import matplotlib.pyplot as plt

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

    # --- 3. Plot the Map ---
    # Use the plot_graph function from osmnx to visualize the street network.
    print("Plotting the map...")
    fig, ax = ox.plot_graph(
        graph,
        node_size=15,          # Set the size of the nodes (intersections)
        node_color='skyblue',  # Set the color of the nodes
        edge_linewidth=0.8,    # Set the thickness of the street lines
        edge_color='gray',     # Set the color of the streets
        bgcolor='white',       # Set the background color of the plot
        show=False,            # Don't display the plot immediately
        close=False            # Don't close the plot immediately
    )

    # --- 4. Customize and Show the Plot ---
    # Add a title to the plot using matplotlib functions.
    ax.set_title(f"Street Network around {address_name}", fontsize=14)

    # Display the plot.
    plt.show()
    print("Plot displayed.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Please ensure you have an active internet connection and that the address is correct.")
    print("You may also need to install the required libraries: pip install osmnx matplotlib")

