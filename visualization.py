import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

def visualize_rtree(rtree, locations, output_file='rtree_visualization.png'):
    """Generate a visualization of the R-tree structure"""
    plt.figure(figsize=(12, 10))
    
    # Extract coordinates from all locations
    all_lats = [loc[1] for loc in locations]
    all_lons = [loc[2] for loc in locations]
    
    # Plot all points
    plt.scatter(all_lons, all_lats, c='blue', alpha=0.5, s=10, label='Locations')
    
    # Function to recursively draw rectangles
    def draw_node(node, level=0):
        if not node.is_leaf:
            for mbr, child in node.entries:
                # Draw MBR rectangle
                rect = plt.Rectangle(
                    (mbr.min_x, mbr.min_y),
                    mbr.max_x - mbr.min_x,
                    mbr.max_y - mbr.min_y,
                    linewidth=1,
                    edgecolor=f'C{level % 7}',
                    facecolor='none',
                    alpha=0.7
                )
                plt.gca().add_patch(rect)
                
                # Recursively draw children
                draw_node(child, level + 1)
    
    # Start recursion from root
    draw_node(rtree.root)
    
    plt.title('R-tree Visualization')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.tight_layout()
    
    # Save to file
    plt.savefig(output_file)
    print(f"R-tree visualization saved to {output_file}")
