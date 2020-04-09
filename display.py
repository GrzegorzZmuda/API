import requests
import pygame
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import psycopg2
from datetime import datetime
import ast
import datetime


def queryselect(a):
    exstr = "select img from images order by abs(extract(epoch from (age(dat , TO_TIMESTAMP('" + a + "','YYYY-MM-DD HH24:MI:SS'))))) asc limit 1"

    return exstr

def queryselectmul(a):
    exstr = "select img from images where extract(hour from dat)="+a
    return exstr

def strcreator():

    print("rok[YYYY]")
    str=input()+"-"
    print("miesiąc[MM]")
    str = str+input() + "-"
    print("dzień[DD]")
    str = str+input() + " "
    print("godzina[HH24]")
    str = str+input() + ":"
    print("minuta[MI]")
    str = str+input() + ":00"
    return str

def strcreator1():
    print("godzina[HH24]")
    str = input()
    return str

def curtimeselect():
    dt = datetime.datetime.now()
    a = str(dt)[0:19]
    return a

def modemenu():
    print("wybierz tryb [1]-najnowsze dane, [2] - wybierz date(najbliższy czas), [3] - maksymalne zagęszczenie o danej godzinie")
    a=input()
    if a=="1":
        disp(postgresquery(queryselect(curtimeselect())))
    elif a=="2":
        disp(postgresquery(queryselect(strcreator())))
    elif a=="3":
        muldisp(postgresquerymul(queryselectmul(strcreator1())))



    return str


def disp(data):
    ls = []
    for i in range(len(data)):
        ls.append([])
        for j in range(len(data[i])):
            ls[i].append([])
            for k in range(3):
                ls[i][j].append(data[i][j][k])

    fdata = np.array(ls)
    surf1 = pygame.surfarray.make_surface(fdata)
    surf1 = pygame.transform.flip(surf1, True, False)
    surf1 = pygame.transform.rotate(surf1, 90)
    screen.blit(surf1, (0, 0))
    pygame.display.flip()
    return None

def muldisp(data):
    l=len(data)
    ls = []
    for z in range(l):
        ls.append([])
        for i in range(len(data[z])):
            ls[z].append([])
            for j in range(len(data[z][i])):
                ls[z][i].append([])
                for k in range(3):
                    ls[z][i][j].append(data[z][i][j][k])

    ls2=[]

    for i in range(len(data[z])):
        ls2.append([])
        for j in range(len(data[z][i])):
            ls2[i].append([])
            lstemp1=[]
            lstemp2 = []
            for z in range(len(data)):
                lstemp1.append(ls[z][i][j][0])
                lstemp2.append(ls[z][i][j][1])
            ls2[i][j].append(max(lstemp1))
            ls2[i][j].append(min(lstemp2))
            ls2[i][j].append(0)
    fdata = np.array(ls2)
    print(fdata)
    surf1 = pygame.surfarray.make_surface(fdata)
    surf1 = pygame.transform.flip(surf1, True, False)
    surf1 = pygame.transform.rotate(surf1, 90)
    screen.blit(surf1, (0, 0))
    pygame.display.flip()
    return None


def postgresquery(a):
    try:
            connection = psycopg2.connect(user="postgres",
                                  password="all",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="API")
            cursor = connection.cursor()
            exstr=a
            cursor.execute(exstr)
            row = cursor.fetchone()
            temp=np.array(ast.literal_eval(bytes(row[0]).decode()))
            data = np.reshape(temp, (512, 512, 4))
            return data

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to select", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def postgresquerymul(a):
    try:
            connection = psycopg2.connect(user="postgres",
                                  password="all",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="API")
            cursor = connection.cursor()
            exstr=a
            cursor.execute(exstr)
            ls=[]
            row = cursor.fetchone()
            temp=np.array(ast.literal_eval(bytes(row[0]).decode()))
            data = np.reshape(temp, (512, 512, 4))
            ls.append(data)
            row = cursor.fetchone()
            while row!=None:

                temp = np.array(ast.literal_eval(bytes(row[0]).decode()))
                data = np.reshape(temp, (512, 512, 4))
                ls.append(data)
                row = cursor.fetchone()
            return ls

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
screen = pygame.display.set_mode((512,512))
modemenu()



Running =True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()