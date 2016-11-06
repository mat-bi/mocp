import curses

import funkcje
import locale
import os
from sys import stderr


def refresh(okno, wysokosc, srodek):
    okno.refresh(0, 0, 1, 2, wysokosc - 2, srodek - 1)


def refreshPrawe(okno, wysokosc, szerokosc, srodek):
    okno.refresh(0, 0, 1, srodek + 2, wysokosc - 2, szerokosc - 3)


def wyswietlPliki(pad, lista, kontroler):
    with funkcje.curses_mutex:
        pad.clear()
        i = 0
        (wys, szer) = pad.getmaxyx()
        pojemnosc = wys - 2
        pom = int(kontroler / pojemnosc)
        if kontroler > len(lista):
            kontroler = len(lista) - 1
        for x in lista:
            if pom * pojemnosc <= i < (pom + 1) * pojemnosc:
                pad.move(i % pojemnosc, 0)
                if i == kontroler:
                    pad.addstr(str(x)[0:szer - 1], curses.A_STANDOUT)
                else:
                    pad.addstr(str(x)[0:szer - 1])
            i += 1
        refresh(pad, wys, szer)


def wyswietlPlayliste(pad, lista, kontroler, srodek, szerokosc):
    with funkcje.curses_mutex:
        pad.clear()
        i = 0
        (wys, szer) = pad.getmaxyx()
        pojemnosc = wys - 2
        pom = int(kontroler / pojemnosc)
        if kontroler > len(lista):
            kontroler = len(lista) - 1
        for x in lista:
            if pom * pojemnosc <= i < (pom + 1) * pojemnosc:
                pad.move(i % pojemnosc, 0)
                if i == kontroler:
                    pad.addstr(os.path.basename(str(x))[0:szer - 1], curses.A_STANDOUT)
                else:
                    pad.addstr(os.path.basename(str(x))[0:szer - 1])
            i += 1
            refreshPrawe(pad, wys, szerokosc, srodek)


def filtrujListe(lista):
    nowaLista = []
    for x in lista:
        if (os.path.isdir(x) or czyMuzyczny(x)) and (not x.startswith(".") or x.startswith("..")):
            nowaLista += [x]

    nowaLista.sort()

    return nowaLista


def wybierzMuzyczne(lista):
    nowaLista = []
    for x in lista:
        if czyMuzyczny(x):
            nowaLista += [os.path.abspath(x)]

    return nowaLista


def czyMuzyczny(plik):
    if os.path.isfile(plik) and (plik.endswith(".mp3") or plik.endswith(".flac") or plik.endswith(".ogg")):
        return True
    else:
        return False
