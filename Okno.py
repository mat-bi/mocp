import curses

import locale
import os


def refresh(okno, wysokosc, srodek):
    okno.refresh(0, 0, 1, 2, wysokosc - 2, srodek - 1)


def wyswietlPliki(pad, lista, kontroler, pojemnosc):
    i = 0
    pom = int(kontroler / pojemnosc)
    if kontroler > len(lista):
        kontroler = len(lista) - 1
    for x in lista:
        if i >= pom * pojemnosc and i < (pom + 1) * pojemnosc:
            pad.move(i % pojemnosc, 0)
            if i == kontroler:
                pad.addstr(str(x), curses.A_STANDOUT)
            else:
                pad.addstr(str(x))
        i += 1
    refresh(pad, 24, 76)
    # pad.refresh(0, 0, 0, 0, 20, 75)


def filtrujListe(lista):
    nowaLista = []
    for x in lista:
        if (os.path.isdir(x) or str(x).endswith(".mp3")) and (not str(x).startswith(".") or str(x).startswith("..")):
            nowaLista += [x]

    nowaLista.sort()

    return nowaLista


def wybierzMuzyczne(lista):
    nowaLista = []
    for x in lista:
        if str(x).endswith(".mp3"):
            nowaLista += [os.path.abspath(x)]

    return nowaLista
