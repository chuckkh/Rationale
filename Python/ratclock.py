#!/usr/bin/env python

##    Copyright 2008, 2009, 2010, 2022 Charles S. Hubbard, Jr.
##
##    This file is part of Rationale.
##
##    Rationale is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    Rationale is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Rationale.  If not, see <http://www.gnu.org/licenses/>.




# -*- coding: utf-8 -*-
#
# midiclock.py
#
"""Receive MIDI clock and print out current BPM.
MIDI clock (status 0xF8) is sent 24 times per quarter note by clock generators.
"""

import time
from collections import deque

from rtmidi.midiconstants import (TIMING_CLOCK, SONG_CONTINUE, SONG_START, SONG_STOP)
from rtmidi.midiutil import open_midiinput


class MIDIClockReceiver:
    def __init__(self, bpm=None):
        self.bpm = bpm if bpm is not None else 120.0
        self.sync = False
        self.running = True
        self._samples = deque()
        self._last_clock = None

    def __call__(self, event, data=None):
        msg, _ = event
        if msg[0] > 241:
            print(msg)
        if msg[0] == 241:
            print("CODE")
        
        if msg[0] == TIMING_CLOCK:
            now = time.time()
            if self._last_clock is not None:
                self._samples.append(now - self._last_clock)

            self._last_clock = now

            if len(self._samples) > 24:
                self._samples.popleft()

            if len(self._samples) >= 2:
                self.bpm = 2.5 / (sum(self._samples) / len(self._samples))
                self.sync = True

        elif msg[0] in (SONG_CONTINUE, SONG_START):
            self.running = True
            pass
#            print("START/CONTINUE received.")
        elif msg[0] == SONG_STOP:
            self.running = False
            pass
#            print("STOP received.")
#        else:
#            print(msg)


def main(args=None):
#    clock = MIDIClockReceiver(float(args[0]) if args else None)
    clock = MIDIClockReceiver(None)

    try:
        m_in, port_name = open_midiinput(args[0] if args else None)
        print(m_in, port_name)
    except (EOFError, KeyboardInterrupt):
        print("error")
        return 1

    m_in.set_callback(clock)
    # Important: enable reception of MIDI Clock messages (status 0xF8)
    m_in.ignore_types(timing=False, sysex=False)

    try:
        print("Waiting for clock sync...")
        while True:
            time.sleep(1)

            if clock.running:
                if clock.sync:
                    pass
#                    print("%.2f bpm" % clock.bpm)
                else:
                    pass
#                    print("%.2f bpm (no sync)" % clock.bpm)

    except KeyboardInterrupt:
        pass
    finally:
        m_in.close_port()
        del m_in
