from mutagen.easyid3 import EasyID3
from mutagen import File


class Track:
    def __init__(self, path):
        self._path = path
        self.info = EasyID3(path)
        self.length = File(path).info.length


    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def __getitem__(self, item):
        if self.info is None:
            return None
        if item == "artist":
            return self.info.get("artist")
        elif item == "length":
            return self.length
        elif item == "title":
            return self.info.get("title")
        else:
            return None


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.path == self.path
        return False

    def __str__(self):
        return self._path
