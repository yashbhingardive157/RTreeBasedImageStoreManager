import psycopg2
from rectangle import Rectangle
from rtree import RTree

def fetch_locations_from_db():
 
    conn = psycopg2.connect(
        dbname="imgdb",
        user="yash",
        password="",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    
    cur.execute("SELECT id, latitude, longitude, name FROM places")
    locations = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return locations

def build_rtree_index(locations):
   
    rtree = RTree(max_entries=8)  
    
    for loc_id, lat, lon, name in locations:
        point_rect = Rectangle(lon, lat, lon, lat)
        rtree.insert(point_rect, (loc_id, lat, lon, name))
    
    return rtree
