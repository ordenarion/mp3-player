import tkinter as tk
import sqlite3
from tkinter import messagebox
import random

# Класс -окно для создания/редактирования плейлистов
class Playlist():
    def __init__(self, window, update_list, status, current_playlist='', place=-1):
        """
        :param window:родительское окно
        :param update_list:список, в который будет вставляться имя созданного/отредактированного плейлиста
        :param status:через эту переменную можно будет изменять переменную status из класса управления плейлистами Pl_Block
        :param current_playlist:имя редактируемого плейлиста, если класс используется как окно редактирования плейлистов; '',если класс используется как окно для создание плейлиста
        :param place:место, на котором находится имя редактируемого плейлиста, если если класс используется как окно редактирования плейлистов; -1,если класс используется как окно для создание плейлиста
        """

        #Сохраним ссылки на следующие параметры в атрибутак класса, чтобы можно было использовать их в методах класса
        self.place=place
        self.current_playlist=current_playlist
        self.update_list=update_list
        self.status=status
        self.win=window

        #Фреймы класса
        self.left_frame=tk.Frame(window)# в левом фрейме будет размещен список треков, которые можно будет добавить в плейлист
        self.left_frame.pack(side=tk.LEFT)

        self.middle_frame=tk.Frame(window)# в первом среднем фрейме будет 3 кнопки
        self.middle_frame.pack(side=tk.LEFT)

        self.middle_frame2=tk.Frame(window)# во втором среднем фрейме будет еще 3 кнопки
        self.middle_frame2.pack(side=tk.LEFT)

        self.right_frame=tk.Frame(window)# в правом фрейме будет список треков плейлиста
        self.right_frame.pack(side=tk.LEFT)

        # Виджеты левого фрейма
        self.label_my_tracks=tk.Label(self.left_frame, width=60, text = 'Мои треки')# Лейбл с надписью "Мои треки"
        self.label_my_tracks.pack()


        self.my_tracks_list=tk.Listbox(self.left_frame, width=60, height=30, selectmode=tk.EXTENDED)# Список треков, которые можно добавить в плейлист
        self.my_tracks_list.pack(side=tk.LEFT)
        self.left_scroll=tk.Scrollbar(self.left_frame, command=self.my_tracks_list.yview)# Создание полосы прокрутки
        self.left_scroll.pack(side=tk.LEFT)
        self.my_tracks_list.config(yscrollcommand=self.left_scroll.set)# Добавление полосы прокрутки к списку


        #Виджеты правого фрейма
        self.label_new_pl = tk.Label(self.right_frame, width=60, text='Новый плейлист')# Лейбл с надписью "Новый плейлист"
        self.label_new_pl.pack()

        self.entry=tk.Entry(self.right_frame, width=60)# Поле ввода для названия нового плейлиста
        self.entry.insert(0, current_playlist)
        self.entry.pack(pady=10)

        self.new_playlist = tk.Listbox(self.right_frame, width=60, height=30, selectmode=tk.EXTENDED)# Список треков плейлиста
        self.new_playlist.pack(side=tk.LEFT)
        self.right_scroll = tk.Scrollbar(self.right_frame, command=self.new_playlist.yview)# Создание полосы прокрутки
        self.right_scroll.pack(side=tk.LEFT)
        self.new_playlist.config(yscrollcommand=self.right_scroll.set)# Добавление полосы прокрутки к списку


        #Виджеты второго среднего фрейма
        self.up_btn=tk.Button(self.middle_frame2, text='up', command=self.up, width=10, heigh=3)# Кнопка для перемещения трека вверх внутри списка треков плейлиста
        self.up_btn.pack(pady=20, padx=10)

        self.down_btn = tk.Button(self.middle_frame2, text='down', command=self.down, width=10, heigh=3)# Кнопка для перемещения трека вниз внутри списка треков плейлиста
        self.down_btn.pack(pady=20, padx=10)

        self.random_btn = tk.Button(self.middle_frame2, text='mix', command=self.mix, width=10, heigh=3)# Кнопка, которая располагает треки внутри плейлиста в случайном порядке
        self.random_btn.pack(pady=20, padx=10)

        #Виджеты первого среднего фрейма
        self.add_btn=tk.Button(self.middle_frame, text='add track', command=self.add, width=10, height=3)# Кнопка перемещения трека из списка доступных треков в список треков плейлиста
        self.add_btn.pack(pady=20, padx=10)

        self.remove_btn = tk.Button(self.middle_frame, text='remove track', command=self.remove, width=10, height=3)# Кнопка перемещения трека из списков трека плейлиста в список доступных треков
        self.remove_btn.pack(pady=20, padx=10)

        self.save_btn = tk.Button(self.middle_frame, text='save playlist', command=self.save_confirm, width=10, height=3)# Кнопка сохранения плейлиста
        self.save_btn.pack(pady=20, padx=10)

        #Открываем базу данных плейлистов
        with sqlite3.connect("playlists.db") as conn:
            cursor=conn.cursor()
            cursor.execute("""
            SELECT name FROM playlists
            """)# получаем список всех имен плейлистов в базе данных
            self.names=cursor.fetchall()# сохраняем их в поле класса, список имен плейлистов понадобится нам, чтобы не допустить создание нового плейлиста с уже существующим именем

            if current_playlist!='':# если это окно редактирования плейлиста
                self.names.remove((current_playlist,)) # удаляем имя редактируемого плейлиста из списка имен плейлистов

                cursor.execute("""
                        SELECT id, tracks FROM playlists
                        WHERE name= ?
                        """, (current_playlist,))# достаем индекс и список треков редактируемого плейлиста из базы данных
                self.id, self.tracks = cursor.fetchall()[0]# сохраняем их в поля класса
        cursor.close()
        conn.close()#закрываем базу данных

        self.pl_tracks = ''# в это поле будем сохранять строку из индексов треков, в ходящих в плейлист, а потом добавлять ее в базу данных


        db_file = 'tracks.db'

        with sqlite3.connect(db_file) as conn:# открываем базу данных с треками
            cursor = conn.cursor()

            if current_playlist == '':# если это окно создание нового плейдиста
                cursor.execute("""
                    select id, name from tracks
                  """)# получаем список записей из базы треков (индекс трека и его название)
                rows = cursor.fetchall()
                for row in rows:
                    id, name = row
                    self.my_tracks_list.insert(tk.END, str(id) + name)# заполняем названиями треков (слева к названию добавляем индекс) список доступных треков


            else: # если это окно редактирования плейлиста
                tracks=self.tracks.split('_')# превращаем строку с индексами треков текущего плейлиста в список индексов треков текущего плейлиста
                tracks.remove('')# удаляем из списка лишний символ
                for track in tracks:# для индексов из списка индексов треков плейлиста

                    cursor.execute(
                            """
                            select name from  tracks
                            where id = ?
                            """, (int(track),)
                    )# достаем из базы данных название трека, соответствующее индексу
                    selected=cursor.fetchall()[0]
                    self.new_playlist.insert(tk.END, track + ' ' + selected[0])# добавляем название в список треков плейлиста

                song_id=1# переменная счетчик
                while True:

                    cursor.execute(
                            """
                            select name from  tracks
                            where id = ?
                            """, (song_id,)
                        )# достаем из базы данных название трека по индексу
                    rows = cursor.fetchall()
                    if len(rows)==0:# если нет записи с соответствующим индексом, то выходим из цикла
                        break
                    for row in rows:
                        name = row[0]
                        if not(str(song_id) in tracks):# если индекс трека не в списке индексов треков плейлиста
                            self.my_tracks_list.insert(tk.END, str(song_id) + name)# добавляем трек+его индекс в список доступных треков
                    song_id=song_id+1# переходим к следующему индексу

        cursor.close()
        conn.close()# закрываем базу данных

        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)# устанавливаем функцию при закрытии окна(нажатии на красный крестик)

    #Функция перемещения трека вверх внутри списка треуов плейлиста
    def up(self):
        curr_tracks=list(self.new_playlist.curselection())# проверяем, треки на каких позициях выделены в списке треков плейлиста
        if len(curr_tracks)==1:# если выделен только 1 трек
            track=curr_tracks[0]# получаем порядковый номер трека в списке треков плейлиста
            if track!=0: # если трек не на вершине списка
                x=self.new_playlist.get(track)# запоминаем трек на даннной позиции
                y=self.new_playlist.get(track-1)# запоминаем трек выше него
                self.new_playlist.delete(track-1)# удаляем трек выше него
                self.new_playlist.insert(track-1, x)# вставляем на его место текущий трек
                self.new_playlist.delete(track)# удаляем текущий трек с изначальной позиции
                self.new_playlist.insert(track, y)# вставляем на его место трек, который был выше

    #Функция перемещения трека вниз внутри списка треуов плейлиста
    def down(self):
        curr_tracks = list(self.new_playlist.curselection())# проверяем, треки на каких позициях выделены в списке треков плейлиста
        if len(curr_tracks) == 1:# если выделен только 1 трек
            track = curr_tracks[0]# получаем порядковый номер трека в списке треков плейлиста
            if track != self.new_playlist.size()-1:# если трек не на дне списка
                x = self.new_playlist.get(track)# запоминаем трек на даннной позиции
                y = self.new_playlist.get(track + 1)# запоминаем трек ниже него
                self.new_playlist.delete(track + 1)# удаляем трек ниже него
                self.new_playlist.insert(track + 1, x)# вставляем на его место текущий трек
                self.new_playlist.delete(track)# удаляем текущий трек с изначальной позиции
                self.new_playlist.insert(track, y)# вставляем на его место трек, который был ниже

    #Функция расположение треков внутри списка треков плейлиста в случайном порядке
    def mix(self):
        size=self.new_playlist.size()# считаем количество треков в списке треков плейлиста
        if size>0:# если их больше, чем 0
            for i in range(size-1):# проходим по порядковым номерам треков
                randomi=random.randint(i, size-1)# генерируем случайное число в диапазоне от текущего порядкового номера до последнего порядкового номера
                tracki=self.new_playlist.get(i)# запоминаем трек на текущем месте
                track_randomi=self.new_playlist.get(randomi)# запоминаем трек на случайном месте, не выше места текущего трека
                self.new_playlist.delete(i)# удаляем текущий трек
                self.new_playlist.insert(i, track_randomi)# на его место ставим трек со случайного места
                self.new_playlist.delete(randomi)# удаляем трек со случайного места
                self.new_playlist.insert(randomi, tracki)# на его место ставим текущий трек


    #Функция перемещения трека из списка доступных треков в список треков плейлиста
    def add(self):
        items=list(self.my_tracks_list.curselection())# получаем список выделенных позиций в списке доступных треков
        items.reverse()# переворачиваем его
        for i in items:# для каждой позиции из списка позиций
            self.new_playlist.insert(tk.END, self.my_tracks_list.get(i))# добавляем трек с этой позиции в конец списка треков плейлиста
            self.my_tracks_list.delete(i)# удаляем трек с текущей позиции

    #Функция перемещения треков из списка треков плейлиста в список доступных треков
    def remove(self):
        items = list(self.new_playlist.curselection())# получаем список выделенных позиций в списке треков плейлиста
        items.reverse()# переворачиваем его
        for i in items:# для каждой позиции из списка позиций
            self.my_tracks_list.insert(tk.END, self.new_playlist.get(i))# добавляем трек с этой позиции в конец списка доступных треков
            self.new_playlist.delete(i)# удаляем трек с текущей позиции


    #Функция сохранения плейлиста
    def save(self):
        if self.entry.get()=='':# если поле с название трека пусто
            messagebox.showerror(
            "Ошибка",
            "Введите название плейлиста")# выдаем соответствующее сообщение

        elif (self.entry.get(),) in self.names:# если имя плейлиста уже занято
            messagebox.showerror(
                "Ошибка",
                "Плейлист с таким именем уже существует. Измените имя.")# выдаем соответствущее сообщение

        elif self.new_playlist.size()==0:# если в плейлист не добавлен ни один трек
            messagebox.showerror(
                "Ошибка",
                "Добавьте треки")# выдаем соответствующее сообщение
        else:# иначе
            for i in range(self.new_playlist.size()):#проходим по всем позициям списка треков плейлиста
                self.pl_tracks=self.pl_tracks+'_'+self.new_playlist.get(i)[0]# берем индекс трека на текущей позиции и добавляем в строку с индексам треков плейлиста символ '_' и индекс трека на текущей позиции

            with sqlite3.connect('playlists.db') as conn:#открываем базу данных плейлистов
                cursor = conn.cursor()

                if self.current_playlist=='':# если мы создавали новый плейлист
                    query = """INSERT INTO playlists
                    (name, tracks)
                    VALUES (?, ?);
                    """
                    cursor.execute(query, (self.entry.get(), self.pl_tracks))# создаем новую запись в базе данных с именем плейлиста и списком треков плейлиста
                    self.update_list.insert(tk.END, self.entry.get())# вставляем название нового плейлиста в список плейлистов в другом окне
                else:# если мы редактировали существующий плейлист
                    query = """UPDATE playlists SET name = ?
                                WHERE id = ?       
                                        """
                    cursor.execute(query, (self.entry.get(), self.id))# заменяем в записи с текущем плейлистом его имя
                    query="""UPDATE playlists SET tracks = ?
                                WHERE id = ?       
                                        """
                    cursor.execute(query, (self.pl_tracks, self.id))# заменяем в записи с текущем плейлистом список его треков
                    if self.entry.get!=self.current_playlist:# если имя редактируемого плейлиста изменилось
                        self.update_list.delete(self.place)# удаляем старое имя из списка плейлистов в другом окне
                        self.update_list.insert(self.place, self.entry.get())# вставляем на эту позиции новое имя плейлиста
            cursor.close()
            conn.close()# закрываем базу данных
            messagebox.showinfo('Сохранение','Плейлист сохранен') # выдаем сообщение, что плейлист сохранен
            self.status.remove(False)
            self.status.append(True)# меняем значение переменной status на True, чтобы в классе Pl_Block снова можно было пользоваться кнопками для управления плейлистами
            self.win.destroy()# уничтожаем окно

    #Функция сохранения с подтверждением действия
    def save_confirm(self):
        answer = messagebox.askyesno("Закрытие", "Сохранить плейлист?")# спрашиваем у пользователя, действительно ли он хочеи сохранить плейлист
        if answer:# если ответ положительный, то вызываем функцию сохранения плейлиста
            self.save()

    def on_closing(self):
        answer = messagebox.askyesno("Закрытие", "Сохранить плейлист?")# спрашиваем у пользователя, действительно ли он хочеи сохранить плейлист
        if answer:# если ответ положительный, то вызываем функцию сохранения плейлиста
            self.save()
        else:# если ответ отрицательный, просто уничтожаем окно
            self.status.remove(False)
            self.status.append(True)# меняем значение переменной status на True, чтобы в классе Pl_Block снова можно было пользоваться кнопками для управления плейлистами
            self.win.destroy()