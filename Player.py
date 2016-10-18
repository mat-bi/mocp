import vlc
from Playlist import Playlist

class Player(object):
    volume = 100
    currentTrack = None
    currentPlaylist = Playlist()
    instance = vlc.Instance()
    mediaplayer = instance.media_list_player_new()
    _instance = None

    def __init__(self):
        #self.mediaplayer.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.next)
        i = self.instance.media_list_new()
        i.insert_media(self.instance.media_new("/home/mat-bi/Untitled.wma"),0)
        i.insert_media(self.instance.media_new("/home/mat-bi/tb2.mp3"),1)
        self.mediaplayer.set_media_list(i)

    @staticmethod
    def get_instance():
        if Player._instance is None:
            Player._instance = Player()
        return Player._instance

   # def next(self, player):
    #    Player.get_instance().mediaplayer.set_mrl(Player.get_instance().currentPlaylist.next().path)
    #    Player.get_instance().play_track()

    @property
    def volume(self):
        return self.volume

    @volume.setter
    def volume(self, value):
        self.mediaplayer.audio_set_volume(value)
        self.volume = value

    def decrease_volume(self):
        if self.volume > 2:
            self.volume -= 2
        else:
            self.volume = 0

    def increase_volume(self):
        if self.volume < 98:
            self.volume += 2
        else:
            self.volume = 100

    def pause_track(self):
        self.mediaplayer.pause()

    def stop_track(self):
        self.mediaplayer.stop()

    def play_track(self):
        #if self.currentTrack is None:
        #    self.mediaplayer.set_mrl(self.currentPlaylist.current().path)
        self.mediaplayer.play()
