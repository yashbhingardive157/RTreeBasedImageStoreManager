import pandas as pd
import psycopg2
df = pd.read_csv('/home/yash/Desktop/Project/ImageManager/Coordinates Task/final_location_data.csv')
conn = psycopg2.connect(
    dbname="imgdb",
    user="yash",
    password="",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
cur.execute("""create table if not exists places (id serial primary key,latitude double precision,longitude double precision,name text);""")
print(df.columns)
for _, row in df.iterrows():
    cur.execute(
        "insert into places (latitude, longitude,name) values (%s, %s, %s)",
        (row['Latitude'], row['Longitude'], row['Location'])
    )
conn.commit()
cur.close()
conn.close()



