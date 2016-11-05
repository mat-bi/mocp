import threading
from Track import Track
from sys import stderr


class Playlist():
    def __init__(self, lista):
        list = []
        for i in lista:
            if isinstance(i, Track):
                list.append(i)
            else:
                list.append(Track(i))
        self._list = list
        if len(lista) > 0:
            self._current = self._list[0]
        else:
            self._current = None
        # stderr.write("{}\n".format(str(lista)))
        stderr.flush()
        self.rlock = threading.RLock()

    def add_track(self, track):
        with self.rlock:
            self._list.append(track)
            if len(self._list) == 1:
                self._current = self._list[0]

    def remove_track(self, track):
        with self.rlock:
            self._list.remove(track)

    def current(self):
        with self.rlock:
            return self._current

    def next(self):
        with self.rlock:
            index = self._list.index(self._current)
            if index == len(self._list) - 1:
                self._current = None
            else:
                self._current = self._list[index + 1]
            return self.current()

    def previous(self):
        with self.rlock:
            index = self._list.index(self._current)
            if index == 0:
                self._current = None
            else:
                self._current = self._list[index - 1]
            return self.current()
