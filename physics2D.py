# Example file showing a circle moving on screen
import pygame
import time
import math

WIDTH=600
HEIGHT=400
FRICTION=.1
ACC_SPEED=1

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

class Line:
    color = 'yellow'
    width = 3
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end
    
    def set_color(self, color):
        self.color = color

class Circle:
    velX = 0
    velY = 0
    pos_x = 0
    pos_y = 0

    size=30
    def __init__(self, color, pos) -> None:
        self.color = color
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.newX = pos[0]
        self.newY = pos[1]
    
    def move(self):
        if self.pos_x <= self.size:
            self.pos_x = self.size

        if self.pos_x >= WIDTH-self.size:
            self.pos_x = WIDTH-self.size

        if self.pos_y <= self.size:
            self.pos_y = self.size

        if self.pos_y >= HEIGHT-self.size:
            self.pos_y = HEIGHT-self.size

        #     self.velY = self.velY*(-1)
        self.pos_x += self.velX
        self.pos_y += self.velY

        if self.velX != 0:
            self.velX -= self.velX*FRICTION
        if self.velY != 0:
            self.velY -= self.velY*FRICTION

player = Circle('green', (WIDTH/2, HEIGHT/4*3))
walls = []

def display_entities():
    # Display all the drawn lines
    for wall in walls:
        pygame.draw.line(screen, wall.color, wall.start, wall.end, wall.width)
    
    #display the player
    pygame.draw.circle(screen, player.color, (player.pos_x, player.pos_y), player.size)

def calculate_distance_from_point_to_line(px,py,sx,sy,ex,ey):
    A = px-sx
    B = py - sy
    C = ex - sx
    D = ey - ex

    dot = A*C + B*D
    len_sq = C*C + D*D
    param = -1
    if len_sq != 0:
        param = dot/len_sq

    if param < 0:
        xx = sx
        yy = sy
    elif param > 1:
        xx = ex
        yy = ey
    else:
        xx = sx + param*C
        yy = sy + param*D
    
    dx = px-xx
    dy = py - yy
    return math.sqrt(dx*dx + dy*dy)


def check_collisions():
    for wall in walls:
        distance = calculate_distance_from_point_to_line(player.pos_x, player.pos_y, wall.start[0], wall.start[1], wall.end[0], wall.end[1])
        if distance <= player.size:
            wall.set_color('red')
            player.velX = 0
            player.velY = 0
        else:
            wall.set_color('yellow')
        
init_point = ()
end_point=()
while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN :
            init_point = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP :
            end_point=pygame.mouse.get_pos()
            walls.append(Line(init_point, end_point))
    
    display_entities()
    player.move()
    check_collisions()

    # Listen to WASD keys for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running=False
    if keys[pygame.K_w]:
        player.velY -= ACC_SPEED
    if keys[pygame.K_s]:
        player.velY += ACC_SPEED
    if keys[pygame.K_a]:
        player.velX -= ACC_SPEED
    if keys[pygame.K_d]:
        player.velX += ACC_SPEED
    if keys[pygame.K_e]:
        screen.fill("black")
        walls=[]

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()