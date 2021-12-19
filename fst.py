import time
import tkinter as tk

import pygame.mixer

from functions import add_track,play_pause,plus_volume,minus_volume
from tkinter import messagebox
import pygame as pg
import easygui as eg
import time as tm
import threading
import sqlite3

class TimeDude:
    def __init__(self,tie = 0):
        self.time = tie

    @staticmethod
    def time_update(gui):
        def count():
            if gui.running:
                if gui.counter == -1:
                    display = f"\n0:0"
                else:
                    tmp = divmod(gui.counter+1,60)
                    display = f"\n{tmp[0]}:{tmp[1]}"

                if gui.counter == gui.track_len:
                    #gui.running=False
                    if not gui.repeatQ:
                        gui.nextQ = True
                    gui.play_selected_track()
                    #gui.running = True
                    gui.song_bar.set(0)
                    gui.counter = -1
                    display = f"\n0:0"

                gui.counter += 1
                gui.label3['text'] = display
                gui.song_bar.set(gui.counter)
                gui.label3.after(1000, count)


        count()
    @staticmethod
    def time_ip(gui):
        gui.label3.config()
class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1280x720")

        self.frame1 = tk.Frame()
        self.frame1.pack(side="top", pady=10, padx=10)

        self.label1 = tk.Label(self.frame1, text="1", bg="green")
        self.label1.pack(ipady=275, ipadx=300, fill="both", expand=True, side="left")

        self.label2 = tk.Label(self.frame1, text="2", bg="red")
        self.label2.pack(ipady=275, ipadx=300, expand=True, fill="both", side="left")

        self.frame2 = tk.Frame()
        self.frame2.pack(fill="x", ipadx=100)

        self.label3 = tk.Label(self.frame2, text="3", bg="white")
        self.label3.pack(fill="x", ipadx=20, ipady=20, expand=1)

        self.frame3 = tk.Frame()
        self.frame3.pack()

        self.label4 = tk.Label(self.frame3, text="3", bg="black")
        self.label4.pack(padx=0, pady=10, ipady=20, side="left")

        self.label4 = tk.Label(self.frame3, text="3", bg="yellow")
        self.label4.pack(padx=5, pady=10, ipadx=20, ipady=20, side="left")
        # self.top_frame = tk.Frame(self.window)
        # self.top_frame.pack(side="left")

        # self.bot_frame = tk.Frame(self.window)
        # self.bot_frame.pack(side = "bottom")

        # self.box = tk.Listbox(self.top_frame,selectmode = "extended",width = 100,height = 100)
        # self.box.pack(side="left",padx=15,pady=15)
        # self.scroll = tk.Scrollbar(self.top_frame,command=self.box.yview)
        # self.scroll.pack(side="left",fill="y")
        # self.box.config(yscrollcommand=self.scroll.set)

        # self.butt = tk.Button(self.bot_frame,text="ыыыы")
        # self.label = tk.Label(self.bot_frame,text=f"{self.minutes} : {self.seconds}  ",width = 100,height = 100,font = 120)
        # self.butt.pack(pady=100)
        # self.label.pack(fill="y")
        self.window.mainloop()

        # self.curr_track


