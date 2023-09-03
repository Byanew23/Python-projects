from tkinter import *
import random

#Create an instance of tkinter frame
win= Tk()
WIDTH = 600
HEIGHT = 600
POINT_WIDTH=2

#Define the geometry of window
win.geometry(f"{WIDTH}x{HEIGHT}")

#Create a canvas object
c= Canvas(win,width=WIDTH, height=HEIGHT, background="black")
c.pack()

def getPoints():
    def isPointInTriangle(randPointX, randPointY):
        def circArea(x1,y1,x2,y2,x3,y3):
            return abs((x1*(y2-y3)+(x2*(y3-y1))+(x3*(y1-y2)))/2.0)
        

        A=circArea(init_triangle[0][0],init_triangle[0][1],init_triangle[1][0],init_triangle[1][1],init_triangle[2][0],init_triangle[2][1])
        A1=circArea(init_triangle[0][0],init_triangle[0][1],init_triangle[1][0],init_triangle[1][1],randPointX,randPointY)
        A2=circArea(init_triangle[1][0],init_triangle[1][1],init_triangle[2][0],init_triangle[2][1],randPointX,randPointY)
        A3=circArea(init_triangle[0][0],init_triangle[0][1],init_triangle[2][0],init_triangle[2][1],randPointX,randPointY)
        return (A1)+(A2)+(A3)==A
    
    isFirst=True
    prevRandPoint=()
    prevTriPoint=()
    allPoints = []
    for i in range(50000):
        if isFirst:
            randPointX = random.randint(0, WIDTH)
            randPointY = random.randint(0, HEIGHT)
            while not isPointInTriangle(randPointX, randPointY):
                randPointX = random.randint(0, WIDTH)
                randPointY = random.randint(0, HEIGHT)
            currPoint = (randPointX, randPointY)
            isFirst = False
        else:
            randPointX = int((prevRandPoint[0] + prevTriPoint[0]) / 2)
            randPointY = int((prevRandPoint[1] + prevTriPoint[1]) / 2)
            currPoint = (randPointX, randPointY)

        triPoint = init_triangle[random.randint(0,2)]
        allPoints.append(currPoint)

        prevTriPoint = triPoint
        prevRandPoint = currPoint
    
    return allPoints

init_triangle = [(WIDTH/2, 0),
                 (0, HEIGHT),
                 (WIDTH, HEIGHT)]

c.create_polygon(init_triangle[0], init_triangle[1], init_triangle[2], fill="red" )

points = getPoints()

for point in points:
    c.create_oval(point[0], point[1], point[0]+POINT_WIDTH, point[1]+POINT_WIDTH, fill="black")

win.mainloop()