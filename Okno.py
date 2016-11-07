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
                    if os.path.isdir(x):
                        pad.addstr(str(x)[0:szer - 1], curses.A_STANDOUT | curses.A_BOLD)
                    else:
                        pad.addstr(str(x)[0:szer - 1], curses.A_STANDOUT)
                else:
                    if os.path.isdir(x):
                        pad.addstr(str(x)[0:szer - 1], curses.A_BOLD)
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
    katalogi = []
    pliki = []
    for x in lista:
        if (os.path.isdir(x)) and (not x.startswith(".") or x.startswith("..")):
            katalogi += [x]
        elif czyMuzyczny(x):
            pliki += [x]

    katalogi = sorted(katalogi, key=str.lower)
    pliki = sorted(pliki, key=str.lower)

    nowaLista = katalogi + pliki

    return nowaLista


def wybierzMuzyczneRekurencyjnie(nazwa, wynik):
    if os.path.isdir(nazwa):
        os.chdir(nazwa)
        for x in os.listdir(os.curdir):
            wynik.append(wybierzMuzyczneRekurencyjnie(x, wynik))
        os.chdir(os.pardir)
    elif czyMuzyczny(nazwa):
        wynik.append(os.path.abspath(nazwa))


def wynikPrzefiltrowany(wynik):
    nowyWynik = []
    for x in wynik:
        if x is not None:
            nowyWynik.append(x)

    return nowyWynik


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
