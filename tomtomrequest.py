import requests

from io import BytesIO
import numpy as np
from PIL import Image
import psycopg2
from datetime import datetime


def main():
    key="cf803Zv11WsSi0J2RcjG6REKXt6w6RAh"

    r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1136/693.png?key="+key)
    stream = BytesIO(r.content)
    UL = Image.open(stream).convert("RGBA")
    stream.close()


    r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1137/693.png?key="+key)
    stream = BytesIO(r.content)
    UR = Image.open(stream).convert("RGBA")
    stream.close()

    r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1136/694.png?key="+key)
    stream = BytesIO(r.content)
    DL = Image.open(stream).convert("RGBA")
    stream.close()


    r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1137/694.png?key="+key)
    stream = BytesIO(r.content)
    DR= Image.open(stream).convert("RGBA")
    stream.close()




    UP=[UL,UR]
    DOWN=[DL,DR]

    uimg= Image.fromarray( np.hstack([UL,UR]))
    dimg= Image.fromarray( np.hstack([DL,DR]))
    img=Image.fromarray(np.vstack([uimg,dimg]))
    img.save('fin.png')


    try:
            connection = psycopg2.connect(user="postgres",
                                  password="all",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="API")
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT INTO images  VALUES (%s,%s)"""

            a=np.array(img)

            temp=a.tolist()


            record_to_insert = (datetime.now(),str.encode(str(temp)))
            cursor.execute(postgres_insert_query, record_to_insert)

            connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

