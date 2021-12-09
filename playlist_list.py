import tkinter as tk
from tkinter import messagebox
import sqlite3

from new_pl_create import Playlist

class Pl_Block:
    def __init__(self, window):
        self.left_frame=tk.Frame(window)
        self.left_frame.pack(side=tk.LEFT)
        self.right_frame=tk.Frame(window)
        self.right_frame.pack(side=tk.RIGHT)
        self.label=tk.Label(self.left_frame, width=60, text='Мои плейлисты')
        self.label.pack()
        self.pl_list=tk.Listbox(self.left_frame, height=40 , width=60)
        self.pl_list.pack(side=tk.LEFT)
        self.scroll=tk.Scrollbar(self.left_frame, command=self.pl_list.yview)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.pl_list.config(yscrollcommand=self.scroll.set)
        self.view_btn=tk.Button(self.right_frame, text='view', command=self.pl_view, width=20)
        self.view_btn.pack()
        self.edit_btn = tk.Button(self.right_frame, text='edit', command=self.pl_edit, width=20)
        self.edit_btn.pack()
        self.del_btn = tk.Button(self.right_frame, text='delete', command=self.pl_dell, width=20)
        self.del_btn.pack()
        self.create_btn = tk.Button(self.right_frame, text='create new playlist', command=self.pl_create, width=20)
        self.create_btn.pack()
        with sqlite3.connect('playlists.db') as conn:
            cursor=conn.cursor()
            cursor.execute(
                        """
                        select name from playlists
                        """
                    )
            pl_name = cursor.fetchall()
            for i in pl_name:
                self.pl_list.insert(tk.END, i[0])
        cursor.close()
        conn.close()


    def pl_view(self):
        if len(list(self.pl_list.curselection()))>0:
            new_window=tk.Tk()
            pl_name=self.pl_list.get(list(self.pl_list.curselection())[0])
            label=tk.Label(new_window, width=60, text=pl_name)
            label.pack()
            tracks=tk.Listbox(new_window, height=40 , width=60)
            tracks.pack(side=tk.LEFT)
            scroll=tk.Scrollbar(new_window, command=tracks.yview())
            scroll.pack(side=tk.LEFT, fill=tk.Y)
            tracks.config(yscrollcommand=scroll.set)
            print(pl_name)
            with sqlite3.connect('playlists.db') as conn:
                cursor=conn.cursor()
                cursor.execute("""
                select tracks from playlists
                where name = ?
                """, (pl_name,))
                curr_tracks=cursor.fetchall()
                curr_tracks=(curr_tracks[0][0]).split('_')
            cursor.close()
            conn.close()
            with sqlite3.connect('tracks.db') as conn:
                cursor=conn.cursor()
                for i in curr_tracks:
                    if i!="":
                        cursor.execute(
                            """
                            select singer, name from  tracks
                            where id = ?
                            """, (int(i),)
                        )
                        for j in cursor.fetchall():
                            tracks.insert(tk.END,str(j[0])+"-"+str(j[1]))
            cursor.close()
            conn.close()
            new_window.mainloop()

    def pl_edit(self):
        new_window=tk.Tk()
        pl_name = self.pl_list.get(list(self.pl_list.curselection())[0])
        block=Playlist(new_window, self.pl_list, pl_name, list(self.pl_list.curselection())[0])
        new_window.mainloop()

    def pl_dell(self):
        i=list(self.pl_list.curselection())[0]
        name=self.pl_list.get(i)
        answer = messagebox.askyesno("Удаление", "Вы действительно хотите удалить плейлист "+name+"?")
        if answer:
            with sqlite3.connect("playlists.db") as conn:
                cursor=conn.cursor()
                cursor.execute("""
                DELETE FROM playlists
                WHERE name = ?
                """,(name,))
            cursor.close()
            conn.close()
            self.pl_list.delete(i)

    def pl_create(self):
        new_window=tk.Tk()
        block=Playlist(new_window, self.pl_list,'',-1)
        new_window.mainloop()

window=tk.Tk()

block=Pl_Block(window)
window.mainloop()