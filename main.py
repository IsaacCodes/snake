import random
import pygame as pg
pg.init()

screen_width, screen_height = 500, 500

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Pygame Snake")

objects = pg.sprite.Group()

class Object(pg.sprite.Sprite):
  def __init__(self, size: tuple[int, int], color: str, pos: tuple[int, int], in_group: bool = False):
    super().__init__()
    if in_group:
      objects.add(self)

    self.image = pg.Surface(size)
    self.image.fill(color)

    self.rect = self.image.get_rect()
    self.rect.topleft = pos

class Block():
  def __init__(self, size: tuple[int, int], pos: tuple[int, int]):
    #0 = empty, 1 = snake, 2 = apple
    self.states = {
      0: Object(size, "grey", pos, True),
      1: Object(size, "red", pos),
      2: Object(size, "green", pos)
    }
    self.state = 0
  
  def switch_state(self, state: int):
    objects.remove(self.states[self.state])

    self.state = state
    objects.add(self.states[self.state])


class Grid():
  def __init__(self, width: int, height: int):
    self.width = width
    self.height = height
    self.matrix = [[] for _ in range(self.width)]

    for x in range(self.width):
      for y in range(self.height):
        rect_size = screen_width/self.width, screen_height/self.height
        rect_pos = x*rect_size[0], y*rect_size[1]
        self.matrix[x].append(Block(rect_size, rect_pos))
    
    self.gen_apple()
  
  def gen_apple(self):
    new_state = 1
    while new_state != 0:
      apple_x = random.randint(0, self.width-1)
      apple_y = random.randint(0, self.height-1)

      new_state = self.matrix[apple_x][apple_y].state

    self.matrix[apple_x][apple_y].switch_state(2)

class Snake():
  def __init__(self, grid: Grid):
    self.grid = grid

    self.body = [(0, 0), (1, 0), (2, 0)]
    self.length = len(self.body)


    self.dir = (1, 0)
  
  def move(self):    
    nx, ny = self.body[-1]
    nx += self.dir[0]
    ny += self.dir[1]

    nx, ny = nx % self.grid.width, ny % self.grid.height

    if self.grid.matrix[nx][ny].state == 2:
      self.grid.gen_apple()

    else:
      tail_x, tail_y = self.body[0]
      self.grid.matrix[tail_x][tail_y].switch_state(0)
      self.body.pop(0)

    self.grid.matrix[nx][ny].switch_state(1)
    self.body.append((nx, ny))

#Objects
grid = Grid(25, 25)
snake = Snake(grid)

#Vars
clock = pg.time.Clock()
running = True
start_moving = False

while running:
  #Limits fps
  clock.tick(4)

  up, down, left, right = False, False, False, False

  #Exits on game quit (close tab)
  for event in pg.event.get():
    if event.type == pg.QUIT: 
      running = False
    
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_UP or event.key == pg.K_w:
        up = True
      if event.key == pg.K_DOWN or event.key == pg.K_s:
        down = True
      if event.key == pg.K_LEFT or event.key == pg.K_a:
        left = True
      if event.key == pg.K_RIGHT or event.key == pg.K_d:
        right = True

  #Handles movement input
  if up or down or left or right:
    start_moving = True

  if up and snake.dir != (0, 1):
    snake.dir = (0, -1)
  elif down and snake.dir != (0, -1):
    snake.dir = (0, 1)
  elif left and snake.dir != (1, 0):
    snake.dir = (-1, 0)
  elif right and snake.dir != (-1, 0):
    snake.dir = (1, 0)

  if start_moving:
    snake.move()
  
  #BG
  screen.fill((255, 255, 255))
  #Objects
  objects.draw(screen)
  #Load
  pg.display.update()