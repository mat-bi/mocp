#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import curses
import time
import locale

from Player import Player
from Playlist import Playlist
from Track import Track

locale.setlocale(locale.LC_ALL, "")

okno = curses.initscr()
curses.curs_set(0)

(h, w) = okno.getmaxyx()
z = u"▀"
ramkaPion = u"┃"
ramkaPoziom = u"━"
ramkaRogLewyGorny = u"┏"
ramkaRogPrawyGorny = u"┓"

pasek = curses.newwin(1, w, h - 1, 0)
ramkaLewa = curses.newwin(h - 2, 1, 1, 0)
ramkaPrawa = curses.newwin(h - 2, 1, 1, w - 1)
ramkaGora = curses.newwin(1, w, 0, 0)

# okno.addstr("jakis napis")
# okno.refresh()

for i in range(0, h - 3):
    ramkaLewa.move(i, 0)
    ramkaLewa.addstr(ramkaPion.encode("utf-8"))
    # ramkaPrawa.move(i, 2)
    # ramkaPrawa.addstr(ramkaPion.encode("utf-8"))

ramkaLewa.refresh()
ramkaPrawa.refresh()

ramkaGora.move(0, 0)
ramkaGora.addstr(ramkaRogLewyGorny.encode("utf-8"))

for i in range(1, w - 2):
    ramkaGora.move(0, i)
    ramkaGora.addstr(ramkaPoziom.encode("utf-8"))

ramkaGora.move(0, w - 2)
ramkaGora.addstr(ramkaRogPrawyGorny.encode("utf-8"))
ramkaGora.refresh()

player = Player.get_instance()
playlist = Playlist()
playlist.add_track(Track("/home/jg/Pulpit/Plik0.flac"))
playlist.add_track(Track("/home/jg/Pulpit/Plik1.wma"))
playlist.add_track(Track("/home/jg/Pulpit/Plik2.wma"))

try:
    player.current_playlist = playlist
    player.play_track()
    for i in range(0, w - 1):
        pasek.move(0, i)
        pasek.addstr(z.encode("utf-8"))
        pasek.refresh()
        time.sleep(0.05)
    time.sleep(4)
    pasek.clear()
    for i in range(0, w - 1):
        pasek.move(0, i)
        pasek.addstr(z.encode("utf-8"))
        pasek.refresh()
        time.sleep(0.05)
    pasek.getch()
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()



# playlist.add_track(Track("/home/mat-bi/Untitled.wma"))
# playlist.add_track(Track("/home/mat-bi/tb2.mp3"))
# playlist.add_track(Track("/home/mat-bi/tb.mp3"))
