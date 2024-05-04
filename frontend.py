import backend
import sys
import time
import random
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image


class Front(object):
    def __init__(self, w, speed=0, length=0, start_time=0, start_play2=True, game_over=False, ai=False):
        # Connect with BackEnd
        self.bk = backend.Back()

        # Initiate Params
        self.speed = speed
        self.length = length
        self.start_time = start_time
        self.start_play2 = start_play2
        self.game_over = game_over
        self.ai = ai

        # Define Colors
        self.bg_color = "#85A7B4"
        self.wall_color = "#313331"
        self.path_color = "#746944"
        self.btn_color = "#5D6568"
        self.font_color = "#B9D7C4"

        # Define Fonts
        self.font_title = font.Font(family='Impact', size=20)
        self.font_body = font.Font(family='Impact', size=14)

        # Add window properties
        self.window = w
        self.window.title("Traffic Tango Game")
        self.window.geometry("925x600")
        self.window.resizable(0, 0)

        # Create main frame
        self.mainframe = tk.Frame(master=window, bg=self.bg_color)
        self.mainframe.pack_propagate(0)
        self.mainframe.pack(fill=tk.BOTH, expand=1)

        # Create Race Track Canvas
        self.racetrack = tk.Canvas(self.mainframe, width=500, height=550, bg=self.path_color, highlightthickness=0)
        self.racetrack.grid(row=0, column=0, rowspan=8, padx=(25, 25), pady=(25, 0))

        # Create Player Car
        car_size = 100, 100
        player_png = Image.open("img/player_car.png")
        player_png.thumbnail(car_size)
        self.player_img = ImageTk.PhotoImage(player_png)
        self.player_car = self.racetrack.create_image(250, 495, image=self.player_img)
        self.upper_lim = 445

        # Create Obstacles
        obstacle_png = Image.open("img/obstacle_car.png")
        obstacle_png.thumbnail(car_size)
        self.obstacle_img = ImageTk.PhotoImage(obstacle_png)
        self.obstacle_car = self.racetrack.create_image(25, -50, image=self.obstacle_img)
        self.obstacle_car2 = self.racetrack.create_image(475, 600, image=self.obstacle_img)

        # --Create Settings Panel--
        # Instructions
        self.instructions = tk.Button(self.mainframe, text="INSTRUCTIONS", command=self.show_instructions)
        self.instructions.config(font=self.font_body, bg=self.btn_color, fg=self.font_color,
                                 disabledforeground=self.font_color)
        self.instructions.grid(row=0, column=1, columnspan=6, pady=(25, 0))

        # Modes: User or Computer AI
        self.mode_lb = tk.Label(self.mainframe, text="MODE", bg=self.bg_color, fg=self.btn_color)
        self.mode_lb.config(font=self.font_title)
        self.mode_lb.grid(row=1, column=1, columnspan=6, pady=(25, 0))

        self.user_btn = tk.Button(self.mainframe, text="USER", command=self.play_user, font=self.font_body)
        self.user_btn.config(bg=self.btn_color, fg=self.font_color, width=15, disabledforeground=self.font_color)
        self.user_btn.grid(row=2, column=1, columnspan=3, padx=(15, 5), pady=(5, 5))

        self.comp_btn = tk.Button(self.mainframe, text="COMPUTER", command=self.play_comp, font=self.font_body)
        self.comp_btn.config(bg=self.btn_color, fg=self.font_color, width=15, disabledforeground=self.font_color)
        self.comp_btn.grid(row=2, column=4, columnspan=3, padx=(5, 15), pady=(5, 5))

        # Levels of Difficulty
        self.difficulties_lb = tk.Label(self.mainframe, text="DIFFICULTY", bg=self.bg_color, fg=self.btn_color)
        self.difficulties_lb.config(font=self.font_title)
        self.difficulties_lb.grid(row=3, column=1, columnspan=6)

        self.difficulties = []
        mode = ["EASY", "MEDIUM", "DIFFICULT"]
        col = 1
        for i in range(3):
            self.diff_opt = tk.Button(self.mainframe, text=mode[i], font=self.font_body, width=10)
            self.diff_opt.config(bg=self.btn_color, fg=self.font_color, disabledforeground=self.font_color,
                                 command=lambda level=self.diff_opt: self.choose_difficulty(level))
            self.diff_opt.grid(row=4, column=i+col, columnspan=2, padx=(10, 5), pady=(5, 5))
            self.difficulties.append(self.diff_opt)
            col += 1

        # Play Button
        self.play = tk.Button(self.mainframe, text="PLAY", command=self.play, font=self.font_title, width=6)
        self.play.config(bg=self.btn_color, fg=self.font_color, disabledforeground=self.btn_color)
        self.play.grid(row=5, column=1, columnspan=6, pady=(25, 10))

        # Arrow Controls Area
        self.controls_frame = tk.Frame(master=self.mainframe, bg=self.bg_color, width=325, height=100)
        self.controls_frame.grid(row=6, column=1, columnspan=6)

        size = 40, 80
        arrow_left = Image.open("img/left.png")
        arrow_left.thumbnail(size)
        self.left_arrow = ImageTk.PhotoImage(arrow_left)
        self.left_btn = tk.Button(self.controls_frame, image=self.left_arrow, bg=self.bg_color, bd=0)
        self.left_btn.config(activebackground=self.bg_color, state="disabled",
                             command=lambda direction="Left": self.move(direction))
        self.left_btn.grid(row=0, column=0)

        space_lb = tk.Label(self.controls_frame, bg=self.bg_color, width=8)
        space_lb.grid(row=0, column=1)

        arrow_right = Image.open("img/right.png")
        arrow_right.thumbnail(size)
        self.right_arrow = ImageTk.PhotoImage(arrow_right)
        self.right_btn = tk.Button(self.controls_frame, image=self.right_arrow, bg=self.bg_color, bd=0)
        self.right_btn.config(activebackground=self.bg_color, state="disabled",
                              command=lambda direction="Right": self.move(direction))
        self.right_btn.grid(row=0, column=2)

        # Exit Button
        self.exit = tk.Button(self.mainframe, text="EXIT", command=sys.exit, font=self.font_body, width=6)
        self.exit.config(bg=self.btn_color, fg=self.font_color)
        self.exit.grid(row=7, column=1, columnspan=6, pady=(15, 0))

    # Show Instructions Message from Back-End
    def show_instructions(self):
        messagebox.showinfo(message=self.bk.get_instructions(), parent=self.mainframe, title="Instructions")

    # If User plays, modify mode buttons colors
    def play_user(self):
        self.comp_btn.config(bg=self.btn_color, fg=self.font_color)
        self.user_btn.config(bg=self.font_color, fg=self.btn_color)

    # If Computer plays, modify their colors and connect with AI
    def play_comp(self):
        self.user_btn.config(bg=self.btn_color, fg=self.font_color)
        self.comp_btn.config(bg=self.font_color, fg=self.btn_color)

    # Modify colors of difficulty buttons, and get track parameters of chosen difficulty
    def choose_difficulty(self, level):
        for btn in self.difficulties:
            btn.config(bg=self.btn_color, fg=self.font_color)
        level.config(bg=self.font_color, fg=self.btn_color, disabledforeground=self.btn_color)
        self.speed = self.bk.get_track(self.difficulties.index(level))[0]
        self.length = self.bk.get_track(self.difficulties.index(level))[1]

    # Disable All Buttons (except Exit Button), Activate Arrows, Bind Arrow Keys, Set Default Game
    def play(self):
        self.play.config(state="disabled", bg=self.font_color)
        self.instructions["state"] = "disabled"
        self.user_btn["state"] = "disabled"
        self.comp_btn["state"] = "disabled"

        # If no Difficulty Level is chosen, play default 'Medium'
        play_default = True
        for btn in self.difficulties:
            btn["state"] = "disabled"
            if btn["bg"] == self.font_color:
                play_default = False
                btn.config(disabledforeground=self.btn_color)
        if play_default:
            self.choose_difficulty(self.difficulties[1])

        bind_left = window.bind("<KeyPress-Left>", lambda e: self.move(e))
        bind_right = window.bind("<KeyPress-Right>", lambda e: self.move(e))
        # If 'User' plays or Default mode
        if self.comp_btn["bg"] == self.btn_color:
            self.user_btn.config(bg=self.font_color, disabledforeground=self.btn_color)
            self.right_btn["state"] = "active"
            self.left_btn["state"] = "active"
        # If 'Computer' plays
        if self.comp_btn["bg"] == self.font_color:
            self.comp_btn.config(disabledforeground=self.btn_color)
            window.unbind("<KeyPress-Left>", bind_left)
            window.unbind("<KeyPress-Right>", bind_right)
            self.ai = True
        # Start timer and background
        self.start_time = time.time()
        self.play_background()

    # Move Player Car to Left/Right through Keys or Arrows on screen
    def move(self, event):
        direction = event
        if type(event) is not str:
            direction = event.keysym
        if direction == "Left":
            if int(self.racetrack.coords(self.player_car)[0]) > 25:
                self.racetrack.move(self.player_car, -15, 0)
        else:
            if int(self.racetrack.coords(self.player_car)[0]) < 475:
                self.racetrack.move(self.player_car, 15, 0)

    # Add obstacles
    def play_background(self):
        if not self.game_over:
            self.game_over = self.check_crash(self.obstacle_car)
        if (time.time() - self.start_time) >= 60 or self.game_over:
            self.end_game(self.game_over)
        else:
            if round((time.time() - self.start_time), 1) == self.length and self.start_play2:
                self.start_play2 = False
                self.play_background2()
            if int(self.racetrack.coords(self.obstacle_car)[1]) < 600:
                self.racetrack.move(self.obstacle_car, 0, 5)
                self.window.after(self.speed, self.play_background)
                if self.ai:
                    if int(self.racetrack.coords(self.obstacle_car)[1]) > 340:
                        if abs(int(self.racetrack.coords(self.player_car)[0]) -
                               int(self.racetrack.coords(self.obstacle_car)[0])) <= 50:
                            if ((int(self.racetrack.coords(self.player_car)[0]) -
                                 int(self.racetrack.coords(self.obstacle_car)[0])) > 0):
                                if int(self.racetrack.coords(self.player_car)[0]) < 475:
                                    self.racetrack.move(self.player_car, 25, 0)
                                elif int(self.racetrack.coords(self.player_car)[0]) == 475:
                                    self.racetrack.move(self.player_car, -50, 0)
                            else:
                                if int(self.racetrack.coords(self.player_car)[0]) > 25:
                                    self.racetrack.move(self.player_car, -25, 0)
                                elif int(self.racetrack.coords(self.player_car)[0]) == 25:
                                    self.racetrack.move(self.player_car, 50, 0)
            else:
                x = random.randint(25, 475)
                self.racetrack.coords(self.obstacle_car, x, -50)
                self.window.after(self.speed, self.play_background)

    # Allows to have two obstacles in the screen at the same time
    def play_background2(self):
        if not self.game_over:
            self.game_over = self.check_crash(self.obstacle_car2)
        if not self.game_over:
            if (time.time() - self.start_time) <= 60:
                if int(self.racetrack.coords(self.obstacle_car2)[1]) < 600:
                    self.racetrack.move(self.obstacle_car2, 0, 5)
                    self.window.after(self.speed, self.play_background2)
                    if self.ai:
                        if int(self.racetrack.coords(self.obstacle_car2)[1]) > 340:
                            if abs(int(self.racetrack.coords(self.player_car)[0]) -
                                   int(self.racetrack.coords(self.obstacle_car2)[0])) <= 50:
                                if ((int(self.racetrack.coords(self.player_car)[0]) -
                                     int(self.racetrack.coords(self.obstacle_car2)[0])) > 0):
                                    if int(self.racetrack.coords(self.player_car)[0]) < 475:
                                        self.racetrack.move(self.player_car, 25, 0)
                                    elif int(self.racetrack.coords(self.player_car)[0]) == 475:
                                        self.racetrack.move(self.player_car, -50, 0)
                                else:
                                    if int(self.racetrack.coords(self.player_car)[0]) > 25:
                                        self.racetrack.move(self.player_car, -25, 0)
                                    elif int(self.racetrack.coords(self.player_car)[0]) == 25:
                                        self.racetrack.move(self.player_car, 50, 0)
                else:
                    x = random.randint(25, 475)
                    self.racetrack.coords(self.obstacle_car2, x, -50)
                    self.window.after(self.speed, self.play_background2)

    # Check if player car has crashed with obstacle (compare coords)
    def check_crash(self, car):
        if int(self.racetrack.coords(car)[1]) > self.upper_lim:
            if abs(int(self.racetrack.coords(self.player_car)[0]) - int(self.racetrack.coords(car)[0])) < 50:
                return True
        return False

    # Game Ended (either time limit is over (player won) or player lost crashing into an obstacle)
    def end_game(self, game_over):
        message = "Congratulations!! You won. \n \n Do you want to play again?"
        if game_over:
            message = "Game Over. \n \n Do you want to try again?"
        msg_box = messagebox.askyesno(message=message)
        if msg_box:
            self.mainframe.destroy()
            Front(self.window)
        else:
            exit()


window = tk.Tk()
new_game = Front(window)
window.mainloop()