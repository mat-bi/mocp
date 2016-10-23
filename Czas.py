import threading
from Ops import Ops
from Player import Player


class Czas(threading.Thread):
    var = threading.Condition()
    czas = None
    dzialanie = Ops.NoOp

    def __init__(self, czas):
        threading.Thread.__init__(self)
        Czas.czas = czas
        self.daemon = True

    def normalize(self, liczba):
        if liczba < 10:
            return "0" + str(liczba)
        else:
            return str(liczba)

    def rysuj(self, co):
        Czas.czas.clear()
        Czas.czas.move(0, 0)
        Czas.czas.addstr(co)
        Czas.czas.refresh()

    def run(self):
        kontrolerCzasu = 0
        while True:
            with Czas.var:
                if Czas.dzialanie == Ops.NoOp:
                    Czas.var.wait()
                elif Czas.dzialanie == Ops.Pause:
                    Czas.dzialanie = Ops.NoOp
                    Czas.var.wait()
                elif Czas.dzialanie == Ops.Stop:
                    Czas.dzialanie = Ops.NoOp
                    kontrolerCzasu = 0
                    self.rysuj("00:00")
                    Czas.var.wait()
                elif kontrolerCzasu <= int(Player.get_instance().current_playlist.current()[
                                               "length"]) or Czas.dzialanie == Ops.Play or Czas.dzialanie == Ops.ChangeTrack:
                    if Czas.dzialanie == Ops.ChangeTrack:
                        kontrolerCzasu = 0
                    Czas.dzialanie = Ops.Play
                    self.rysuj(
                        "{}:{}".format(self.normalize(int(kontrolerCzasu / 60)), self.normalize(kontrolerCzasu % 60)))
                    kontrolerCzasu += 1
                    Czas.var.wait(1)
                elif kontrolerCzasu > Czas.dlugosc and Czas.dzialanie != Ops.ChangeTrack:
                    Czas.dzialanie = Ops.NoOp
                    Czas.var.wait()
