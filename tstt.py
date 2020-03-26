import requests

from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import psycopg2
from datetime import datetime
import ast
try:
        connection = psycopg2.connect(user="postgres",
                              password="all",
                              host="127.0.0.1",
                              port="5432",
                              database="API")
        cursor = connection.cursor()
        cursor.execute("SELECT img FROM images limit 1")
        row = cursor.fetchone()
        temp=np.array(ast.literal_eval(bytes(row[0]).decode()))
        print(temp)
        data=np.reshape(temp, (512, 512,4))
        plt.imshow(data)
        plt.show()
        count = cursor.rowcount


except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to select", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")