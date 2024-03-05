
import pygame
import sys
from pygame.locals import *

# 颜色常量
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 错误码
G_POS_PLACED = -4
G_RANGE_ERR = -3
G_STAT_ERR = -2
G_ERR = -1
G_OK = 0
G_FINISH = 1
G_WIN = 2


class GoBang:
    def __init__(self, map_size=16):
        self.map_size = map_size
        # map_size * map_size
        # 0: none， 1: black，-1: white
        self.map = [[0 for y in range(0, map_size)] for x in range(0, map_size)]

        self.move_stack = []

        self.status = 0
        self.winner = 0

    def start_move(self):
        self.status = 1

    def get_last_move(self):
        return self.move_stack[-1]

    def get_winner(self):
        return self.winner

    def get_steps(self):
        return len(self.move_stack)


    def __check_winner_(self):
        tmp = 0
        last_step = self.move_stack[-1]
        # column
        for y in range(0, self.map_size):
            # continuity
            if y > 0 \
                    and self.map[last_step[1]][y] != self.map[last_step[1]][y - 1]:
                tmp = 0
            tmp += self.map[last_step[1]][y]
            if abs(tmp) >= 5:
                return last_step[0]

        # line
        tmp = 0
        for x in range(0, self.map_size):
            # continuity
            if x > 0 \
                    and self.map[x][last_step[2]] != self.map[x - 1][last_step[2]]:
                tmp = 0
            tmp += self.map[x][last_step[2]]
            if abs(tmp) >= 5:
                return last_step[0]

        # /
        tmp = 0
        min_dist = min(last_step[1], last_step[2])
        top_point = [last_step[1] - min_dist, last_step[2] - min_dist]
        for incr in range(0, self.map_size):
            # border
            if top_point[0] + incr > self.map_size - 1 \
                    or top_point[1] + incr > self.map_size - 1:
                break
            # continuity
            if incr > 0 \
                    and self.map[top_point[0] + incr][top_point[1] + incr] \
                    != self.map[top_point[0] + incr - 1][top_point[1] + incr - 1]:
                tmp = 0
            tmp += self.map[top_point[0] + incr][top_point[1] + incr]
            if abs(tmp) >= 5:
                return last_step[0]

        # \
        tmp = 0
        min_dist = min(self.map_size - 1 - last_step[1], last_step[2])
        top_point = [last_step[1] + min_dist, last_step[2] - min_dist]
        for incr in range(0, self.map_size):
            # border
            if top_point[0] - incr < 0 \
                    or top_point[1] + incr > self.map_size - 1:
                break
            # continuity
            if incr > 0 \
                    and self.map[top_point[0] - incr][top_point[1] + incr] \
                    != self.map[top_point[0] - incr + 1][top_point[1] + incr - 1]:
                tmp = 0
            tmp += self.map[top_point[0] - incr][top_point[1] + incr]
            if abs(tmp) >= 5:
                return last_step[0]

        return 0

    # end
    def __check_(self):
        # all steps are placed
        if len(self.move_stack) >= self.map_size ** 2:
            return G_FINISH
        # win
        winner = self.__check_winner_()
        if winner != 0:
            self.winner = winner
            return G_WIN
        # unfinished
        return G_OK

    # one move
    def move(self, x, y):
        if self.status != 1 and self.status != 2:
            return G_STAT_ERR
        if self.map_size <= x or x < 0 \
                or self.map_size <= y or y < 0:
            return G_RANGE_ERR
        if self.map[x][y] != 0:
            return G_POS_PLACED

        t = 1 if self.status == 1 else -1
        self.map[x][y] = t
        self.move_stack.append((t, x, y))

        # end
        ret = self.__check_()
        if self.is_finish(ret):
            if ret == G_WIN:
                self.__set_status(3)
            else:
                self.__set_status(4)
            return ret

        # swap
        last_step = self.move_stack[-1]
        stat = 2 if last_step[0] == 1 else 1
        self.__set_status(stat)
        return G_OK

    def __set_status(self, stat):
        self.status = stat

    def is_finish(self, err_code):
        if err_code == G_FINISH \
                or err_code == G_WIN:
            return True
        return False



    # get status
    # 0: not start
    # 1: waiting for black
    # 2: waiting for white
    # 3: end (win)
    # 4: end (draw)
    def get_status(self):
        return self.status

    def get_move_stack(self):
        return self.move_stack


