import pygame, sys, random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

width, height = 640, 480
tile_size = (10, 10)
bg_pos = (100, 100)
#bg_size = (50, 200)
tiles = (5, 20)
starting_pos = (bg_pos[0] + (tiles[0]/2-1)*tile_size[0] + 1, bg_pos[1]+1+10)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame tetris clone')

colors = {'red': pygame.Color(255, 0, 0),
          'green': pygame.Color(0, 255, 0),
          'blue': pygame.Color(0, 0, 255),
          'white': pygame.Color(255, 255, 255),
          'black': pygame.Color(0, 0, 0)}

directions = {'left': (-tile_size[0], 0),
              'right': (tile_size[0], 0),
              'up': (0, -tile_size[0]),
              'down': (0, tile_size[0])}

shapes = {'l': [[1,0,0,0] for i in range(4)],
          'J': [[0,1,0], [0,1,0], [1,1,0]],
          'L': [[1,1,0],[0,1,0],[0,1,0]],
          'O': [[1,1], [1,1]],
          'S': [[0,1,0], [1,1,0], [1,0,0]],
          'T': [[0,1,0], [1,1,0], [0,1,0]],
          'Z': [[1,0,0], [1,1,0], [0,1,0]]}

fontObj = pygame.font.Font('freesansbold.ttf', 32)
msg = 'Hello world!'

#def rotate_1dlist(1dlist):
#    result = []
#    while 1dlist:
#        result.append(1dlist.pop)
#    return result

def check_line_full(group, line_rect, tiles):
    n = 0
    toclear = []
    for b in group.sprites():
        if line_rect.contains(b):
            toclear.append(b)
            n = n + 1
    if n == tiles:
        return toclear
    else:
        return False
    

def rotate_right(d2list):
    result = [[] for _ in range(len(d2list))]
    for l in d2list:
        l_len = len(l)
        for i in range(l_len):
            result[i].append(l.pop())
    return result

def rotate_left(d2list):
    cols = len(d2list)
    result = [[0 for _ in range(len(d2list[i]))] for i in range(cols)]
    #d2list_len = len(d2list)
    #i = d2list_len - 1
    
    for i in range(cols):
        rows = len(d2list[i])
        for j in range(rows):
            result[j][rows-i-1] = d2list[i][j] 
        
    return result

def create_world(start_pos, world_wh, rect_wh):
    rect_w, rect_h = rect_wh[0], rect_wh[1]
    world_w, world_h = world_wh[0], world_wh[1]
    world = [[pygame.Rect(start_pos[0]+x*rect_w, start_pos[1]+y*rect_h, rect_w, rect_h)  for y in range(world_h)]
             for x in range(world_w)]
    #for w in range(width):
    #    for h in range(height):
    #        pass
    return world

def create_shape(shapes, shape_type, box_size=(9,9), color=colors['red'], initial_pos=(0,0)):
    result = []
    shape = shapes[shape_type]
    for i in range(len(shape)):
        result.append([])
        for j in range(len(shape[i])):
            if shape[i][j] == 1:
                pos = (initial_pos[0] + (box_size[0]+1)*i, initial_pos[1] + (box_size[1]+1)*j)
                result[i].append(Box(box_size, color, pos))
            else:
                result[i].append(0)
    return result
    #for i in len(shapes[shape_type]):
    #    result.append([])
    #    l_length = len(l)
    #    for j in l_length:
    #        if l[j] == 1:
                            

def draw_background_image((width, height), (tile_w, tile_h), line_color=colors['black'], bg_color=colors['white']):
    background = pygame.Surface([width, height])
    background.fill(bg_color)
    x_tiles = width / tile_w
    y_tiles = height /tile_h
    for i in range(x_tiles):
        pygame.draw.line(background, line_color, (i*tile_w, 0), (i*tile_w, y_tiles*tile_h))
    for i in range(y_tiles):
        pygame.draw.line(background, line_color, (0, i*tile_h), (x_tiles*tile_w, i*tile_h))
    return background

class Background():
    #def __init__(self, initial_pos, bg_size, tile_size, line_color=colors['black'], bg_color=colors['white']):
    def __init__(self, initial_pos, tiles, tile_size, line_color=colors['black'], bg_color=colors['white']):
        #self.image = draw_background_image(bg_size, tile_size, line_color, bg_color)
        self.image = draw_background_image((tiles[0]*tile_size[0], tiles[1]*tile_size[1]), tile_size, line_color, bg_color)

        self.rect = self.image.get_rect()
        self.rect.topleft = initial_pos
    

#world = create_world((50, 50), (3,5), (10,10))
#print world

class Box(pygame.sprite.Sprite):
    def __init__(self, size=(9,9), color=colors['red'], initial_pos=(0,0)):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.lastrect = None
        self.rect.topleft = initial_pos

        #self.lastmove = None

    def move(self, (x, y)):
        self.lastrect = self.rect
        self.rect = self.rect.move(x, y)

    def change_pos(self, (x, y)):
        self.lastrect = self.rect
        self.rect.topleft = (x, y)

    def undo_move(self):
        self.rect = self.lastrect

