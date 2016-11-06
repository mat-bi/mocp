#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import curses
import time
import locale
import os
import sys

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

# os.close(2)
# os.open("/dev/null", os.O_WRONLY)
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
# playlist = Playlist([])
os.chdir(os.path.expanduser('~'))
leweOkno = curses.newpad(wysokoscOkna - 2, srodek - 2)
(wysokoscLeweOkno, szerokoscLeweOkno) = leweOkno.getmaxyx()
praweOkno = curses.newpad(wysokoscOkna - 2, srodek - 2)
(wysokoscPraweOkno, szerokoscPraweOkno) = praweOkno.getmaxyx()
# refreshPrawe(praweOkno, wysokoscPraweOkno, szerokoscOkna, srodek)
kontroler = 0
listaPom = [os.pardir] + os.listdir(os.curdir)
lista = filtrujListe(listaPom)
# stderr.write(str(lista))
# stderr.flush()
stosKatalogow = [0]
wyswietlPliki(leweOkno, lista, kontroler)
czas = Czas(czasTrwania)
czas.start()
pasek = Pasek(pasekPostepu)
pasek.start()
# playlist.add_track(Track("/home/mat-bi/Untitled.wma"))
# playlist.add_track(Track("/home/mat-bi/tb.mp3"))
# playlist.add_track(Track("/home/mat-bi/tb2.mp3"))
# playlist.add_track(Track("/home/jg/Pulpit/Plik4.mp3"))
# playlist.add_track(Track("/home/jg/Pulpit/Plik0.mp3"))
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
EventManager.get_instance().add_event(Event.TimeChanged, ustawPrzestawionyCzas)
EventManager.get_instance().add_event(Event.TimeChanged, ustawPrzestawionyPasek)

try:
    # player.current_playlist = playlist
    # player.play_track()
    glownaPlaylista = []
    kontrolerPrawy = 0
    przelacznikKontrolera = 0
    while True:
        c = pasekPostepu.getch()
        if c == 65:  # strzałka w górę
            if przelacznikKontrolera == 0:
                if kontroler > 0:
                    kontroler -= 1
                    wyswietlPliki(leweOkno, lista, kontroler)
            elif przelacznikKontrolera == 1:
                if kontrolerPrawy > 0:
                    kontrolerPrawy -= 1
                    wyswietlPlayliste(praweOkno, glownaPlaylista, kontrolerPrawy, srodek, szerokoscOkna)
        elif c == 66:  # strzałka w dół
            if przelacznikKontrolera == 0:
                if not kontroler >= len(lista) - 1:
                    kontroler += 1
                    wyswietlPliki(leweOkno, lista, kontroler)
            elif przelacznikKontrolera == 1:
                if not kontrolerPrawy >= len(glownaPlaylista) - 1:
                    kontrolerPrawy += 1
                    wyswietlPlayliste(praweOkno, glownaPlaylista, kontrolerPrawy, srodek, szerokoscOkna)
        elif c == 10: # Enter
            if przelacznikKontrolera == 0:
                if os.path.isdir(lista[kontroler]):
                    os.chdir(lista[kontroler])
                    listaPom = [os.pardir] + os.listdir(os.curdir)
                    lista = filtrujListe(listaPom)
                    if kontroler == 0:
                        kontroler = stosKatalogow.pop()
                    else:
                        stosKatalogow.append(kontroler)
                        kontroler = 0
                    wyswietlPliki(leweOkno, lista, kontroler)
                elif os.path.isfile(lista[kontroler]) and czyMuzyczny(lista[kontroler]):
                    listaOdtw = wybierzMuzyczne(lista[kontroler:len(lista) + 1])
                    playlista = Playlist(listaOdtw)
                    player.stop_track()
                    player.current_playlist = playlista
                    player.play_track()
                    pass
            elif przelacznikKontrolera == 1:
                player.stop_track()
                player.current_playlist = Playlist(glownaPlaylista)
                player.selected_track(kontrolerPrawy)
                player.stop_track()
                player.play_track()
        elif c == 115:  # zatrzymanie odtwarzania (znak "s")
            player.stop_track()
            with funkcje.curses_mutex:
                pasekPostepu.clear()
                pasekPostepu.refresh()
        elif c == 32:  # pauza (spacja)
            player.pause_track()
            # sys.stderr.write(str(player.stan()))
            # sys.stderr.flush()
        elif c == 113:  # wyjście z programu
            stderr.flush()
            break
        elif c == 68:
            player.decrease_time()
        elif c == 67:
            player.increase_time()
        elif 48 <= c <= 57:
            player.selected_track(c - 48)
            player.stop_track()
            player.play_track()
        elif c == 97 and przelacznikKontrolera == 0:  # litera "a" - dodanie utworu/katalogu do playlisty
            if czyMuzyczny(lista[kontroler]):
                glownaPlaylista.append(os.path.abspath(lista[kontroler]))
                wyswietlPlayliste(praweOkno, glownaPlaylista, -1, srodek, szerokoscOkna)
            if kontroler + 1 < len(lista):
                kontroler += 1
                wyswietlPliki(leweOkno, lista, kontroler)
        elif c == 100 and przelacznikKontrolera == 1:   # litera "d" - usunięcie utworu z playlisty
            # TUTAJ TRZEBA ZROBIĆ USUWANIE UTWORU Z RZECZYWISTEJ PLAYLISTY, PÓKI CO USUWA TYLKO Z WYŚWIETLANIA
            glownaPlaylista.remove(glownaPlaylista[kontrolerPrawy])
            if kontrolerPrawy >= len(glownaPlaylista):
                kontrolerPrawy -= 1
            wyswietlPlayliste(praweOkno, glownaPlaylista, kontrolerPrawy, srodek, szerokoscOkna)
        elif c == 117 and przelacznikKontrolera == 1:   # litera "u" - przesunięcie utworu w górę listy
            if kontrolerPrawy > 0:
                glownaPlaylista[kontrolerPrawy - 1], glownaPlaylista[kontrolerPrawy] = glownaPlaylista[kontrolerPrawy], glownaPlaylista[kontrolerPrawy - 1]
                kontrolerPrawy -= 1;
                wyswietlPlayliste(praweOkno, glownaPlaylista, kontrolerPrawy, srodek, szerokoscOkna)
        elif c == 106 and przelacznikKontrolera == 1:  # litera "j" - przesunięcie utworu w dół listy
            if kontrolerPrawy < len(glownaPlaylista) - 1:
                glownaPlaylista[kontrolerPrawy + 1], glownaPlaylista[kontrolerPrawy] = glownaPlaylista[kontrolerPrawy], glownaPlaylista[kontrolerPrawy + 1]
                kontrolerPrawy += 1;
                wyswietlPlayliste(praweOkno, glownaPlaylista, kontrolerPrawy, srodek, szerokoscOkna)
        elif c == 9:  # tabulator - przechodzenie między wirtualnymi oknami
            if przelacznikKontrolera == 0 and len(glownaPlaylista) > 0:
                przelacznikKontrolera = 1
                wyswietlPliki(leweOkno, lista, -1)
                wyswietlPlayliste(praweOkno, glownaPlaylista, kontrolerPrawy, srodek, szerokoscOkna)
            elif przelacznikKontrolera == 1:
                przelacznikKontrolera = 0
                wyswietlPliki(leweOkno, lista, kontroler)
                wyswietlPlayliste(praweOkno, glownaPlaylista, -1, srodek, szerokoscOkna)
        # stderr.write(u"Żyję!\n")
        stderr.flush()

except KeyboardInterrupt:
    pass
finally:
    stderr.flush()
    curses.endwin()
