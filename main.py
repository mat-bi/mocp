#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import curses
import time
import locale
import os

from Player import Player
from Playlist import Playlist
from Track import Track
from EventManager import *
from Event import *
from funkcje import *
from Czas import *
from Pasek import *
from Okno import *

locale.setlocale(locale.LC_ALL, "")

okno = curses.initscr()
curses.curs_set(0)
curses.noecho()
curses.cbreak()

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
playlist = Playlist([])
os.chdir(os.path.expanduser('~'))
leweOkno = curses.newpad(wysokoscOkna, srodek - 2)
kontroler = 0
listaPom = [os.pardir] + os.listdir(os.curdir)
lista = filtrujListe(listaPom)
stosKatalogow = [0]
wyswietlPliki(leweOkno, lista, kontroler, wysokoscOkna - 4)
czas = Czas(czasTrwania)
czas.start()
pasek = Pasek(pasekPostepu)
pasek.start()
# playlist.add_track(Track("/home/mat-bi/Untitled.wma"))
# playlist.add_track(Track("/home/mat-bi/tb.mp3"))
# playlist.add_track(Track("/home/mat-bi/tb2.mp3"))
playlist.add_track(Track("/home/jg/Pulpit/Plik4.mp3"))
playlist.add_track(Track("/home/jg/Pulpit/Plik0.mp3"))
# playlist.add_track(Track("/home/jg/Pulpit/Plik1.mp3"))
# playlist.add_track(Track("/home/mat-bi/Pobrane/Plik4.mp3"))
EventManager.get_instance().add_event(Event.MediaStarted, zmienTytul, tytulUtworu)
EventManager.get_instance().add_event(Event.MediaStarted, ustawCalkowitaDlugosc, calkowitaDlugosc)
EventManager.get_instance().add_event(Event.MediaPlay, odtwarzanieZnak, playPause)
EventManager.get_instance().add_event(Event.MediaStarted, odtwarzanieZnak, playPause)
EventManager.get_instance().add_event(Event.MediaPaused, pauzaZnak, playPause)
EventManager.get_instance().add_event(Event.MediaStopped, stopZnak, playPause)
EventManager.get_instance().add_event(Event.PlaylistEnded, stopZnak, playPause)
EventManager.get_instance().add_event(Event.MediaPlay, pokazujBiezacyCzas, czasTrwania)
EventManager.get_instance().add_event(Event.MediaStarted, pokazujPasek, pasekPostepu)
EventManager.get_instance().add_event(Event.MediaStarted, nowyUtwor)

try:
    player.current_playlist = playlist
    player.play_track()
    while True:
        c = pasekPostepu.getch()
        leweOkno.clear()
        if c == 65:  # strzałka w górę
            if kontroler > 0:
                kontroler -= 1
            wyswietlPliki(leweOkno, lista, kontroler, wysokoscOkna - 4)
        elif c == 66:  # strzałka w dół
            if not kontroler >= len(lista) - 1:
                kontroler += 1
            wyswietlPliki(leweOkno, lista, kontroler, wysokoscOkna - 4)
        elif c == 10:  # Enter
            if os.path.isdir(lista[kontroler]):
                os.chdir(lista[kontroler])
                listaPom = [os.pardir] + os.listdir(os.curdir)
                lista = filtrujListe(listaPom)
                if kontroler == 0:
                    kontroler = stosKatalogow.pop()
                else:
                    stosKatalogow.append(kontroler)
                    kontroler = 0
                wyswietlPliki(leweOkno, lista, kontroler, wysokoscOkna - 4)
            elif os.path.isfile(lista[kontroler]) and czyMuzyczny(lista[kontroler]):
                playlista = Playlist(wybierzMuzyczne(lista[kontroler:len(lista) + 1]))
                player.stop_track()
                player.current_playlist = playlista
                player.play_track()
                pass
        elif c == 115:  # zatrzymanie odtwarzania (znak "s")
            player.stop_track()
            pasekPostepu.clear()
            pasekPostepu.refresh()
        elif c == 32:  # pauza (spacja)
            player.pause_track()
            sys.stderr.write(str(player.stan()))
            sys.stderr.flush()
        elif c == 113:  # wyjście z programu
            break
            # wyswietlPliki(leweOkno, lista, kontroler, wysokoscOkna - 4)
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()