class TigerGoBang(GoBang):
    def __init__(self, map_size=16, map_unit=40):
        self.SIZE = map_size
        self.UNIT = map_unit
        self.TITLE = 'GoBang'
        self.PANEL_WIDTH = 200
        self.BORDER_WIDTH = 50


        self.RANGE_X = [self.BORDER_WIDTH, self.BORDER_WIDTH + (self.SIZE - 1) * self.UNIT]
        self.RANGE_Y = [self.BORDER_WIDTH, self.BORDER_WIDTH + (self.SIZE - 1) * self.UNIT]


        self.PANEL_X = [self.BORDER_WIDTH + (self.SIZE - 1) * self.UNIT, \
                        self.BORDER_WIDTH + (self.SIZE - 1) * self.UNIT + self.PANEL_WIDTH]
        self.PANEL_Y = [self.BORDER_WIDTH, self.BORDER_WIDTH + (self.SIZE - 1) * self.UNIT]


        self.WINDOW_WIDTH = self.BORDER_WIDTH * 2 \
                            + self.PANEL_WIDTH \
                            + (self.SIZE - 1) * self.UNIT
        self.WINDOW_HEIGHT = self.BORDER_WIDTH * 2 \
                             + (self.SIZE - 1) * self.UNIT


        super(TigerGoBang, self).__init__(map_size=map_size)

        self.__game_init_()


    def __draw_map(self):

        POS_START = [self.BORDER_WIDTH, self.BORDER_WIDTH]

        s_font = pygame.font.SysFont('arial', 16)
        # line
        for item in range(0, self.SIZE):
            pygame.draw.line(self.screen, BLACK,
                             [POS_START[0], POS_START[1] + item * self.UNIT],
                             [POS_START[0] + (self.SIZE - 1) * self.UNIT, POS_START[1] + item * self.UNIT],
                             1)
            s_surface = s_font.render(f'{item + 1}', True, BLACK)
            self.screen.blit(s_surface, [POS_START[0] - 30, POS_START[1] + item * self.UNIT - 10])

        # column
        for item in range(0, self.SIZE):
            pygame.draw.line(self.screen, BLACK,
                             [POS_START[0] + item * self.UNIT, POS_START[1]],
                             [POS_START[0] + item * self.UNIT, POS_START[1] + (self.SIZE - 1) * self.UNIT],
                             1)
            s_surface = s_font.render(chr(ord('A') + item), True, BLACK)
            self.screen.blit(s_surface, [POS_START[0] + item * self.UNIT - 5, POS_START[1] - 30])

    # chess
    def __draw_chess(self):
        mst = self.get_move_stack()
        for item in mst:
            x = self.BORDER_WIDTH + item[1] * self.UNIT
            y = self.BORDER_WIDTH + item[2] * self.UNIT
            t_color = BLACK if item[0] == 1 else WHITE
            pygame.draw.circle(self.screen, t_color, [x, y], int(self.UNIT / 2.5))


    def __redraw_all(self):

        self.screen.blit(pygame.image.load(r"bg.jpg"), (0, 0))

        self.__draw_map()

        self.__draw_chess()

        self.__draw_panel_()

    def __game_init_(self):

        pygame.init()

        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        pygame.display.set_caption(self.TITLE)

        background = pygame.image.load(r"bg.jpg")
        self.screen.blit(background, (0, 0))

        self.__draw_map()

        self.__draw_panel_()

    def __draw_panel_(self):

        pygame.draw.rect(self.screen, WHITE,
                         [self.PANEL_X[0] + 30, 0,
                          1000, 1000])

        self.panel_font = pygame.font.SysFont('simhei', 20)


        stat = self.get_status()
        if stat == 0:
            stat_str = 'Start'
        elif stat == 1:
            stat_str = 'Awaiting Black Move..'
        elif stat == 2:
            stat_str = 'Awaiting White Move..'
        elif stat == 4:
            stat_str = 'End!'
        elif stat == 3:
            winner = self.get_winner()
            if winner == 1:
                stat_str = 'Black Win!'
            else:
                stat_str = 'White Win!'
        else:
            stat_str = ''
        self.surface_stat = self.panel_font.render(stat_str, False, BLACK)
        self.screen.blit(self.surface_stat, [self.PANEL_X[0] + 50, self.PANEL_Y[0] + 50])


        steps = self.get_steps()
        self.surface_steps = self.panel_font.render(f'Step: {steps}', False, BLACK)
        self.screen.blit(self.surface_steps, [self.PANEL_X[0] + 50, self.PANEL_Y[0] + 150])

        # new game
        offset_x = self.PANEL_X[0] + 50
        offset_y = self.PANEL_Y[0] + 400
        btn_h = 50
        btn_w = 150
        btn_gap = 20
        btn_text_x = 35
        btn_text_y = 15
        self.BTN_RANGE_NEW_START_X = [offset_x, offset_x + btn_w]
        self.BTN_RANGE_NEW_START_Y = [offset_y, offset_y + btn_h]
        pygame.draw.rect(self.screen, BLACK,
                         [offset_x, offset_y,
                          btn_w, btn_h])
        self.surface_btn = self.panel_font.render(f'New Game', False, WHITE)
        self.screen.blit(self.surface_btn, [offset_x + btn_text_x, offset_y + btn_text_y])

        # exit game
        self.BTN_RANGE_EXIT_GAME_X = [offset_x, offset_x + btn_w]
        self.BTN_RANGE_EXIT_GAME_Y = [offset_y + btn_h + btn_gap,
                                      offset_y + btn_h + btn_gap + btn_h]
        pygame.draw.rect(self.screen, BLACK,
                         [offset_x, offset_y + btn_h + btn_gap,
                          btn_w, btn_h])
        self.surface_btn = self.panel_font.render(f'Exit Game', False, WHITE)
        self.screen.blit(self.surface_btn,
                         [offset_x + btn_text_x, offset_y + btn_h + btn_gap + btn_text_y])


    def __do_move_(self, pos):

        if pos[0] < self.RANGE_X[0] or pos[0] > self.RANGE_X[1] \
                or pos[1] < self.RANGE_Y[0] or pos[1] > self.RANGE_Y[1]:

            return G_ERR

        s_x = round((pos[0] - self.BORDER_WIDTH) / self.UNIT)
        s_y = round((pos[1] - self.BORDER_WIDTH) / self.UNIT)
        x = self.BORDER_WIDTH + self.UNIT * s_x
        y = self.BORDER_WIDTH + self.UNIT * s_y

        ret = self.move(s_x, s_y)
        if ret < 0:

            return G_ERR
        # draw
        last_move = self.get_last_move()
        t_color = BLACK if last_move[0] == 1 else WHITE
        pygame.draw.circle(self.screen, t_color, [x, y], int(self.UNIT / 2.5))
        # pygame.draw.circle(self.screen, BLACK, [x, y], int(self.UNIT / 2.5), 1)

        self.__draw_panel_()

        return G_OK



    def __do_new_start(self):
        self.__init__()
        self.start()

    def __do_btn_(self, pos):
        if self.BTN_RANGE_NEW_START_X[0] < pos[0] < self.BTN_RANGE_NEW_START_X[1] \
                and self.BTN_RANGE_NEW_START_Y[0] < pos[1] < self.BTN_RANGE_NEW_START_Y[1]:
            self.__do_new_start()
            return G_OK
        elif self.BTN_RANGE_EXIT_GAME_X[0] < pos[0] < self.BTN_RANGE_EXIT_GAME_X[1] \
                and self.BTN_RANGE_EXIT_GAME_Y[0] < pos[1] < self.BTN_RANGE_EXIT_GAME_Y[1]:
            sys.exit()
        else:
            return G_ERR

    def start(self):
        self.start_move()
        self.__draw_panel_()
        while True:

            for event in pygame.event.get():

                if event.type == QUIT:

                    pygame.quit()

                    sys.exit()

                if event.type == MOUSEBUTTONUP:
                    if self.__do_btn_(event.pos) < 0:

                        self.__do_move_(event.pos)

            pygame.display.update()


if __name__ == '__main__':
    inst1 = TigerGoBang(map_unit=40)
    inst1.start()