class Shape():
    def __init__(self, shapes, shape_type, box_size=(9,9), color=colors['red'], initial_pos=starting_pos):
        self.shape = create_shape(shapes, shape_type, box_size, color, initial_pos)
        #self.boxes = [box for box in self.shape if box != 0]
        self.boxes = []
        for l in self.shape:
            for e in l:
                if e != 0:
                    self.boxes.append(e)

        self.pos = initial_pos
        self.lastpos = None

        self.box_size = box_size

        self.last_actions = []

    def move(self, (x, y)):
        for b in self.boxes:
            b.move((x, y))

        self.lastpos = self.pos
        self.pos = (self.pos[0] + x, self.pos[1] + y)

        self.last_actions.append('move')

    def undo_move(self):
        for b in self.boxes:
            b.undo_move()

        self.pos = self.lastpos

    def undo_last_action(self):
        if self.last_actions != []:
            last_action = self.last_actions.pop()
        else:
            last_action = None
        if last_action == 'move':
            self.undo_move()
        elif last_action == 'rotate_left':
            self.rotate_right()
        elif last_action == 'rotate_right':
            self.rotate_left()
        
    def rotate_right(self):
        self.shape = rotate_right(self.shape)
        self.update_pos()

        self.last_actions.append('rotate_right')

    def rotate_left(self):
        self.shape = rotate_left(self.shape)
        self.update_pos()

        self.last_actions.append('rotate_left')

    def update_pos(self):
        shape = self.shape
        initial_pos = self.pos
        box_size = self.box_size
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                box = shape[i][j]
                if box != 0:
                    pos = (initial_pos[0] + (box_size[0]+1)*i, initial_pos[1] + (box_size[1]+1)*j)
                    box.change_pos(pos)

    #def fell_out(self, rect):
    #    for b in self.boxes:
    #        if b.bottom > rect.bottom:
    #            return True

    def blit_to_surface(self, surface):
        for b in self.boxes:
            surface.blit(b.image, b.rect)


#b = Box((9, 9), colors['red'], [111, 111])
current_shape = Shape(shapes, 'J')
#screen.blit(b.image, b.rect)

#background = draw_background_image((100, 100), (10, 10))
background = Background(bg_pos, tiles, tile_size)
#screen.blit(background, bg_pos)
#screen.blit(b.image, b.rect)

#pygame.display.update()
#while pygame.event.poll().type != KEYDOWN: pygame.time.delay(10)

#print shapes

if __name__ == '__main__':
    time_to_fall = 0
    rate = 10
    make_new_shape = False
    #shapes_list = []
    shapes_group = pygame.sprite.Group()
    bottom_line_rect = pygame.Rect(bg_pos[0], bg_pos[1] + (tiles[1]-1)*tile_size[1], tiles[0]*tile_size[0], tile_size[1])

    random.seed()
    while True:
        #windowSurfaceObj.fill(colors['white'])

        #pygame.draw.rect(windowSurfaceObj, colors['red'], (10, 10, 50, 100))

        #b.move(directions['right'])

        screen.blit(background.image, background.rect)
        #screen.blit(b.image, b.rect)
        current_shape.blit_to_surface(screen)
        #for s in shapes_list:
        #    if isinstance(s, Shape):
        #        s.blit_to_surface(screen)
        shapes_group.draw(screen)

        pygame.display.update()
        fpsClock.tick(30)

        if time_to_fall > rate:
            current_shape.move(directions['down'])
            time_to_fall = 0
        else:
            time_to_fall = time_to_fall + 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    current_shape.move(directions['left'])
                elif event.key == K_RIGHT:
                    current_shape.move(directions['right'])
                elif event.key == K_UP:
                    #current_shape.move(directions['up'])
                    current_shape.rotate_right()
                elif event.key == K_DOWN:
                    #current_shape.move(directions['down'])
                    current_shape.rotate_left()  
    
        for b in current_shape.boxes:
            if b.rect.bottom > background.rect.bottom:
                make_new_shape = True
            while not background.rect.contains(b.rect):
                current_shape.undo_last_action()
            while pygame.sprite.spritecollide(b, shapes_group, False):
                make_new_shape = True
                current_shape.undo_last_action()

        toclear = check_line_full(shapes_group, bottom_line_rect, tiles[0])
        if toclear:
            shapes_group.remove(toclear)
            for b in shapes_group:
                b.move(directions['down'])
                
        #if check_line_full(shapes_group, bottom_line_rect, tiles[0]):
        #    print "clear!"

        if make_new_shape:
            make_new_shape = False
            #shapes_list.append(current_shape)
            shapes_group.add(current_shape.boxes)
            current_shape = Shape(shapes, random.choice(shapes.keys()))   

        #pygame.time.delay(1000)
