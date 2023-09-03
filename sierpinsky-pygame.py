# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
dt = 0

init_triangle = [
    (screen.get_width() / 2,100), 
    (screen.get_width() / 4,screen.get_height() / 3 * 2), 
    (screen.get_width() / 4*3,screen.get_height() / 3 * 2)
    ]

def isPointInTriangle(randPointX, randPointY):
    def circArea(x1,y1,x2,y2,x3,y3):
        return abs((x1*(y2-y3)+(x2*(y3-y1))+(x3*(y1-y2)))/2.0)
    

    A=circArea(init_triangle[0][0],init_triangle[0][1],init_triangle[1][0],init_triangle[1][1],init_triangle[2][0],init_triangle[2][1])
    A1=circArea(init_triangle[0][0],init_triangle[0][1],init_triangle[1][0],init_triangle[1][1],randPointX,randPointY)
    A2=circArea(init_triangle[1][0],init_triangle[1][1],init_triangle[2][0],init_triangle[2][1],randPointX,randPointY)
    A3=circArea(init_triangle[0][0],init_triangle[0][1],init_triangle[2][0],init_triangle[2][1],randPointX,randPointY)
    return (A1)+(A2)+(A3)==A

currLines = []
isFirst=True
prevRandPoint=()
prevTriPoint=()
allPoints=[]
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # pygame.draw.circle(screen, "white", player_pos, 20)
    pygame.draw.lines(screen, "white", True, init_triangle)

    if isFirst:
        randPointX = random.randint(screen.get_width() / 4, screen.get_width() / 4*3)
        randPointY = random.randint(100, screen.get_height() / 3 * 2)
        while not isPointInTriangle(randPointX, randPointY):
            randPointX = random.randint(screen.get_width() / 4, screen.get_width() / 4*3)
            randPointY = random.randint(100, screen.get_height() / 3 * 2)
        currPoint = (randPointX, randPointY)
        isFirst = False
    else:
        randPointX = int((prevRandPoint[0] + prevTriPoint[0]) / 2)
        randPointY = int((prevRandPoint[1] + prevTriPoint[1]) / 2)
        currPoint = (randPointX, randPointY)

    triPoint = init_triangle[random.randint(0,2)]
    currLines.append([triPoint, currPoint])
    allPoints.append(currPoint)

    # for line in currLines:
    #     pygame.draw.line(screen, "yellow", line[0], line[1], width=1)

    for point in allPoints:
       pygame.draw.circle(screen, "white", point, 1)

    prevTriPoint = triPoint
    prevRandPoint = currPoint


    # Listen to WASD keys for movement
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()