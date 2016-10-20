#!/usr/bin/env python3.4
import time

from Event import Event
from EventManager import *
from Player import Player
from Playlist import Playlist
from Track import Track


# sys.stderr = open(os.devnull,'w')

def funkcja(args):
    print(Player.get_instance().current_playlist.current()["artist"][0],
          Player.get_instance().current_playlist.current()["title"][0],
          Player.get_instance().current_playlist.current()["length"])


def funkcja2(args):
    print("MediaPaused, jeeeej")


def funkcja3(args):
    print("MediaPlayed2, jeeej")


player = Player.get_instance()
EventManager.get_instance().add_event(Event.Event.MediaPlay, funkcja)
EventManager.get_instance().add_event(Event.Event.MediaPaused, funkcja2)
EventManager.get_instance().add_event(Event.Event.MediaPlay, funkcja3)
playlist = Playlist()
# playlist.add_track(Track("/home/mat-bi/Untitled.wma"))

playlist.add_track(Track("/home/mat-bi/tb2.mp3"))
playlist.add_track(Track("/home/mat-bi/tb.mp3"))
player.current_playlist = playlist
player.play_track()

playlist2 = Playlist()
for i in range(0, 100):
    time.sleep(0.5)
    print(i, "Test")
