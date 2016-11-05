import threading
from Ops import Ops
import funkcje
from Player import Player
import sys


class Pasek(threading.Thread):
    var = threading.Condition()
    dzialanie = Ops.NoOp
    liczbaBlokow = 0
    blok = u"█"
    event_table = None
    pasekPostepu = None

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
                    with funkcje.curses_mutex:
                        Pasek.pasekPostepu.move(0, 0)
                    Pasek.var.wait()
                elif Pasek.dzialanie == Ops.Play:
                    czas = int(self.event_table["length"])
                    facet_wait = czas / szerokoscPasek
                    with funkcje.curses_mutex:
                        Pasek.pasekPostepu.move(0, Pasek.liczbaBlokow)
                        Pasek.pasekPostepu.addstr(Pasek.blok.encode("utf-8"))
                        Pasek.pasekPostepu.refresh()
                    if Pasek.liczbaBlokow + 1 < szerokoscPasek - 1:
                        Pasek.liczbaBlokow += 1
                    Pasek.var.wait(facet_wait)
                elif Pasek.dzialanie == Ops.ChangeTrack:
                    Pasek.liczbaBlokow = 0

                    Pasek.dzialanie = Ops.Play
                    czas = int(self.event_table["length"])
                    facet_wait = czas / szerokoscPasek
                    with funkcje.curses_mutex:
                        Pasek.pasekPostepu.clear()
                        Pasek.pasekPostepu.move(0, 0)
                        Pasek.pasekPostepu.addstr(Pasek.blok.encode("utf-8"))
                        Pasek.pasekPostepu.refresh()
                    if Pasek.liczbaBlokow + 1 < szerokoscPasek - 1:
                        Pasek.liczbaBlokow += 1
                    Pasek.var.wait(facet_wait)
                elif Pasek.dzialanie == Ops.TimeChanged:
                    czas = int(self.event_table["length"])
                    facet_wait = czas / szerokoscPasek
                    czasUstawiany = int(self.event_table["time"])
                    pom = int(czasUstawiany / czas * szerokoscPasek)

                    if pom < Pasek.liczbaBlokow:
                        i = 0
                        with funkcje.curses_mutex:
                            Pasek.pasekPostepu.clear()
                    else:
                        i = Pasek.liczbaBlokow

                    Pasek.liczbaBlokow = pom
                    with funkcje.curses_mutex:
                        while i <= Pasek.liczbaBlokow:
                            Pasek.pasekPostepu.move(0, i)
                            Pasek.pasekPostepu.addstr(Pasek.blok.encode("utf-8"))
                            i += 1
                        Pasek.pasekPostepu.refresh()
                    Pasek.dzialanie = Ops.Play
                    Pasek.var.wait(facet_wait)
