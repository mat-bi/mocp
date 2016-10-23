#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import curses
import time
import locale

from Player import Player
from Playlist import Playlist
from Track import Track
from EventManager import *
from Event import *
from funkcje import *
from Czas import *

locale.setlocale(locale.LC_ALL, "")

okno = curses.initscr()
curses.curs_set(0)

(wysokoscOkna, szerokoscOkna) = okno.getmaxyx()
z = u"█"
ramkaPion = u"┃"
ramkaPoziom = u"━"
ramkaRogLewyGorny = u"┏"
ramkaRogPrawyGorny = u"┓"
ramkaRogLewyDolny = u"┗"
ramkaRogPrawyDolny = u"┛"
ramkaSrodekGora = u"┳"
ramkaSrodekDol = u"┻"
play = u"▶"
pause = u"▐"
koniecPaska = u"┤"

srodek = int(szerokoscOkna / 2)

pasekPostepu = curses.newwin(1, szerokoscOkna - 4, wysokoscOkna - 1, 3)
playPause = curses.newwin(1, 3, wysokoscOkna - 1, 0)
ramkaLewa = curses.newwin(wysokoscOkna - 3, 1, 1, 0)
ramkaPrawa = curses.newwin(wysokoscOkna - 3, 1, 1, szerokoscOkna - 1)
ramkaSrodek = curses.newwin(wysokoscOkna - 3, 1, 1, srodek)
ramkaGora = curses.newwin(1, szerokoscOkna + 1, 0, 0)
ramkaDol = curses.newwin(1, szerokoscOkna + 1, wysokoscOkna - 3, 0)
tytulUtworu = curses.newwin(1, 45, wysokoscOkna - 2, 3)

(wysokoscPasek, szerokoscPasek) = pasekPostepu.getmaxyx()
(wysokoscRamkaLewa, szerokoscRamkaLewa) = ramkaGora.getmaxyx()
(wysokoscRamkaPrawa, szerokoscRamkaPrawa) = ramkaPrawa.getmaxyx()
(wysokoscRamkaGora, szerokoscRamkaGora) = ramkaGora.getmaxyx()
(wysokoscRamkaDol, szerokoscRamkaDol) = ramkaGora.getmaxyx()

blokKoncaPaska = curses.newwin(1, 2, wysokoscOkna - 1, szerokoscPasek + 3)
blokKoncaPaska.move(0, 0)
blokKoncaPaska.addstr(koniecPaska.encode("utf-8"))
blokKoncaPaska.refresh()

czasTrwania = curses.newwin(1, 7, wysokoscOkna - 2, szerokoscOkna - 16)
# czasTrwania.move(0, 0)
# czasTrwania.addstr("101:00")  # maksymalnie 6 znaków
# czasTrwania.refresh()

calkowitaDlugosc = curses.newwin(1, 9, wysokoscOkna - 2, szerokoscOkna - 9)

for i in range(0, wysokoscRamkaPrawa - 1):
    ramkaPrawa.move(i, 0)
    ramkaPrawa.addstr(ramkaPion.encode("utf-8"))
    ramkaLewa.move(i, 0)
    ramkaLewa.addstr(ramkaPion.encode("utf-8"))
    ramkaSrodek.move(i, 0)
    ramkaSrodek.addstr(ramkaPion.encode("utf-8"))

ramkaLewa.refresh()
ramkaPrawa.refresh()
ramkaSrodek.refresh()

ramkaGora.move(0, 0)
ramkaGora.addstr(ramkaRogLewyGorny.encode("utf-8"))
ramkaDol.move(0, 0)
ramkaDol.addstr(ramkaRogLewyDolny.encode("utf-8"))

for i in range(1, szerokoscRamkaGora - 2):
    ramkaGora.move(0, i)
    ramkaGora.addstr(ramkaPoziom.encode("utf-8"))
    ramkaDol.move(0, i)
    ramkaDol.addstr(ramkaPoziom.encode("utf-8"))

ramkaGora.move(0, szerokoscRamkaGora - 2)
ramkaGora.addstr(ramkaRogPrawyGorny.encode("utf-8"))
ramkaDol.move(0, szerokoscRamkaDol - 2)
ramkaDol.addstr(ramkaRogPrawyDolny.encode("utf-8"))
ramkaGora.move(0, srodek)
ramkaGora.addstr(ramkaSrodekGora.encode("utf-8"))
ramkaDol.move(0, srodek)
ramkaDol.addstr(ramkaSrodekDol.encode("utf-8"))
ramkaGora.refresh()
ramkaDol.refresh()

player = Player.get_instance()
playlist = Playlist()
czas = Czas(czasTrwania)
czas.start()
playlist.add_track(Track("/home/mat-bi/Untitled.wma"))
# playlist.add_track(Track("/home/mat-bi/tb.mp3"))
# playlist.add_track(Track("/home/mat-bi/tb2.mp3"))
# playlist.add_track(Track("/home/jg/Pulpit/Plik0.mp3"))
# playlist.add_track(Track("/home/jg/Pulpit/Plik1.mp3"))
# playlist.add_track(Track("/home/jg/Pulpit/Plik2.mp3"))
EventManager.get_instance().add_event(Event.MediaPlay, zmienTytul, tytulUtworu)
EventManager.get_instance().add_event(Event.MediaPlay, ustawCalkowitaDlugosc, calkowitaDlugosc)
EventManager.get_instance().add_event(Event.MediaPlay, odtwarzanieZnak, playPause)
EventManager.get_instance().add_event(Event.MediaPaused, pauzaZnak, playPause)
EventManager.get_instance().add_event(Event.MediaStopped, stopZnak, playPause)
EventManager.get_instance().add_event(Event.PlaylistEnded, stopZnak, playPause)
EventManager.get_instance().add_event(Event.MediaPlay, pokazujBiezacyCzas, czasTrwania)

try:
    player.current_playlist = playlist
    player.play_track()

    for i in range(0, szerokoscPasek - 1):
        pasekPostepu.move(0, i)
        pasekPostepu.addstr(z.encode("utf-8"))
        pasekPostepu.refresh()
        time.sleep(0.01)
    time.sleep(4)
    pasekPostepu.clear()
    for i in range(0, szerokoscPasek - 1):
        pasekPostepu.move(0, i)
        pasekPostepu.addstr(z.encode("utf-8"))
        pasekPostepu.refresh()
        time.sleep(0.01)
    pasekPostepu.getch()
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()
