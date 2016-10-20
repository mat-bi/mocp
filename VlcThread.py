from Ops import *
import vlc
import time
from EventManager import *
from Event import *
from Player import *


class VlcThread(threading.Thread):
    def __init__(self, player):
        threading.Thread.__init__(self)
        self.player = player

    def run(self):
        instance = vlc.Instance()
        p = vlc.MediaPlayer(str(self.player.current_playlist.current()))
        while True:
            with self.player.rlock:
                a = p.get_media().get_state()
                if a == 6:
                    p = vlc.MediaPlayer(str(self.player.current_playlist.next()))
                    p.play()
                    EventManager.get_instance().trigger_event(Event.MediaPlay)
                elif self.player._op == Ops.NoOp or self.player._op == Ops.Done:
                    pass
                else:
                    op = self.player._op
                    self.player._op = Ops.Done
                    if op == Ops.Play and a != 3:
                        if a != 4:
                            p = vlc.MediaPlayer(str(self.player.current_playlist.current()))
                        p.play()
                        EventManager.get_instance().trigger_event(Event.MediaPlay)
                    elif op == Ops.Pause:
                        p.pause()
                        EventManager.get_instance().trigger_event(Event.MediaPaused)
                    elif op == Ops.ChangePlaylist:
                        p.stop()
                        p = vlc.MediaPlayer(str(self.player.current_playlist.current()))
                        # EventManager.get_instance().trigger_event(Event.MediaStopped)
                    elif op == Ops.ChangeVolume:
                        p.audio_set_volume(self.player.volume)
                        EventManager.get_instance().trigger_event(Event.VolumeChanged)
                        # elif

                        # EventManager.get_instance().trigger_event(Event.Event.MediaEnded)
            try:
                self.player.lock.release()
                self.player.lock.release()
            except RuntimeError:
                pass
            time.sleep(0.01)
