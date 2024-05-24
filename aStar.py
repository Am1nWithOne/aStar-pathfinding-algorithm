import math
from queue import PriorityQueue
import pygame

# seting up the display
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

# caption for the display
pygame.display.set_caption("A* Path Finding Algorithm")


# define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        #bayad position daghigh be pygame bedim, injoori start x, y cube ro peyda mikonim
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    

    # methodes for get the state of Nodes

    #indexing with row column
    def get_pos(self):
        return self.row, self.col 
    
    # have we already look at u? Have we consider you??? (Red squares)
    def is_closed(self):
        return self.color == RED
    
    # check for open spots
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = WHITE
    

    # change the Node colors

    def make_start(self):
        self.color = ORANGE

    def make_close(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_end(self):
        self.color = TURQUOISE

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = PURPLE

    # win: window, where we are gonna draw the table
    def draw(self, win):
        # draw a cube in pygame
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row < self.total_rows -1 and not grid[self.row +1][self.col].is_barrier(): # Chekc DOWN
            self.neighbors.append(grid[self.row +1][self.col])
        
        if self.row > 0 and not grid[self.row -1][self.col].is_barrier(): # Chekc UP
            self.neighbors.append(grid[self.row -1][self.col])
        
        if self.col < self.total_rows -1 and not grid[self.row][self.col +1].is_barrier(): # Chekc Right
            self.neighbors.append(grid[self.row][self.col +1])
        
        if self.col > 0 and not grid[self.row][self.col -1].is_barrier(): # Chekc Left
            self.neighbors.append(grid[self.row][self.col-1])

    # 34:30
    def __lt__(self, other):
        return False

# p1: point1, p2: point2
def h(p1, p2):
    # Manhatan distance: L distance
    x1, y1, = p1
    x2, y2, = p2
    return abs(x2 - x1) + abs(y2 - y1)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    # we can call it like this because we defind it as a lambda
    # draw()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # list comperhenssion
    g_score = {node : float('inf') for row in grid for node in row}
    g_score[start] = 0
    
    f_score = {node : float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # open_set gonna store the [f_scrore, the_count, node]
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            # make path
            reconstruct_path(came_from, end, draw)
            # ke roye start ya end purple nashe v betoonim bbinimeshon
            end.make_end()
            return True
        
        for neghibor in current.neighbors:
            # print(neghibor)
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neghibor]:
                came_from[neghibor] = current
                g_score[neghibor] = temp_g_score
                f_score[neghibor] = temp_g_score + h(neghibor.get_pos(), end.get_pos()) 
                if neghibor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neghibor], count, neghibor))
                    open_set_hash.add(neghibor)
                    neghibor.make_open()


        draw()

        if current != start:
            current.make_close()
            # print(22)
    
    return False

# create the grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    # draw line for each one of this rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False

            # leftlick
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if row >=0 and row <50 and col >=0 and col<50:
                    node = grid[row][col]
                # print(not end, node != start)
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    # print(1)
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
                
            # Right click
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if row >=0 and row <50 and col >=0 and col<50:
                    node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

                # Running the Algorithm
            if event.type == pygame.KEYDOWN:
                    
                if event.key == pygame.K_SPACE and start and end:
                     
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
            
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)