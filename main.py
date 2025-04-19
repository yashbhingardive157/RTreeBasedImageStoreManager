from database import fetch_locations_from_db, build_rtree_index
from search import find_locations_within_radius
from visualization import visualize_rtree
from place_search import search_places_by_keyword

def main():
    locations = fetch_locations_from_db()
    print(f"Loaded {len(locations)} locations")
    print("Building custom R-tree index...")
    rtree = build_rtree_index(locations)
    print("R-tree index built successfully")
    visualize_rtree(rtree, locations)
    
    while True:
        print("\n=== Location Search Tool ===")
        print("1. Search by coordinates and radius")
        print("2. Search by location name and radius")
        print("3. Search places by keyword")  # New option
        print("4. Visualize R-tree structure")
        print("5. See R-Tree Structure")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            try:
                lat = float(input("Enter latitude: "))
                lon = float(input("Enter longitude: "))
                radius = float(input("Enter radius in km: "))
                
                print(f"Searching for locations within {radius} km of ({lat}, {lon})...")
                results = find_locations_within_radius(rtree, locations, lat, lon, radius)
                
                print(f"\nFound {len(results)} locations within {radius} km:")
                for loc_id, lat, lon, name, distance in results:
                    print(f"ID: {loc_id}, Distance: {distance:.2f} km, Name: {name}")
                
                # Note: visualize_search_results function is called here but not defined in your files
                # visualize_search_results(locations, results, lat, lon, radius)
                
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                
        elif choice == '2':
            try:
                name_query = input("Enter location name (partial match): ")
                
                matches = []
                for loc in locations:
                    loc_id, lat, lon, name = loc
                    if name_query.lower() in name.lower():
                        matches.append(loc)
                
                if not matches:
                    print(f"No locations matching '{name_query}' found.")
                    continue
                
                print(f"Found {len(matches)} matching locations:")
                for i, (loc_id, lat, lon, name) in enumerate(matches):
                    print(f"{i+1}. {name} (ID: {loc_id}, {lat}, {lon})")
                
                if len(matches) > 1:
                    idx = int(input(f"Select location (1-{len(matches)}): ")) - 1
                    if idx < 0 or idx >= len(matches):
                        print("Invalid selection.")
                        continue
                    selected = matches[idx]
                else:
                    selected = matches[0]
                
                radius = float(input("Enter radius in km: "))
                
                center_lat = selected[1]
                center_lon = selected[2]
                
                print(f"Searching for locations within {radius} km of {selected[3]}...")
                results = find_locations_within_radius(rtree, locations, center_lat, center_lon, radius)
                
                print(f"\nFound {len(results)} locations within {radius} km:")
                for loc_id, lat, lon, name, distance in results:
                    print(f"ID: {loc_id}, Distance: {distance:.2f} km, Name: {name}")
      
                
            except ValueError:
                print("Invalid input. Please enter numeric values for radius.")
        
        elif choice == '3':  # New option for searching places by keyword
            keyword = input("Enter search keyword: ")
            
            # Search for places matching the keyword
            results = search_places_by_keyword(locations, keyword)
            
            if not results:
                print(f"No locations matching '{keyword}' found.")
                continue
            
            # Display the results
            print(f"\nFound {len(results)} locations matching '{keyword}':")
            for i, (loc_id, lat, lon, name) in enumerate(results):
                print(f"{i+1}. {name} (ID: {loc_id}, Coordinates: {lat:.6f}, {lon:.6f})")
            
            # Allow the user to select a location and perform a radius search
            if len(results) > 0:
                perform_radius = input("\nWould you like to search around one of these locations? (y/n): ")
                if perform_radius.lower() == 'y':
                    idx = int(input(f"Select location (1-{len(results)}): ")) - 1
                    if idx < 0 or idx >= len(results):
                        print("Invalid selection.")
                        continue
                    
                    selected = results[idx]
                    radius = float(input("Enter radius in km: "))
                    
                    center_lat = selected[1]
                    center_lon = selected[2]
                    
                    print(f"Searching for locations within {radius} km of {selected[3]}...")
                    nearby = find_locations_within_radius(rtree, locations, center_lat, center_lon, radius)
                    
                    print(f"\nFound {len(nearby)} locations within {radius} km:")
                    for loc_id, lat, lon, name, distance in nearby:
                        print(f"ID: {loc_id}, Distance: {distance:.2f} km, Name: {name}")
        
        elif choice == '4':
            print("Generating R-tree visualization...")
            visualize_rtree(rtree, locations)
            print("Visualization complete.")
        
        elif choice == '5':
            print("\nR-Tree structure:")
            rtree.print_structure()

        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()