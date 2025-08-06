import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

# Import the data generation function
from streets_as_noisy_nodes import sample_noisy_nodes


def recover_center_points(noisy_points_df):
    """Recovers the center point for each cluster of noisy points.

    This function calculates the centroid (geometric mean) of each cluster
    found by the DBSCAN algorithm. It uses a single, efficient pandas
    operation to achieve this.

    Args:
        noisy_points_df (pd.DataFrame): 
            A DataFrame with 'x', 'y', and 'cluster' columns for the noisy points.

    Returns:
        pd.DataFrame: 
            A DataFrame with the x and y coordinates of each cluster's centroid.
    """
    # Filter out noise points (cluster label -1)
    valid_clusters = noisy_points_df[noisy_points_df['cluster'] != -1]
    
    # Group by cluster and find the mean for 'x' and 'y' to get the centroid
    center_points = valid_clusters.groupby('cluster')[['x', 'y']].mean()
    
    return center_points


def main():
    """
    Main function to generate noisy data, recover cluster centers, save the
    results to a CSV file, and visualize.
    """
    # --- 1. Define Parameters & Set Seed ---
    np.random.seed(42)
    center_point = (-15.7998, -47.8645)
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
    
    # --- 3. Cluster the Noisy Data using DBSCAN ---
    print("Clustering noisy points with DBSCAN...")
    dbscan = DBSCAN(eps=noise_level * 1.5, min_samples=5)
    noisy_points_df['cluster'] = dbscan.fit_predict(noisy_points_df[['x', 'y']])
    
    num_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
    print(f"Found {num_clusters} clusters.")

    # --- 4. Recover and Save Center Points ---
    print("Recovering the center point of each cluster...")
    recovered_points_df = recover_center_points(noisy_points_df)
    
    # --- THIS IS THE NEW PART ---
    output_filename = 'noisy_points.csv'
    noisy_points_df.to_csv(output_filename, index=False)
    print(f"Results saved successfully to '{output_filename}'.")
    # ---------------------------

    # --- 5. Visualize the Results ---
    print("Plotting results...")
    fig, ax = ox.plot_graph(graph_proj, node_size=0, edge_linewidth=1,
                            edge_color='gray', bgcolor='white',
                            show=False, close=False,
                            figsize=(12, 12))
    
    ax.scatter(noisy_points_df['x'], noisy_points_df['y'], s=10, c='red', alpha=0.3, label='Noisy Input Data')
    ax.scatter(recovered_points_df['x'], recovered_points_df['y'], s=50, c='blue', edgecolor='black', label='Recovered Center Points')
    
    ax.set_title("Recovering Cluster Centroids from Noisy Points", fontsize=16)
    ax.legend()
    plt.show()
    print("Done.")


if __name__ == "__main__":
    main()