import vlc
from Playlist import Playlist

class Player(object):
    volume = 100
    currentTrack = None
    _current_playlist = Playlist()
    instance = vlc.Instance()
    mediaplayer = instance.media_list_player_new()
    _instance = None

    def __init__(self):
        #self.mediaplayer.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.next)
        pass

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

    @property
    def current_playlist(self):
        return self._current_playlist

    @current_playlist.setter
    def current_playlist(self, value):
        i = self.instance.media_list_new()
        l = 0
        for track in value.current:
            i.insert_media(self.instance.media_new(track.path), l)
            l += 1
        self.mediaplayer.set_media_list(i)

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
        self.mediaplayer.play()

    
