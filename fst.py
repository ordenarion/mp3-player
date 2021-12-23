import tkinter as tk
from tkinter import messagebox
import pygame as pg
import easygui as eg
import sqlite3
from playlist_list import Pl_Block


class TimeDude:
    def __init__(self, tie=0):
        self.time = tie

    @staticmethod
    def time_update(gui):
        def count():
            if gui.running:
                if gui.counter == -1:
                    display = f"\n0:0"
                else:
                    tmp = divmod(gui.counter + 1, 60)
                    display = f"\n{tmp[0]}:{tmp[1]}"

                if gui.counter == gui.track_len:
                    if not gui.repeatQ:
                        gui.nextQ = True
                    gui.play_selected_track()
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


class GUI2:
    def __init__(self):
        pg.init()
        # self.x = TimeDude()
        self.repeatQ = False
        self.first_enter = True
        self.nextQ = False
        self.prevQ = False
        self.track_list = []
        self.track_list2 = []
        self.track_number = 0
        self.current_playlist_path = []
        self.track_len = 0
        self.flag = False
        self.counter = -1
        self.lvl = 0.5
        self.id = 0
        self.prev_status = True
        self.pause_status = True
        self.not_started = False
        self.container = {}
        self.time = 0
        self.running = False
        self.startQ = False
        self.window = tk.Tk()
        self.window.geometry("1280x720")
        self.window.title("mp3-player")
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

        self.all_tracks = tk.Listbox(self.songs_scroll_frame, selectmode="single", font=("Times", 10))  # "extended"
        self.all_tracks.pack(side="left", padx=15, pady=15, ipady=200, ipadx=100, fill="both", expand=True)

        self.scroll = tk.Scrollbar(self.songs_scroll_frame, command=self.all_tracks.yview)
        self.scroll.pack(side="left", ipady=255, )
        self.all_tracks.config(yscrollcommand=self.scroll.set)

        self.buttons_collumn_frame = tk.Frame(self.songs_scroll_frame)
        self.buttons_collumn_frame.pack(expand=True, side="left")

        self.queue_playlist_frame = tk.Frame(self.songs_scroll_frame)
        self.queue_playlist_frame.pack(expand=True, padx=10, fill="both")

        self.left_qpf = tk.Frame(self.queue_playlist_frame)
        self.left_qpf.pack(side=tk.LEFT)

        self.right_qpf = tk.Frame(self.queue_playlist_frame)
        self.right_qpf.pack(side=tk.LEFT)

        self.cp_label = tk.Label(self.left_qpf, width=60, text='Текущий плейлист:Мои треки')
        self.cp_label.pack()

        self.play_all_tracks_button = tk.Button(self.left_qpf, text='Запустить мои треки', command=self.play_my_tracks)
        self.play_all_tracks_button.pack()

        self.box = tk.Listbox(self.left_qpf, height=34, width=60)
        self.box.pack(side=tk.LEFT)

        self.scroll = tk.Scrollbar(self.left_qpf, command=self.box.yview)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.box.config(yscrollcommand=self.scroll.set)

        with sqlite3.connect('tracks.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT name, path FROM tracks
            """)
            rows = cursor.fetchall()
            for row in rows:
                name, path = row
                self.track_list.append(path)
                self.track_list2.append(path)
                self.box.insert(tk.END, str(self.track_number) + name)
                self.all_tracks.insert(tk.END, name)
                self.track_number = self.track_number + 1
        cursor.close()
        conn.close()

        self.playlist_manage = Pl_Block(self.right_qpf)

        self.KEKW_BUTTON = tk.Button(self.playlist_manage.right_frame, text='Start', command=self.start_playlist)
        self.KEKW_BUTTON.pack()

        self.prev1_button = tk.Button(self.buttons_collumn_frame, text="PC", command=self.play_selected_track, height=2,
                                      width=4)
        self.prev1_button.pack(padx=2, pady=2, ipady=5, ipadx=5, expand=True)

        self.prev2_button = tk.Button(self.buttons_collumn_frame, text="<<", height=2, width=4)
        self.prev2_button.pack(padx=0, pady=2, ipady=5, ipadx=5, expand=True, )

        self.prev3_button = tk.Button(self.buttons_collumn_frame, text="<<", height=2, width=4)
        self.prev3_button.pack(padx=0, pady=2, ipady=5, ipadx=5, expand=True)

        self.repeat_button = tk.Button(self.buttons_collumn_frame, text="( )", command=self.repeat_track, height=2,
                                       width=4)
        self.repeat_button.pack(padx=0, pady=2, ipady=5, ipadx=5, expand=True)

        # self.label2 = tk.Label(self.queue_playlist_frame, text="playlists block", bg="red")
        # self.label2.pack(ipady=275, ipadx=400, expand=True, fill="both")

        self.frame2 = tk.Frame()
        self.frame2.pack(fill="x", ipadx=100)

        self.song_bar = tk.Scale(self.frame2, from_=0, to=100, sliderlength=25, showvalue=1, length=1000,
                                 orient="horizontal", tickinterval=0.1, command=self.time_work_test)
        self.song_bar.pack(side="left", padx=10, expand=True, fill="x")  # expand=True, fill="x")

        self.label3 = tk.Label(self.frame2, font=((100)), text="\n0:0")
        self.label3.pack(ipadx=5, ipady=3, expand=1, side="right")  # fill="x",

        self.frame3 = tk.Frame()
        self.frame3.pack(padx=10, expand=True, fill="both", side="left")

        self.prev_button = tk.Button(self.frame3, text="<<", command=self.play_prev_song)  # command=self.state_tst)
        self.prev_button.pack(padx=0, pady=10, ipady=5, ipadx=5, side="left")

        self.pause_play_button = tk.Button(self.frame3, text="||", command=self.play_pause_beta, height=2, width=2)
        self.pause_play_button.pack(padx=10, pady=10, ipady=10, ipadx=10, side="left")

        self.next_button = tk.Button(self.frame3, text=">>", command=self.play_next_song)
        self.next_button.pack(padx=0, pady=10, ipady=5, ipadx=5, side="left")

        self.song_name = tk.Label(self.frame3, text="song name", anchor="w")
        self.song_name.pack(padx=20, pady=10, ipady=10, ipadx=420, side="left")
        self.song_name.pack_propagate(False)

        self.frame4 = tk.Frame()
        self.frame4.pack(expand=True, fill="both", side="left")

        self.volume_bar = tk.Scale(self.frame4, from_=0, to=100, sliderlength=25, showvalue=1, length=1000,
                                   orient="horizontal", tickinterval=0.1, variable=self.scale_var,
                                   command=self.change_volume)  # command = pass)
        self.volume_bar.pack(padx=10, pady=5, ipadx=50, ipady=20)

        self.volume_bar.set(self.lvl * 100)

        self.window.mainloop()

    def start_playlist(self):
        if len(list(self.playlist_manage.pl_list.curselection())) > 0:
            try:
                pg.mixer.music.unload(self.track_list[int(self.box.get(self.id)[0])])
            except:
                pass
            i = list(self.playlist_manage.pl_list.curselection())[
                0]  # Получаем позицию выбранного плейлиста в списке плейлистов
            tname = self.playlist_manage.pl_list.get(i)  # Получаем имя этого плейлиста
            self.track_list.clear()
            with sqlite3.connect('playlists.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT tracks FROM playlists
                WHERE name = ?
                ''', (tname,))
                rows = cursor.fetchall()
                for row in rows:
                    tracks = row[0]
                    tracks = tracks.split('_')
            cursor.close()
            conn.close()
            self.box.delete(0, tk.END)
            with sqlite3.connect('tracks.db') as conn:
                cursor = conn.cursor()
                number = 0
                for i in tracks:
                    cursor.execute('''SELECT name, path FROM TRACKS
                WHERE id = ?
                ''', (i,))
                    rows = cursor.fetchall()
                    for row in rows:
                        name, path = row
                        self.box.insert(tk.END, str(number) + name)
                        self.track_list.append(path)
                        number = number + 1
            cursor.close()
            conn.close()
            self.cp_label['text'] = 'Текущий плейлист:' + tname

            self.id = 0
            self.box.selection_set(self.id)
            self.song_name.config(text=self.box.get(self.id))
            pg.mixer.music.stop()
            tmp = self.track_list[int(self.box.get(self.id)[0])]
            pg.mixer.music.load(tmp)
            pg.mixer.music.play()
            self.track_len = round(pg.mixer.Sound(self.track_list[int(self.box.get(self.id)[0])]).get_length())
            self.song_bar.config(to=self.track_len)

            self.not_started = True
            self.pause_status = False
            self.change_pause_play_icon()
            self.counter = 0
            self.running = True
            self.track_len = round(pg.mixer.Sound(tmp).get_length())

    def play_my_tracks(self):
        try:
            pg.mixer.music.unload(self.track_list[int(self.box.get(self.id)[0])])
        except:
            pass
        self.cp_label['text'] = 'Текущий плейлист:Мои треки'
        self.track_list = self.track_list2
        self.box.delete(0, tk.END)
        for i in range(0, self.all_tracks.size()):
            self.box.insert(tk.END, str(i) + self.all_tracks.get(i))

        self.id = 0
        self.box.selection_set(self.id)
        self.song_name.config(text=self.box.get(self.id))
        pg.mixer.music.stop()
        tmp = self.track_list[int(self.box.get(self.id)[0])]
        pg.mixer.music.load(tmp)
        pg.mixer.music.play()
        self.track_len = round(pg.mixer.Sound(self.track_list[int(self.box.get(self.id)[0])]).get_length())
        self.song_bar.config(to=self.track_len)
        self.not_started = True
        self.pause_status = False
        self.change_pause_play_icon()
        self.counter = 0
        self.running = True
        self.track_len = round(pg.mixer.Sound(tmp).get_length())


    def add_new_track(self):

        if self.add_track():
            a = "\\"
            if self.cp_label['text'] == 'Текущий плейлист:Мои треки':
                self.box.insert("end", str(self.track_number) + self.music_file.split(a)[-1])
            self.all_tracks.insert("end", self.music_file.split(a)[-1])
            with sqlite3.connect("tracks.db") as conn:
                cursor = conn.cursor()
                sn = self.music_file.split(a)[-1]
                cursor.execute("""
                INSERT INTO tracks
                (name, path)
                VALUES (?, ?);
                """, (sn, self.music_file))
            cursor.close()
            conn.close()

            self.track_number = self.track_number + 1
        else:
            messagebox.showerror("Ошибка", "Неверный формат файла")

    def add_track(self):
        # открывает проводник, чтобы пользователь смог выбрать музыкальный файл
        self.music_file = eg.fileopenbox()
        if self.cp_label['text'] == 'Текущий плейлист:Мои треки':
            self.track_list.append(self.music_file)
        self.track_list2.append(self.music_file)
        return True

    def play_pause_beta(self):
        if self.first_enter:
            print(f"first_enter {self.first_enter}")
            self.play_selected_track()
            self.first_enter = False
            self.not_started = False
            TimeDude.time_update(self)
            print(f"not_started {self.not_started}")

        if not self.pause_status:
            pg.mixer.music.pause()
            self.running = False

        else:
            pg.mixer.music.unpause()
            self.running = True
        self.change_pause_play_icon()

    def play_pause(self):
        self.change_pause_play_icon()

    def time_work_test(self, arg):
        a = self.song_bar.get()
        b = self.counter
        if a != b:
            self.counter = a
            pg.mixer.music.set_pos(a)

    def change_pause_play_icon(self):
        if self.pause_status:
            self.pause_play_button.config(text="Play")
            self.pause_status = False
        else:
            self.pause_play_button.config(text="||")
            self.pause_status = True

    def play_selected_track(self):

        if self.box.size() == 0:
            pass
        else:
            try:
                pg.mixer.music.unload(self.track_list[int(self.box.get(self.id)[0])])
            except:
                pass
            if self.nextQ:
                self.box.select_clear(self.id, self.id)
                self.id = (self.id + 1) % self.box.size()
                self.nextQ = False

            elif self.prevQ:
                self.box.select_clear(self.id, self.id)
                self.id = (self.id - 1) % self.box.size()
                self.prevQ = False

            elif self.repeatQ:
                pass
            else:
                try:
                    self.id = self.box.curselection()[0]
                except:
                    self.id = 0
            self.box.selection_set(self.id)
            self.song_name.config(text=self.box.get(self.id))
            pg.mixer.music.stop()
            tmp = self.track_list[int(self.box.get(self.id)[0])]
            pg.mixer.music.load(tmp)
            pg.mixer.music.play()
            self.track_len = round(pg.mixer.Sound(self.track_list[int(self.box.get(self.id)[0])]).get_length())
            self.song_bar.config(to=self.track_len)
            self.not_started = True
            self.pause_status = False
            self.change_pause_play_icon()
            self.counter = 0
            self.running = True
            self.track_len = round(pg.mixer.Sound(tmp).get_length())

    def play_next_song(self):
        self.nextQ = True
        self.play_selected_track()

    def repeat_track(self):
        if self.repeatQ:
            self.repeatQ = False
            self.repeat_button.config(relief="raised")
        else:
            self.repeatQ = True
            self.repeat_button.config(relief="sunken")

    def play_prev_song(self):
        self.prevQ = True
        self.play_selected_track()

    def start_song(self):

        if self.pause_status:
            pg.mixer.music.unpause()
        else:
            pg.mixer.music.pause()

    def change_volume(self, a):
        pg.mixer.music.set_volume(int(a) * 0.01)


f = GUI2()
