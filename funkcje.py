#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import curses
import time
import locale
from Czas import *
from Pasek import *

from Player import Player

curses_mutex = threading.RLock()

pause = u"▐"
play = u"▶"
stop = u"■"


def zmienTytul(
        args):  # ustawia tytuł bieżącego utworu w oknie wirtualnym "tytulUtworu" (przy zdarzeniu "MediaPlay")
    tytulUtworu = args["user"]
    t = ""
    if isinstance(args["title"], str):
        t = args["title"]
    else:
        t = args["title"][0]
    with curses_mutex:
        tytulUtworu.clear()
        tytulUtworu.addstr(t)
        tytulUtworu.refresh()


def pauzaZnak(
        args):  # ustawia znak odtwarzania "pause" w oknie wirtualnym "playPause" (przy zdarzeniu "MediaPause")
    playPause = args["user"]
    with curses_mutex:
        playPause.clear()
        playPause.move(0, 0)
        playPause.addstr(pause.encode("utf-8"))
        playPause.move(0, 1)
        playPause.addstr(pause.encode("utf-8"))
        playPause.refresh()
    with Czas.var:
        Czas.dzialanie = Ops.Pause
        Czas.event_table = args
        Czas.var.notify_all()
    with Pasek.var:
        Pasek.dzialanie = Ops.Pause
        Pasek.event_table = args
        Pasek.var.notify_all()



def odtwarzanieZnak(
        args):  # ustawia znak odtwarzania "play" w oknie wirtualnym "playPause" (przy zdarzeniu "MediaPlay")
    playPause = args["user"]
    with curses_mutex:
        playPause.clear()
        playPause.move(0, 1)
        playPause.addstr(play.encode("utf-8"))
        playPause.refresh()
    with Czas.var:
        Czas.dzialanie = Ops.Play
        Czas.event_table = args
        Czas.var.notify_all()
    with Pasek.var:
        Pasek.dzialanie = Ops.Play
        Pasek.event_table = args
        Pasek.var.notify_all()

def stopZnak(
        args):  # ustawia znak odtwarzania "stop" w oknie wirtualnym "playPause" (przy zdarzeniu "MediaStopped")
    playPause = args["user"]
    with curses_mutex:
        playPause.clear()
        playPause.move(0, 1)
        playPause.addstr(stop.encode("utf-8"))
        playPause.refresh()
    with Czas.var:
        Czas.dzialanie = Ops.Stop
        Czas.event_table = args
        Czas.var.notify_all()
    with Pasek.var:
        Pasek.dzialanie = Ops.Stop
        Pasek.event_table = args
        Pasek.var.notify_all()


def ustawCalkowitaDlugosc(
        args):  # ustawia całkowitą długość utworu w oknie wirtualnym "calkowitaDlugosc" (przy zdarzeniu "MediaPlay")
    dlugosc = int(args["length"])
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
    calkowitaDlugosc = args["user"]
    with curses_mutex:
        calkowitaDlugosc.move(0, 0)
        calkowitaDlugosc.addstr(dlugosc)
        calkowitaDlugosc.refresh()


def pokazujBiezacyCzas(
        args):  # ustawia biezący czas utworu w oknie wirtualnym "czasTrwania" (przy zdarzeniu "MediaPlay")
    with Czas.var:
        Czas.dzialanie = Ops.Play
        Czas.event_table = args
        Czas.var.notify_all()
        # Czas.var.wait()

def pokazujPasek(args):
    with Pasek.var:
        Pasek.dzialanie = Ops.ChangeTrack
        Pasek.event_table = args
        Pasek.var.notify_all()


def nowyUtwor(args):
    with Czas.var:
        Czas.dzialanie = Ops.ChangeTrack
        Pasek.event_table = args
        Czas.var.notify_all()


def ustawPrzestawionyCzas(args):
    with Czas.var:
        Czas.dzialanie = Ops.TimeChanged
        Czas.event_table = args
        Czas.var.notify_all()


def ustawPrzestawionyPasek(args):
    with Pasek.var:
        Pasek.dzialanie = Ops.TimeChanged
        Pasek.event_table = args
        Pasek.var.notify_all()
