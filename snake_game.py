#Konstantinos Routsis
import pygame as pg
import random

BOARD_SIZE = WIDTH, HEIGHT = 880, 640
BOARD_COLOR = 0, 0, 0
SNAKE_COLOR = 180, 255, 100
FOOD_COLOR = 200, 0, 0
CELL_SIZE = 16
MAX_FPS = 7

class snake_game:
    
    def __init__(self):
        pg.init()
        pg.display.set_caption('Snake Game')
        self.screen = pg.display.set_mode(BOARD_SIZE)
        self.last_update_completed = 0
        self.desired_ms_between_updates = (1.0 / MAX_FPS) * 1000.0
        self.num_col = int(WIDTH / CELL_SIZE) - 2
        self.num_row = int(HEIGHT / CELL_SIZE) - 2
        self.init_food()
        self.init_snake()
        
    def init_snake(self):
        orientations = ('right', 'left', 'up', 'down')
        self.orientation = random.choice(orientations)
        self.col = random.randint(0, self.num_col)
        self.row = random.randint(0, self.num_row)
        self.snake = [(self.col, self.row)]
        self.length = len(self.snake)
        
    def init_food(self):
        self.food_col = random.randint(0, self.num_col)
        self.food_row = random.randint(0, self.num_row)
        self.food = (self.food_col, self.food_row)
        
    def draw_snake(self):
        for snake_cell in self.snake:
            col, row = snake_cell
            snake = pg.draw.rect(self.screen,
                                     SNAKE_COLOR,
                                     (int(col * CELL_SIZE + CELL_SIZE),
                                      int(row * CELL_SIZE + CELL_SIZE),
                                      int(CELL_SIZE),
                                      int(CELL_SIZE)),
                                      0)
        
        food = pg.draw.rect(self.screen,
                                FOOD_COLOR,
                                (int(self.food_col * CELL_SIZE + CELL_SIZE),
                                 int(self.food_row * CELL_SIZE + CELL_SIZE),
                                 int(CELL_SIZE),
                                 int(CELL_SIZE)),
                                 0)    
        
        pg.display.flip()
        
    def eat_food(self):
        self.init_food()
        self.length += 1
        self.snake.append(self.food)
            
    def kill_snake(self):
        self.__init__()
        
    def grow_snake(self):
        for i in range(self.length):
            prev_head_position = self.snake[i]
            self.snake.append(prev_head_position)
            self.snake.pop(i)
            break
        self.update_head_position()
        if self.snake[0] == self.food:
            self.eat_food()
        if len(self.snake) != len(set(self.snake)):
            self.kill_snake()
        self.draw_snake()
        #print(self.snake)

    def update_head_position(self):
        if self.orientation == 'right':
            self.col += 1
            if self.col > self.num_col:
                self.col = 0
        elif self.orientation == 'left':
            self.col -= 1
            if self.col < 0:
                self.col = self.num_col
        elif self.orientation == 'up':
            self.row -= 1
            if self.row < 0:
                self.row = self.num_row
        elif self.orientation == 'down':
            self.row += 1
            if self.row > self.num_row:
                self.row = 0
        self.snake[0] = (self.col, self.row)

    def event_handler(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.unicode == 'w' :#or event.unicode == 'K_UP':
                    if self.orientation == 'right' or self.orientation == 'left':
                        self.orientation = 'up'
                if event.unicode == 's' :#or event.unicode == 'K_DOWN':
                    if self.orientation == 'right' or self.orientation == 'left':
                        self.orientation = 'down'
                if event.unicode == 'd' :#or event.unicode == 'K_RIGHT':
                    if self.orientation == 'up' or self.orientation == 'down':
                        self.orientation = 'right'
                if event.unicode == 'a' :#or event.unicode == 'K_LEFT':
                    if self.orientation == 'up' or self.orientation == 'down':
                        self.orientation = 'left'
                if event.unicode == 'q': #exit game
                    pg.quit()
                    exit()
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def cap_frame_rate(self):
        now = pg.time.get_ticks()
        ms_since_last_update = now - self.last_update_completed
        sleep_time = self.desired_ms_between_updates - ms_since_last_update
        if sleep_time > 0:
            pg.time.delay(int(sleep_time))
        self.last_update_completed = now
        
    def run(self):
        while True:
            self.cap_frame_rate()
            self.screen.fill(BOARD_COLOR)
            self.event_handler()
            self.grow_snake()

        
if __name__ == "__main__":
    game = snake_game()
    game.run()