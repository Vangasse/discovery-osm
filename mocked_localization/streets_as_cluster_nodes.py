import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans # Import KMeans

# (The 'sample_noisy_nodes' and 'recover_center_points' functions remain the same)
from streets_as_noisy_nodes import sample_noisy_nodes

def recover_center_points(noisy_points_df):
    """Recovers the center point for each cluster of noisy points."""
    valid_clusters = noisy_points_df[noisy_points_df['cluster'] != -1]
    center_points = valid_clusters.groupby('cluster')[['x', 'y']].mean()
    return center_points


def main():
    """
    Main function with a lightweight post-processing step to split large clusters.
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

    # --- 3. Initial Clustering with DBSCAN ---
    # We'll use the tighter eps from the previous "lightweight" solution
    tuned_eps = 7.0
    min_samples = 5
    
    print(f"Clustering with a single DBSCAN pass (eps={tuned_eps}, min_samples={min_samples})...")
    dbscan = DBSCAN(eps=tuned_eps, min_samples=min_samples)
    noisy_points_df['cluster'] = dbscan.fit_predict(noisy_points_df[['x', 'y']])

    # --- 4. NEW: Split Clusters That Are Too Large ---
    print("Checking for and splitting oversized clusters...")
    max_cluster_size = 50 # Define your desired maximum cluster size
    
    # Get the sizes of each cluster
    cluster_counts = noisy_points_df['cluster'].value_counts()
    
    # Find clusters that are too large (ignoring noise points, cluster -1)
    oversized_clusters = cluster_counts[cluster_counts > max_cluster_size]
    oversized_clusters = oversized_clusters.drop(-1, errors='ignore')
    
    # Use a high number to start new cluster labels to avoid conflicts
    new_cluster_label_start = noisy_points_df['cluster'].max() + 1
    
    for cluster_id, count in oversized_clusters.items():
        # Calculate how many sub-clusters we need to create
        k = int(np.ceil(count / max_cluster_size))
        print(f"Splitting cluster {cluster_id} (size {count}) into {k} sub-clusters...")
        
        # Select the points belonging to the oversized cluster
        cluster_points_idx = noisy_points_df['cluster'] == cluster_id
        cluster_points = noisy_points_df.loc[cluster_points_idx]
        
        # Run KMeans to split the cluster
        kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
        sub_cluster_labels = kmeans.fit_predict(cluster_points[['x', 'y']])
        
        # Assign the new, unique sub-cluster labels back to the main DataFrame
        noisy_points_df.loc[cluster_points_idx, 'cluster'] = sub_cluster_labels + new_cluster_label_start
        
        # Update the starting point for the next set of new labels
        new_cluster_label_start += k

    num_clusters = len(noisy_points_df[noisy_points_df['cluster'] != -1]['cluster'].unique())
    print(f"Process finished. Final number of clusters: {num_clusters}")

    # --- 5. Recover Center Points ---
    print("Recovering the center point of each cluster...")
    recovered_points_df = recover_center_points(noisy_points_df)
    
    # --- 6. Visualize the Results ---
    print("Plotting results...")
    fig, ax = ox.plot_graph(graph_proj, node_size=0, edge_linewidth=1,
                            edge_color='gray', bgcolor='white',
                            show=False, close=False,
                            figsize=(12, 12))
    
    ax.scatter(noisy_points_df['x'], noisy_points_df['y'], s=10, c=noisy_points_df['cluster'], 
               cmap='gist_ncar', alpha=0.5) 
               
    ax.scatter(recovered_points_df['x'], recovered_points_df['y'], s=50, c='black', 
               edgecolor='white', label='Recovered Center Points', zorder=5)
    
    ax.set_title("Recovering Centroids with Cluster Splitting", fontsize=16)
    plt.show()

if __name__ == "__main__":
    main()