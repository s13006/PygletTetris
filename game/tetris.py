import pyglet
import random

window = pyglet.window.Window(320, 640)
BACKGROUND = pyglet.resource.image('fonas.png')
block = pyglet.resource.image('plyta.png')

BLOCK_HEIGHT = 32
BLOCK_WIDTH = 32

TETROMINOS = [
        [(0, 1), (1, 1), (1, 0), (2, 0)], #Z
        [(0, 0), (1, 0), (1, 1), (2, 1)], #S
        [(0, 0), (1, 0), (2, 0), (1, 1)], #T
        [(0, 1), (0, 0), (1, 0), (2, 0)], #J
        [(0, 0), (1, 0), (2, 0), (2, 1)], #L
        [(0, 0), (1, 0), (0, 1), (1, 1)], #O
        [(0, 0), (1, 0), (2, 0), (3, 0)]  #I
]

#XY
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SULINYS = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

SCORE = 0

#座標
HEAVEN = (4, 18)

current_block = 0
unit_location = (0, 0)
block_angle = 0

def new_block():
        global current_block, unit_location, block_angle
        current_block = random.randint(0, 6)
        unit_location = HEAVEN
        block_angle = 0

def game_over():
    global SULINYS, SCORE
    SULINYS = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    SCORE = 0

def draw_block(blocks):
    for p in blocks:
            block.blit(BLOCK_WIDTH * p[0], BLOCK_HEIGHT * p[1])

def pies_sulina(sulinys):
    for y, prompt in enumerate(sulinys):
        for x, w in enumerate(prompt):
            if w == 1:
                block.blit(x * BLOCK_WIDTH, y * BLOCK_HEIGHT)

def rotate_block(block, angle):
    if angle % 4 == 0:
        return block
    return rotate_block([(1-y, x) for (x, y) in block], angle - 1)

def creep_block(block, poslinkis):
    return [(x + poslinkis[0], y + poslinkis[1]) for (x, y) in block]

def block_move(block, angle, poslinkis):
    return creep_block(rotate_block(block, angle), poslinkis)

def with_space(sulinys, block):
    for p in block:
        if p[1] >= BOARD_HEIGHT:
            continue
        if p[1] < 0 or p[0] < 0 or p[0] >= BOARD_WIDTH:
            return False
        if sulinys[p[1]][p[0]] == 1:
            return False
    return True

def imprinted(sulinys, block):
        for p in block:
                sulinys[p[1]][p[0]] = 1

def delete_lines():
        global SULINYS, SCORE
        i = 0
        while i < len(SULINYS):
                if SULINYS[i] == [1] * BOARD_WIDTH:
                        SULINYS = SULINYS[:i] + SULINYS[i+1:] + [[0] * BOARD_WIDTH]
                        SCORE += 1
                        print(SCORE)
                else:
                        i += 1

def kristi(dt):
        global unit_location
        new_place = (unit_location[0], unit_location[1] - 1)
        if with_space(SULINYS, block_move(
                TETROMINOS[current_block], block_angle, new_place)):
                        unit_location = new_place
        else:
                imprinted(SULINYS, block_move(
                        TETROMINOS[current_block], block_angle, unit_location))
                if unit_location[1] >= 18:
                    game_over()
                delete_lines()
                print(unit_location)
                new_block()

pyglet.clock.schedule_interval(kristi, 1.0)

@window.event
def on_draw():
        window.clear()
        BACKGROUND.blit(0, 0)
        draw_block(block_move(TETROMINOS[current_block],
                block_angle, unit_location))
        pies_sulina(SULINYS)
        score_label = pyglet.text.Label(
            text="Score : " + str(SCORE),
            x = 10, y = 10,
            color = (0, 0, 0, 255)
            ,font_size = 20)
        score_label.draw()

@window.event
def on_key_press(simbolis, _):
        global unit_location, block_angle
        from pyglet.window import key
        new_place = unit_location
        new_angle = block_angle
        if simbolis == key.LEFT:
                new_place = (unit_location[0] - 1, unit_location[1])
        if simbolis == key.RIGHT:
                new_place = (unit_location[0] + 1, unit_location[1])
        if simbolis == key.SPACE:
                new_angle += 1
        if simbolis == key.DOWN:
                new_place = (unit_location[0], unit_location[1] - 1)
                if with_space(SULINYS, block_move(
                        TETROMINOS[current_block], block_angle, new_place)):
                        unit_location = new_place
                        new_place = (unit_location[0], unit_location[1])
        if simbolis == key.UP:
                while with_space(SULINYS, block_move(TETROMINOS[current_block], block_angle, new_place)):
                        unit_location = new_place
                        new_place = (unit_location[0], unit_location[1] - 1)

        if with_space(SULINYS, block_move(
                TETROMINOS[current_block], new_angle, new_place)):
                unit_location = new_place
                block_angle = new_angle


if __name__ == '__main__':
    new_block()
pyglet.app.run()