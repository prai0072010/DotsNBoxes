from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import time
import Minimax
import MinimaxPruning

class DotsNBoxes():
    size_of_board = 600
    number_of_dots = 4
    symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
    symbol_thickness = 50
    images = []
    dot_color = '#7BC043'
    player_color = '#0492CF'
    player_color_light = '#67B0CF'
    computer_color = '#FF6522'
    computer_color_light = '#FFA882'
    Green_color = '#7BC043'
    dot_width = 0.25*size_of_board/number_of_dots
    edge_width = 0.1*size_of_board/number_of_dots
    distance_between_dots = size_of_board / (number_of_dots)
    minimax_depth = 6
    # minimax_depth = round((((number_of_dots-1)**2)/2)+1)

    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('DotsNBoxes')
        self.canvas = Canvas(self.window, width=self.size_of_board, height=self.size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player_starts = False
        self.refresh_board()
        self.play_again()
        print("minimax_depth: ", self.minimax_depth)

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(self.number_of_dots - 1, self.number_of_dots - 1))
        self.row_status = np.zeros(shape=(self.number_of_dots, self.number_of_dots - 1))
        self.col_status = np.zeros(shape=(self.number_of_dots - 1, self.number_of_dots))

        self.move_log = ''
        self.player_score = 0
        self.computer_score = 0
        
        # Input from user in form of clicks
        # self.player_starts = not self.player_starts
        self.player_turn = not self.player_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()

    # # ------------------------------------------------------------------
    # # Logical Functions:
    # # The modules required to carry out game logic
    # # ------------------------------------------------------------------

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position-self.distance_between_dots/4)//(self.distance_between_dots/2)
        
        axis = False
        logical_position = []
        if np.any(position < 0):
            return logical_position, axis
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            c = int((position[0]-1)//2)
            r = int(position[1]//2)
            logical_position = [r, c]
            axis = 'row'
            
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            r = int((position[1] - 1) // 2)
            c = int(position[0] // 2)
            logical_position = [r, c]
            axis = 'col'

        return logical_position, axis
    
    def is_grid_occupied(self, logical_position, axis):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if axis == 'row' and self.row_status[r][c] == 0:
            occupied = False
        if axis == 'col' and self.col_status[r][c] == 0:
            occupied = False

        return occupied
    
    def update_board(self, axis, logical_position):
        r = logical_position[0]
        c = logical_position[1]

        if r < (self.number_of_dots-1) and c < (self.number_of_dots-1):
            self.board_status[r][c] += 1

        if axis == 'row':
            self.row_status[r][c] = 1
            if r >= 1:
                self.board_status[r-1][c] += 1

        elif axis == 'col':
            self.col_status[r][c] = 1
            if c >= 1:
                self.board_status[r][c-1] += 1

    def mark_box(self):
        is_score = False
        if self.player_turn:
            color = self.player_color_light
        else:
            color = self.computer_color_light
        
        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                self.shade_box(box, color)
                score_row, score_col = box
                if self.player_turn:
                    self.player_score += 1
                    self.board_status[score_row][score_col] = -4
                else:
                    self.computer_score += 1
                is_score = True
                
        return is_score

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # # ------------------------------------------------------------------
    # # Drawing Functions:
    # # The modules required to draw required game based object on canvas
    # # ------------------------------------------------------------------

    def make_edge(self, axis, logical_position):
        if axis == 'row':
            start_x = self.distance_between_dots/2 + logical_position[1]*self.distance_between_dots
            end_x = start_x+self.distance_between_dots
            start_y = self.distance_between_dots/2 + logical_position[0]*self.distance_between_dots
            end_y = start_y
        elif axis == 'col':
            start_y = self.distance_between_dots / 2 + logical_position[0] * self.distance_between_dots
            end_y = start_y + self.distance_between_dots
            start_x = self.distance_between_dots / 2 + logical_position[1] * self.distance_between_dots
            end_x = start_x

        if self.player_turn:
            color = self.player_color
        else:
            color = self.computer_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.edge_width)

    def display_gameover(self):

        if self.player_score > self.computer_score:
            text = 'Winner: Player '
            color = self.player_color
        elif self.computer_score > self.player_score:
            text = 'Winner: Computer '
            color = self.computer_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete(self.turntext_handle)

        self.create_rectangle(0, 0, self.size_of_board, self.size_of_board, fill='gray', alpha=.8)

        self.canvas.create_text(self.size_of_board / 2, self.size_of_board / 4, font="cmr 40 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.size_of_board / 2, 5 * self.size_of_board / 8, font="cmr 40 bold", fill=self.Green_color,
                                text=score_text)

        score_text = 'Player : ' + str(self.player_score) + '\n'
        score_text += 'Computer : ' + str(self.computer_score) + '\n'
        self.canvas.create_text(self.size_of_board / 2, 3 * self.size_of_board / 4, font="cmr 30 bold", fill=self.Green_color,
                                text=score_text)

        text = 'Click to play again \n'
        self.canvas.create_text(self.size_of_board / 2, 15 * self.size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=text)
        
        self.reset_board = True
        
    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.window.winfo_rgb(fill) + (alpha,)
            image = Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.images.append(ImageTk.PhotoImage(image))
            self.canvas.create_image(x1, y1, image=self.images[-1], anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

    def refresh_board(self):
        for i in range(self.number_of_dots):
            x = i*self.distance_between_dots+self.distance_between_dots/2
            self.canvas.create_line(x, self.distance_between_dots/2, x,
                                    self.size_of_board-self.distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(self.distance_between_dots/2, x,
                                    self.size_of_board-self.distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(self.number_of_dots):
            for j in range(self.number_of_dots):
                start_x = i*self.distance_between_dots+self.distance_between_dots/2
                end_x = j*self.distance_between_dots+self.distance_between_dots/2
                self.canvas.create_oval(start_x-self.dot_width/2, end_x-self.dot_width/2, start_x+self.dot_width/2,
                                        end_x+self.dot_width/2, fill=self.dot_color,
                                        outline=self.dot_color)

    def shade_box(self, box, color):
        start_x = self.distance_between_dots / 2 + box[1] * self.distance_between_dots + self.edge_width/2
        start_y = self.distance_between_dots / 2 + box[0] * self.distance_between_dots + self.edge_width/2
        end_x = start_x + self.distance_between_dots - self.edge_width
        end_y = start_y + self.distance_between_dots - self.edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def display_turn_text(self):
        text = 'Turn: '
        if self.player_turn:
            text += 'Player'
            color = self.player_color
        else:
            text += 'Computer..'
            color = self.computer_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(10*len(text),
                                                       self.size_of_board-self.distance_between_dots/8,
                                                       font="cmr 15 bold",text=text, fill=color)

    def write_game_log(self):
        lines = self.move_log.split('\n')
        player_text = '\n'.join([line for line in lines if 'player' in line.lower()])
        computer_text = '\n'.join([line for line in lines if 'computer' in line.lower()])
        seperate_line = f"\n{'-'*25}\n"
        with open('last_game_log.txt', 'w') as file:
            log_text = "Summary\n" + \
                        self.move_log +\
                        seperate_line +\
                        "Player\n" +\
                        player_text +\
                        seperate_line +\
                        "Computer\n" +\
                        computer_text
            file.write(log_text)

    def board_process(self, axis, logical_positon, process_time=None):
        if (axis and not self.is_grid_occupied(logical_positon, axis)):
            self.update_board(axis, logical_positon)
            self.make_edge(axis, logical_positon)
            is_score = self.mark_box()
            self.refresh_board()

            if self.player_turn:
                self.move_log += f"player: {(axis, logical_positon)}\n"
            else:
                self.move_log += f"computer: {(axis, logical_positon)} in {process_time} s\n"

            if is_score:
                self.player_turn = self.player_turn
            else:
                self.move_log += "\n"
                self.player_turn = not self.player_turn
            
            self.display_turn_text()
            
            if self.is_gameover():
                self.write_game_log()
                time.sleep(0.3)
                self.display_gameover()

    def click(self, event):
        if not self.reset_board:
            if self.player_turn:
                grid_position = [event.x, event.y]
                logical_positon, axis = self.convert_grid_to_logical_position(grid_position)
                self.board_process(axis, logical_positon)
            
            self.window.after(1, self.ai_move)
            
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def ai_move(self):
        if not self.reset_board:
            if not self.player_turn:
                start_time = time.time()
                # ans = Minimax.mini_max(self.row_status.copy(), self.col_status.copy(), self.board_status.copy(), self.already_marked_boxes.copy(), self.minimax_depth)
                ans = MinimaxPruning.mini_max(self.row_status.copy(), self.col_status.copy(), self.board_status.copy(), self.already_marked_boxes.copy(), self.minimax_depth)
                # ans = ParallelMinimax.mini_max(self.row_status.copy(), self.col_status.copy(), self.board_status.copy(), self.already_marked_boxes.copy(), self.minimax_depth)
                process_time = round((time.time() - start_time), 2)
                print(f"Answer: {ans} in {process_time} seconds")
                axis, r, c = ans
                logical_positon = [r, c]
                self.board_process(axis, logical_positon, process_time)
                time.sleep(0.3)
                self.window.after(1, self.ai_move)

game_instance = DotsNBoxes()
game_instance.mainloop()