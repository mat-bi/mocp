from VlcThread import *
from Playlist import *
from Ops import *


class Player(object):
    _instance = None
    rlock = threading.RLock()
    lock = threading.Lock()


    def __init__(self):
        # self.mediaplayer.event_manager().event_attach(vlc.EventType.MediaPlayerEndReached, self.next)
        self._current_playlist = Playlist([])
        self._op = Ops.Done
        self._time = 0
        EventManager.get_instance()
        thread = VlcThread(self)
        thread.setDaemon(True)
        thread.start()

    def wait(self):
        self.lock.acquire()
        self.lock.acquire()

    def decrease_time(self):
        self.time -= 3

    def increase_time(self):
        self.time += 3

    @property
    def time(self):
        with self.rlock:
            return self._time

    @time.setter
    def time(self, time):
        with self.rlock:
            if time > self.current_playlist.current()["length"]:
                time = self.current_playlist.current()["length"]
            if time < 0:
                time = 0
            self._op = Ops.TimeChanged
            self._time = time
        self.wait()

    @staticmethod
    def get_instance():
        with Player.rlock:
            if Player._instance is None:
                Player._instance = Player()
            return Player._instance

            # def next(self, player):

    #    Player.get_instance().mediaplayer.set_mrl(Player.get_instance().currentPlaylist.next().path)
    #    Player.get_instance().play_track()

    @property
    def volume(self):
        with self.rlock:
            return self._volume

    def selected_track(self, number):
        with self.rlock:
            return self.current_playlist.selected(number)

    @volume.setter
    def volume(self, value):
        with self.rlock:
            if value < 0:
                value = 0
            elif value > 100:
                value = 100
            self._op = Ops.ChangeVolume
            self._volume = value
        self.wait()

    @property
    def current_playlist(self):
        with self.rlock:
            return self._current_playlist

    @current_playlist.setter
    def current_playlist(self, value):
        with self.rlock:
            self._op = Ops.ChangePlaylist
            self._current_playlist = value
        self.wait()

    def decrease_volume(self):
        with self.rlock:
            self.volume -= 2

    def increase_volume(self):
        with self.rlock:
            self.volume += 2

    def pause_track(self):
        with self.rlock:
            self._op = Ops.Pause
        self.wait()

    def stop_track(self):
        with self.rlock:
            self._op = Ops.Stop
        self.wait()

    def play_track(self):
        with self.rlock:
            self._op = Ops.Play
        self.wait()

    def stan(self):
        with self.rlock:
            return self._op


