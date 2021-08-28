import pygame as pg
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import sys
from sys import exit


pg.init()
FPS = 30
clock = pg.time.Clock()


WINDOW_SIZE = (950, 700)
BACKGROUND = (200, 240, 255)
FONT18 = pg.font.SysFont('Calibri', 18)
FREQ = 26
BLOCK_SIZE = [400, 25]
BLOCK_IMAGE = './assets/block.jpg'
NOTE_IMAGE = './assets/note.jpg'
BACKGROUND_IM = './assets/paper.png'


bg_image = pg.transform.scale(pg.image.load(BACKGROUND_IM), WINDOW_SIZE)
play_flag = False
play_timer = 0
prog_arr = {}
play_sur: pg.Surface
screen: pg.display
pygame_flag = False
removing_arr = []
new_arr = {}
python_file: str
play_counter = 0


root = tk.Tk()
bg_color = 'azure'
root['bg'] = bg_color
finish_flag = False

lbl = tk.Label(root, anchor='w', text='Выберите уровень:', font='Times 14', bg=bg_color)
lbl.grid(row=0, column=0)

level1_btn = tk.Button(root, text='Уровень 1, вывод чисел на экран', font='Times 12', width=50,
                       command=lambda: select_level('./levels/level1.txt', 'level1.py'))
level1_btn.grid(row=1, column=0, padx=5, pady=10)

level2_btn = tk.Button(root, text='Уровень 2, нахождение остатка от деления', font='Times 12', width=50,
                       command=lambda: select_level('./levels/level2.txt', 'level2.py'))
level2_btn.grid(row=2, column=0, padx=5, pady=10)

level4_btn = tk.Button(root, text='Уровень 4, решение квадратного уравнения', font='Times 12', width=50,
                       command=lambda: select_level('./levels/level4.txt', 'level4.py'))
level4_btn.grid(row=4, column=0, padx=5, pady=10)

level3_btn = tk.Button(root, text='Уровень 3, работа со списком', font='Times 12', width=50,
                       command=lambda: select_level('./levels/level3.txt', 'level3.py'))
level3_btn.grid(row=3, column=0, padx=5, pady=10)


def select_level(level_text=None, level_script=None):
    global prog_arr, new_arr, removing_arr, python_file
    blocks.empty()
    fields.empty()
    new_arr = {}
    if level_text is None:
        level_text = fd.askopenfilename()
    if level_script is None:
        level_script = fd.askopenfilename()

    if level_text != '' and level_script != '':
        task = ''
        f = open(level_text, 'r')
        end_flag = False
        it = 0
        prog_arr.clear()
        for lines in f:
            if lines == '\n':
                end_flag = True
            if end_flag is False:
                task += lines
            else:
                if lines != 'def prog():\n' and lines != '\n':

                    prog_arr[it] = lines.replace('\n', '')
                    it += 1
        f.close()
        task = task[0:-1]
        removing_arr = sorted(prog_arr.values())
        python_file = level_script

        init_pygame_window(task)


