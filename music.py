from tkinter import ttk
from tkinter import *
import pygame
import spotipy
import spotipy.util as util
import os

class MusicPlayer:

    # constructor
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("700x500")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar()
        # self.CLIENT_ID = "018892e26d5c445083b18ad1b9d7b646"
        # self.CLIENT_SECRET = "753c83550edc4c48bedb478e2559f6f8"
        #
        # token = util.oauth2.SpotifyClientCredentials(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET)
        # cache_token = token.get_access_token()
        # sp = spotipy.Spotify(cache_token)

        # frame-ul in care va aparea vizualizarea frecventei audio

        vizframe = ttk.LabelFrame(self.root, text="Vizualizare")
        vizframe.place(x=0, y=0, width=700, height=400)

        # frame-ul pentru butoane
        buttonframe = ttk.LabelFrame(self.root, text="Controls",)
        buttonframe.place(x=0, y=400, width=700, height=100)

        # buton de play si pause
        # playbtn = Button(self.root, Image="/Users/georgianaraschitor/Documents/fac/licenta/4/PIU/play.jpg",
         #                command = self.playsong).grid(column=0)
        # playbtn = Button(self.root, Image="/Users/georgianaraschitor/Documents/fac/licenta/4/PIU/pause.jpg",
          #               command=self.pausesong).grid(column=1)
        playbtn = ttk.Button(buttonframe, text="PLAY", command=self.playsong, width=6).grid(row=0, column=0, padx=10,
                                                                                            pady=5)
        # Inserting Pause Button
        playbtn = ttk.Button(buttonframe, text="PAUSE", command=self.pausesong, width=8).grid(row=0, column=1, padx=10,
                                                                                              pady=5)
        # Inserting Unpause Button
        playbtn = ttk.Button(buttonframe, text="UNPAUSE", command=self.unpausesong, width=10).grid(row=0,
                                                                                            column=2, padx=10, pady=5)
        # get the song
        # self.file = "smu.mp3"

        # Playlist
        songsframe = ttk.LabelFrame(self.root, text="Playlist")
        songsframe.place(x=500, y=0, width=250, height=400)
        # Inserting scrollbar
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectmode=SINGLE, relief=GROOVE, height=300)
        # self.playlist = Listbox(songsframe, relief=FLAT)

        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        # Changing Directory for fetching Songs
        os.chdir("/Users/georgianaraschitor/Documents/fac/licenta/4/PIU/songs")
        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
            self.playlist.insert(END, track)

    def playsong(self):
        # pygame.init()
        # pygame.mixer.init()
        # pygame.mixer.music.load(self.file)
        # pygame.mixer.music.play()

        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        # Playing Selected Song
        pygame.mixer.music.play()

    def pausesong(self):
        # Displaying Status
        self.status.set("-Paused")
        # Paused Song
        pygame.mixer.music.pause()

    def unpausesong(self):
        # Displaying Status
        self.status.set("-Playing")
        # Playing back Song
        pygame.mixer.music.unpause()

# Creating TK Container
root = Tk()
# Passing Root to MusicPlayer Class
MusicPlayer(root)
# Root Window Looping
# root.resizable(False, False)
root.mainloop()