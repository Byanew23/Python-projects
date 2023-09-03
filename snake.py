# Example file showing a circle moving on screen
import pygame
import math
import random

WIDTH=600
HEIGHT=400

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Snake")
clock = pygame.time.Clock()
running = True
dt = 0

font = pygame.font.Font('freesansbold.ttf', 32)
font_sm = pygame.font.Font('freesansbold.ttf', 24)

high_score = 0


class Snake:
    velX = 0
    velY = 0
    pos_x = WIDTH/2
    pos_y = HEIGHT/4*3
    speed = 20
    size=20
    segments = []
    dir = ""
    offset = size*2-5
    prev_direction = dir
    over = False

    score = 0

    def __init__(self, color) -> None:
        self.color = color
    
    def turn(self, dir):
        self.prev_direction = self.dir if self.dir else dir

        match dir:
            case "U":
                if self.dir == "D":
                    return
                self.velY = -self.speed
                self.velX = 0
            case "D":
                if self.dir == "U":
                    return
                self.velY = self.speed
                self.velX = 0
            case "L":
                if self.dir == "R":
                    return
                self.velX = -self.speed
                self.velY = 0
            case "R":
                if self.dir == "L":
                    return
                self.velX = self.speed
                self.velY = 0
            case _:
                pass
        self.dir = dir

    def apply_offset(self, dir, x, y):
        match dir:
            case "U":
                y += self.offset
            case "D":
                y -= self.offset
            case "R":
                x -= self.offset
            case "L":
                x += self.offset
            case _:
                pass
        return [x,y]
            
    def move_in_direction(self, dir, x, y):
        if dir == "U" or dir == "D":
            y += self.velY
        else:
            x += self.velX
        return [x,y]

    def move(self):
        prev_pos = [self.pos_x, self.pos_y]
        self.pos_x += self.velX
        self.pos_y += self.velY

        # Wrap around the Edges
        if self.pos_x <= 0:
            self.pos_x = WIDTH
        elif self.pos_x >= WIDTH:
            self.pos_x = 0

        if self.pos_y <= 0:
            self.pos_y = HEIGHT
        elif self.pos_y >= HEIGHT:
            self.pos_y = 0

        for segment in self.segments:
            temp = segment["pos"]
            segment["pos"] = prev_pos
            prev_pos = temp
            temp_dir = segment["dir"]
            segment["dir"] = self.prev_direction
            self.prev_direction = temp_dir
            
    def eat(self):
        if len(self.segments):
            seg_pos = self.segments[-1]["pos"]
        else:
            seg_pos = [self.pos_x, self.pos_y]
        self.segments.append({"dir": self.dir, "pos": seg_pos})
        self.score += 10

    def restart(self):
        self.segments = []
        self.velX = 0
        self.velY = 0
        self.pos_x = WIDTH/2
        self.pos_y = HEIGHT/4*3
        self.over = False
        self.dir = ""
        self.prev_direction = self.dir
        self.score = 0


player = Snake('green')
foods = [{"id":0,"pos": (random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30))},{"id":1,"pos": (random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30))}]

def draw_head():
    pygame.draw.circle(screen, player.color, (player.pos_x, player.pos_y), player.size)
    pygame.draw.circle(screen, "yellow", (player.pos_x, player.pos_y), player.size-3, width=2)
    if player.dir == "L" or player.dir == "R":
        l_eye_pos = [player.pos_x - 5 if player.dir == "L" else player.pos_x + 5, player.pos_y + player.size/3]
        r_eye_pos = [player.pos_x - 5 if player.dir == "L" else player.pos_x + 5, player.pos_y - player.size/3]
    else:
        l_eye_pos = [player.pos_x - player.size/3, player.pos_y + 5 if player.dir == "D" else player.pos_y - 5]
        r_eye_pos = [player.pos_x + player.size/3, player.pos_y + 5 if player.dir == "D" else player.pos_y - 5]
    pygame.draw.circle(screen, "black", l_eye_pos, 3)
    pygame.draw.circle(screen, "black", r_eye_pos, 3)

def draw_tail():
    for i in reversed(range(len(player.segments))):
        pygame.draw.circle(screen, player.color, (player.segments[i]["pos"][0], player.segments[i]["pos"][1]), player.size-5)
        pygame.draw.circle(screen, "yellow", (player.segments[i]["pos"][0], player.segments[i]["pos"][1]), player.size-10)
        pygame.draw.circle(screen, "black", (player.segments[i]["pos"][0], player.segments[i]["pos"][1]), player.size-13)
        pygame.draw.circle(screen, "yellow", (player.segments[i]["pos"][0], player.segments[i]["pos"][1]), player.size-16)
        pygame.draw.circle(screen, "green", (player.segments[i]["pos"][0], player.segments[i]["pos"][1]), player.size-18)

def render_score():
    text_end = font_sm.render(f"SCORE: {player.score}", True, "white", "black")
    text_rect = text_end.get_rect()
    text_rect.center = (WIDTH/2, 30)
    screen.blit(text_end, text_rect)

def display_entities():

    render_score()

    # Display all the food
    for food in foods:
        pygame.draw.circle(screen, 'yellow', food["pos"], 10)
    
    # Display the tail
    draw_tail()

    # Display the head
    draw_head()


def measure_distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def check_collisions():
    for food in foods:
        dist = measure_distance(player.pos_x, player.pos_y, food["pos"][0], food["pos"][1])
        if dist <= player.size+10:
            player.eat()
            tempId = food["id"]
            foods.remove(food)
            foods.append({"id":tempId,"pos": (random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30))})
    
    for i in range(len(player.segments)):
        if i == 0:
            continue
        dist = measure_distance(player.pos_x, player.pos_y, player.segments[i]["pos"][0], player.segments[i]["pos"][1])
        if dist <= player.size-5:
            player.over = True

def check_inputs(running) -> bool:

    # Listen to WASD keys for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running=False
    if keys[pygame.K_w]:
        player.turn('U')
    if keys[pygame.K_s]:
        player.turn("D")
    if keys[pygame.K_a]:
        player.turn("L")
    if keys[pygame.K_d]:
        player.turn("R")
    if keys[pygame.K_r]:
        player.restart()

    return running

time = 0
while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    display_entities()
    running = check_inputs(running)
    if time > 0.2 and not player.over:
        time = 0
        player.move()
        check_collisions()

    if player.over:
        pygame.draw.polygon(screen, "beige", [(80,100), (WIDTH-80,100),(WIDTH-80, HEIGHT-100), (80, HEIGHT-100)])
        text_end = font.render('GAME OVER ;(', True, "black", "beige")
        text_rect = text_end.get_rect()
        text_rect.center = (WIDTH/2, HEIGHT/2)
        screen.blit(text_end, text_rect)

        text_res = font_sm.render('Press "R" to Restart', True, "black", "beige")
        text_rect = text_res.get_rect()
        text_rect.center = (WIDTH/2, HEIGHT/2+70)
        screen.blit(text_res, text_rect)

        if(player.score > high_score):
            high_score = player.score

        text_res = font_sm.render(f"HIGH SCORE: {high_score}", True, "white", "black")
        text_rect = text_res.get_rect()
        text_rect.center = (WIDTH/2, 30)
        screen.blit(text_res, text_rect)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    time += dt

pygame.quit()