import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

def sample_noisy_nodes(edges_gdf, num_samples_per_edge, noise_level):
    """
    Generates randomly sampled points along the LineString geometries of edges,
    with added noise.

    Args:
        edges_gdf (GeoDataFrame): A GeoDataFrame containing road edge geometries.
        num_samples_per_edge (int): The number of random points to sample on each edge.
        noise_level (float): The maximum distance (in meters) to shift each point.

    Returns:
        tuple: A tuple containing two lists (x_coords, y_coords) for the new nodes.
    """
    new_nodes_x = []
    new_nodes_y = []

    # Iterate through each edge's geometry
    for geom in edges_gdf['geometry']:
        length = geom.length
        # For each edge, generate N random points
        for _ in range(num_samples_per_edge):
            # Get a random distance along the line's length
            random_distance = np.random.uniform(0, length)
            point = geom.interpolate(random_distance)

            # Add random noise to the point's coordinates
            noise_x = np.random.uniform(-noise_level, noise_level)
            noise_y = np.random.uniform(-noise_level, noise_level)

            new_nodes_x.append(point.x + noise_x)
            new_nodes_y.append(point.y + noise_y)

    return new_nodes_x, new_nodes_y


def main():
    """
    Main function to download, process, and plot the street network data.
    """
    # --- 1. Define Parameters & Set Seed ---
    np.random.seed(42) # Set seed for reproducible random results
    center_point = (-15.7998, -47.8645)
    map_distance = 500
    num_samples_per_edge = 500
    noise_level = 6.0

    # --- 2. Download and Project the Graph ---
    print(f"Downloading street network data for the area around {center_point}...")
    try:
        graph = ox.graph_from_point(center_point, dist=map_distance, network_type='all')
        print("Projecting graph to a local CRS...")
        graph_proj = ox.project_graph(graph)
        print("Download and projection complete.")

        # --- 3. Plot the Base Map and Nodes ---
        print("Plotting the map...")
        fig, ax = ox.plot_graph(graph_proj, node_size=0, edge_linewidth=0.8,
                                edge_color='gray', bgcolor='white',
                                show=False, close=False)

        nodes_proj = ox.graph_to_gdfs(graph_proj, edges=False)
        ax.scatter(nodes_proj['x'], nodes_proj['y'], s=30, c='skyblue',
                   edgecolor='black', linewidths=1.0, zorder=2)

        # --- 4. Sample and Plot New Nodes ---
        print("Sampling and plotting new noisy nodes...")
        edges_proj = ox.graph_to_gdfs(graph_proj, nodes=False)
        new_x, new_y = sample_noisy_nodes(edges_proj, num_samples_per_edge, noise_level)
        
        ax.scatter(new_x, new_y, s=15, c='purple', edgecolor='none',
                   alpha=0.5, zorder=3)

        # --- 5. Finalize and Show Plot ---
        ax.set_title(f"Street Network Nodes around {center_point}", fontsize=14)
        plt.show()
        print("Plot displayed.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure an active internet connection.")


if __name__ == "__main__":
    main()