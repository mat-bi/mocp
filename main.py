#!/usr/bin/env python3.4
import time

from Player import Player
from Playlist import Playlist
from Track import Track

player = Player.get_instance()
playlist = Playlist()
playlist.add_track(Track("/home/mat-bi/Untitled.wma"))
playlist.add_track(Track("/home/mat-bi/tb2.mp3"))
playlist.add_track(Track("/home/mat-bi/tb.mp3"))
player.current_playlist = playlist
player.play_track()

while True:
    pass
