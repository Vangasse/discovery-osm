import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors # Import NearestNeighbors

# Import the data generation function
from streets_as_noisy_nodes import sample_noisy_nodes


def recover_center_points(noisy_points_df):
    """Recovers the center point for each cluster of noisy points."""
    # Filter out noise points (cluster label -1)
    valid_clusters = noisy_points_df[noisy_points_df['cluster'] != -1]
    
    # Group by cluster and find the mean for 'x' and 'y' to get the centroid
    center_points = valid_clusters.groupby('cluster')[['x', 'y']].mean()
    
    return center_points


def main():
    """
    Main function to generate noisy data, recover cluster centers, and visualize.
    """
    # --- 1. Define Parameters & Set Seed ---
    np.random.seed(42)
    center_point = (-15.7998, -47.8645) # Brasília, Brazil
    map_distance = 500
    num_samples_per_edge = 100
    noise_level = 6.0

    # --- 2. Generate Noisy Data ---
    print("Downloading street network and generating data...")
    graph = ox.graph_from_point(center_point, dist=map_distance, network_type='all')
    graph_proj = ox.project_graph(graph)
    edges_proj = ox.graph_to_gdfs(graph_proj, nodes=False)
    
    noisy_x, noisy_y = sample_noisy_nodes(edges_proj, num_samples_per_edge, noise_level)
    noisy_points_df = pd.DataFrame({'x': noisy_x, 'y': noisy_y})
    
    # --- THIS IS THE NEW PART: Estimate DBSCAN `eps` parameter ---
    print("Estimating optimal 'eps' for DBSCAN...")
    # We will find the distance to the k-th nearest neighbor for each point.
    # A good value for k (min_samples) is often 2 * number_of_dimensions.
    # For our 2D data, let's start with min_samples = 5.
    min_samples = 5 
    
    # Calculate distances
    neighbors = NearestNeighbors(n_neighbors=min_samples)
    neighbors_fit = neighbors.fit(noisy_points_df[['x', 'y']])
    distances, indices = neighbors_fit.kneighbors(noisy_points_df[['x', 'y']])
    
    # Sort the distances to the k-th neighbor
    k_distances = np.sort(distances[:, min_samples-1])
    
    # Plot the k-distance graph
    plt.figure(figsize=(10, 6))
    plt.plot(k_distances)
    plt.xlabel("Points (sorted by distance)")
    plt.ylabel(f"Distance to {min_samples-1}-th Nearest Neighbor (k-distance)")
    plt.title("K-Distance Graph for Estimating DBSCAN 'eps'")
    
    # The "elbow" of this curve is a good candidate for `eps`.
    # By inspecting the plot, we can see the curve starts bending sharply around 8.5.
    # We will add a line to the plot to show our choice.
    estimated_eps = 8.5
    plt.axhline(y=estimated_eps, color='r', linestyle='--', label=f'Chosen eps = {estimated_eps}')
    plt.legend()
    plt.grid(True)
    plt.show()
    # -------------------------------------------------------------
    
    # --- 3. Cluster the Noisy Data using DBSCAN ---
    print(f"Clustering noisy points with DBSCAN (eps={estimated_eps}, min_samples={min_samples})...")
    # Use the estimated_eps and our chosen min_samples
    dbscan = DBSCAN(eps=estimated_eps, min_samples=min_samples)
    noisy_points_df['cluster'] = dbscan.fit_predict(noisy_points_df[['x', 'y']])
    
    num_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
    print(f"Found {num_clusters} clusters.")

    # --- 4. Recover and Save Center Points ---
    print("Recovering the center point of each cluster...")
    recovered_points_df = recover_center_points(noisy_points_df)
    
    output_filename = 'noisy_points_with_clusters.csv'
    noisy_points_df.to_csv(output_filename, index=False)
    print(f"Results saved successfully to '{output_filename}'.")

    # --- 5. Visualize the Results ---
    print("Plotting results...")
    fig, ax = ox.plot_graph(graph_proj, node_size=0, edge_linewidth=1,
                            edge_color='gray', bgcolor='white',
                            show=False, close=False,
                            figsize=(12, 12))
    
    ax.scatter(noisy_points_df['x'], noisy_points_df['y'], s=10, c=noisy_points_df['cluster'], cmap='viridis', alpha=0.3, label='Noisy Input Data')
    ax.scatter(recovered_points_df['x'], recovered_points_df['y'], s=50, c='red', edgecolor='black', label='Recovered Center Points', zorder=5)
    
    ax.set_title("Recovering Cluster Centroids from Noisy Points", fontsize=16)
    ax.legend()
    plt.show()
    print("Done.")


if __name__ == "__main__":
    main()