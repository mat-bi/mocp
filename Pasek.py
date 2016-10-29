import threading
from Ops import Ops
from Player import Player
import sys


class Pasek(threading.Thread):
    var = threading.Condition()
    dzialanie = Ops.NoOp
    liczbaBlokow = 0
    blok = u"█"

    def __init__(self, pasekPostepu):
        threading.Thread.__init__(self)
        Pasek.pasekPostepu = pasekPostepu
        self.daemon = True

    def run(self):
        while True:
            with Pasek.var:
                (wysokoscPasek, szerokoscPasek) = Pasek.pasekPostepu.getmaxyx()
                if (Pasek.dzialanie == Ops.NoOp) or (Pasek.dzialanie == Ops.Pause):
                    Pasek.var.wait()
                elif Pasek.dzialanie == Ops.Stop:
                    Pasek.liczbaBlokow = 0
                    Pasek.pasekPostepu.move(0, 0)
                elif Pasek.dzialanie == Ops.Play:
                    czas = int(Player.get_instance().current_playlist.current()["length"])
                    facet_wait = czas / szerokoscPasek
                    Pasek.pasekPostepu.move(0, Pasek.liczbaBlokow)
                    Pasek.pasekPostepu.addstr(Pasek.blok.encode("utf-8"))
                    Pasek.pasekPostepu.refresh()
                    if Pasek.liczbaBlokow + 1 < szerokoscPasek - 1:
                        Pasek.liczbaBlokow += 1
                    Pasek.var.wait(facet_wait)
                elif Pasek.dzialanie == Ops.ChangeTrack:
                    Pasek.liczbaBlokow = 0
                    Pasek.pasekPostepu.clear()
                    Pasek.dzialanie = Ops.Play
                    czas = int(Player.get_instance().current_playlist.current()["length"])
                    facet_wait = czas / szerokoscPasek
                    Pasek.pasekPostepu.move(0, 0)
                    Pasek.pasekPostepu.addstr(Pasek.blok.encode("utf-8"))
                    Pasek.pasekPostepu.refresh()
                    if Pasek.liczbaBlokow + 1 < szerokoscPasek - 1:
                        Pasek.liczbaBlokow += 1
                    Pasek.var.wait(facet_wait)