def init_pygame_window(task):
    global play_sur, pygame_flag, screen, play_counter
    task = 'Задание:' + '\n' + task

    screen = pg.display.set_mode(WINDOW_SIZE)
    screen.blit(bg_image, (0, 0))

    # поле для отображения задания:
    task_sur = pg.transform.scale(pg.image.load(NOTE_IMAGE), (WINDOW_SIZE[0], WINDOW_SIZE[1]//5))
    # игровое поле:
    play_sur = pg.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]//5*4))
    play_sur.fill((220, 220, 255))
    # отрисовка задания:
    blit_text(task_sur, task, (20, 10), FONT18)
    screen.blit(task_sur, (0, 0))
    # отрисовка поля:
    screen.blit(play_sur, (0, WINDOW_SIZE[1] // 5))
    # создание полей для перетаскивания:
    for i in range(len(prog_arr)):
        fields.add(Field(30, BLOCK_SIZE[1]*i + 10, BLOCK_SIZE[0], BLOCK_SIZE[1], str(i)))

    pg.display.flip()
    play_counter = True
    pygame_flag = True


def blit_text(surface, text, pos, font, color=pg.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


class Field(pg.sprite.Sprite):  # класс поля для перетаскивания
    def __init__(self, x, y, width, height, num):
        pg.sprite.Sprite.__init__(self)
        surface = pg.Surface((width, height))
        surface.fill((255, 255, 255))
        pg.draw.rect(surface, (0, 0, 0), (0, 0, width, height), 1)
        blit_text(surface, str(num), (width//2 - len(num)*5, height//2 - 5), FONT18)
        self.image = surface
        self.rect = surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.number = num


class Block(pg.sprite.Sprite):  # класс блока, который падает
    def __init__(self, text: str, x, y):
        pg.sprite.Sprite.__init__(self)
        surface = pg.Surface((x, y))
        surface.fill((240, 220, 255))
        pg.draw.rect(surface, (0, 0, 0), (0, 0, x, y), 2)
        image = pg.transform.scale(pg.image.load(BLOCK_IMAGE), (x, y))
        # image.set_alpha(100)
        pg.draw.rect(image, (0, 0, 0), (0, 0, x, y), 2)
        blit_text(image, text, (5, 5), FONT18)
        self.image = image
        self.rect = image.get_rect()
        self.rect.bottom = 0
        self.rect.left = WINDOW_SIZE[0]-self.rect.width-20
        self.flag = True
        self.text = text
        self.dragging = False

    def fall(self):
        self.rect.bottom += 1

    def stop(self):
        self.flag = False

    def update(self):
        if self.rect.y >= WINDOW_SIZE[1]//5*4:
            self.rect.bottom = 0

        if self.flag is True:
            self.fall()


def move_coord(coords: tuple):
    lst = list(coords)
    lst[1] = lst[1] - WINDOW_SIZE[1] // 5
    return tuple(lst)


class Mouse:  # класс для работы с действиями мышью
    def __init__(self):
        self.clicked_block: Block = None
        self.clicked_pos = None

    def btn_down(self, pos):
        self.clicked_pos = pos
        if self.clicked_block is None:
            self.clicked_block = self.get_block(pos)
            if self.clicked_block is not None:
                self.clicked_block.stop()
                self.clicked_block.rect.center = pos

    def btn_up(self, pos):
        global new_arr, finish_flag

        upped: Field = self.get_field(pos)

        if self.clicked_block is not None and upped is not None:
            self.clicked_block.dragging = False
            field_took: Field = self.get_field(self.clicked_pos)
            cur_block = self.get_block(pos)
            if cur_block is None:

                if field_took is not None and int(field_took.number) in list(new_arr.keys()):
                    new_arr.pop(int(field_took.number))
                self.clicked_block.rect = upped.rect.copy()
                new_arr[int(upped.number)] = self.clicked_block.text
                self.clicked_block = None
                finish_flag = False
            elif field_took is not None:  # когда меняем местами
                cur_block.rect = field_took.rect.copy()
                self.clicked_block.rect = upped.rect.copy()
                new_arr[int(upped.number)] = self.clicked_block.text
                new_arr[int(field_took.number)] = cur_block.text
                self.clicked_block = None
                finish_flag = False
            else:  # когда сдвигаем вниз
                self.move_down(self.clicked_block, upped)
                self.clicked_block = None

        elif self.clicked_block is not None:
            self.clicked_block.dragging = False
            field_took: Field = self.get_field(self.clicked_pos)

            if pos[1] > 0:
                self.clicked_block.rect.center = pos
            else:
                self.clicked_block.rect.center = (pos[0], 0)
            self.clicked_block = None
            if field_took is not None and int(field_took.number) in list(new_arr.keys()):
                new_arr.pop(int(field_took.number))
            finish_flag = False

    def drag(self, pos):
        if self.clicked_block is not None and pos[1] > 0:
            self.clicked_block.rect.center = pos
            self.clicked_block.dragging = True

    def get_block(self, pos):
        for cur_sprite in blocks:
            if cur_sprite.rect.collidepoint(pos) and self.clicked_block != cur_sprite:
                return cur_sprite
        return None

    def get_field(self, pos):
        for cur_sprite in fields:
            if cur_sprite.rect.collidepoint(pos):
                return cur_sprite
        return None

    def move_down(self, block, field):
        next_field: Field = self.get_field((field.rect.center[0], field.rect.center[1] + BLOCK_SIZE[1]))
        next_block: Block = self.get_block((field.rect.center[0], field.rect.center[1] + BLOCK_SIZE[1]))
        cur_block: Block = self.get_block(field.rect.center)
        block.rect = field.rect.copy()
        new_arr[int(field.number)] = block.text

        if next_field:
            if next_block is None:
                cur_block.rect.y += BLOCK_SIZE[1]
                new_arr[int(next_field.number)] = cur_block.text
            else:
                self.move_down(cur_block, next_field)
        else:
            cur_block.rect.y += BLOCK_SIZE[1]+10


def level_pass():
    global pygame_flag
    sys.path.append('./levels')
    messagebox.showinfo('message', 'Congratulation! Now click "OK" and check program work in your console!')
    m_name = python_file[python_file.rfind('/') + 1:-3]
    module = __import__(m_name)
    module.prog()


def level_not_pass():
    messagebox.showerror('message', 'Wrong! Please try again!')


def screen_update():
    play_sur.blit(bg_image, (0, 0))
    blocks.update()
    fields.update()
    fields.draw(play_sur)
    blocks.draw(play_sur)
    pg.draw.rect(play_sur, (0, 0, 0), (WINDOW_SIZE[0] - BLOCK_SIZE[0] -
                                       30, 0, BLOCK_SIZE[0]+20, WINDOW_SIZE[1]//5*4), 1)
    pg.draw.rect(play_sur, (0, 0, 0), (0, 0, WINDOW_SIZE[0], WINDOW_SIZE[1]//5*4), 1)
    pg.draw.rect(play_sur, (0, 0, 0), (WINDOW_SIZE[0] - BLOCK_SIZE[0] - 39, 0, 10, WINDOW_SIZE[1]//5*4), 1)
    screen.blit(play_sur, (0, WINDOW_SIZE[1] // 5))


blocks = pg.sprite.Group()
fields = pg.sprite.Group()
mouse = Mouse()

while True:
    clock.tick(FPS)
    try:
        root.update()
    except:
        exit()
    if pygame_flag:

        if play_counter:    # если игра запущена
            if play_counter == FREQ:
                play_counter = 0

                if len(removing_arr) != 0:
                    line = removing_arr[0]
                    removing_arr.pop(0)
                    blocks.add(Block(line, BLOCK_SIZE[0], BLOCK_SIZE[1]))
            play_counter += 1

        screen_update()
        pg.display.flip()
        sprite: Block
        for sprite in blocks:
            if sprite.dragging:
                play_sur.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
                screen.blit(play_sur, (0, WINDOW_SIZE[1] // 5))

        pg.display.flip()
        if len(new_arr) == len(prog_arr):

            if new_arr == prog_arr:
                pygame_flag = False
                level_pass()
                pg.display.quit()
                continue

            elif not finish_flag:
                level_not_pass()
                finish_flag = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.display.quit()
                pygame_flag = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse.btn_down(move_coord(event.pos))
            if event.type == pg.MOUSEBUTTONUP:
                mouse.btn_up(move_coord(event.pos))
            if event.type == pg.MOUSEMOTION:
                mouse.drag(move_coord(event.pos))
