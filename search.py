from rectangle import Rectangle
from haversine import haversine

def find_locations_within_radius(rtree, locations, center_lat, center_lon, radius_km):
    """find all locations within radius_km of the center point"""
    radius_deg = radius_km/111.0
    
    # Define the search bounding box
    search_rect = Rectangle(
        center_lon - radius_deg,
        center_lat - radius_deg,
        center_lon + radius_deg,
        center_lat + radius_deg
    )
    
    # Search the R-tree
    candidates = rtree.search(search_rect)
    
    # Refine candidates using haversine distance
    results = []
    for loc_id, lat, lon, name in candidates:
        distance = haversine(center_lat, center_lon, lat, lon)
        if distance <= radius_km:
            results.append((loc_id, lat, lon, name, distance))
    
    # Sort by distance
    results.sort(key=lambda x: x[4])  # Sort by distance (5th element)
    
    return results
