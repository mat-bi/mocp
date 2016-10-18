import time

from Player import Player
from Playlist import Playlist
from Track import Track

player = Player.get_instance()
#player.currentPlaylist = Playlist()
player.currentPlaylist.add_track(Track("/home/mat-bi/Untitled.wma"))
player.currentPlaylist.add_track(Track("/home/mat-bi/tb2.mp3"))
player.play_track()



while True:
    pass



