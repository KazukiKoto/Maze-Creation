import math
import tkinter

######################################

def Creator_GUI(): #Creating GUI for defining size and startpos of maze
    global root
    global WidthEntry
    global HeightEntry
    global StartPosXEntry
    global StartPosYEntry
    global EndPosXEntry
    global EndPosYEntry
    root=tkinter.Tk()
    
    WidthLabel = tkinter.Label(root, text = "Width")
    WidthLabel.grid(column=0,row=0, columnspan=2)
    HeightLabel = tkinter.Label(root, text = "Height")
    HeightLabel.grid(column=0,row=1, columnspan=2)
    WidthEntry = tkinter.Entry(root)
    WidthEntry.grid(column=3,row=0, columnspan=5,rowspan=1)
    HeightEntry = tkinter.Entry(root)
    HeightEntry.grid(column=3,row=1, columnspan=5,rowspan=1)
    
    StartPosLabel = tkinter.Label(root, text = "StartPos")
    StartPosLabel.grid(column=0,row=2, columnspan=2)
    EndPosLabel = tkinter.Label(root, text = "EndPos")
    EndPosLabel.grid(column=0,row=5, columnspan=2)
    XLabel = tkinter.Label(root, text = "X: ")
    XLabel.grid(column=0,row=3, columnspan=2)
    YLabel = tkinter.Label(root, text = "Y: ")
    YLabel.grid(column=0,row=4, columnspan=2)
    XLabel2 = tkinter.Label(root, text = "X: ")
    XLabel2.grid(column=0,row=6, columnspan=2)
    YLabel2 = tkinter.Label(root, text = "Y: ")
    YLabel2.grid(column=0,row=7, columnspan=2)
    StartPosXEntry = tkinter.Entry(root)
    StartPosXEntry.grid(column=3,row=3, columnspan=5,rowspan=1)
    StartPosYEntry = tkinter.Entry(root)
    StartPosYEntry.grid(column=3,row=4, columnspan=5,rowspan=1)
    EndPosXEntry = tkinter.Entry(root)
    EndPosXEntry.grid(column=3,row=6, columnspan=5,rowspan=1)
    EndPosYEntry = tkinter.Entry(root)
    EndPosYEntry.grid(column=3,row=7, columnspan=5,rowspan=1)
    
    GoButton = tkinter.Button(root, text = "Go!", command = lambda:[Input_Verify()])
    GoButton.grid(column=0, row=8, columnspan=12)
    
    root.mainloop()
    
def Maze_GUI():
    global maze
    maze = tkinter.Tk()
    maze.geometry("+100+100") #Uses a Fixed window position
    maze.resizable(False,False)
    for y in range ((len(MazeGrid)-1)):
        for x in range ((len(MazeGrid[y])-1)):
            Grid_Button(y,x) #Call appropriate number of cells
    SolveButton = tkinter.Button(maze, text = "Solve", command = lambda:[Maze_Solver()]) #Creates button to call the solver
    SolveButton.grid(row = len(MazeGrid), column = 0, columnspan=len(MazeGrid)) #Places button in grid
    maze.mainloop() 

######################################

class Grid_Button:
    def __init__(self, y, x): #Constructor for cell class object
        self.y=y #Y co-ordinate on board
        self.x=x #X co-ordinate on board
        self.state = MazeGrid[y][x] #Wall Path or Start/End Pos
        if self.state==0:
            self.Button = tkinter.Button(maze, text="", bg="white", height=2, width=4, command = lambda:[self.Change_State(self.state,y,x)]) #Creation of tkinter button element with ability to increase its value on click
            self.Button.grid(row=y, column=x) #Place button in grid
        elif self.state==1:
            self.Button = tkinter.Button(maze, text="", bg="black", height=2, width=4, command = lambda:[self.Change_State(self.state,y,x)]) #Creation of tkinter button element with ability to increase its value on click
            self.Button.grid(row=y, column=x) #Place button in grid
        elif self.state==2:
            self.Label = tkinter.Label(maze, text="", background="green", height=2, width=4)
            self.Label.grid(row=y, column=x)
        elif self.state==3:
            self.Label = tkinter.Label(maze, text="", background="red", height=2, width=4)
            self.Label.grid(row=y, column=x)   
    def Change_State(self,state,y,x):
        if self.state==0:
            self.state=1
            self.Button = tkinter.Button(maze, text="", bg="black", height=2, width=4, command = lambda:[self.Change_State(self.state,y,x)]) #Creation of tkinter button element with ability to increase its value on click
            self.Button.grid(row=y, column=x) #Place button in grid
        else:
            self.state=0
            self.Button = tkinter.Button(maze, text="", bg="white", height=2, width=4, command = lambda:[self.Change_State(self.state,y,x)]) #Creation of tkinter button element with ability to increase its value on click
            self.Button.grid(row=y, column=x) #Place button in grid
        MazeGrid[y][x]=state
               
def Input_Verify():
    check=0
    ErrorLabel =tkinter.Label(root, text="")
    ErrorLabel.grid(column=0, row=9, columnspan=12)
    try:    
        Width = int(WidthEntry.get()) #Getting data from entries
        Height = int(HeightEntry.get())
        StartPosX = int(StartPosXEntry.get())
        StartPosY = int(StartPosYEntry.get())
        EndPosX = int(EndPosXEntry.get())
        EndPosY = int(EndPosYEntry.get())
    except:
        ErrorLabel.config(text="Entered data is not numeric")
        ErrorLabel.grid(column=0, row=9, columnspan=12)
        check=1
    finally:
        if check==0:
            if Width<=0 or Height<=0 or StartPosX<0 or StartPosY<0 or EndPosX<0 or EndPosY<0: #all checks for valid inputs
                ErrorLabel.config(text="Value(s) out of range")
            else:
                if StartPosX>=Width or StartPosY>=Width:
                    ErrorLabel.config(text="Start Pos out of Bounds of grid")
                else:
                    if EndPosX>=Width or EndPosY>=Width:
                        ErrorLabel.config(text="End Pos out of Bounds of grid")
                    else:
                        if StartPosX==EndPosX and StartPosY==EndPosY:
                            ErrorLabel.config(text="Start and end positions cannot be the same")
                        else:
                            root.destroy()
                            Maze_Creator(Width,Height,StartPosX,StartPosY,EndPosX,EndPosY)

def Maze_Creator(Width,Height,StartPosX,StartPosY,EndPosX,EndPosY):
    global MazeGrid
    MazeGrid = []
    for y in range(Width+1):
        MazeGrid.append([])
        for x in range(Height+1):
            MazeGrid[y].append([])
            if (x == StartPosX and y == StartPosY):
                MazeGrid[y][x] = 2
            else:
                if (x == EndPosX and y == EndPosY):
                    MazeGrid[y][x] = 3
                else:
                    MazeGrid[y][x] = 0
    Maze_GUI()
    
def Maze_Solver():
    print("temp") #Put Maze solver Here
    
######################################Main Code

Creator_GUI()