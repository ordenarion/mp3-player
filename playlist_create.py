import tkinter as tk
from tkinter import messagebox
import sqlite3

class ListFrame(tk.Frame):
    def __init__(self, master, items=[],heading=''):
        super().__init__(master)
        self.text=tk.Label(self,text=heading)
        self.text.pack()
        if heading=='Плейлист':
            self.name=tk.Label(self,text='Название плейлиста')
            self.name.pack()
            self.entry=tk.Entry(self)
            self.entry.pack()
            self.curr_tracks=tk.Label(self,text='Треки плейлиста')
            self.curr_tracks.pack()
        self.list = tk.Listbox(self)
        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL,
                                   command=self.list.yview)
        self.list.config(yscrollcommand=self.scroll.set)
        self.list.insert(0, *items)
        self.list.pack(side=tk.LEFT)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)

    def pop_selection(self):
        index = self.list.curselection()
        if index:
            value = self.list.get(index)
            self.list.delete(index)
            return value

    def insert_item(self, item):
        self.list.insert(tk.END, item)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        tracks = []

        db_file = 'tracks.db'
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            cursor.execute("""
          select id, singer, name from tracks
          """)
            rows = cursor.fetchall()
            for row in rows:
                id, singer, name = row
                tracks.append(str(id)+' '+singer+'-'+name)
        cursor.close()
        conn.close()
        self.frame_a = ListFrame(self, tracks,'Мои треки')
        self.frame_b = ListFrame(self,[],'Плейлист')
        self.count = 0
        self.pl_tracks=''
        self.btn_add = tk.Button(self, text="Add track",
                                   command=self.add_track)
        self.btn_remove = tk.Button(self, text="Remove track",
                                  command=self.remove_track)
        self.btn_save = tk.Button(self, text="Save playlist", command=self.save)

        self.frame_a.pack(side=tk.LEFT, padx=10, pady=10)
        self.frame_b.pack(side=tk.RIGHT, padx=10, pady=10)
        self.btn_add.pack(expand=True, ipadx=5)
        self.btn_remove.pack(expand=True, ipadx=5)
        self.btn_save.pack(expand=True, ipadx=5)


    def add_track(self):
        self.move(self.frame_a, self.frame_b)
        self.count+=1
    def remove_track(self):
        self.move(self.frame_b, self.frame_a)
        self.count-=1
    def save(self):
        if self.frame_b.entry.get()=='':
            messagebox.showerror(
            "Ошибка",
            "Введите название плейлиста")
        elif self.count==0:
            messagebox.showerror(
                "Ошибка",
                "Добавьте треки")
        else:
            for i in range(self.count):
                self.pl_tracks=self.pl_tracks+self.frame_b.list.get(i)[0]+'_'
            with sqlite3.connect('playlists.db') as conn:
                cursor = conn.cursor()
                query = """INSERT INTO playlists
                               (name, tracks)
                               VALUES (?, ?);
                               """
                cursor.execute(query, (self.frame_b.entry.get(), self.pl_tracks))
            cursor.close()
            messagebox.showinfo('Сохранение','Плейлист сохранен')
            self.destroy()



    def move(self, frame_from, frame_to):
        value = frame_from.pop_selection()
        if value:
            frame_to.insert_item(value)

if __name__ == "__main__":
    app = App()
    app.mainloop()