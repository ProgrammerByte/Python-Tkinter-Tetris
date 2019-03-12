from tkinter import *
from tkinter import messagebox
import math
from random import randint, shuffle
from copy import copy

#Gamesize = 10 x 20

class gamewindow():
    def __init__(s):
        s.root = Tk()
        s.root.title("Tetris")
        s.root.grid()

        s.pressed = "False"
        s.root.bind("<KeyPress>", lambda event = "<KeyPress>": gamewindow.KeyPress(s, event))
        s.root.bind("<KeyRelease>", lambda event = "<KeyRelease>": gamewindow.KeyRelease(s, event))

        s.piecesdict = {
            "piece1": {"indexes": [[0, 3], [0, 4], [0, 5], [0, 6]], "colour": "Light Blue"},
            "piece2": {"indexes": [[1, 4], [1, 5], [1, 6], [0, 4]], "colour": "royal blue"},
            "piece3": {"indexes": [[1, 4], [1, 5], [1, 6], [0, 6]], "colour": "Orange"},
            "piece4": {"indexes": [[1, 4], [1, 5], [1, 6], [0, 5]], "colour": "Purple"},
            "piece5": {"indexes": [[0, 4], [1, 5], [0, 5], [1, 6]], "colour": "Red"},
            "piece6": {"indexes": [[0, 6], [1, 5], [1, 4], [0, 5]], "colour": "Lime Green"},
            "piece7": {"indexes": [[0, 5], [0, 6], [1, 5], [1, 6]], "colour": "Yellow"},
            }
            
        s.maingrid = list()

        for i in range(20):
            s.maingrid.append([])
            for x in range(10):
                s.maingrid[i].append("")
                s.maingrid[i][x] = Label(height = 2, width = 4, bg = "Black", bd = 2)#, bordercolour = "White")
                s.maingrid[i][x].grid(row = i, column = x, padx = 1, pady = 1)
                s.maingrid[i][x].occupied = "False"

        s.rotations = 0
        s.running = "False"
        s.piecedrop = "False" #If a piece is currently falling
        s.direction = "None"
        s.time = 1000
        s.clean = "N"
        s.done = "False"
        s.indexlist = list() #The bag arrangement of pieces which shall be used
        gamewindow.loop(s)
        s.root.mainloop()

    def loop(s):
        if s.done == "False" and s.time != 100:
            gamewindow.gravity(s)
            gamewindow.RefreshScreen(s)
            s.running = "True"
            s.root.after(s.time, gamewindow.loop, s)
        else:
            s.running = "False"

    def fastloop(s):
        if s.done == "False" and s.time != 1000:
            gamewindow.gravity(s)
            gamewindow.RefreshScreen(s)
            s.root.after(s.time, gamewindow.fastloop, s)

    def RefreshScreen(s):
        if s.done == "False":
            for i in range(20):
                amount = 0
                for x in range(10):
                    if s.maingrid[i][x].occupied == "True":
                        amount += 1

                    elif s.maingrid[i][x].occupied == "Player":
                            found = "N"
                            for z in range(4):
                                if len(s.playing) == 4:
                                    if i == s.playing[z][0] and x == s.playing[z][1]:
                                        found = "Y"
                            if found == "N":
                                s.maingrid[i][x].occupied = "False"
                                s.maingrid[i][x].configure(bg = "Black")
                            s.clean = "N"

                if amount == 10:
                    for z in range(10):
                        s.maingrid[i][z].configure(bg = "Black")
                        s.maingrid[i][z].occupied = "False"
                        
                    for a in range(i):
                        for b in range(10):
                            atemp = i - a
                            if s.maingrid[atemp][b].occupied == "True":
                                colour = s.maingrid[atemp][b]["bg"]
                                s.maingrid[atemp][b].configure(bg = "Black")
                                s.maingrid[atemp][b].occupied = "False"
                                s.maingrid[atemp + 1][b].occupied = "True"
                                s.maingrid[atemp + 1][b].configure(bg = colour)
        

                            
    def gravity(s):
        if s.done == "False":
            if s.piecedrop == "False":
                s.playing = list()
                s.piecedrop = "True"

                if len(s.indexlist) == 0:
                    s.indexlist = [1, 2, 3, 4, 5, 6, 7]
                    shuffle(s.indexlist)

                s.piece = s.indexlist[0]
                del s.indexlist[0]
                
                piece = "piece" + str(s.piece)
                for z in range(4):
                    if s.done == "False":
                        s.playing.append(s.piecesdict[piece]["indexes"][z])
                        i = s.piecesdict[piece]["indexes"][z][0]
                        x = s.piecesdict[piece]["indexes"][z][1]
                        s.colour = s.piecesdict[piece]["colour"]
                        s.maingrid[i][x].configure(bg = s.colour)

                        if s.maingrid[i][x].occupied == "True":
                            if s.done == "False":
                                messagebox.showinfo("GAME OVER", "You have lost!")
                                s.done = "True"
                                s.root.destroy()

                        else:
                            s.maingrid[i][x].occupied = "Player"

            else:
                verf = 0
                for z in range(4):
                    if len(s.playing) == 4:
                        i = s.playing[z][0]
                        x = s.playing[z][1]
                        if i < 19:
                            if s.maingrid[i + 1][x].occupied != "True":   #"True" refers to whether the location is occupied and is not currently in control by the player
                                verf += 1 

                templist = list()
                for z in range(4):
                    if len(s.playing) == 4:
                        i = s.playing[z][0]
                        x = s.playing[z][1]
                        if verf != 4:
                            s.rotations = 0
                            s.piecedrop = "False"
                            s.maingrid[i][x].occupied = "True"
                            s.maingrid[i][x].configure(bg = s.colour)
                            
                            if s.time == 1:
                                    s.time = 1000
                        else:
                            templist.append([i + 1, x])
                            s.maingrid[i][x].occupied = "False"
                            s.maingrid[i][x].configure(bg = "Black")

                for z in range(len(templist)):
                    if len(s.playing) == 4:
                        s.playing[z] = templist[z]
                        i = s.playing[z][0]
                        x = s.playing[z][1]
                        s.maingrid[i][x].configure(bg = s.colour)
                        s.maingrid[i][x].occupied = "Player"

    def move(s):
        if s.direction == "Left":
            changex = -1
        else:
            changex = 1

        if s.piecedrop == "True":
            verf = 0
            for z in range(4):
                i = s.playing[z][0]
                x = s.playing[z][1]
                if x + changex >= 0 and x + changex <= 9:
                    if s.maingrid[i][x + changex].occupied != "True":
                        verf += 1

            templist = list()
            if verf == 4:
                for z in range(4):
                    i = s.playing[z][0]
                    x = s.playing[z][1]
                    
                    templist.append([i, x + changex])
                    s.maingrid[i][x].occupied = "False"
                    s.maingrid[i][x].configure(bg = "Black")

            for z in range(len(templist)):
                s.playing[z] = templist[z]
                i = s.playing[z][0]
                x = s.playing[z][1]
                s.maingrid[i][x].configure(bg = s.colour)
                s.maingrid[i][x].occupied = "Player"

        gamewindow.RefreshScreen(s)


    def rotate(s):
        if s.piece != 7 and s.piecedrop == "True":
            
            if s.rotatedirection == "Right":
                rotations = copy(s.rotations) + 1
                multiply = -1
            else:
                rotations = copy(s.rotations) - 1
                multiply = 1
                
            if rotations < 0:
                rotations = 4 + rotations
                
            rotations = rotations % 4
            
            playtemp = list(s.playing)
            
            origini = copy(s.playing[1][0])
            originx = copy(s.playing[1][1])

            templist = [copy(s.playing[0]), copy(s.playing[2]), copy(s.playing[3])]
            
            for z in range(3):
                i = templist[z][0]
                x = templist[z][1]

                di = i - origini
                di = -di

                dx = x - originx

                        
                length = math.sqrt((di * di) + (dx * dx))

                angle = round(math.degrees(math.asin(dx / length)))

                if di > 0:
                    temp = 90 - angle
                    angle = 90 + temp

                if s.rotatedirection == "Right":
                    angle -= 90
                elif s.rotatedirection == "Left":
                    angle += 90
                        
                afterchangeinx = round(math.sin(math.radians(angle)) * length)
                afterchangeiny = round(math.cos(math.radians(angle)) * length)
                    
                
                templist[z][1] = afterchangeinx + originx
                templist[z][0] = afterchangeiny + origini

                if s.piece == 1:
                    if (s.rotations == 0 and multiply == 1) or (s.rotations == 3 and multiply == -1): #Down 1
                        templist[z][0] += multiply
                    elif (s.rotations == 1 and multiply == 1) or (s.rotations == 0 and multiply == -1): #Right 1
                        templist[z][1] -= multiply
                    elif (s.rotations == 2 and multiply == 1) or (s.rotations == 1 and multiply == -1): #Up 1
                        templist[z][0] -= multiply
                    elif (s.rotations == 3 and multiply == 1) or (s.rotations == 2 and multiply == -1): #Left 1
                        templist[z][1] += multiply
                

            verf = 0
            for z in range(3):
                if int(templist[z][0]) >= 0 and int(templist[z][0]) < 20 and int(templist[z][1]) >= 0 and int(templist[z][1] < 10):
                    if s.maingrid[templist[z][0]][templist[z][1]].occupied != "True":
                        verf += 1

            if s.piece == 1:
                    tempval = copy(s.playing[1])
                    temp = copy(tempval)
                    if (s.rotations == 0 and multiply == 1) or (s.rotations == 3 and multiply == -1): #Down 1
                        tempval[0] += multiply
                    elif (s.rotations == 1 and multiply == 1) or (s.rotations == 0 and multiply == -1): #Right 1
                        tempval[1] -= multiply
                    elif (s.rotations == 2 and multiply == 1) or (s.rotations == 1 and multiply == -1): #Up 1
                        tempval[0] -= multiply
                    elif (s.rotations == 3 and multiply == 1) or (s.rotations == 2 and multiply == -1): #Left 1
                        tempval[1] += multiply

                    if s.maingrid[tempval[0]][tempval[1]].occupied == "True":
                        verf -= 1

            if verf == 3:
                for z in range(len(s.playing)):
                    if z != 1:
                        s.maingrid[s.playing[z][0]][s.playing[z][1]].configure(bg = "Black")
                        s.maingrid[s.playing[z][0]][s.playing[z][1]].occupied = "False"

                for z in range(len(templist)):
                    s.maingrid[templist[z][0]][templist[z][1]].configure(bg = s.colour)
                    s.maingrid[templist[z][0]][templist[z][1]].occupied = "Player"


                s.playing = [templist[0], s.playing[1], templist[1], templist[2]]
                s.rotations = rotations

                if s.piece == 1:
                    s.maingrid[temp[0]][temp[1]].configure(bg = "Black")
                    s.maingrid[temp[0]][temp[1]].occupied = "False"
                    
                    s.maingrid[tempval[0]][tempval[1]].configure(bg = s.colour)
                    s.maingrid[tempval[0]][tempval[1]].occupied = "Player"
                    s.playing[1] = tempval

                for z in range(len(s.playing)): #This is a failsafe to make sure that all player tiles are correctly coloured
                    s.maingrid[s.playing[z][0]][s.playing[z][1]].configure(bg = s.colour)

            s.clean = "Y"
        


    def KeyPress(s, event):
        if s.pressed == "False":
            key = event.keysym
            s.pressed = "True"

            if s.time != 1:
                if key == "Left":
                    s.direction = "Left"
                    gamewindow.move(s)
                    
                elif key == "Right":
                    s.direction = "Right"
                    gamewindow.move(s)
                    
                elif key == "Down" and s.time != 100:
                    s.time = 100
                    gamewindow.fastloop(s)
                    
                elif key == "Up":
                    s.time = 1
                    while s.time == 1:
                        gamewindow.gravity(s)
                        gamewindow.RefreshScreen(s)
                    
                elif key == "z" or key == "Z":
                    s.rotatedirection = "Left"
                    gamewindow.rotate(s)
                    
                elif key == "x" or key == "X":
                    s.rotatedirection = "Right"
                    gamewindow.rotate(s)

    def KeyRelease(s, event):
        s.pressed = "False"
        key = event.keysym

        if key == "Down":
            s.time = 1000
            if s.running == "False":
                gamewindow.loop(s)

        



if __name__ == "__main__":
    game = gamewindow()
    quit()

