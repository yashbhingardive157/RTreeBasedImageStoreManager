# place_search.py
def search_places_by_keyword(locations, keyword):
    """
    Search for places that match the given keyword.
    
    Args:
        locations: List of tuples (loc_id, lat, lon, name)
        keyword: Search term to match against place names
    
    Returns:
        List of matching locations sorted by relevance
    """
    if not keyword or not keyword.strip():
        return []
    
    keyword = keyword.lower().strip()
    matches = []
    
    # Find all places that contain the keyword in their name
    for loc in locations:
        loc_id, lat, lon, name = loc
        if keyword in name.lower():
            # Calculate a simple relevance score
            # - Exact match gets highest score
            # - Starts with keyword gets medium score
            # - Contains keyword gets lowest score
            if name.lower() == keyword:
                relevance = 3  # Exact match
            elif name.lower().startswith(keyword):
                relevance = 2  # Starts with keyword
            else:
                relevance = 1  # Contains keyword
                
            matches.append((loc_id, lat, lon, name, relevance))
    
    # Sort by relevance (highest first)
    matches.sort(key=lambda x: x[4], reverse=True)
    
    # Return the matches without the relevance score for display
    return [(loc_id, lat, lon, name) for loc_id, lat, lon, name, _ in matches]