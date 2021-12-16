import tkinter as tk
import sqlite3
from tkinter import messagebox

class Playlist():
    def __init__(self, window, update_list, current_playlist, place):
        self.place=place
        self.current_playlist=current_playlist
        self.update_list=update_list
        self.win=window
        self.left_frame=tk.Frame(window)
        self.left_frame.pack(side=tk.LEFT)
        self.middle_frame=tk.Frame(window)
        self.middle_frame.pack(side=tk.LEFT)
        self.middle_frame2 = tk.Frame(window)
        self.middle_frame2.pack(side=tk.LEFT)
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
        self.entry.insert(0, current_playlist)
        self.entry.pack(pady=10)



        self.new_playlist = tk.Listbox(self.right_frame, width=40, height=30, selectmode=tk.EXTENDED)
        self.new_playlist.pack(side=tk.LEFT)
        self.right_scroll = tk.Scrollbar(self.right_frame, command=self.new_playlist.yview)
        self.right_scroll.pack(side=tk.LEFT)
        self.new_playlist.config(yscrollcommand=self.right_scroll.set)

        self.up_btn = tk.Button(self.middle_frame2, text='up', command=self.up, width=10, heigh=3)
        self.up_btn.pack(pady=20, padx=10)

        self.down_btn = tk.Button(self.middle_frame2, text='down', command=self.down, width=10, heigh=3)
        self.down_btn.pack(pady=20, padx=10)

        self.random_btn = tk.Button(self.middle_frame2, text='mix', command=self.mix, width=10, heigh=3)
        self.random_btn.pack(pady=20, padx=10)

        self.add_btn=tk.Button(self.middle_frame, text='add track', command=self.add, width=10, height=3)
        self.add_btn.pack(pady=20, padx=10)

        self.remove_btn = tk.Button(self.middle_frame, text='remove track', command=self.remove, width=10, height=3)
        self.remove_btn.pack(pady=20, padx=10)

        self.save_btn = tk.Button(self.middle_frame, text='save playlist', command=self.save_confirm, width=10, height=3)
        self.save_btn.pack(pady=20, padx=10)

        with sqlite3.connect("playlists.db") as conn:
            cursor=conn.cursor()
            cursor.execute("""
            SELECT name FROM playlists
            """)
            self.names=cursor.fetchall()

            if current_playlist!='':
                self.names.remove((current_playlist,))

                cursor.execute("""
                        SELECT id, tracks FROM playlists
                        WHERE name= ?
                        """, (current_playlist,))
                self.id, self.tracks = cursor.fetchall()[0]
        cursor.close()

        conn.close()




        self.pl_tracks = ''


        db_file = 'tracks.db'

        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            if current_playlist == '':
                cursor.execute("""
                    select id, singer, name from tracks
                  """)
                rows = cursor.fetchall()
                for row in rows:
                    id, singer, name = row
                    self.my_tracks_list.insert(tk.END, str(id) + ' ' + singer + '-' + name)


            else:
                tracks=self.tracks.split('_')
                tracks.remove('')
                for track in tracks:

                    cursor.execute(
                            """
                            select singer, name from  tracks
                            where id = ?
                            """, (int(track),)
                    )
                    selected=cursor.fetchall()[0]
                    self.new_playlist.insert(tk.END, track + ' ' + selected[0] + '-' + selected[1])

                song_id=1
                while True:

                    cursor.execute(
                            """
                            select singer, name from  tracks
                            where id = ?
                            """, (song_id,)
                        )
                    rows = cursor.fetchall()
                    if len(rows)==0:
                        break
                    for row in rows:
                        singer, name = row
                        if not(str(song_id) in tracks):
                            self.my_tracks_list.insert(tk.END, str(song_id) + ' ' + singer + '-' + name)
                    song_id=song_id+1






        cursor.close()
        conn.close()

        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
    def up(self):
        curr_tracks=list(self.new_playlist.curselection())
        if len(curr_tracks)==1:
            track=curr_tracks[0]
            if track!=0:
                x=self.new_playlist.get(track)
                y=self.new_playlist.get(track-1)
                self.new_playlist.delete(track-1)
                self.new_playlist.insert(track-1, x)
                self.new_playlist.delete(track)
                self.new_playlist.insert(track, y)

    def down(self):
        curr_tracks = list(self.new_playlist.curselection())
        if len(curr_tracks) == 1:
            track = curr_tracks[0]
            if track != self.new_playlist.size()-1:
                x = self.new_playlist.get(track)
                y = self.new_playlist.get(track + 1)
                self.new_playlist.delete(track + 1)
                self.new_playlist.insert(track + 1, x)
                self.new_playlist.delete(track)
                self.new_playlist.insert(track, y)

    def mix(self):
        size=self.new_playlist.size()
        if size>0:
            for i in range(size-1):
                randomi=random.randint(i, size-1)
                tracki=self.new_playlist.get(i)
                track_randomi=self.new_playlist.get(randomi)
                self.new_playlist.delete(i)
                self.new_playlist.insert(i, track_randomi)
                self.new_playlist.delete(randomi)
                self.new_playlist.insert(randomi, tracki)

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
        elif (self.entry.get(),) in self.names:
            messagebox.showerror(
                "Ошибка",
                "Плейлист с таким именем уже существует. Измените имя.")

        elif self.new_playlist.size()==0:
            messagebox.showerror(
                "Ошибка",
                "Добавьте треки")
        else:
            for i in range(self.new_playlist.size()):
                self.pl_tracks=self.pl_tracks+'_'+self.new_playlist.get(i)[0]
            with sqlite3.connect('playlists.db') as conn:
                cursor = conn.cursor()

                if self.current_playlist=='':
                    query = """INSERT INTO playlists
                    (name, tracks)
                    VALUES (?, ?);
                    """
                    cursor.execute(query, (self.entry.get(), self.pl_tracks))
                    self.update_list.insert(tk.END, self.entry.get())
                else:
                    query = """UPDATE playlists SET name = ?
                                WHERE id = ?       
                                        """
                    cursor.execute(query, (self.entry.get(), self.id))
                    query="""UPDATE playlists SET tracks = ?
                                WHERE id = ?       
                                        """
                    cursor.execute(query, (self.pl_tracks, self.id))
                    if self.entry.get!=self.current_playlist:
                        self.update_list.delete(self.place)
                        self.update_list.insert(self.place, self.entry.get())
            cursor.close()
            conn.close()
            messagebox.showinfo('Сохранение','Плейлист сохранен')
            self.win.destroy()

    def save_confirm(self):
        answer = messagebox.askyesno("Закрытие", "Сохранить плейлист?")
        if answer:
            self.save()

    def on_closing(self):
        answer = messagebox.askyesno("Закрытие", "Сохранить плейлист?")
        if answer:
            self.save()
        else:
            self.win.destroy()