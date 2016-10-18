class Track:
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.path == self.path
        return False
