import requests
import pygame
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
        cursor.execute("SELECT img FROM images order by dat asc limit 1 ")
        row = cursor.fetchone()
        temp=np.array(ast.literal_eval(bytes(row[0]).decode()))

        data = np.reshape(temp, (512, 512, 4))





except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to select", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")




pygame.init()
ls=[]
for i in range(len(data)):
    ls.append([])
    for j in range(len(data[i])):
        ls[i].append([])
        for k in range(3):
            ls[i][j].append(data[i][j][k])
screen = pygame.display.set_mode((512,512))
fdata=np.array(ls)
surf1 = pygame.surfarray.make_surface(fdata)
surf1=pygame.transform.flip(surf1, True, False)
surf1=pygame.transform.rotate(surf1, 90)
screen.blit(surf1, (0, 0))
Running =True
pygame.display.flip()
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()