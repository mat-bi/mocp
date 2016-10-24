from enum import Enum


class Event(Enum):
    MediaEnded = 0
    MediaPlay = 1
    MediaPaused = 2
    MediaStopped = 3
    PlaylistEnded = 4
    PlaylistPlay = 5
    VolumeChanged = 6