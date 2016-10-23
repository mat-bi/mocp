#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

import curses
import time
import locale

from Player import Player

pause = u"▐"
play = u"▶"
stop = u"■"


def zmienTytul(tytulUtworu):
    t = str(Player.get_instance().current_playlist.current()["title"][0])
    tytulUtworu.clear()
    tytulUtworu.addstr(t)
    tytulUtworu.refresh()
    return


def pauzaZnak(playPause):
    playPause.clear()
    playPause.move(0, 0)
    playPause.addstr(pause.encode("utf-8"))
    playPause.move(0, 1)
    playPause.addstr(pause.encode("utf-8"))
    playPause.refresh()


def odtwarzanieZnak(playPause):
    playPause.clear()
    playPause.move(0, 1)
    playPause.addstr(play.encode("utf-8"))
    playPause.refresh()

def stopZnak(playPause):
    playPause.clear()
    playPause.move(0, 1)
    playPause.addstr(stop.encode("utf-8"))
    playPause.refresh()
