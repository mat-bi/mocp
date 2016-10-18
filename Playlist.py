class Playlist:
    _current = None

    def __init__(self):
        self._list = []

    def add_track(self, track):
        self._list.append(track)
        if len(self._list) == 1:
            self._current = track

    def previous(self):
        return self._list[self._list.index(self._current)-1]

    def next(self):
        return  self._list[self._list.index(self._current)+1]

    def current(self):
        return self._current