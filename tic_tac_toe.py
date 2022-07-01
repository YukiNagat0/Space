#Konstantinos Routsis
import pygame as pg
from time import sleep
import random

BOARD_SIZE = WIDTH, HEIGHT = 480, 480
BOARD_COLOR = 0, 0, 0
LINE_COLOR = 255, 255, 255
MOVE_COLOR = 200, 0, 0
CELL_SIZE = int(480 / 3)

class tic_tac_toe:
    
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tic Tac Toe')
        self.screen = pg.display.set_mode(BOARD_SIZE)
        self.draw_grid()
        self.grid = [[0,0,0],[0,0,0],[0,0,0]]
        self.winner = ''
        self.rounds = 0
        player = ('x', 'o')
        self.player = random.choice(player)
        
    def draw_grid(self):
        for x in range(CELL_SIZE, WIDTH, CELL_SIZE):
            pg.draw.line(self.screen, LINE_COLOR, (x, 0), (x, HEIGHT),5) #vertical lines
            pg.draw.line(self.screen, LINE_COLOR, (0, x), (WIDTH, x),5)  #horizontal lines
        pg.display.flip()
        
    def draw_x(self, x, y):
        pg.draw.line(self.screen, MOVE_COLOR, 
                         (25 + x * CELL_SIZE,25 + y * CELL_SIZE), 
                         (CELL_SIZE - 25 + x * CELL_SIZE, CELL_SIZE - 25 + y * CELL_SIZE),
                         8)
        pg.draw.line(self.screen, MOVE_COLOR, 
                         (CELL_SIZE - 25 + x * CELL_SIZE, 25 + y * CELL_SIZE), 
                         (25 + x * CELL_SIZE, CELL_SIZE - 25 + y * CELL_SIZE), 
                         8)
        pg.display.flip()
        
    def draw_o(self, x, y):
        pg.draw.circle(self.screen, MOVE_COLOR, 
                           (int(CELL_SIZE / 2) + x * CELL_SIZE, int(CELL_SIZE / 2) + y * CELL_SIZE),
                           60, 7)
        pg.display.flip()
        
    def update_grid(self, x, y):
        if x < CELL_SIZE:
            self.col = 0
        elif x < CELL_SIZE * 2 and x > CELL_SIZE:
            self.col = 1
        elif x > CELL_SIZE * 2:
            self.col = 2
        if y < CELL_SIZE:
            self.row = 0
        elif y < CELL_SIZE * 2 and y > CELL_SIZE:
            self.row = 1
        elif y > CELL_SIZE * 2:
            self.row = 2
            
        if self.player == 'o' and self.grid[self.row][self.col] == 0:
            self.rounds += 1
            self.grid[self.row][self.col] = 'o'
            self.draw_o(self.col, self.row)
            self.player = 'x'
        elif self.player == 'x' and self.grid[self.row][self.col] == 0:
            self.rounds += 1
            self.grid[self.row][self.col] = 'x'
            self.draw_x(self.col, self.row)
            self.player = 'o'

    def check_horizontal_winner(self):
        for i,row in enumerate(self.grid):
            if 0 not in row:
                if row.count('o') == 3 or row.count('x') == 3:
                    pg.draw.line(self.screen, LINE_COLOR, 
                                     (25 ,int(CELL_SIZE / 2) + CELL_SIZE * i), 
                                     (480 - 25, int(CELL_SIZE / 2) + CELL_SIZE * i),
                                     8)
                    pg.display.flip()
                    print("Winner: " + row[0])
                    sleep(2)
                    self.__init__()
                    
    def check_vertical_winner(self):
        col = []
        for i in range(3):
            col.append([row[i] for row in self.grid])
            if 0 not in col[i]:
                if col[i].count('o') == 3 or col[i].count('x') == 3:
                    pg.draw.line(self.screen, LINE_COLOR, 
                                     (int(CELL_SIZE / 2) + CELL_SIZE * i, 25),
                                     (int(CELL_SIZE / 2) + CELL_SIZE * i, 480 - 25),
                                     8)
                    pg.display.flip()
                    print("Winner: " + col[i][0])
                    sleep(2)
                    self.__init__()
                    
    def check_diagonal_winner(self):
         if self.grid[1][1] != 0:
             mid = self.grid[1][1]
             if self.grid[0][0] == self.grid[2][2] and self.grid[2][2] == mid:
                 pg.draw.line(self.screen, LINE_COLOR, (25 ,25), (480 - 25, 480 - 25), 8)
                 pg.display.flip()
                 print("Winner: " + mid)
                 sleep(2)
                 self.__init__()
             if self.grid[2][0] == self.grid[0][2] and self.grid[0][2] == mid:
                 pg.draw.line(self.screen, LINE_COLOR, (480 - 25, 25), (25, 480 - 25), 8)
                 pg.display.flip()
                 print("Winner: " + mid)
                 sleep(2)
                 self.__init__()

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.unicode == 'q': #exit game
                    pg.quit()
                    exit()
            if pg.mouse.get_pressed() == (1,0,0): #select cell
                mx, my = pg.mouse.get_pos()
                self.update_grid(mx, my)
                if self.rounds > 4:# and self.rounds < 9:
                    self.check_vertical_winner()
                    self.check_horizontal_winner()
                    self.check_diagonal_winner()
                if self.rounds >= 9:
                    print("No winners")
                    sleep(2)
                    self.__init__()
            if event.type == pg.QUIT:
                pg.quit()
                exit()
                    
    def run(self):
        while True:
            self.event_handler()
            

if __name__ == "__main__":
    game = tic_tac_toe()
    game.run()