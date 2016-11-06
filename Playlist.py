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
            if not isinstance(track, Track):
                track = Track(track)
            self._list.append(track)
            if len(self._list) == 1:
                self._current = self._list[0]

    def remove_track(self, track=None, number=None):
        with self.rlock:
            if isinstance(track, Track):
                self._list.remove(track)
            elif isinstance(number, int):
                del self._list[number]

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

    def selected(self, number):
        with self.rlock:
            self._current = self._list[number]
            return self.current()

    def __len__(self):
        return len(self._list)

    def __iter__(self):
        return iter(self._list)

    def __getitem__(self, item):
        return self._list[item]
