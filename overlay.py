import tkinter as tk
import time

from tkinter import ttk
from tkinter import colorchooser
from threading import Thread
from random import randint
from ctypes import *
from maths import *

from keyboard import Keyboard

keyboard = Keyboard()


class Overlay:
    TRANSPARENTCOLOR = "black"

    def __init__(self):
        #  Styling
        self.loaded = False
        self.font = "fixedsys 8"
        self.overlay_padding = 5

        #  Insert toggle gui
        self.pressed = False
        self.gui = True

        #  Default norecoil settings
        self.norecoil = False
        self.recoil_value = 0.0
        self.recoil_aimcone = -1.0

        #  ESP features
        self.esp = True
        self.playeresp = True
        self.playeresp_snapline = True
        self.lootesp = False
        self.stashesp = False
        self.nodesesp = False
        self.supplydropesp = True
        self.animalesp = False

        #  Other
        self.crosshair = True

        #  Entities
        self.entities = []

        #  4X4 Matrix Camera View
        self.matrix4x4 = []

        #  Storing info about width, height and window title
        self.title = randomString(randint(5, 10))
        self.buttonhold = False
        self.screen_width = windll.user32.GetSystemMetrics(0) - self.overlay_padding * 2
        self.screen_height = windll.user32.GetSystemMetrics(1) - self.overlay_padding * 2

    def init(self):
        Thread(target=self.mainloop).start()
        while not self.loaded:
            time.sleep(0.01)

    def mainloop(self):
        self.__root = tk.Tk()
        self.__root.minsize(self.screen_width, self.screen_height)
        self.__root.overrideredirect(True)
        self.__root.attributes("-topmost", True)
        self.__root.attributes("-transparentcolor", self.TRANSPARENTCOLOR)
        self.__root["bg"] = self.TRANSPARENTCOLOR
        self.__root.title(self.title)

        self.__root.geometry('+%d+%d' % (self.overlay_padding, self.overlay_padding))

        hwnd = windll.user32.FindWindowA(None, self.title)
        lExStyle = windll.user32.GetWindowLongA(hwnd, -20)
        lExStyle |= 0x00000020 | 0x00080000
        windll.user32.SetWindowLongA(hwnd, -20, lExStyle)

        self.__canvas = tk.Canvas(self.__root, height=self.screen_height, width=self.screen_width)
        self.__canvas["bg"] = self.TRANSPARENTCOLOR

        #  Overlay border
        self.__canvas["highlightthickness"] = 0
        self.__canvas["highlightbackground"] = "red"
        self.__canvas.pack(fill="both")

        self.__canvas.after(10, self.update)

        bgcolor = "#%02x%02x%02x" % (25, 17, 17)
        fgcolor = "white"
        font_ = "Arial 11"

        #  TTK SETTINGS
        s = ttk.Style()
        s.theme_use('alt')
        s.configure("TSeparator", background="red")
        s.configure("Horizontal.TScale", background=bgcolor, fieldbackground="red",
                    troughcolor="#%02x%02x%02x" % (255, 46, 46))
        s.configure("TMenubutton", relief=tk.FLAT, font=font_, bd=0, highlightthickness=0,
                    arrowcolor="#909090", foreground=fgcolor, background=bgcolor)
        s.map("TMenubutton",
              background=[('disabled', bgcolor), ('pressed', bgcolor), ('active', bgcolor)],
              foreground=[('disabled', "#707070")])

        self.__gui = tk.Toplevel(self.__root)
        self.__gui.overrideredirect(True)
        self.__gui.resizable(False, False)
        self.__gui.attributes("-alpha", 0.75)
        self.__gui.attributes("-topmost", True)
        self.__gui.config(bg=bgcolor)

        self.frame = tk.Frame(self.__gui, bg=bgcolor, highlightbackground="#%02x%02x%02x" % (55, 8, 8),
                              highlightthickness=3)
        self.frame.bind('<Button-1>', self.clickwin)
        self.frame.bind('<B1-Motion>', lambda event: self.dragwin(event, self.__gui))

        #  Widgets Column 0
        self.label0var = tk.IntVar()
        self.label0var.set(self.playeresp)
        self.label0 = tk.Checkbutton(self.frame, variable=self.label0var,
                                     command=self.esp_toggle, font=font_, text="ESP", bg=bgcolor,
                                     fg=fgcolor,
                                     activebackground=bgcolor, activeforeground=fgcolor,
                                     selectcolor=bgcolor)

        self.separator0 = ttk.Separator(self.frame)
        self.checkbox_playeresp_var = tk.IntVar()
        self.checkbox_playeresp_var.set(self.playeresp)
        self.checkbox_playeresp = tk.Checkbutton(self.frame, variable=self.checkbox_playeresp_var,
                                                 command=self.playeresp_toggle, font=font_, text="Player", bg=bgcolor,
                                                 fg=fgcolor,
                                                 activebackground=bgcolor, activeforeground=fgcolor,
                                                 selectcolor=bgcolor)

        self.checkbox_playerespsnapline_var = tk.IntVar()
        self.checkbox_playerespsnapline_var.set(self.playeresp_snapline)
        self.checkbox_playerespsnapline = tk.Checkbutton(self.frame, variable=self.checkbox_playerespsnapline_var,
                                                         command=self.playerespsnapline_toggle, font=font_,
                                                         text="Player snapline",
                                                         bg=bgcolor, fg=fgcolor,
                                                         activebackground=bgcolor, activeforeground=fgcolor,
                                                         selectcolor=bgcolor)

        self.checkbox_lootesp_var = tk.IntVar()
        self.checkbox_lootesp_var.set(self.lootesp)
        self.checkbox_lootesp = tk.Checkbutton(self.frame, variable=self.checkbox_lootesp_var,
                                               command=self.lootesp_toggle, font=font_,
                                               text="Loot",
                                               bg=bgcolor, fg=fgcolor,
                                               activebackground=bgcolor, activeforeground=fgcolor,
                                               selectcolor=bgcolor)

        self.checkbox_stashesp_var = tk.IntVar()
        self.checkbox_stashesp_var.set(self.stashesp)
        self.checkbox_stashesp = tk.Checkbutton(self.frame, variable=self.checkbox_stashesp_var,
                                                command=self.stashesp_toggle, font=font_,
                                                text="Stash",
                                                bg=bgcolor, fg=fgcolor,
                                                activebackground=bgcolor, activeforeground=fgcolor,
                                                selectcolor=bgcolor)

        self.checkbox_nodesesp_var = tk.IntVar()
        self.checkbox_nodesesp_var.set(self.nodesesp)
        self.checkbox_nodesesp = tk.Checkbutton(self.frame, variable=self.checkbox_nodesesp_var,
                                                command=self.nodesesp_toggle, font=font_,
                                                text="Nodes",
                                                bg=bgcolor, fg=fgcolor,
                                                activebackground=bgcolor, activeforeground=fgcolor,
                                                selectcolor=bgcolor)

        self.checkbox_supplydropesp_var = tk.IntVar()
        self.checkbox_supplydropesp_var.set(self.supplydropesp)
        self.checkbox_supplydropesp = tk.Checkbutton(self.frame, variable=self.checkbox_supplydropesp_var,
                                                     command=self.supplydropesp_toggle, font=font_,
                                                     text="Supplydrop",
                                                     bg=bgcolor, fg=fgcolor,
                                                     activebackground=bgcolor, activeforeground=fgcolor,
                                                     selectcolor=bgcolor)

        self.checkbox_animalesp_var = tk.IntVar()
        self.checkbox_animalesp_var.set(self.animalesp)
        self.checkbox_animalesp = tk.Checkbutton(self.frame, variable=self.checkbox_animalesp_var,
                                                 command=self.animalesp_toggle, font=font_,
                                                 text="Animal",
                                                 bg=bgcolor, fg=fgcolor,
                                                 activebackground=bgcolor, activeforeground=fgcolor,
                                                 selectcolor=bgcolor)

        #  Column 1
        self.separator1 = ttk.Separator(self.frame)

        #  Column 2
        self.label2var = tk.IntVar()
        self.label2var.set(self.norecoil)
        self.label2 = tk.Checkbutton(self.frame, variable=self.label2var,
                                     command=self.norecoil_toggle, font=font_,
                                     text="NORECOIL",
                                     bg=bgcolor, fg=fgcolor,
                                     activebackground=bgcolor, activeforeground=fgcolor,
                                     selectcolor=bgcolor)

        self.separator2 = ttk.Separator(self.frame)

        self.norecoilvar = tk.DoubleVar()
        self.norecoilvar.trace("w", self.scale_update)
        self.scale_recoil_label = tk.Label(self.frame, text="Recoil: " + str(self.recoil_value), fg=fgcolor, bg=bgcolor,
                                           font=font_)
        self.scale_recoil = ttk.Scale(self.frame, variable=self.norecoilvar, from_=-10, to=10, value=self.recoil_value,
                                      length=200)

        self.aimconevar = tk.DoubleVar()
        self.aimconevar.trace("w", self.scale_update)
        self.scale_aimcone_label = tk.Label(self.frame, text="Aimcone: " + str(self.recoil_aimcone), fg=fgcolor,
                                            bg=bgcolor, font=font_)
        self.scale_aimcone = ttk.Scale(self.frame, variable=self.aimconevar, from_=-10, to=10,
                                       value=self.recoil_aimcone, length=200)

        #  Column 3
        self.separator3 = ttk.Separator(self.frame)

        #  Column 4
        self.label4 = tk.Label(self.frame, text="OTHER", fg=fgcolor, bg=bgcolor, font=font_)
        self.separator4 = ttk.Separator(self.frame)

        self.checkbox_crosshair_var = tk.IntVar()
        self.checkbox_crosshair_var.set(self.crosshair)
        self.checkbox_crosshair = tk.Checkbutton(self.frame, variable=self.checkbox_crosshair_var,
                                                 command=self.crosshair_callback, font=font_,
                                                 text="Crosshair",
                                                 bg=bgcolor, fg=fgcolor,
                                                 activebackground=bgcolor, activeforeground=fgcolor,
                                                 selectcolor=bgcolor)

        #  Gridding
        self.frame.grid(row=0, column=0, padx=3, pady=3)
        self.label0.grid(row=0, column=0, padx=3, pady=3, sticky="w")
        self.separator0.grid(row=1, column=0, padx=3, pady=3, sticky="we", columnspan=2)
        self.checkbox_playeresp.grid(row=2, column=0, padx=3, pady=3, sticky="w")
        self.checkbox_playerespsnapline.grid(row=3, column=0, padx=3, pady=3, sticky="w")
        self.checkbox_lootesp.grid(row=4, column=0, padx=3, pady=3, sticky="w")
        self.checkbox_stashesp.grid(row=5, column=0, padx=3, pady=3, sticky="w")
        self.checkbox_nodesesp.grid(row=6, column=0, padx=3, pady=3, sticky="w")
        self.checkbox_supplydropesp.grid(row=7, column=0, padx=3, pady=3, sticky="w")
        self.checkbox_animalesp.grid(row=8, column=0, padx=3, pady=3, sticky="w")

        self.separator1.grid(row=0, column=2, sticky="ns", rowspan=100)

        self.label2.grid(row=0, column=3, padx=3, pady=3, sticky="w")
        self.separator2.grid(row=1, column=3, padx=3, pady=3, sticky="we")
        self.scale_recoil.grid(row=3, column=3, padx=6, pady=6, sticky="we")
        self.scale_recoil_label.grid(row=2, column=3, padx=3, pady=3, sticky="w")
        self.scale_aimcone.grid(row=5, column=3, padx=6, pady=6, sticky="we")
        self.scale_aimcone_label.grid(row=4, column=3, padx=3, pady=3, sticky="w")

        self.separator3.grid(row=0, column=4, sticky="ns", rowspan=100)

        self.label4.grid(row=0, column=5, padx=3, pady=3, sticky="w")
        self.separator4.grid(row=1, column=5, padx=3, pady=3, sticky="we")
        self.checkbox_crosshair.grid(row=2, column=5, padx=3, pady=3, sticky="w")

        self.loaded = True
        self.__root.mainloop()

    def draw_entity(self, entity):
        screen_pos = self.world_to_screen(entity)
        if screen_pos and entity.render:
            x1 = screen_pos[0] - (screen_pos[1] - screen_pos[2]) * entity.x_scratch
            y1 = screen_pos[2]
            x2 = screen_pos[0] + (screen_pos[1] - screen_pos[2]) * entity.x_scratch
            y2 = screen_pos[1]
            if str(entity) == "Player":
                if self.playeresp and entity.health > 0:
                    self.__canvas.create_rectangle(x1, y1, x2, y2,
                                                   tags="overlay", outline=entity.box_color,
                                                   fill=self.TRANSPARENTCOLOR, width=2)

                    self.__canvas.create_rectangle(x1, y1 - 1, x1 + (x2 - x1) * (entity.health / 100),
                                                   y1 - 8, tags="overlay", fill=self.get_health_color(entity.health),
                                                   outline=self.TRANSPARENTCOLOR)

                    self.__canvas.create_text(x1 + (x2 - x1) / 2, y1 - 13,
                                              text=entity.name + " | " + str(entity.health) + "HP",
                                              fill="white", tags="overlay")

                if self.playeresp_snapline and entity.health > 0:
                    self.__canvas.create_line(self.screen_width / 2, self.screen_height,
                                              x1 + (x2 - x1) / 2, y2, tags="overlay",
                                              width=2, fill=entity.snap_color)

            elif str(entity) == "Loot" and self.lootesp or str(entity) == "Stash" and self.stashesp or str(
                    entity) == "Node" and self.nodesesp or str(entity) == "Supplydrop" and self.supplydropesp or str(
                    entity) == "Animal" and self.animalesp:
                self.__canvas.create_rectangle(x1, y1, x2, y2, tags="overlay", outline=entity.box_color,
                                               fill=self.TRANSPARENTCOLOR, width=2)
                self.__canvas.create_text(x1 + (x2 - x1) / 2, y1 - 13, text=entity.name, fill="white", tags="overlay")

    def world_to_screen(self, entity):
        trans_vec = Vector3(self.matrix4x4[3], self.matrix4x4[7], self.matrix4x4[11])
        right_vec = Vector3(self.matrix4x4[0], self.matrix4x4[4], self.matrix4x4[8])
        up_vec = Vector3(self.matrix4x4[1], self.matrix4x4[5], self.matrix4x4[9])

        w = (trans_vec.x * entity.vector3.x + trans_vec.y * (
                entity.vector3.y + entity.height) + trans_vec.z * entity.vector3.z) + self.matrix4x4[15]
        if w < 0.098:
            return False

        y = (up_vec.x * entity.vector3.x + up_vec.y * entity.vector3.y + up_vec.z * entity.vector3.z) + self.matrix4x4[
            13]
        y_head = (up_vec.x * entity.vector3.x + up_vec.y * (
                entity.vector3.y + entity.height) + up_vec.z * entity.vector3.z) + self.matrix4x4[13]
        x = (right_vec.x * entity.vector3.x + right_vec.y * (
                entity.vector3.y + entity.height) + right_vec.z * entity.vector3.z) + self.matrix4x4[12]

        screen_pos = [(self.screen_width / 2) * (1.0 + x / w), (self.screen_height / 2) * (1.0 - y / w),
                      self.screen_height / 2 * (1.0 - y_head / w)]
        return screen_pos

    def clean(self, items="all"):
        self.__canvas.delete(items)

    def create_crosshair(self, fill_="red"):
        if self.crosshair:
            self.__canvas.create_line(self.screen_width / 2 - 10, self.screen_height / 2,
                                      self.screen_width / 2 + 10, self.screen_height / 2,
                                      fill=fill_, tags="crosshair")

            self.__canvas.create_line(self.screen_width / 2, self.screen_height / 2 - 10,
                                      self.screen_width / 2, self.screen_height / 2 + 10,
                                      fill=fill_, tags="crosshair")

            self.__canvas.create_rectangle(self.screen_width / 2 - 1, self.screen_height / 2 - 1,
                                           self.screen_width / 2 + 1, self.screen_height / 2 + 1,
                                           fill=self.TRANSPARENTCOLOR, outline=self.TRANSPARENTCOLOR,
                                           tags="crosshair")

    def update(self):
        self.clean(items="overlay")

        if self.esp:
            for i in range(len(self.entities)):
                try:
                    self.draw_entity(self.entities[i].entity)
                except Exception as e:
                    pass
        else:
            self.clean(items="overlay")

        if keyboard.check_if_down("insert") and not self.pressed:
            self.pressed = True
            self.gui = not (self.gui)
            if self.gui:
                self.__gui.deiconify()
            else:
                self.__gui.withdraw()

        elif not keyboard.check_if_down("insert") and self.pressed:
            self.pressed = False

        self.__canvas.after(10, self.update)

    def dragwin(self, event, parent):
        x = parent.winfo_pointerx() - self._offsetx
        y = parent.winfo_pointery() - self._offsety
        parent.geometry('+{x}+{y}'.format(x=x, y=y))

    def clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y

    def get_health_color(self, health):
        health = health / 100
        return "#%02x%02x%02x" % (int(255 * (1 - health)), int(255 * health), 0)

    def scale_update(self, *args):
        if self.norecoilvar.get() < 0.075 and self.norecoilvar.get() > 0:
            self.recoil_value = 0.0
        else:
            self.recoil_value = round(self.norecoilvar.get(), 1)

        if self.aimconevar.get() < -0.8 and self.aimconevar.get() > -1.2:
            self.recoil_aimcone = -1.0
        else:
            self.recoil_aimcone = round(self.aimconevar.get(), 1)

        self.scale_aimcone_label.config(text="Aimcone: " + str(self.recoil_aimcone))
        self.scale_recoil_label.config(text="Recoil: " + str(self.recoil_value))

    def norecoil_toggle(self):
        self.norecoil = not self.norecoil

    def esp_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.esp
        else:
            self.esp = not self.esp

    def playeresp_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.playeresp
        else:
            self.playeresp = not self.playeresp

    def playerespsnapline_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.playeresp_snapline
        else:
            self.playeresp_snapline = not self.playeresp_snapline

    def lootesp_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.lootesp
        else:
            self.lootesp = not self.lootesp

    def stashesp_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.stashesp
        else:
            self.stashesp = not self.stashesp

    def nodesesp_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.nodesesp
        else:
            self.nodesesp = not self.nodesesp

    def supplydropesp_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.supplydropesp
        else:
            self.supplydropesp = not self.supplydropesp

    def animalesp_toggle(self, input_name="overlay"):
        if input_name == "__main__":
            return self.animalesp
        else:
            self.animalesp = not self.animalesp

    def crosshair_callback(self, *args):
        self.crosshair = not self.crosshair

        if self.crosshair:
            self.create_crosshair()
        else:
            self.__canvas.delete("crosshair")


def randomString(length):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    string = ""

    string += alphabet[randint(0, len(alphabet) - 1)]

    for i in range(length - 1):
        if randint(0, 1) == 1:
            if randint(0, 1) == 1:
                string += alphabet[randint(0, len(alphabet) - 1)].upper()
            else:
                string += alphabet[randint(0, len(alphabet) - 1)]
        else:
            string += numbers[randint(0, len(numbers) - 1)]

    return string
