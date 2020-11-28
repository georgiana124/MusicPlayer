from tkinter import ttk
from tkinter import *
import pygame
import os
import threading
import time
from mutagen.mp3 import MP3


class MusicPlayer:
    # constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("700x500")
        pygame.init()
        pygame.mixer.init()
        self.paused = True
        self.played = False
        self.stop_event = threading.Event()
        self.track = StringVar()
        self.status = StringVar()

        # frame-ul in care va aparea vizualizarea frecventei audio
        vizframe = ttk.LabelFrame(self.root, text="Vizualizare")
        vizframe.place(x=0, y=0, width=700, height=400)

        # poza pana facem vizualizarea:
        poza = Label(vizframe, image=img, width=700, height=400)
        poza.config(width=700, height=400)
        poza.pack()

        self.buttonframe = ttk.LabelFrame(self.root, text="Controls", )
        self.buttonframe.place(x=0, y=380, width=700, height=70)

        self.timing = ttk.LabelFrame(self.root)
        self.timing.place(x=0, y=450, width=700, height=50)

        self.lengthlabel = ttk.Label(self.timing, text='Total Length : --:--')
        self.lengthlabel.grid(row=1, column=0, padx=10, pady=5)
        # self.lengthlabel.pack(pady=5)
        #
        self.currenttimelabel = ttk.Label(self.timing, text='Current Time : --:--', relief=GROOVE)
        self.currenttimelabel.grid(row=1, column=1, padx=10, pady=5)

        # create player control buttons
        back_btn_img = PhotoImage(file='icons/previous.gif')
        forward_btn_img = PhotoImage(file='icons/next.gif')
        play_btn_img = PhotoImage(file='icons/pause.gif')
        pause_btn_img = PhotoImage(file='icons/play.gif')

        ttk.Button(self.buttonframe, text="PLAY", command=self.playsong, width=6).grid(row=0, column=0,
                                                                                       padx=10,
                                                                                       pady=5)

        # Inserting Pause Button
        ttk.Button(self.buttonframe, text="PAUSE", command=self.pausesong, width=8).grid(row=0, column=1,
                                                                                         padx=10,
                                                                                         pady=5)
        # # Inserting Unpause Button
        # ttk.Button(self.buttonframe, text="UNPAUSE", command=self.unpausesong, width=10).grid(row=0,
        #                                                                                       column=2,
        #                                                                                       padx=10, pady=5)

        ttk.Button(self.buttonframe, text="NEXT", command=self.next, width=12).grid(row=0, column=2,
                                                                                    padx=10,
                                                                                    pady=5)

        ttk.Button(self.buttonframe, text="BACK", command=self.previous_song, width=12).grid(row=0, column=3,
                                                                                             padx=10,
                                                                                             pady=5)
        # volum

        self.volume = DoubleVar()
        self.slider = Scale(self.buttonframe, from_=0, to=30, orient=HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        pygame.mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=15, padx=5)

        # Playlist
        songsframe = ttk.LabelFrame(self.root, text="Playlist")
        songsframe.place(x=500, y=0, width=250, height=400)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        # Inserting Playlist listbox
        # self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectmode=SINGLE, relief=GROOVE, height=300)
        self.playlist = Listbox(songsframe, bg="black", fg="white", width=60, selectbackground="gray",
                                selectforeground="black",
                                height=23)
        # self.playlist = Listbox(songsframe, relief=FLAT)

        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        os.chdir("songs")
        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
            self.playlist.insert(END, track)

    def playsong(self):
        pygame.mixer.music.stop()
        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        # Playing Selected Song
        pygame.mixer.music.play()
        self.paused = False
        self.played = True
        self.show_time(self.playlist.get(ACTIVE))

    # play next song
    def next(self):
        next_one = self.playlist.curselection()
        # add one to the current song number
        next_one = next_one[0] + 1
        # grab song title from playlist
        song = self.playlist.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.playlist.selection_clear(0, END)
        self.playlist.activate(next_one)
        # set active bar to next song
        self.playlist.selection_set(next_one, last=None)

    # play previous song
    def previous_song(self):
        # get the current song tuple number
        next_one = self.playlist.curselection()
        # add one to the current song number
        next_one = next_one[0] - 1
        song = self.playlist.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.playlist.selection_clear(0, END)
        self.playlist.activate(next_one)
        # set active bar to next song
        self.playlist.selection_set(next_one, last=None)

    def pausesong(self):
        # Displaying Status
        self.status.set("-Paused")
        self.paused = True
        # Paused Song
        pygame.mixer.music.pause()

    def unpausesong(self):
        # Displaying Status
        self.status.set("-Playing")
        # Playing back Song
        pygame.mixer.music.unpause()

    def show_time(self, song):
        audio = MP3(song)
        total_length = audio.info.length
        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        # self.lengthlabel['text'] = "Total Length" + ' - ' + timeformat

        self.lengthlabel.config(text="Total Length" + ' - ' + timeformat)
        # self.currenttimelabel.config(text="Total Length" + ' - ' + timeformat)
        # self.start_count(int(round(total_length)))
        # print(int(round(total_length)))

        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()

    def start_count(self, t):
        # paused = 0
        # if self.status == "-Paused":
        #     paused = 1
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        current_time = 0
        while current_time <= t and pygame.mixer.music.get_busy():
            if self.paused:
                # continue
                self.stop_event.set()
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                # self.currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
                self.currenttimelabel.config(text="Current Time" + ' - ' + timeformat)
                time.sleep(1)
                current_time += 1

    def change_volume(self, event=None):
        v = self.volume.get()
        pygame.mixer.music.set_volume(v / 10)


if __name__ == '__main__':
    # Creating TK Container
    root = Tk()
    img = PhotoImage(file='icons/ok.gif')
    next_ = PhotoImage(file='icons/next.gif')
    prev = PhotoImage(file='icons/previous.gif')
    play = PhotoImage(file='icons/play.gif')
    pause = PhotoImage(file='icons/pause.gif')
    # Passing Root to MusicPlayer Class
    MusicPlayer(root)

    # Root Window Looping
    # root.resizable(False, False)

    def on_closing():
        pygame.mixer.music.stop()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
