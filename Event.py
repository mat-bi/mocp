from enum import Enum


class Event(Enum):
    MediaEnded = 0
    MediaPlay = 1
    MediaPaused = 2
    PlaylistEnded = 3
    PlaylistPlay = 4
    VolumeChanged = 5
