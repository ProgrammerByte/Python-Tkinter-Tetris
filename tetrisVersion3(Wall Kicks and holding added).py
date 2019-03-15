#TODO - MAKE THE SIZE OF THE TEMPLIST 1 LARGER SO THAT IT CHECKS ALL PIECES AND THEREFORE IMPROVE CODE EFFICIENCY!!!


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
        s.root.geometry("1000x760")
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

        s.holdlabel = Label(font = "Calibri 20 bold", text = "HOLD")
        s.holdlabel.place(x = 155, y = 0)

        s.holdframe = Frame()
        s.holdgrid = list()
        for i in range(4):
            s.holdgrid.append([])
            for x in range(4):
                s.holdgrid[i].append("")
                s.holdgrid[i][x] = Label(s.holdframe, height = 2, width = 4, bg = "Black", bd = 2)
                s.holdgrid[i][x].grid(row = i, column = x, padx = 1, pady = 1)

        s.holdframe.place(x = 120, y = 50)

        s.gridframe = Frame()
        s.maingrid = list()
        for i in range(20):
            s.maingrid.append([])
            for x in range(10):
                s.maingrid[i].append("")
                s.maingrid[i][x] = Label(s.gridframe, height = 2, width = 4, bg = "Black", bd = 2)#, bordercolour = "White")
                s.maingrid[i][x].grid(row = i, column = x, padx = 1, pady = 1)
                s.maingrid[i][x].occupied = "False"

        s.gridframe.place(x = 300)

        s.nextlabel = Label(font = "Calibri 20 bold", text = "NEXT")
        s.nextlabel.place(x = 740, y = 0)
        
        s.nextframe = Frame()
        s.nextpiecegrid = list()
        for i in range(4):
            s.nextpiecegrid.append([])
            for x in range(4):
                s.nextpiecegrid[i].append("")
                s.nextpiecegrid[i][x] = Label(s.nextframe, height = 2, width = 4, bg = "Black", bd = 2)
                s.nextpiecegrid[i][x].grid(row = i, column = x, padx = 1, pady = 1)

        s.isrotating = "False" #If a piece is currently being rotated then it cannot be held
        s.interrupt = "False"
        s.holding = "False" #If a piece is currently being held
        s.holdturn = "False"
        s.rotations = 0
        s.running = "False" #Ensures that the mainloop doesn't run more than once at a time
        s.piecedrop = "False" #If a piece is currently falling
        s.direction = "None"
        s.time = 1000
        s.clean = "N"
        s.done = "False"
        s.cpressed = "False" #Checks whether the c kay is currently being pressed
        s.indexlist = list() #The bag arrangement of pieces which shall be used

        s.nextframe.place(x = 700, y = 50)
        gamewindow.newnext(s)
        
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
        
    def newnext(s):
        for a in range(4):
            for b in range(4):
                s.nextpiecegrid[a][b].configure(bg = "Black")
            
        if len(s.indexlist) == 0:
            s.indexlist = [1, 2, 3, 4, 5, 6, 7]
            shuffle(s.indexlist)

        if s.interrupt == "False":
            s.nextpiececopy = s.indexlist[0] #A copy of the nextpiece variable to be used for rerieving held pieces
            s.nextpiece = s.indexlist[0]
            del s.indexlist[0]
        else:
            s.nextpiece = s.nextpiececopy
            s.interrupt = "False"

        piece = "piece" + str(s.nextpiece)
        for z in range(4):
            if s.done == "False":
                i = s.piecesdict[piece]["indexes"][z][0]
                x = s.piecesdict[piece]["indexes"][z][1]
                s.colour = s.piecesdict[piece]["colour"]
                s.nextpiecegrid[i + 1][x - 4].configure(bg = s.colour)

        
        
                            
    def gravity(s):
        if s.done == "False":
            if s.piecedrop == "False":
                s.piece = s.nextpiece
                gamewindow.newnext(s)
                s.playing = list()
                s.piecedrop = "True"
                    
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
                            s.holdturn = "False"
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
        s.isrotating == "True"
        
        #s.rotations == previous position
        #rotations == next position
        #Order presented is s.rotations -> rotations
        #Note how the first condition for the tests in each table are identical and the second are reversed
        #The tables and test generation works as far as I am currently concerned
        
        s.wallkicks = [ #The wallkick tests for all non I pieces
            [[0, 0], [-1, 0], [-1, 1],  [0, -2], [-1, -2]], #0 -> 1 or 2 -> 1
            [[0, 0], [1, 0],  [1, -1],  [0, 2],  [1, 2]],   #1 -> 0 or 1 -> 2
            [[0, 0], [1, 0],  [1, 1],   [0, -2], [1, -2]],  #0 -> 3 or 2 -> 3
            [[0, 0], [-1, 0], [-1, -1], [0, 2],  [-1, 2]]   #3 -> 0 or 3 -> 2
            ]

        s.wallkicksI = [ #The wallkick tests for I pieces
            [[0, 0], [-2, 0], [1, 0],  [-2, -1], [1, 2]],   #0 -> 1 or 3 -> 2
            [[0, 0], [2, 0],  [-1, 0], [2, 1],   [-1, -2]], #1 -> 0 or 2 -> 3
            [[0, 0], [-1, 0], [2, 0],  [-1, 2],  [2, -1]],  #0 -> 3 or 1 -> 2
            [[0, 0], [1, 0],  [-2, 0], [1, -2],  [-2, 1]]   #3 -> 0 or 2 -> 1
            ]
        
        if s.piece != 7 and s.piecedrop == "True":

            if s.piece != 1:
                table = copy(s.wallkicks) #The table of tests which will be used for wall kicks
            else:
                table = copy(s.wallkicksI)
            
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

            finished = "N"
            testnumber = 0

            if (s.rotations == 0 and rotations == 1) or (s.piece != 1 and s.rotations == 2 and rotations == 1) or (s.piece == 1 and s.rotations == 3 and rotations == 2):
                tempindex = 0
            elif (s.rotations == 1 and rotations == 0) or (s.piece != 1 and s.rotations == 1 and rotations == 2) or (s.piece == 1 and s.rotations == 2 and rotations == 3):
                tempindex = 1
            elif (s.rotations == 0 and rotations == 3) or (s.piece != 1 and s.rotations == 2 and rotations == 3) or (s.piece == 1 and s.rotations == 1 and rotations == 2):
                tempindex = 2
            elif (s.rotations == 3 and rotations == 0) or (s.piece != 1 and s.rotations == 3 and rotations == 2) or (s.piece == 1 and s.rotations == 2 and rotations == 1):
                tempindex = 3

            if s.piece != 1:
                tests = s.wallkicks[tempindex]
            else:
                tests = s.wallkicksI[tempindex]
            
            while finished == "N" and testnumber < 5:

                currenttest = tests[testnumber]
                
                origini = copy(s.playing[1][0]) - currenttest[1]
                originx = copy(s.playing[1][1]) + currenttest[0]

                templist = [copy(s.playing[0]), copy(s.playing[2]), copy(s.playing[3])]
                
                for z in range(3):
                    i = templist[z][0] - currenttest[1]
                    x = templist[z][1] + currenttest[0]

                    di = i - origini
                    di = -di

                    dx = x - originx

                            
                    length = math.sqrt((di * di) + (dx * dx))

                    angle = round(math.degrees(math.asin(dx / length))) #ANGLE WORKS FOR TRANSLATED SHAPES

                    if di > 0:
                        temp = 90 - angle
                        angle = 90 + temp

                    if s.rotatedirection == "Right":
                        angle -= 90
                    elif s.rotatedirection == "Left":
                        angle += 90
                    
                    afterchangeinx = round(math.sin(math.radians(angle)) * length)
                    afterchangeiny = round(math.cos(math.radians(angle)) * length)  #AFTER CHANGE IN Y AND AFTER CHANGE IN X STILL WORKS FOR TRANSLATED SHAPES
                    
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
                for z in range(4):
                    if z < 3:
                        if int(templist[z][0]) >= 0 and int(templist[z][0]) < 20 and int(templist[z][1]) >= 0 and int(templist[z][1] < 10):
                            if s.maingrid[templist[z][0]][templist[z][1]].occupied != "True":
                                verf += 1
                    else:
                        tempval = ["",""]
                        tempval[0] = origini
                        tempval[1] = originx
                        if int(tempval[0]) >= 0 and int(tempval[0]) < 20 and int(tempval[1]) >= 0 and int(tempval[1] < 10):
                            if s.maingrid[tempval[0]][tempval[1]].occupied != "True":
                                verf += 1
                        

                if s.piece == 1:
                        
                        temp = copy(tempval)
                        if (s.rotations == 0 and multiply == 1) or (s.rotations == 3 and multiply == -1): #Down 1
                            tempval[0] += multiply
                        elif (s.rotations == 1 and multiply == 1) or (s.rotations == 0 and multiply == -1): #Right 1
                            tempval[1] -= multiply
                        elif (s.rotations == 2 and multiply == 1) or (s.rotations == 1 and multiply == -1): #Up 1
                            tempval[0] -= multiply
                        elif (s.rotations == 3 and multiply == 1) or (s.rotations == 2 and multiply == -1): #Left 1
                            tempval[1] += multiply

                        if tempval[0] >= 0 and tempval[0] < 20 and tempval[1] >= 1 and tempval[1] < 10:
                            if s.maingrid[tempval[0]][tempval[1]].occupied == "True":
                                verf -= 1
                            
                if verf == 4:
                    finished = "Y"
                    for z in range(len(s.playing)):
                        s.maingrid[s.playing[z][0]][s.playing[z][1]].configure(bg = "Black")
                        s.maingrid[s.playing[z][0]][s.playing[z][1]].occupied = "False"

                    for z in range(len(templist)):
                        s.maingrid[templist[z][0]][templist[z][1]].configure(bg = s.colour)
                        s.maingrid[templist[z][0]][templist[z][1]].occupied = "Player"


                    s.playing = [templist[0], s.playing[1], templist[1], templist[2]]
                    s.playing[1][0] = origini
                    s.playing[1][1] = originx
                    s.rotations = rotations

                    if s.piece == 1:
                        s.maingrid[tempval[0]][tempval[1]].configure(bg = s.colour)
                        s.maingrid[tempval[0]][tempval[1]].occupied = "Player"
                        s.playing[1] = tempval

                    for z in range(len(s.playing)): #This is a failsafe to make sure that all player tiles are correctly coloured
                        s.maingrid[s.playing[z][0]][s.playing[z][1]].configure(bg = s.colour)

                else:
                    testnumber += 1

            s.clean = "Y"
            s.isrotating == "False"
        

    def hold(s):
        if s.holding == "True":
            s.nextpiece = s.holdpiece
            s.interrupt = "True"
        
        s.holding = "True" #Put piece into hold box
        for z in range(len(s.playing)):
            s.maingrid[s.playing[z][0]][s.playing[z][1]].configure(bg = "Black")
            s.maingrid[s.playing[z][0]][s.playing[z][1]].occupied = "False"
        s.piecedrop = "False"

        for a in range(4):
            for b in range(4):
                s.holdgrid[a][b].configure(bg = "Black")

        s.holdpiece = copy(s.piece)
        piece = "piece" + str(copy(s.holdpiece))
        for z in range(4):
            if s.done == "False":
                i = s.piecesdict[piece]["indexes"][z][0]
                x = s.piecesdict[piece]["indexes"][z][1]
                s.colour = s.piecesdict[piece]["colour"]
                s.holdgrid[i + 1][x - 4].configure(bg = s.colour)
    

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

                elif (key == "c" or key == "C") and s.cpressed == "False" and s.holdturn == "False" and s.piecedrop == "True" and s.isrotating == "False":
                    s.holdturn = "True" #checks whether a full turn has been made before the hold button has been pressed again
                    s.cpresed = "True"

                    gamewindow.hold(s)
                    

    def KeyRelease(s, event):
        s.pressed = "False"
        key = event.keysym

        if key == "Down":
            s.time = 1000
            if s.running == "False":
                gamewindow.loop(s)

        elif key == "c" or key == "C":
            s.cpressed = "False"

        



if __name__ == "__main__":
    game = gamewindow()
    quit()

