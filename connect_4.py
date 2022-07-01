#kroutsis
import pygame as pg
from time import sleep
import math

SIZE = WIDTH, HEIGHT = 420, 360
ROWS = 6
COLLUMNS = 7 + 1

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 204
YELLOW = 255, 255, 0

class connect_4:

    def __init__(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption('CONNECT4')
        self.screen = pg.display.set_mode(SIZE)
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.board = self.create_board()
        self.moves = 0

    def create_board(self):
        #board = np.zeros((ROWS, COLLUMNS))
        self.board = [[0]*COLLUMNS for i in range(ROWS)]
        self.screen.fill(BLUE)
        for i in range(ROWS):
            for j in range(COLLUMNS):
                pg.draw.circle(self.screen, BLACK, [30 + j * 60, 30 + i * 60], 26)
        return self.board

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.pos = pg.mouse.get_pos()
                self.player = (self.moves % 2) + 1
                self.update_board(self.pos, self.player)
                self.moves += 1

    def update_board(self, pos, player):
        j = 5
        i = math.floor(pos[0] / (WIDTH / (COLLUMNS - 1)))

        while (j >= 0 and (self.board[j][i] == 1 or self.board[j][i] == 2)):
            j -= 1
        if self.player == 1:
            pg.draw.circle(self.screen, YELLOW, [30 + i * 60, 30 + j * 60], 26)
            self.board[j][i] = 1 
        else:
            pg.draw.circle(self.screen, RED, [30 + i * 60, 30 + j * 60], 26)
            self.board[j][i] = 2
        #print(self.moves)
        
        if self.moves > 5 and self.moves < 10:
            if self.check_for_winner_1(self.board, self.player, i, j):
                return
        elif self.moves == 10:
            if self.check_for_winner_1(self.board, self.player, i, j):
                return
            if self.check_for_winner_2(self.board, self.player, i, j):
                return
        elif self.moves > 10:
            if self.check_for_winner_1(self.board, self.player, i, j):
                return
            if self.check_for_winner_2(self.board, self.player, i, j):
                return
            if self.check_for_winner_3(self.board, self.player, i, j):
                return
        
    def check_for_winner_1(self, board, player, i, j):
        try:
            last_chip = self.board[j][i]
            if self.board[j][i+1] == last_chip and self.board[j][i+2] == last_chip and self.board[j][i+3] == last_chip:
                #print("right")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+2) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+3) * 60, 30 + j * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j][i-1] == last_chip and self.board[j][i-2] == last_chip and self.board[j][i-3] == last_chip:
                #print("left")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-2) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-3) * 60, 30 + j * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j][i-1] == last_chip and self.board[j][i+1] == last_chip and self.board[j][i+2] == last_chip:
                #print("mid right")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+2) * 60, 30 + j * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j][i-1] == last_chip and self.board[j][i-2] == last_chip and self.board[j][i+1] == last_chip:
                #print("mid left")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-2) * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + j * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j+1][i] == last_chip and self.board[j+2][i] == last_chip and self.board[j+3][i] == last_chip:
                #print("down")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + (j+1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + (j+2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + (j+3) * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j+1][i+1] == last_chip and self.board[j+2][i+2] == last_chip and self.board[j+3][i+3] == last_chip:
                #print("diagonal right top")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + (j+1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+2) * 60, 30 + (j+2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+3) * 60, 30 + (j+3) * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j+1][i-1] == last_chip and self.board[j+2][i-2] == last_chip and self.board[j+3][i-3] == last_chip:
                #print("diagonal left top")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + (j+1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-2) * 60, 30 + (j+2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-3) * 60, 30 + (j+3) * 60], 26)
                self.print_winner(self.player)
                return True
        except IndexError:
            pass  
            
    def check_for_winner_2(self, board, player, i, j):
        try:
            last_chip = self.board[j][i]
            if self.board[j-1][i+1] == last_chip and self.board[j-2][i+2] == last_chip and self.board[j+1][i-1] == last_chip:
                #print("d2l")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + (j-1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+2) * 60, 30 + (j-2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + (j+1) * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j-1][i-1] == last_chip and self.board[j-2][i-2] == last_chip and self.board[j+1][i+1] == last_chip:
                #print("d2r")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + (j-1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-2) * 60, 30 + (j-2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + (j+1) * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j+1][i-1] == last_chip and self.board[j+2][i-2] == last_chip and self.board[j-1][i+1] == last_chip:
                #print("d1l")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + (j+1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-2) * 60, 30 + (j+2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + (j-1) * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j-1][i-1] == last_chip and self.board[j+1][i+1] == last_chip and self.board[j+2][i+2] == last_chip:
                #print("d1r")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + (j-1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + (j+1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+2) * 60, 30 + (j+2) * 60], 26)
                self.print_winner(self.player)
                return True
        except IndexError:
            pass
            
    def check_for_winner_3(self, board, player, i, j):
        try:
            last_chip = self.board[j][i] 
            if self.board[j-1][i-1] == last_chip and self.board[j-2][i-2] == last_chip and self.board[j-3][i-3] == last_chip:
                #print("diagonal right bot")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-1) * 60, 30 + (j-1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-2) * 60, 30 + (j-2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i-3) * 60, 30 + (j-3) * 60], 26)
                self.print_winner(self.player)
                return True
            elif self.board[j-1][i+1] == last_chip and self.board[j-2][i+2] == last_chip and self.board[j-3][i+3] == last_chip:
                #print("diagonal left bot")
                print("Player " + str(self.player) + " WINS")
                pg.draw.circle(self.screen, GREEN, [30 + i * 60, 30 + j * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+1) * 60, 30 + (j-1) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+2) * 60, 30 + (j-2) * 60], 26)
                pg.draw.circle(self.screen, GREEN, [30 + (i+3) * 60, 30 + (j-3) * 60], 26)
                self.print_winner(self.player)
                return True
        except IndexError:
            pass

    def print_winner(self, player):
        msg = "Player " + str(self.player) +" Wins!"
        textsurface = self.font.render(msg, False, WHITE)
        self.screen.blit(textsurface,(115,150))
        pg.display.update()
        sleep(1)
        self.__init__()

    def gameloop(self):
        while True:
            self.event_handler()
            pg.display.flip()

if __name__ == "__main__": 
    game = connect_4()
    game.gameloop()  