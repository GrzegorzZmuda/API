import requests

from io import BytesIO
import numpy as np
from PIL import Image
import psycopg2
from datetime import datetime
key="cf803Zv11WsSi0J2RcjG6REKXt6w6RAh"

r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1136/693.png?key="+key)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
stream.close()
image.save('out1.png')

r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1137/693.png?key="+key)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
stream.close()
image.save('out2.png')

r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1136/694.png?key="+key)
stream = BytesIO(r.content)
image = Image.open(stream).convert("RGBA")
stream.close()
image.save('out3.png')

r = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/11/1137/694.png?key="+key)
stream = BytesIO(r.content)
image= Image.open(stream).convert("RGBA")
stream.close()
image.save('out4.png')


DR=Image.open("out4.png")
DL=Image.open("out3.png")
UR=Image.open("out2.png")
UL=Image.open("out1.png")

UP=[UL,UR]
DOWN=[DL,DR]

uimg= Image.fromarray( np.hstack([UL,UR]))
dimg= Image.fromarray( np.hstack([DL,DR]))
img=Image.fromarray(np.vstack([uimg,dimg]))
img.save('fin2.png')


try:
        connection = psycopg2.connect(user="postgres",
                              password="all",
                              host="127.0.0.1",
                              port="5432",
                              database="API")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO images  VALUES (%s,%s)"""
        #print(img)
        a=np.array(img)
        print(a)
        temp=a.tolist()

        #print(len(temp))
        #print(temp[771])

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