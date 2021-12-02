import tkinter as tk
import sqlite3
from tkinter import messagebox

class Playlist():
    def __init__(self, window, update_list):
        self.update_list=update_list
        self.win=window
        self.left_frame=tk.Frame(window)
        self.left_frame.pack(side=tk.LEFT)
        self.middle_frame=tk.Frame(window)
        self.middle_frame.pack(side=tk.LEFT)
        self.right_frame=tk.Frame(window)
        self.right_frame.pack(side=tk.LEFT)

        self.label_my_tracks=tk.Label(self.left_frame, width=40, text = 'Мои треки')
        self.label_my_tracks.pack()

        self.my_tracks_list=tk.Listbox(self.left_frame, width=40, height=30, selectmode=tk.EXTENDED)
        self.my_tracks_list.pack(side=tk.LEFT)
        self.left_scroll=tk.Scrollbar(self.left_frame, command=self.my_tracks_list.yview)
        self.left_scroll.pack(side=tk.LEFT)
        self.my_tracks_list.config(yscrollcommand=self.left_scroll.set)

        self.label_my_tracks = tk.Label(self.right_frame, width=40, text='Новый плейлист')
        self.label_my_tracks.pack()

        self.entry=tk.Entry(self.right_frame, width=40)
        self.entry.pack(pady=10)

        self.new_playlist = tk.Listbox(self.right_frame, width=40, height=30, selectmode=tk.EXTENDED)
        self.new_playlist.pack(side=tk.LEFT)
        self.right_scroll = tk.Scrollbar(self.right_frame, command=self.new_playlist.yview)
        self.right_scroll.pack(side=tk.LEFT)
        self.new_playlist.config(yscrollcommand=self.right_scroll.set)

        self.add_btn=tk.Button(self.middle_frame, text='add track', command=self.add, width=10, height=3)
        self.add_btn.pack(pady=20, padx=10)

        self.remove_btn = tk.Button(self.middle_frame, text='remove track', command=self.remove, width=10, height=3)
        self.remove_btn.pack(pady=20, padx=10)

        self.save_btn = tk.Button(self.middle_frame, text='save playlist', command=self.save, width=10, height=3)
        self.save_btn.pack(pady=20, padx=10)




        self.pl_tracks = ''

        tracks=[]

        db_file = 'tracks.db'
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                  select id, singer, name from tracks
                  """)
            rows = cursor.fetchall()
            for row in rows:
                id, singer, name = row
                tracks.append(str(id) + ' ' + singer + '-' + name)
        cursor.close()
        conn.close()
        for i in tracks:
            self.my_tracks_list.insert(tk.END, i)


    def add(self):
        items=list(self.my_tracks_list.curselection())
        items.reverse()
        for i in items:
            self.new_playlist.insert(tk.END, self.my_tracks_list.get(i))
            self.my_tracks_list.delete(i)

    def remove(self):
        items = list(self.new_playlist.curselection())
        items.reverse()
        for i in items:
            self.my_tracks_list.insert(tk.END, self.new_playlist.get(i))
            self.new_playlist.delete(i)

    def save(self):
        if self.entry.get()=='':
            messagebox.showerror(
            "Ошибка",
            "Введите название плейлиста")
        elif self.new_playlist.size()==0:
            messagebox.showerror(
                "Ошибка",
                "Добавьте треки")
        else:
            for i in range(self.new_playlist.size()):
                self.pl_tracks=self.pl_tracks+'_'+self.new_playlist.get(i)[0]
            with sqlite3.connect('playlists.db') as conn:
                cursor = conn.cursor()
                query = """INSERT INTO playlists
                    (name, tracks)
                    VALUES (?, ?);
                    """
                cursor.execute(query, (self.entry.get(),  self.pl_tracks))
                self.update_list.insert(tk.END, self.entry.get())
            cursor.close()
            conn.close()
            messagebox.showinfo('Сохранение','Плейлист сохранен')
            self.win.destroy()