import tkinter as tk



class GUI:
    def __init__(self):

        self.window = tk.Tk()
        self.window.geometry("1280x720")

        self.frame1 = tk.Frame()
        self.frame1.pack(side = "top",pady=10,padx=10)

        self.label1 = tk.Label(self.frame1,text="1",bg="green")
        self.label1.pack(ipady=275,ipadx=300,fill="both",expand = True,side="left")

        self.label2 = tk.Label(self.frame1,text="2", bg="red")
        self.label2.pack(ipady=275,ipadx=300,expand = True,fill="both",side="left")

        self.frame2 = tk.Frame()
        self.frame2.pack(fill="x",ipadx=100)

        self.label3 = tk.Label(self.frame2,text="3", bg="white")
        self.label3.pack(fill="x",ipadx=20,ipady=20,expand = 1)

        self.frame3 = tk.Frame()
        self.frame3.pack()

        self.label4 = tk.Label(self.frame3, text="3", bg="black")
        self.label4.pack(padx=0,pady=10,ipady=20,side="left")

        self.label4 = tk.Label(self.frame3, text="3", bg="yellow")
        self.label4.pack(padx=5, pady=10,ipadx=20, ipady=20,side="left")
        #self.top_frame = tk.Frame(self.window)
        #self.top_frame.pack(side="left")

        #self.bot_frame = tk.Frame(self.window)
        #self.bot_frame.pack(side = "bottom")

        #self.box = tk.Listbox(self.top_frame,selectmode = "extended",width = 100,height = 100)
        #self.box.pack(side="left",padx=15,pady=15)
        #self.scroll = tk.Scrollbar(self.top_frame,command=self.box.yview)
        #self.scroll.pack(side="left",fill="y")
        #self.box.config(yscrollcommand=self.scroll.set)

        #self.butt = tk.Button(self.bot_frame,text="ыыыы")
        #self.label = tk.Label(self.bot_frame,text=f"{self.minutes} : {self.seconds}  ",width = 100,height = 100,font = 120)
        #self.butt.pack(pady=100)
        #self.label.pack(fill="y")
        self.window.mainloop()

        #self.curr_track









class GUI2:
    def __init__(self):
        self.pause_status = True
        self.window = tk.Tk()
        self.window.geometry("1280x720")

        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=False)

        self.menu.add_cascade(label="Menu",menu = self.file_menu)

        self.file_menu.add_command(label="Add Songs",command = self.window.destroy)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")







        self.frame1 = tk.Frame()
        self.frame1.pack(side = "top",pady=10,padx=10,)

        self.box = tk.Listbox(self.frame1, selectmode="extended")
        self.box.pack(side="left",padx=15,pady=15,ipady=200,ipadx=300,fill="both",expand = True)

        self.scroll = tk.Scrollbar(self.frame1,command=self.box.yview)
        self.scroll.pack(side="left",ipady=255,)
        self.box.config(yscrollcommand=self.scroll.set)

        self.label2 = tk.Label(self.frame1,text="playlists block", bg="red")
        self.label2.pack(ipady=275,ipadx=300,expand = True,fill="both",side="left")

        self.frame2 = tk.Frame()
        self.frame2.pack(fill="x",ipadx=100)

        self.label3 = tk.Label(self.frame2,text="current time of song/soundbar", bg="white")
        self.label3.pack(fill="x",ipadx=20,ipady=10,expand = 1)

        self.frame3 = tk.Frame()
        self.frame3.pack(padx=10,expand = True,fill="both",side="left")

        self.prev_button = tk.Button(self.frame3, text="<<")
        self.prev_button.pack(padx=0,pady=10,ipady=5,ipadx=5,side="left")

        self.pause_play_button = tk.Button(self.frame3, text="||",command = self.change_pause_play_icon)
        self.pause_play_button.pack(padx=10, pady=10, ipady=10, ipadx=10, side="left")

        self.next_button = tk.Button(self.frame3, text=">>")
        self.next_button.pack(padx=0, pady=10, ipady=5, ipadx=5, side="left")

        self.song_name = tk.Label(self.frame3, text="song name",bg = "green")
        self.song_name.pack(padx=20, pady=10, ipady=10, ipadx = 400, side="left")

        self.frame4 = tk.Frame()
        self.frame4.pack(expand = True,fill="both",side="left")

        self.label4 = tk.Label(self.frame4, text="volume settings", bg="yellow")
        self.label4.pack(padx=10, pady=10,ipadx=50, ipady=20)
        #self.top_frame = tk.Frame(self.window)
        #self.top_frame.pack(side="left")

        #self.bot_frame = tk.Frame(self.window)
        #self.bot_frame.pack(side = "bottom")

        #self.box = tk.Listbox(self.top_frame,selectmode = "extended",width = 100,height = 100)
        #self.box.pack(side="left",padx=15,pady=15)
        #self.scroll = tk.Scrollbar(self.top_frame,command=self.box.yview)
        #self.scroll.pack(side="left",fill="y")
        #self.box.config(yscrollcommand=self.scroll.set)

        #self.butt = tk.Button(self.bot_frame,text="ыыыы")
        #self.label = tk.Label(self.bot_frame,text=f"{self.minutes} : {self.seconds}  ",width = 100,height = 100,font = 120)
        #self.butt.pack(pady=100)
        #self.label.pack(fill="y")
        self.window.mainloop()

    def change_pause_play_icon(self):
        if self.pause_status:
            self.pause_play_button.config(text= "ы")
            self.pause_status = False
        else:
            self.pause_play_button.config(text = "||")
            self.pause_status = True

f=GUI2()