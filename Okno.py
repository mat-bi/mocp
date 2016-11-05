import curses

import locale
import os


def refresh(okno, wysokosc, srodek):
    okno.refresh(0, 0, 1, 2, wysokosc - 2, srodek - 1)


def wyswietlPliki(pad, lista, kontroler, pojemnosc):
    i = 0
    (wys, szer) = pad.getmaxyx()
    pom = int(kontroler / pojemnosc)
    if kontroler > len(lista):
        kontroler = len(lista) - 1
    for x in lista:
        if i >= pom * pojemnosc and i < (pom + 1) * pojemnosc:
            pad.move(i % pojemnosc, 0)
            if i == kontroler:
                pad.addstr(str(x)[0:szer - 1], curses.A_STANDOUT)
            else:
                pad.addstr(str(x)[0:szer - 1])
        i += 1
    refresh(pad, 24, 76)
    # pad.refresh(0, 0, 0, 0, 20, 75)


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
    if plik.endswith(".mp3") or plik.endswith(".flac") or plik.endswith(".ogg"):
        return True
    else:
        return False
