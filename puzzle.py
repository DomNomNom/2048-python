import sys
isPython2 = sys.version_info[0] == 2
if isPython2:
    from Tkinter import *
else:
    from tkinter import *
import game_logic
from mutable_game_model import GameModel
import random

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {   2:"#eee4da", 4:"#ede0c8", 8:"#f2b179", 16:"#f59563", \
                            32:"#f67c5f", 64:"#f65e3b", 128:"#edcf72", 256:"#edcc61", \
                            512:"#edc850", 1024:"#edc53f", 2048:"#edc22e" , 4096:"#edc22e", 8192:"#edc22e", 16384:"#edc22e", 32768:"#edc22e", 65536:"#edc22e"}
CELL_COLOR_DICT = { 2:"#776e65", 4:"#776e65", 8:"#f9f6f2", 16:"#f9f6f2", \
                    32:"#f9f6f2", 64:"#f9f6f2", 128:"#f9f6f2", 256:"#f9f6f2", \
                    512:"#f9f6f2", 1024:"#f9f6f2", 2048:"#f9f6f2" , 4096:"#f9f6f2", 8192:"#f9f6f2", 16384:"#f9f6f2", 32768:"#f9f6f2", 65536:"#f9f6f2"}
GAME_OVER_TEXT_COLOR = "#ede0c8"
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"


class GameGrid(Frame):
    def __init__(self, is_ai_game=False, seed = None, showGUI = True):
        if seed is None:
            seed = [ random.choice(game_logic.all_directions) for i in range(17) ]
        self.game_model = GameModel(seed)
        self.GUImode = showGUI

        self.endless_mode = True
        self.grid_cells = []

        if self.GUImode:
            Frame.__init__(self)
            # for widget in self.master.winfo_children():
            #     if widget is not self:
            #         widget.destroy()
            self.grid(row=0, column=len(self.master.winfo_children()))
            self.master.title('2048')
            self.master.bind("<Escape>", lambda x: sys.exit())
            self.master.bind("<Return>", lambda x: sys.exit())
            if not is_ai_game:
                self.master.bind("<Key>", self.key_down)

            self.init_grid()
            self.redraw()


        if not is_ai_game:
            self.mainloop()

    def init_grid(self):
        game_and_score = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        game_and_score.grid()

        background = Frame(game_and_score, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid(row=1, column=0)
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE/GRID_LEN, height=SIZE/GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

        # background2 = Frame(self, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE, height=SIZE)
        # background2.grid()
        # self.scoreLabel = Label(master=background2, text="HELLO", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=SIZE, height=2)
        # self.scoreLabel.grid(row=1, column=1)
        self.scoreLabel = Label(master=game_and_score, text="2048", bg=BACKGROUND_COLOR_GAME, fg=GAME_OVER_TEXT_COLOR, justify=CENTER, font=FONT, width=18 , height=2)
        self.scoreLabel.grid(row=0, column=0)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                number = self.game_model.mat[i][j]
                if number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(number), bg=BACKGROUND_COLOR_DICT[number], fg=CELL_COLOR_DICT[number])
        self.update_idletasks()

    def key_down(self, event):
        if event.keycode in [38, 87]: self.game_model.do_swipe(game_logic.dir_up)
        if event.keycode in [40, 83]: self.game_model.do_swipe(game_logic.dir_down)
        if event.keycode in [37, 65]: self.game_model.do_swipe(game_logic.dir_left)
        if event.keycode in [39, 68]: self.game_model.do_swipe(game_logic.dir_right)
        self.redraw()

    def ai_move(self, direction):
        old_mat = self.game_model.mat
        new_mat = self.game_model.do_swipe(direction)

        if self.GUImode:
            self.redraw()
        return old_mat != new_mat

    def redraw(self):

        self.update_grid_cells()

        status_text = ''
        if game_state(self.game_model.mat, self.endless_mode)=='win':
            status_text += "You Win!\n"
        if game_state(self.game_model.mat, self.endless_mode)=='lose':
            status_text += "Game Over.\n"
        status_text += 'Score: ' + str(self.calc_score())
        self.scoreLabel.configure(text = status_text)




    def calc_score(self):
        """ calculated the score
        Adds scores if each cell, where each cell has a score according to:
        2 -> 3
        4 -> 9
        8 -> 27
        ...
        """
        return game_logic.score(self.game_model.mat)

    def game_over(self):
        if game_state(self.game_model.mat, self.endless_mode)=='not over': return False
        else: return True

def game_state(mat, endless_mode = True):
    if not endless_mode:
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j]==2048:
                    return 'win'
    for i in range(len(mat)-1): #intentionally reduced to check the row on the right and below
        for j in range(len(mat[0])-1): #more elegant to use exceptions but most likely this will be their solution
            if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                return 'not over'
    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                return 'not over'
    for k in range(len(mat)-1): #to check the left/right entries on the last row
        if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1): #check up/down entries on last column
        if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'

if __name__ == '__main__':
    gamegrid = GameGrid()
