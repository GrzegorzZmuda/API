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
import gui
import tomtomrequest

def tomreq():
    tomtomrequest.main()
    return 0

def queryselect(a):
    exstr = "select img from images order by abs(extract(epoch from (age(dat , TO_TIMESTAMP('" + a + "','YYYY-MM-DD HH24:MI:SS'))))) asc limit 1"
    return exstr

def queryselectmul(a):
    exstr = "select img from images where extract(hour from dat)="+a
    return exstr

def guistrcreator():
    a=gui.clickbox()
    a.posx=100
    a.posy=100
    a.controltext="rok[YYYY]"
    str=a.main()
    str=str+"-"
    b=gui.clickbox()
    b.posx=100
    b.posy=100
    b.controltext="miesiąc[MM]"
    str=str+b.main()+"-"
    c = gui.clickbox()
    c.posx = 100
    c.posy = 100
    c.controltext = "dzień[DD]"
    str = str + c.main() + "-"
    d = gui.clickbox()
    d.posx = 100
    d.posy = 100
    d.controltext = "godzina[HH24]"
    str = str + d.main() + "-"
    e = gui.clickbox()
    e.posx = 100
    e.posy = 100
    e.controltext = "minuta[MM]"
    str = str + e.main() + "-"
    return str

def guistrcreator1():
    a=gui.clickbox()
    a.posx=100
    a.posy=100
    a.controltext="godzina[HH]"
    str=a.main()
    return str

def curtimeselect():
    dt = datetime.datetime.now()
    a = str(dt)[0:19]
    return a

def menudisp(screen):
    while True:
        screen.fill((0, 0, 0))
        gui.draw_text('jammology', font, (255, 255, 255), screen, 100, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(100, 100, 200, 50)
        button_2 = pygame.Rect(100, 160, 200, 50)
        button_3 = pygame.Rect(100, 220, 200, 50)
        button_4 = pygame.Rect(100, 280, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                disp(postgresquery(queryselect(curtimeselect())))
        if button_2.collidepoint((mx, my)):
            if click:
                disp(postgresquery(queryselect(guistrcreator())))
        if button_3.collidepoint((mx, my)):
            if click:
                muldisp(postgresquerymul(queryselectmul(guistrcreator1())))
        if button_4.collidepoint((mx, my)):
            if click:
                tomreq()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        pygame.draw.rect(screen, (255, 0, 0), button_4)
        gui.draw_text('Najnowsze', font, (255, 255, 255), screen, 110, 110)
        gui.draw_text('Wybierz Datę', font, (255, 255, 255), screen, 110, 170)
        gui.draw_text('Max Danej Godziny', font, (255, 255, 255), screen, 110, 230)
        gui.draw_text('Pobierz Dane', font, (255, 255, 255), screen, 110, 290)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

    return 0

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
    flag=True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    flag = False
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
            lstemp3 = []
            for z in range(len(data)):
                lstemp1.append(ls[z][i][j][0])
                lstemp2.append(ls[z][i][j][1])
                lstemp3.append(ls[z][i][j][2])
            ls2[i][j].append(max(lstemp1))
            ls2[i][j].append(min(lstemp2))
            ls2[i][j].append(max(lstemp3))

    fdata = np.array(ls2)
    #print(fdata)
    surf1 = pygame.surfarray.make_surface(fdata)
    surf1 = pygame.transform.flip(surf1, True, False)
    surf1 = pygame.transform.rotate(surf1, 90)
    screen.blit(surf1, (0, 0))
    pygame.display.flip()
    flag=True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    flag = False
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


clock = pygame.time.Clock()
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
screen = pygame.display.set_mode((512,512))
menudisp(screen)
#modemenu()

Running =True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()