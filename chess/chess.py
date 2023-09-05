# Example file showing a circle moving on screen
import pygame
import math

# pygame setup
pygame.init()

WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

pieces = {
    "p": "Pawn",
    "R": "Rook",
    "K": "Knight",
    "B": "Bishop",
    "Q": "Queen",
    "K": "King"
}

class Square:
    piece = None
    selected = False
    available = False
    def __init__(self, file, num, color):
        self.file = file
        self.num = num
        self.color = color
        
class Board:
    ready = False
    sprites = {}
    squares = []
    should_move = False
    selected_square = None
    current_player = "W"
    debug = False

    def file_to_num(self, file):
        return ord(file)-97
    
    def num_to_file(self, num):
        return chr(num + 97)
    
    def is_own_piece(self, file, num):
        return self.squares[num][file].piece is not None and self.squares[num][file].piece.split("_")[0] == self.current_player
    
    def reset_pieces(self, file, num, sq):
        if num == 1:
            match file:
                case "a":
                    sq.piece = "W_Rook"
                case "b":
                    sq.piece = "W_Knight"
                case "c":
                    sq.piece = "W_Bishop"
                case "d":
                    sq.piece = "W_Queen"
                case "e":
                    sq.piece = "W_King"
                case "f":
                    sq.piece = "W_Bishop"
                case "g":
                    sq.piece = "W_Knight"
                case "h":
                    sq.piece = "W_Rook"
        elif num == 2:
            sq.piece = "W_Pawn"
        elif num == 7:
            sq.piece = "B_Pawn"
        elif num == 8:
            match file:
                case "a":
                    sq.piece = "B_Rook"
                case "b":
                    sq.piece = "B_Knight"
                case "c":
                    sq.piece = "B_Bishop"
                case "d":
                    sq.piece = "B_Queen"
                case "e":
                    sq.piece = "B_King"
                case "f":
                    sq.piece = "B_Bishop"
                case "g":
                    sq.piece = "B_Knight"
                case "h":
                    sq.piece = "B_Rook"
        else:
            sq.piece = None

    def load_sprites(self):
        self.sprites["W_King"] = pygame.image.load("chess/W_King.png").convert_alpha()
        self.sprites["W_Queen"] = pygame.image.load("chess/W_Queen.png").convert_alpha()
        self.sprites["W_Rook"] = pygame.image.load("chess/W_Rook.png").convert_alpha()
        self.sprites["W_Bishop"] = pygame.image.load("chess/W_Bishop.png").convert_alpha()
        self.sprites["W_Knight"] = pygame.image.load("chess/W_Knight.png").convert_alpha()
        self.sprites["W_Pawn"] = pygame.image.load("chess/W_Pawn.png").convert_alpha()

        self.sprites["B_King"] = pygame.image.load("chess/B_King.png").convert_alpha()
        self.sprites["B_Queen"] = pygame.image.load("chess/B_Queen.png").convert_alpha()
        self.sprites["B_Rook"] = pygame.image.load("chess/B_Rook.png").convert_alpha()
        self.sprites["B_Bishop"] = pygame.image.load("chess/B_Bishop.png").convert_alpha()
        self.sprites["B_Knight"] = pygame.image.load("chess/B_Knight.png").convert_alpha()
        self.sprites["B_Pawn"] = pygame.image.load("chess/B_Pawn.png").convert_alpha()
    
    def load(self):
        self.load_sprites()
        for i in range(8):
            self.squares.append([])
            for j in range(8):
                self.squares[i].append(Square(chr(97+j), 8-i, "grey" if abs(j%2-i%2) == 0 else "brown"))
                self.reset_pieces(chr(97+j), 8-i, self.squares[i][j])
        self.ready = True

    def render(self):
        for file in self.squares:
            for square in file:
                pygame.draw.rect(screen,
                                 "grey" if square.num%2-(self.file_to_num(square.file))%2 == 0 else "brown",
                                 ((self.file_to_num(square.file))*SQUARE_SIZE, (8-square.num)*SQUARE_SIZE, WIDTH/8, HEIGHT/8))
                
                if square.selected:
                    pygame.draw.rect(screen,
                                 "blue",
                                 ((self.file_to_num(square.file))*SQUARE_SIZE+5, (8-square.num)*SQUARE_SIZE+5, WIDTH/8-10, HEIGHT/8-10), width=2)
                    
                if square.piece is not None:
                    sprite_rect = self.sprites[square.piece].get_rect()
                    sprite_rect.center = ((self.file_to_num(square.file))*SQUARE_SIZE+SQUARE_SIZE/2, (8-square.num)*SQUARE_SIZE+SQUARE_SIZE/2)
                    screen.blit(self.sprites[square.piece], (sprite_rect))

                if square.available:
                    if square.piece is not None:
                        if self.current_player != square.piece.split("_")[0]:
                            pygame.draw.rect(screen,
                                 "red",
                                 ((self.file_to_num(square.file))*SQUARE_SIZE+5, (8-square.num)*SQUARE_SIZE+5, WIDTH/8-10, HEIGHT/8-10), width=3)
                    else:
                        pygame.draw.circle(screen, 'green',(self.file_to_num(square.file)*SQUARE_SIZE+SQUARE_SIZE/2,(8-square.num)*SQUARE_SIZE+SQUARE_SIZE/2), 10)
        
    def move(self, end_square):
        if end_square.available:
            end_square.piece = self.selected_square.piece
            self.selected_square.piece = None
            self.selected_square.selected = False
            self.should_move = False
            self.current_player = "B" if self.current_player == "W" else "W"
            for num in self.squares:
                for square in num:
                    square.available = False
        elif end_square.piece is not None and end_square.piece.split("_")[0] == self.current_player:
            for num in self.squares:
                for square in num:
                    square.available = False
            self.selected_square.selected = False
            self.selected_square = end_square
            self.selected_square.selected = True
            self.should_move = True
            self.show_allowed_moves()
        else:
            self.selected_square.selected = False
            self.should_move = False

            for num in self.squares:
                for square in num:
                    square.available = False
    
    def check_if_available(self, num, file ):
        print(f"checking pos [{num, file}]")
        if self.squares[num][file].piece is None:
            return True
        elif not self.is_own_piece(file, num):
            return True
        else:
            return False

    def check_moves_left(self, curr_file, curr_num):
        file_pos = self.file_to_num(curr_file)
        for i in range(1,file_pos+1):
            if self.debug:
                print(f"{i}. In check moves left, 1 -> file_pos+1 ({file_pos+1})")
            self.squares[8-curr_num][file_pos-i].available = self.check_if_available(8-curr_num, file_pos-i)

    def check_moves_right(self, curr_file, curr_num):
        file_pos = self.file_to_num(curr_file)
        for i in range(1, 8-file_pos):
            if self.debug:
                print(f"{i}. In check moves right, 1 -> 8-file_pos ({8-file_pos})")
            if self.squares[8-curr_num][file_pos+i].piece is None:
                self.squares[8-curr_num][file_pos+i].available = True
            elif not self.is_own_piece(file_pos+i, 8-curr_num):
                self.squares[8-curr_num][file_pos+i].available = True
                break
            else:
                break
        
    def check_moves_up(self, curr_file, curr_num):
        file_pos = self.file_to_num(curr_file)
        for i in range(curr_num+1, 9):
            if self.debug:
                print(f"{i}. In check moves up, curr_num+1 ({curr_num+1}) -> 9 ")
            if self.squares[8-i][file_pos].piece is None:
                self.squares[8-i][file_pos].available = True
            elif not self.is_own_piece(file_pos, 8-i):
                self.squares[8-i][file_pos].available = True
                break
            else:
                break

    def check_moves_down(self, curr_file, curr_num):
        file_pos = self.file_to_num(curr_file)
        for i in range(curr_num-1, 0, -1):
            if self.debug:
                print(f"{i}. In check moves down\nChecking square: {curr_file}{i}\nIsOwnPiece: {self.is_own_piece(file_pos, 8-i)}")
            if self.squares[8-i][file_pos].piece is None:
                self.squares[8-i][file_pos].available = True
            elif not self.is_own_piece(file_pos, 8-i):
                self.squares[8-i][file_pos].available = True
                break
            else:
                break

    def check_knight(self, curr_file, curr_num):
        file_pos = self.file_to_num(curr_file)
        if self.debug:
            print(f"Check knight\nSquare {curr_file}({file_pos}) {curr_num}\nPlace in Matrix: [(8-curr_num),(file_pos)] [{8-curr_num},{file_pos}]")

        matrix_pos = [8-curr_num, file_pos]
        if matrix_pos[0]+2 < 8:
            if matrix_pos[1] + 1 < 8:
                self.squares[matrix_pos[0]+2][matrix_pos[1] + 1].available = self.check_if_available(matrix_pos[0]+2, matrix_pos[1] + 1)
            if matrix_pos[1] - 1 >= 0:
                self.squares[matrix_pos[0]+2][matrix_pos[1] - 1].available = self.check_if_available(matrix_pos[0]+2, matrix_pos[1] - 1)

        if matrix_pos[0]-2 > 0:
            if matrix_pos[1] + 1 < 8:
                self.squares[matrix_pos[0]-2][matrix_pos[1] + 1].available = self.check_if_available(matrix_pos[0]-2, matrix_pos[1] + 1)
            if matrix_pos[1] - 1 >= 0:
                self.squares[matrix_pos[0]-2][matrix_pos[1] - 1].available = self.check_if_available(matrix_pos[0]-2, matrix_pos[1] - 1)

        if matrix_pos[1]+2 < 8:
            if matrix_pos[0] + 1 < 8:
                self.squares[matrix_pos[0] + 1][matrix_pos[1]+2].available = self.check_if_available(matrix_pos[0] + 1, matrix_pos[1]+2)
            if matrix_pos[0] - 1 >= 0:
                self.squares[matrix_pos[0] - 1][matrix_pos[1]+2].available = self.check_if_available(matrix_pos[0] - 1, matrix_pos[1]+2)

        if matrix_pos[1]-2 > 0:
            if matrix_pos[0] + 1 < 8:
                self.squares[matrix_pos[0] + 1][matrix_pos[1]-2].available = self.check_if_available(matrix_pos[0] + 1, matrix_pos[1]-2)
            if matrix_pos[0] - 1 >= 0:
                self.squares[matrix_pos[0] - 1][matrix_pos[1]-2].available = self.check_if_available(matrix_pos[0] - 1, matrix_pos[1]-2)
    
    def check_horizontals(self, curr_file, curr_num):
        # look right
        self.check_moves_right(curr_file, curr_num)
        # look left
        self.check_moves_left(curr_file, curr_num)
        # look down
        self.check_moves_down(curr_file, curr_num)
        # look up
        self.check_moves_up(curr_file, curr_num)

    def check_diagonals(self, curr_file, curr_num):
        file_pos = self.file_to_num(curr_file)
        # if self.debug:
        print(f"Check bishop\nSquare {curr_file}({file_pos}) {curr_num}\nPlace in Matrix: [(8-curr_num),(file_pos)] [{8-curr_num},{file_pos}]")
        found = [False, False, False, False]
        # Up
        for num in range(8-curr_num-1, -1, -1):
            if file_pos+(8-curr_num-num) < 8 and not found[0]:
                print(f"1. Check [{num}, {file_pos+(8-curr_num-num)}]")
                isAvailable = self.check_if_available(num, file_pos+(8-curr_num-num))
                self.squares[num][file_pos+(8-curr_num-num)].available = isAvailable
                if not isAvailable or self.squares[num][file_pos+(8-curr_num-num)].piece is not None:
                    found[0] = True
            if file_pos-(8-curr_num-num) >= 0 and not found[1]:
                isAvailable = self.check_if_available(num, file_pos-(8-curr_num-num))
                self.squares[num][file_pos-(8-curr_num-num)].available = isAvailable
                if not isAvailable or self.squares[num][file_pos-(8-curr_num-num)].piece is not None:
                    found[1] = True

        # Down
        for num in range(8-curr_num+1, 8):
            if file_pos+(num-(8-curr_num)) < 8 and not found[2]:
                isAvailable = self.check_if_available(num, file_pos+(num-(8-curr_num)))
                self.squares[num][file_pos+(num-(8-curr_num))].available = isAvailable
                if not isAvailable or self.squares[num][file_pos+(num-(8-curr_num))].piece is not None:
                    found[2] = True
            
            if file_pos-(num-(8-curr_num)) >= 0 and not found[3]:
                isAvailable = self.check_if_available(num, file_pos-(num-(8-curr_num)))
                self.squares[num][file_pos-(num-(8-curr_num))].available = isAvailable
                if not isAvailable or self.squares[num][file_pos-(num-(8-curr_num))].piece is not None:
                    found[3] = True

    def show_allowed_moves(self):
        curr_file = self.file_to_num(self.selected_square.file)
        curr_num = self.selected_square.num
        if self.debug:
            print(f"Selected: {self.selected_square.piece.split('_')[1]} on {self.selected_square.file}{curr_num}")
        
        match self.selected_square.piece.split("_")[1]:
            case "Pawn":
                if self.current_player == "W":
                    if curr_file > 0 and self.squares[7-curr_num][curr_file-1].piece is not None:
                        self.squares[7-curr_num][curr_file-1].available = self.check_if_available(7-curr_num, curr_file-1)

                    if curr_file < 7 and self.squares[7-curr_num][curr_file+1].piece is not None:
                        self.squares[7-curr_num][curr_file+1].available = self.check_if_available(7-curr_num, curr_file+1)

                    if self.squares[7-curr_num][curr_file].piece is None:
                        self.squares[7-curr_num][curr_file].available = True
                        if curr_num == 2:
                            self.squares[6-curr_num][curr_file].available = self.check_if_available(6-curr_num, curr_file)
                else:
                    if curr_file > 0 and self.squares[9-curr_num][curr_file-1].piece is not None:
                        self.squares[9-curr_num][curr_file-1].available = self.check_if_available(9-curr_num, curr_file-1)

                    if curr_file < 7 and self.squares[9-curr_num][curr_file+1].piece is not None:
                        self.squares[9-curr_num][curr_file+1].available = self.check_if_available(9-curr_num, curr_file+1)

                    if self.squares[9-curr_num][curr_file].piece is None:
                        self.squares[9-curr_num][curr_file].available = True
                        if curr_num == 7:
                            self.squares[10-curr_num][curr_file].available = self.check_if_available(10-curr_num, curr_file)
            case "Rook":
                self.check_horizontals(self.selected_square.file, self.selected_square.num)
            case "Knight":
                self.check_knight(self.selected_square.file, self.selected_square.num)
            case "Bishop":
                self.check_diagonals(self.selected_square.file, self.selected_square.num)
            case "Queen":
                self.check_diagonals(self.selected_square.file, self.selected_square.num)
                self.check_horizontals(self.selected_square.file, self.selected_square.num)
            case "King":
                for i in range(3):
                    if 8-curr_num+(1-i) >= 0 and 8-curr_num+(1-i) < 8:
                        for j in range (3):
                            if curr_file+(1-j) >= 0 and curr_file+(1-j) < 8:
                                self.squares[8-curr_num+(1-i)][curr_file+(1-j)].available = self.check_if_available(8-curr_num+(1-i), curr_file+(1-j))
    
    def get_square(self):
        mouse_pos = pygame.mouse.get_pos()
        square_file = chr(math.floor((mouse_pos[0])/SQUARE_SIZE) +97)
        square_num = math.floor((mouse_pos[1])/SQUARE_SIZE)
        return board.squares[square_num][self.file_to_num(square_file)]

def get_event():
    # Listen to WASD keys for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pass
    if keys[pygame.K_s]:
        pass
    if keys[pygame.K_a]:
        pass
    if keys[pygame.K_d]:
        pass


def select_square():
    curr_square = board.get_square()
    if not board.should_move and curr_square.piece is not None:
        curr_piece_color = curr_square.piece.split("_")[0]
        if curr_piece_color == board.current_player:
            curr_square.selected = True
            board.selected_square = curr_square
            board.should_move = True
            board.show_allowed_moves()
    elif board.should_move:
        board.move(curr_square)


board = Board()
while running:

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("beige")

    if not board.ready:
        board.load()
        pass
    
    board.render()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            select_square()
            

    get_event()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()