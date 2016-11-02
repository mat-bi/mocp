#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import curses
import time
import locale
from Czas import *
from Pasek import *

from Player import Player

pause = u"▐"
play = u"▶"
stop = u"■"


def zmienTytul(
        tytulUtworu):  # ustawia tytuł bieżącego utworu w oknie wirtualnym "tytulUtworu" (przy zdarzeniu "MediaPlay")
    t = str(Player.get_instance().current_playlist.current()["title"][0])
    tytulUtworu.clear()
    tytulUtworu.addstr(t)
    tytulUtworu.refresh()
    return


def pauzaZnak(
        playPause):  # ustawia znak odtwarzania "pause" w oknie wirtualnym "playPause" (przy zdarzeniu "MediaPause")
    playPause.clear()
    playPause.move(0, 0)
    playPause.addstr(pause.encode("utf-8"))
    playPause.move(0, 1)
    playPause.addstr(pause.encode("utf-8"))
    playPause.refresh()
    with Czas.var:
        Czas.dzialanie = Ops.Pause
        Czas.var.notify_all()
    with Pasek.var:
        Pasek.dzialanie = Ops.Pause
        Pasek.var.notify_all()



def odtwarzanieZnak(
        playPause):  # ustawia znak odtwarzania "play" w oknie wirtualnym "playPause" (przy zdarzeniu "MediaPlay")
    playPause.clear()
    playPause.move(0, 1)
    playPause.addstr(play.encode("utf-8"))
    playPause.refresh()
    with Czas.var:
        Czas.dzialanie = Ops.Play
        Czas.var.notify_all()
    with Pasek.var:
        Pasek.dzialanie = Ops.Play
        Pasek.var.notify_all()

def stopZnak(
        playPause):  # ustawia znak odtwarzania "stop" w oknie wirtualnym "playPause" (przy zdarzeniu "MediaStopped")
    playPause.clear()
    playPause.move(0, 1)
    playPause.addstr(stop.encode("utf-8"))
    playPause.refresh()
    Czas.dzialanie = Ops.Stop
    Pasek.dzialanie = Ops.Stop


def ustawCalkowitaDlugosc(
        calkowitaDlugosc):  # ustawia całkowitą długość utworu w oknie wirtualnym "calkowitaDlugosc" (przy zdarzeniu "MediaPlay")
    dlugosc = int(Player.get_instance().current_playlist.current()["length"])
    minuty = int(dlugosc / 60)
    sekundy = int(dlugosc % 60)

    if minuty < 10:
        minutyString = "0" + str(minuty)
    else:
        minutyString = str(minuty)

    if sekundy < 10:
        sekundyString = "0" + str(sekundy)
    else:
        sekundyString = str(sekundy)

    dlugosc = "/ " + minutyString + ":" + sekundyString

    calkowitaDlugosc.move(0, 0)
    calkowitaDlugosc.addstr(dlugosc)
    calkowitaDlugosc.refresh()


def pokazujBiezacyCzas(
        czasTrwania):  # ustawia biezący czas utworu w oknie wirtualnym "czasTrwania" (przy zdarzeniu "MediaPlay")
    with Czas.var:
        Czas.dzialanie = Ops.Play
        Czas.var.notify_all()
        # Czas.var.wait()

def pokazujPasek(args):
    with Pasek.var:
        Pasek.dzialanie = Ops.ChangeTrack
        Pasek.var.notify_all()


def nowyUtwor(args):
    with Czas.var:
        Czas.dzialanie = Ops.ChangeTrack
        Czas.var.notify_all()