class GUI2:
    def __init__(self):
        pg.init()
        #self.x = TimeDude()
        self.repeatQ = False
        self.first_enter = True
        self.nextQ = False
        self.prevQ = False
        self.track_list = []
        self.track_number = 0
        self.track_len = 0
        self.flag = False
        self.counter =-1
        self.lvl = 0.5
        self.id = 0
        self.prev_status = True
        self.pause_status = True
        self.not_started = True
        self.container = {}
        self.time = 0
        #self.x.time_update(self)
        self.running = False
        self.startQ = False
        self.window = tk.Tk()
        self.window.geometry("1280x720")
        self.scale_var = tk.DoubleVar()
        self.scale_var = self.lvl
        self.curr_song_name = ""
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)

        self.menu.add_cascade(label="Menu", menu=self.file_menu)

        self.file_menu.add_command(label="Add Songs", command=self.add_new_track)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")

        self.songs_scroll_frame = tk.Frame()
        self.songs_scroll_frame.pack(expand=True, fill="both", pady=10, padx=10, side="top")

        self.box = tk.Listbox(self.songs_scroll_frame, selectmode="single",font=("Times",10))  # "extended"
        self.box.pack(side="left", padx=15, pady=15, ipady=200, ipadx=100, fill="both", expand=True)

        self.scroll = tk.Scrollbar(self.songs_scroll_frame, command=self.box.yview)
        self.scroll.pack(side="left", ipady=255, )
        self.box.config(yscrollcommand=self.scroll.set)

        self.buttons_collumn_frame = tk.Frame(self.songs_scroll_frame)
        self.buttons_collumn_frame.pack(expand=True, side="left")

        self.queue_playlist_frame = tk.Frame(self.songs_scroll_frame)
        self.queue_playlist_frame.pack(expand=True, padx=10,fill="both")



        self.prev1_button = tk.Button(self.buttons_collumn_frame, text="lst_tst", command=self.play_selected_track, height=2, width=4)
        self.prev1_button.pack(padx=2, pady=2, ipady=5, ipadx=5, expand=True)

        self.prev2_button = tk.Button(self.buttons_collumn_frame, text="<<", command=self.state_tst, height=2, width=4)
        self.prev2_button.pack(padx=0, pady=2, ipady=5, ipadx=5, expand=True,)

        self.prev3_button = tk.Button(self.buttons_collumn_frame, text="<<", command=self.state_tst, height=2, width=4)
        self.prev3_button.pack(padx=0, pady=2, ipady=5, ipadx=5, expand=True)

        self.repeat_button = tk.Button(self.buttons_collumn_frame, text="( )", command=self.repeat_track, height=2, width=4)
        self.repeat_button.pack(padx=0, pady=2, ipady=5, ipadx=5, expand=True)

        self.label2 = tk.Label(self.queue_playlist_frame, text="playlists block", bg="red")
        self.label2.pack(ipady=275, ipadx=400, expand=True, fill="both")

        self.frame2 = tk.Frame()
        self.frame2.pack(fill="x", ipadx=100)

        self.song_bar = tk.Scale(self.frame2, from_=0, to=100, sliderlength=25, showvalue=1, length=1000,
                                 orient="horizontal", tickinterval=0.1, command=self.time_work_test)
        self.song_bar.pack(side = "left",padx=10,expand=True,fill ="x")#expand=True, fill="x")

        self.label3 = tk.Label(self.frame2,font=((100)), text="\n0:0")
        self.label3.pack( ipadx=5, ipady=3, expand=1,side ="right") #fill="x",



        self.frame3 = tk.Frame()
        self.frame3.pack(padx=10, expand=True, fill="both", side="left")

        self.prev_button = tk.Button(self.frame3, text="<<", command = self.play_prev_song)#command=self.state_tst)
        self.prev_button.pack(padx=0, pady=10, ipady=5, ipadx=5, side="left")

        self.pause_play_button = tk.Button(self.frame3, text="||", command=self.play_pause_beta, height=2, width=2)
        self.pause_play_button.pack(padx=10, pady=10, ipady=10, ipadx=10, side="left")

        self.next_button = tk.Button(self.frame3, text=">>",command = self.play_next_song)
        self.next_button.pack(padx=0, pady=10, ipady=5, ipadx=5, side="left")

        self.song_name = tk.Label(self.frame3, text="song name", bg="green",anchor = "w")
        self.song_name.pack(padx=20, pady=10, ipady=10, ipadx=420, side="left" )
        self.song_name.pack_propagate(False)


        #self.queue_add_button = tk.Button()
        #self.queue_delete_button = tk.Button()
        #self.queue_mix_button = tk.Button()
        #self.queue_repeat_button = tk.Button()


        self.frame4 = tk.Frame()
        self.frame4.pack(expand=True, fill="both", side="left")

        self.volume_bar = tk.Scale(self.frame4, from_=0, to = 100, sliderlength = 25,showvalue = 1,length = 1000,orient = "horizontal",tickinterval = 0.1,variable = self.scale_var,command=self.change_volume)#command = pass)
        self.volume_bar.pack(padx=10, pady=5, ipadx=50, ipady=20)
        #self.label4.set(self.lvl*100)
        self.volume_bar.set(self.lvl*100)
        # self.top_frame = tk.Frame(self.window)
        # self.top_frame.pack(side="left")
        #pg.mixer.set_voulume(self.scale_var*0.01)
        # self.bot_frame = tk.Frame(self.window)
        # self.bot_frame.pack(side = "bottom")

        # self.box = tk.Listbox(self.top_frame,selectmode = "extended",width = 100,height = 100)
        # self.box.pack(side="left",padx=15,pady=15)
        # self.scroll = tk.Scrollbar(self.top_frame,command=self.box.yview)
        # self.scroll.pack(side="left",fill="y")
        # self.box.config(yscrollcommand=self.scroll.set)

        # self.butt = tk.Button(self.bot_frame,text="ыыыы")
        # self.label = tk.Label(self.bot_frame,text=f"{self.minutes} : {self.seconds}  ",width = 100,height = 100,font = 120)
        # self.butt.pack(pady=100)
        # self.label.pack(fill="y")

        self.window.mainloop()
    def ad(self):
        while not self.flag:
            t = threading.Thread(target=TimeDude.time_update(self))
            t.start()

    def asdsd(self):
        if self.running:
            self.running = False
        else:
            self.running = True
        TimeDude.time_update(self)

    def add_new_track(self):

        if self.add_track():
            a= "\\"
            self.box.insert("end",str(self.track_number)+self.music_file.split(a)[-1])
            self.track_number = self.track_number + 1
        else:
            messagebox.showerror("Ошибка","Неверный формат файла")

    def add_track(self):
        # открывает проводник, чтобы пользователь смог выбрать музыкальный файл
        self.music_file = eg.fileopenbox()
        self.track_list.append(self.music_file)
        return True
        # если файл нужного формата, то он загружается в проигрыватель и возвращается путь файла
        # try:
        #     tmp = pg.mixer.music.load(self.music_file)
        #     tmp = pg.mixer.music.unload(self.music_file)
        #
        #     return True
        # #  если файл неверного формата, то функция возвращает строку с соответствующим сообщением
        # except:
        #      return False



    def play_pause_beta(self):
        if self.first_enter:
            self.play_selected_track()
            self.first_enter = False
        if self.not_started:
            try:
                pg.mixer.music.play()
                self.not_started=False
                self.running=True
                self.track_len = round(pg.mixer.Sound(self.music_file).get_length())
                self.song_bar.config(to = self.track_len)
            except:
                pass
        else:
            if not self.pause_status:
                pg.mixer.music.pause()
                self.running=False
            else:
                pg.mixer.music.unpause()
                self.running=True
        self.change_pause_play_icon()
        TimeDude.time_update(self)

    def play_pause(self):
        self.change_pause_play_icon()

        # if self.box.size() == 0:
        #     pass
        # else:
        #     if self.startQ:
        #         self.start_song()
        #     else:
        #         pg.mixer.music.play()
        #         self.startQ = not self.startQ
        #     self.pause_status = not self.pause_status

    def time_work_test(self,arg):
        a = self.song_bar.get()
        b = self.counter
        if a != b:
            self.counter = a
        if abs(pg.mixer.music.get_pos() - a * 1000) > 1000:
            pg.mixer.music.set_pos(a)

    def change_pause_play_icon(self):
        if self.pause_status:
            self.pause_play_button.config(text="ы")
            self.pause_status = False
        else:
            self.pause_play_button.config(text="||")
            self.pause_status = True

    def play_selected_track(self):

        if self.box.size() ==0:
            pass
        else:
            try:
                pg.mixer.music.unload(self.track_list[int(self.box.get(self.id)[0])])
            except:
                pass
            print(f"id которое убиваем {self.id}")
            #self.running = False

            if self.nextQ:
                self.box.select_clear(self.id, self.id)
                self.id = (self.id + 1)%self.box.size()
                self.nextQ = False

                print("next")
            elif self.prevQ:
                self.box.select_clear(self.id, self.id)
                self.id = (self.id - 1)%self.box.size()
                self.prevQ = False

                print("prev")
            elif self.repeatQ:
                #id остается прежнем
                pass
            else:
                try:
                 self.id = self.box.curselection()[0]
                except:
                    self.id = 0
            print(f"id которое запускается {self.id}")

            self.box.selection_set(self.id)
            self.song_name.config(text=self.box.get(self.id))
            pg.mixer.music.stop()
            tmp = self.track_list[int(self.box.get(self.id)[0])]
            pg.mixer.music.load(tmp)
            pg.mixer.music.play()
            self.track_len = round(pg.mixer.Sound(self.track_list[int(self.box.get(self.id)[0])]).get_length())
            self.song_bar.config(to=self.track_len)
            #self.not_started = False
            #self.pause_status = True
            self.not_started = True
            self.pause_status = False
            self.change_pause_play_icon()
            self.counter = 0
            #self.running = True
            self.track_len = round(pg.mixer.Sound(tmp).get_length())
            # if self.first_enter:
            #     TimeDude.time_update(self)
            #     self.first_enter = False

            #TimeDude.time_update(self)
            #self.to_add = pg.mixer.music.load(self.box.get(self.box.curselection()))
    def play_next_song(self):
        self.nextQ = True
        self.play_selected_track()
    def repeat_track(self):
        if self.repeatQ:
            self.repeatQ = False
            self.repeat_button.config(relief = "raised")
        else:
            self.repeatQ = True
            self.repeat_button.config(relief = "sunken")
    def play_prev_song(self):
        self.prevQ = True
        self.play_selected_track()

    def start_song(self):

        if self.pause_status:
            pg.mixer.music.unpause()
        else:
            pg.mixer.music.pause()


    def state_tst(self):
        if self.prev_status:
            self.prev1_button.config(relief="sunken")
            self.prev_status = False
        else:
            self.prev1_button.config(relief="raised")
            self.prev_status = True

    def set_volume_down(self):
        if self.lvl == 0:
            pass
        else:
            pg.mixer.music.set_volume(self.lvl-0.1)
            self.lvl -= 0.1
            self.volume_bar.set(self.lvl*100)

    def set_volume_up(self):
        if self.lvl == 1.0:
            pass
        else:
            pg.mixer.music.set_volume(self.lvl + 0.1)
            self.lvl += 0.1
            self.volume_bar.set(self.lvl*100)

    def start_curr_track(self):
        pass
    def change_volume(self,a):
        pg.mixer.music.set_volume(int(a)*0.01)


f = GUI2()
