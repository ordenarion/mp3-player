import tkinter as tk
from tkinter import messagebox
import sqlite3

from playlist_create import Playlist

#Класс - окно управление плейлистами
class Pl_Block:
    def __init__(self, window):
        self.status=[True]#это поле позволит отслеживать, открыты ли какие-то из окн редактирования, создания или просмотра плейлиста, чтобы не дать пользователю открыть другие окна, пока тот не закроет эти
        self.win=window
#        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)#Изменяем функцию при закрытии родительского окна, чтобы оно запросило подтверждение при закрытии и закрылось только в том случае, если нет открытых окон

        #Фреймы класса
        self.left_frame=tk.Frame(window)#Левый фрейм
        self.left_frame.pack(side=tk.LEFT)

        self.right_frame=tk.Frame(window)#Правый фрейм
        self.right_frame.pack(side=tk.RIGHT)

        #Виджеты левого фрейма
        self.label=tk.Label(self.left_frame, width=40, text='Мои плейлисты')#Лейбл с надписью "Мои Плейлисты"
        self.label.pack()

        self.pl_list=tk.Listbox(self.left_frame, height=34 , width=40)#Список плейлистов
        self.pl_list.pack(side=tk.LEFT)

        self.scroll=tk.Scrollbar(self.left_frame, command=self.pl_list.yview)#Создание полосы прокрутки
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.pl_list.config(yscrollcommand=self.scroll.set)#Добавление полосы прокрутки к списку плейлистов

        #Виджеты правого фрейма
        self.view_btn=tk.Button(self.right_frame, text='view', command=self.pl_view, width=20)#Кнопка просмотра плейлиста
        self.view_btn.pack()

        self.edit_btn = tk.Button(self.right_frame, text='edit', command=self.pl_edit, width=20)#Кнопка редактирования плейлиста
        self.edit_btn.pack()

        self.del_btn = tk.Button(self.right_frame, text='delete', command=self.pl_dell, width=20)#Кнопка удаления плейлиста
        self.del_btn.pack()


        self.create_btn = tk.Button(self.right_frame, text='create new playlist', command=self.pl_create, width=20)#Кнопка создания плейлиста
        self.create_btn.pack()

        with sqlite3.connect('playlists.db') as conn:#Открываем базу данных плейлистов
            cursor=conn.cursor()
            cursor.execute(
                        """
                        select name from playlists
                        """
                    )#Получаем имена всех плейлистов из базы данных
            pl_name = cursor.fetchall()
            for i in pl_name:
                self.pl_list.insert(tk.END, i[0])#Вставляем имена плейлистов в список плейлистов
        cursor.close()
        conn.close()#Закрываем базу данных

    #Функция при закрытии родительского окна управления плейлистами
    def on_closing(self):
        answer = messagebox.askyesno("Закрытие", "Вы действительно хотите закрыть окно управления плейлистами?")#Запрашиваем подтверждение закрытия окна
        if answer:#Если ответ положительный
            if self.status[0]:#Если нет открытых окон
                self.win.destroy()#Уничтожаем родительское окно
            else:#Иначе
                messagebox.showerror(
                    "Ошибка",
                    "Закройте другие окна")#Просим пользователя закрыть другие окна


    #Функция изменения поля status и закрытия окна(просмотра, редактирования, создания) будет работать при закрытии одного из окн(нажатии на красный крестик)
    def true_status(self):
        self.status.remove(False)
        self.status.append(True)
        self.new_window.destroy()

    #Функция просмотра плейлиста
    def pl_view(self):
        if not self.status[0]:#Если статус [False], то ничего не происходит
            return

        if len(list(self.pl_list.curselection()))>0:#Если в списке выделен какой-то плейлист
            # Меняем статус на [False], чтобы другие кнопки временно не работали
            self.status.remove(True)
            self.status.append(False)
            self.new_window=tk.Tk()#Создаем новое окно
            pl_name=self.pl_list.get(list(self.pl_list.curselection())[0])#Получаем имя выделенного плейлиста
            label=tk.Label(self.new_window, width=60, text=pl_name)#Создаем лейбл с именем выделенного плейлиста
            label.pack()

            tracks=tk.Listbox(self.new_window, height=40 , width=60)#Создаем список треков выделенного плейлиста
            tracks.pack(side=tk.LEFT)
            scroll=tk.Scrollbar(self.new_window, command=tracks.yview())#Создаем полосу прокрутки
            scroll.pack(side=tk.LEFT, fill=tk.Y)
            tracks.config(yscrollcommand=scroll.set)#Добавляем полосу прокрутки к списку треков

            with sqlite3.connect('playlists.db') as conn:#Открываем базу данных плейлистов
                cursor=conn.cursor()
                cursor.execute("""
                select tracks from playlists
                where name = ?
                """, (pl_name,))#Получаем строку индексов треков для данного плейлиста
                curr_tracks=cursor.fetchall()
                curr_tracks=(curr_tracks[0][0]).split('_')#Превращаем строку в список индексов
            cursor.close()
            conn.close()#Закрываем базу данных плейлистов

            with sqlite3.connect('tracks.db') as conn:#Открываем базу данных треков
                cursor=conn.cursor()
                for i in curr_tracks:#Проходимся по списку индексов треков
                    if i!="":
                        cursor.execute(
                            """
                            select name from  tracks
                            where id = ?
                            """, (int(i),)
                        )#Достаем название трека с соответствующим индексом из базы данных
                        for j in cursor.fetchall():
                            tracks.insert(tk.END, j[0])#Вставляем в список треков выделенного плейлиста
            cursor.close()
            conn.close()#Закрываем базу данных треков

            self.new_window.protocol("WM_DELETE_WINDOW", self.true_status)#Изменяем комманду при закрытии окна(нажатии на крестик)
            self.new_window.mainloop()#Запускаем цикл окна

    #Функция редактирования плейлиста
    def pl_edit(self):
        if not self.status[0]:#Если статус [False], то ничего не происходит
            return

        if len(list(self.pl_list.curselection())) > 0:  # Если в списке выделен какой-то плейлист
        # Меняем статус на [False], чтобы другие кнопки временно не работали
            self.status.remove(True)
            self.status.append(False)
            new_window=tk.Tk()#Создаем новое окно
            pl_name = self.pl_list.get(list(self.pl_list.curselection())[0])#Получаем имя выделенного трека
            block=Playlist(new_window, self.pl_list, self.status, pl_name, list(self.pl_list.curselection())[0])#Создаем объект класса Playlist в этом окне
            new_window.mainloop()#Запускаем цикл окна

    #Функция удаления плейлиста
    def pl_dell(self):
        if not self.status[0]:#Если статус [False], то ничего не происходит
            return
        if len(list(self.pl_list.curselection())) > 0:#Если в списке выделен какой-то плейлист
            i=list(self.pl_list.curselection())[0]#Получаем позицию выбранного плейлиста в списке плейлистов
            name=self.pl_list.get(i)#Получаем имя этого плейлиста
            answer = messagebox.askyesno("Удаление", "Вы действительно хотите удалить плейлист "+name+"?")#Запрашиваем подтверждение удаления выбранного плейлиста
            if answer:#Если ответ положительный
                with sqlite3.connect("playlists.db") as conn:#Открываем базу данных плейлистов
                    cursor=conn.cursor()
                    cursor.execute("""
                DELETE FROM playlists
                WHERE name = ?
                """,(name,))#Удаляем плейлист с данным именем из базы данных
                cursor.close()
                conn.close()#Закрываем базу данных плейлистов
                self.pl_list.delete(i)#Удаляем имя плейлиста в списке плейлистов


    #Функция создания нового плейлиста
    def pl_create(self):
        if not self.status[0]:#Если статус [False], то ничего не происходит
            return

        with sqlite3.connect('tracks.db') as conn:
            cursor=conn.cursor()
            cursor.execute("""
                SELECT name FROM tracks
                """)
            rows=cursor.fetchall()
        cursor.close()
        conn.close()
        if len(rows)==0:
            messagebox.showerror(
                "Ошибка",
                "Добавьте треки")
            return

        # Меняем статус на [False], чтобы другие кнопки временно не работали
        self.status.remove(True)
        self.status.append(False)
        new_window=tk.Tk()#Создаем новое окно
        block=Playlist(new_window, self.pl_list, self.status)#Создаем экземпляр класса Playlist в этом окне
        new_window.mainloop()#Запускаем цикл окна




