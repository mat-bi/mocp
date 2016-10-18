class Playlist:
    _current = None

    def __init__(self):
        self._list = []

    def add_track(self, track):
        self._list.append(track)

    @property
    def current(self):
        return self._list
