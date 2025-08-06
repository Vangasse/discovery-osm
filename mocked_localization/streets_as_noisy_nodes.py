import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np

def sample_noisy_nodes(edges_gdf, num_samples_per_edge, noise_level):
    """Generates random points along road geometries using a fast, vectorized approach.

    Args:
        edges_gdf (geopandas.GeoDataFrame): 
            A GeoDataFrame containing the projected road edge geometries.
        num_samples_per_edge (int): 
            The number of random points to sample on each road segment.
        noise_level (float): 
            The maximum distance (in the GeoDataFrame's units, typically meters)
            to randomly offset each point.

    Returns:
        tuple[np.ndarray, np.ndarray]: 
            A tuple containing two NumPy arrays for the x and y coordinates of the
            generated points.
    """
    # 1. Create a series by repeating each road's geometry N times
    total_samples = len(edges_gdf) * num_samples_per_edge
    repeated_geoms = edges_gdf.geometry.repeat(num_samples_per_edge)
    repeated_geoms.index = range(len(repeated_geoms)) # A clean index is crucial

    # 2. Generate random distances for interpolation along each road segment
    # First, get the length of each original road and repeat it N times
    repeated_lengths = edges_gdf.length.repeat(num_samples_per_edge)
    repeated_lengths.index = range(len(repeated_lengths))
    # Then, create random factors and multiply to get distances
    random_factors = np.random.rand(total_samples)
    random_distances = repeated_lengths * random_factors

    # 3. Interpolate all points in a single, fast operation
    points = repeated_geoms.interpolate(random_distances)

    # 4. Generate random noise and apply it to the points' coordinates
    noise_x = np.random.uniform(-noise_level, noise_level, total_samples)
    noise_y = np.random.uniform(-noise_level, noise_level, total_samples)

    final_x = points.x + noise_x
    final_y = points.y + noise_y
    
    return final_x, final_y

def main():
    """
    Main entry point for the script.
    
    This function downloads a street network for a specified area, generates a
    cloud of noisy data points along the roads, and visualizes the original
    network and the new points on a map.
    """
    # --- 1. Define Parameters & Set Random Seed ---
    np.random.seed(42)  # For reproducible results
    center_point = (-15.7998, -47.8645)
    map_distance = 500
    num_samples_per_edge = 500
    noise_level = 6.0

    # --- 2. Download and Project the Street Network ---
    print(f"Downloading street network for the area around {center_point}...")
    try:
        # Download the graph data from OpenStreetMap
        graph = ox.graph_from_point(center_point, dist=map_distance, network_type='all')
        
        # Project the graph to a local CRS (Coordinate Reference System) for
        # accurate distance calculations in meters
        graph_proj = ox.project_graph(graph)
        print("Download and projection complete.")

        # --- 3. Generate Noisy Data Points ---
        print("Generating noisy data points along roads...")
        edges_proj = ox.graph_to_gdfs(graph_proj, nodes=False)
        new_x, new_y = sample_noisy_nodes(edges_proj, num_samples_per_edge, noise_level)
        
        # --- 4. Plot the Network and the New Points ---
        print("Plotting the final map...")
        # Plot the base map (streets)
        fig, ax = ox.plot_graph(graph_proj, node_size=0, edge_linewidth=0.8,
                                edge_color='gray', bgcolor='white',
                                show=False, close=False)

        # Plot the original street intersections (nodes)
        nodes_proj = ox.graph_to_gdfs(graph_proj, edges=False)
        ax.scatter(nodes_proj['x'], nodes_proj['y'], s=30, c='skyblue',
                   edgecolor='black', linewidths=1.0, zorder=2)

        # Plot the new, noisy points
        ax.scatter(new_x, new_y, s=15, c='purple', edgecolor='none',
                   alpha=0.5, zorder=3)

        # --- 5. Finalize and Display Plot ---
        ax.set_title(f"Street Network and Simulated Data Points near {center_point}", fontsize=14)
        plt.show()
        print("Done.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have an active internet connection.")


if __name__ == "__main__":
    main()