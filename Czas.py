import threading
from Ops import Ops
from Player import Player
from sys import stderr
import funkcje


class Czas(threading.Thread):
    var = threading.Condition()
    czas = None
    dzialanie = Ops.NoOp
    event_table = None

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
        with funkcje.curses_mutex:
            Czas.czas.clear()
            Czas.czas.move(0, 0)
            Czas.czas.addstr(co)
            Czas.czas.refresh()

    @staticmethod
    def number(number):
        stderr.write("{}\n".format(number))
        stderr.flush()

    def run(self):
        kontrolerCzasu = 0
        dlugosc = 0
        while True:
            # Czas.number(1)
            with Czas.var:
                if Czas.dzialanie == Ops.NoOp:
                    # Czas.number(2)
                    Czas.var.wait()
                elif Czas.dzialanie == Ops.Pause:
                    # Czas.number(3)
                    Czas.dzialanie = Ops.NoOp
                    Czas.var.wait()
                elif Czas.dzialanie == Ops.Stop:
                    # Czas.number(4)
                    Czas.dzialanie = Ops.NoOp
                    kontrolerCzasu = 0
                    self.rysuj("00:00")
                    Czas.var.wait()
                elif kontrolerCzasu <= dlugosc and Czas.dzialanie == Ops.Play or Czas.dzialanie == Ops.ChangeTrack:
                    # Czas.number(5)
                    if Czas.dzialanie == Ops.ChangeTrack:
                        # Czas.number(6)
                        kontrolerCzasu = 0
                        dlugosc = int(self.event_table["length"])
                    Czas.dzialanie = Ops.Play
                    self.rysuj(
                        "{}:{}".format(self.normalize(int(kontrolerCzasu / 60)), self.normalize(kontrolerCzasu % 60)))
                    kontrolerCzasu += 1
                    # Czas.var.notify_all()
                    Czas.var.wait(1)
                elif kontrolerCzasu > dlugosc and Czas.dzialanie != Ops.ChangeTrack:
                    Czas.dzialanie = Ops.NoOp
                    Czas.var.wait()
                elif Czas.dzialanie == Ops.TimeChanged:
                    self.rysuj("{}:{}".format(
                        self.normalize(int(self.event_table["time"] / 60)),
                        self.normalize(self.event_table["time"] % 60)))
                    Czas.dzialanie = Ops.Play
                    kontrolerCzasu = self.event_table["time"]
                    Czas.var.wait(1)
