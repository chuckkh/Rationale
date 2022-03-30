#!/usr/bin/env python

##    Copyright 2008, 2009 Charles S. Hubbard, Jr.
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


####STANDARD MODULES
import Tkinter as tk
import tkFileDialog as tkfd
import tkMessageBox as tkmb
#import tkColorChooser as tkcc
import math
import os
import threading
import sys
import copy
import pickle
import subprocess
#import sched
import socket
#import select
import Queue
#import time
####NOT ALWAYS PRESENT
#import Tix as tk
import csnd
#import notestorage
import mdialog
import ndialog
import odialog
import rdialog
import tdialog

class rationale(object):
    def __init__(self, parent, version):
        self.myparent = parent
        self.version = version
        self.myparent.rowconfigure(0, weight=1)
        self.myparent.columnconfigure(0, weight=1)


        #note: instr/voice, time, dur, db, num, den, region, bar, selected, guihandle, arb-tuple
        self.notelist = []
        self.notewidgetlist = []
        #meter: bar, beats, count
        self.meterlist = []
        #tempo: beat (in quarters), bpm, unit (in quarters)
        self.tempolist = []
        #region: num, den, color, r11
        initregion = rdialog.region(self, 1, 1, '#999999', 240)
        self.regionlist = [initregion]
        self.instlist = [0]
        self.instlist.append(odialog.instrument(self, 1, '#999999'))
        self.instdefault = []
        self.notebankactive = 0
        self.notebanklist = [ndialog.notebank([(1, 1), (33, 32), (21, 20), (16, 15), (15, 14), (14, 13), (13, 12), (12, 11), (11, 10), (10, 9), (9, 8), (8, 7), (7, 6), (13, 11), (32, 27), (6, 5), (11, 9), (16, 13), (5, 4), (81, 64), (14, 11), (9, 7), (13, 10), (21, 16), (4, 3), (11, 8), (18, 13), (7, 5), (10, 7), (13, 9), (16, 11), (3, 2), (32, 21), (20, 13), (20, 13), (14, 9), (11, 7), (128, 81), (8, 5), (13, 8), (18, 11), (5, 3), (27, 16), (22, 13), (12, 7), (7, 4), (16, 9), (9, 5), (20, 11), (11, 6), (24, 13), (13, 7), (28, 15), (15, 8), (40, 21), (64, 33), (2, 1)])]
#        self.solo = 0
        self.csdimport = None
        self.csdimported = ''
        self.outautoload = False
        self.norepeat = 0
        self.dispatcher = dispatcher(self)
        self.noteid = 0
        self.clipboard = []
        self.sf2list = []
        self.filetosave = None
        self.unsaved = 0
        self.ties = {}
        self.barlist = []
        self.primelimit = 13
        self.editreference = None
        self.n16 = tk.BitmapImage(file="img/rnssixteenth.xbm")
        self.nnb16 = tk.BitmapImage(file="img/rnsnbsixteenth.xbm")
        self.n8 = tk.BitmapImage(file="img/rnseighth.xbm")
        self.nnb8 = tk.BitmapImage(file="img/rnsnbeighth.xbm")
        self.nd8 = tk.BitmapImage(file="img/rnsdottedeighth.xbm")
        self.nnbd8 = tk.BitmapImage(file="img/rnsnbdottedeighth.xbm")
        self.n4 = tk.BitmapImage(file="img/rnsquarter.xbm")
        self.nnb4 = tk.BitmapImage(file="img/rnsnbquarter.xbm")
        self.nd4 = tk.BitmapImage(file="img/rnsdottedquarter.xbm")
        self.nnbd4 = tk.BitmapImage(file="img/rnsnbdottedquarter.xbm")
        self.n2 = tk.BitmapImage(file="img/rnshalf.xbm")
        self.nnb2 = tk.BitmapImage(file="img/rnsnbhalf.xbm")
        self.nd2 = tk.BitmapImage(file="img/rnsdottedhalf.xbm")
        self.nnbd2 = tk.BitmapImage(file="img/rnsnbdottedhalf.xbm")
        self.n1 = tk.BitmapImage(file="img/rnswhole.xbm")
        self.nnb1 = tk.BitmapImage(file="img/rnsnbwhole.xbm")
        self.icon = tk.PhotoImage(file="img/rat32.gif")
        if sys.platform.count("win32"):
            self.shiftnum1 = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
            self.shiftnum2 = [96, 97, 98, 99, 100, 101, 102, 103, 104, 105]
        elif sys.platform.count("linux"):
            self.shiftnum1 = [19, 10, 11, 12, 13, 14, 15, 16, 17, 18]
            self.shiftnum2 = [90, 87, 88, 89, 83, 84, 85, 79, 80, 81]
        elif sys.platform.count("darwin"):
            self.shiftnum1 = [1900585, 1179681, 1245248, 1310755, 1376292, 1507365, 1441886, 1703974, 1835050, 1638440]
            self.shiftnum2 = [5374000, 5439537, 5505074, 5570611, 5636148, 5701685, 5767222, 5832759, 5963832, 6029369]
####### Csound Audio Options
        self.audiomodule = 'portaudio'
        try:
            self.dac = self.getaudiodevices(self.audiomodule)[0].split(':')[0].strip()
        except:
            self.dac = 0
        self.sr = 44100
        self.ksmps = 16
        self.kr = float(self.sr)/self.ksmps
        self.nchnls = 2
        self.outputmethod = 0
        self.b = -1
        self.B = -1
        self.csdcommandline = ''
        self.csdcommandlineuse = 0
        self.wavfile = ''
        self.aifffile = ''
#######        
        self.realtime = False
        self.cbport = 5899
        self.cbscrubport = 6999
        self.outport = 5880
        self.outscrubport = 7888
        self.basefreq = 261.625565301
        self.curnum = 1
        self.curden = 1
        self.log2 = math.log(2)
	if sys.platform.count("darwin"):
	    self.control, self.ctlacc, self.alt, self.altacc = "Alt_L", "Cmd", "Control_L", "Ctl"
	else: self.control, self.ctlacc, self.alt, self.altacc = "Control", "Ctl", "Alt", "Alt"
        self.ctlkey = self.shiftkey = self.altkey = self.numkey = self.rkey = self.vkey = self.bkey = 0
        self.hinstch = 0
        self.hide = 0
        self.hidden = []
        self.quant = 6.0
        self.editvoice = 0
        self.editinst = 0
        self.editregion = 0
        self.overdur = 0
        #mode 0:add; 1:edit; 2:delete; 3:scrub
        welcome = 'Welcome to Rationale v. %s%s%sCopyright 2008, 2009%sCharles S. Hubbard, Jr.%s%sReleased under GPL v3%s(see the COPYING file for more details)%s%s' % (self.version, os.linesep, os.linesep, os.linesep, os.linesep, os.linesep, os.linesep, os.linesep, os.linesep)
        copyright = '''
Copyright 2008, 2009 Charles S. Hubbard, Jr.

This file is part of Rationale.

Rationale is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Rationale is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Rationale.  If not, see <http://www.gnu.org/licenses/>.
'''
        self.mode = tk.IntVar()
        modehelp = 'Press:%s\t"a" for ADD mode;%s\t"e" for EDIT mode;%s\t"d" for DELETE mode;%s\t"s" for SCRUB mode%s' % (os.linesep, os.linesep, os.linesep, os.linesep, os.linesep)
        self.stdouttext = tk.StringVar()
        self.stdouttext.set('%s%s%s%s' % (welcome, os.linesep, modehelp, os.linesep))
        self.playing = 0
        self.allowed2play = 1
        self.scrubbing = 0

### The Score Window ###
        self.scorebd = 3
        self.scoreh = 600
        self.scorew = 800
        self.scorecursor = "ur_angle"
        self.mainwin = tk.PanedWindow(self.myparent, orient='horizontal', relief='ridge', bd=self.scorebd, height=self.scoreh, width=1040, handlepad=2, opaqueresize=True, sashpad=0, sashwidth=5, showhandle=False)
        self.scorewin = tk.Frame(self.myparent, relief='ridge')
        self.scorewinwin = self.mainwin.add(self.scorewin, width=self.scorew)
        self.scorewin.rowconfigure(3, weight=1)
        self.scorewin.columnconfigure(2, weight=1)
        if sys.platform.count("darwin"):
            self.scorewin.columnconfigure(3, minsize=25)
        self.xscroll = tk.Scrollbar(self.scorewin, orient='horizontal', takefocus=0, troughcolor="#cc9966", activebackground="#bb8866", bg="#aa7755")
        self.xscroll.grid(row=4, column=2, sticky='ew')
        self.statusbar = tk.Frame(self.scorewin, height=24, bd=1, relief="raised")
        self.statusbar.grid_propagate(0)
        self.statusbar.columnconfigure(0, minsize=90)
        self.statusbar.columnconfigure(1, minsize=55)
        self.statusbar.columnconfigure(2, minsize=50)
        self.statusbar.columnconfigure(3, minsize=80)
        self.statusbar.columnconfigure(4, minsize=100)
        self.statusbar.columnconfigure(5, minsize=80)
        self.statusbar.columnconfigure(7, weight=1)
        self.statusbar.grid(row=5, column=0, columnspan=4, sticky='ew')
        if self.mode.get() == 0:
            statmode = "ADD mode"
        elif self.mode.get() == 1:
            statmode = "EDIT mode"
        elif self.mode.get() == 2:
            statmode = "DELETE mode"
        elif self.mode.get() == 3:
            statmode = "SCRUB mode"
        self.statusmode = tk.Label(self.statusbar, text=statmode, bd=2, relief="ridge", anchor='w')
        self.statusmode.grid(row=0, column=0, sticky='ew')
        self.statusplay = tk.Label(self.statusbar, text='Stopped', bd=2, relief="ridge", anchor='w')
        self.statusplay.grid(row=0, column=1, sticky='ew')
        self.statusinst = tk.Label(self.statusbar, text='Inst 1', bd=2, relief="ridge", anchor='w')
        self.statusinst.grid(row=0, column=2, sticky='ew')
        self.statusvoice = tk.Label(self.statusbar, text='Voice 0', bd=2, relief="ridge", anchor='w')
        self.statusvoice.grid(row=0, column=3, sticky='ew')
        self.statusregion = tk.Label(self.statusbar, text='Region 0 = 1:1', bd=2, relief="ridge", anchor='w')
        self.statusregion.grid(row=0, column=4, sticky='ew')
        self.statusbank = tk.Label(self.statusbar, text='Bank 0', bd=2, relief="ridge", anchor='w')
        self.statusbank.grid(row=0, column=5, sticky='ew')
        self.statusrat = tk.Label(self.statusbar, text='Hover   1:1', bd=2, relief="ridge", anchor='w')
        self.statusrat.grid(row=0, column=6, sticky='ew', padx=5)
        self.statushidden = tk.Label(self.statusbar, text='None Hidden', bd=2, relief="ridge", anchor='e')
	if sys.platform.count("darwin"):
	    padx = 22
	else:
	    padx = 0
        self.statushidden.grid(row=0, column=8, sticky='ew', padx=padx)
        self.yscroll = tk.Scrollbar(self.scorewin, orient='vertical', takefocus=0, troughcolor="#cc9966", activebackground="#bb8866", bg="#aa7755")
        self.yscroll.grid(row=3, column=3, rowspan=1, sticky='nws')
        self.stdoutwin = tk.Frame(self.myparent, width=240)
        self.stdoutwinwin = self.mainwin.add(self.stdoutwin, width=240, before=self.scorewin)
        self.stdoutwin.rowconfigure(0, weight=1)
        self.stdoutwin.columnconfigure(0, weight=1)
        self.mainwin.grid(row=0, column=0, sticky='nesw')
        self.stdouttxt = tk.Text(self.stdoutwin, bg = "#114433", fg="#aaaaff")
        self.stdouttxt.grid(sticky='nesw')
        self.stdouttxt.insert('end', self.stdouttext.get())
        self.stdouttxt.configure(state="disabled")
        self.stdscroll = tk.Scrollbar(self.stdoutwin, orient='vertical', takefocus=0, troughcolor="#ccaaaa", activebackground="#cc7777", bg="#cc8f8f")
        self.stdouttxt.config(yscrollcommand=self.stdscroll.set)
        self.stdscroll.config(command=self.stdouttxt.yview)
        self.octaveres = 240
        self.yadj = self.octave11 = 240
        self.xquantize = .25
        self.xperquarter = 30
        self.xpxquantize = float(self.xquantize * self.xperquarter)
        self.miny = self.octave11 - self.octaveres * 5
        self.maxy = self.octave11 + self.octaveres * 5
        self.minx = -60
        self.maxx = 12000
	if sys.platform.count("darwin"):
	    h = 12
	else: h = 8
        self.meters = tk.Canvas(self.scorewin, height=h, width=self.scorew, scrollregion=(self.minx,0,self.maxx,0), bg="#eeeeaa", confine="false")
        self.meters.myparent = self
        self.meters.grid(row=0, column=2, sticky='ew', pady=0)
#        self.meters.bind("<Button-1>", self.meteradd)
        self.meters.bind("<Button-1>", self.openmeterdialog)
        self.meters.bind("<Button-3>", self.openmeterdialog)
        self.meters.columnconfigure(1, weight=1)
        self.meterlabel = tk.Label(self.meters, text="M", anchor='w', font=("Times", h), pady=0, bg="#eeeeaa")
        self.meterlabel.grid(row=0, column=0, sticky='w')
        self.tempos = tk.Canvas(self.scorewin, height=h, width=self.scorew, scrollregion=(self.minx,0,self.maxx,0), bg="#ddcccc", confine="false")
        self.tempos.myparent = self
        self.tempos.grid(row=1, column=2, sticky='ew', pady=0)
#        self.tempos.bind("<Button-1>", self.tempoinit)
#        self.tempos.bind("<B1-Motion>", self.tempoadjust)
#        self.tempos.bind("<ButtonRelease-1>", self.tempoadd)
        self.tempos.bind("<Button-1>", self.opentempodialog)
        self.tempos.bind("<Button-3>", self.opentempodialog)
        self.tempos.columnconfigure(1, weight=1)
        self.tempolabel = tk.Label(self.tempos, text="T", anchor='w', font=("Times", h), pady=0, bg="#ddcccc")
        self.tempolabel.grid(row=0, column=0, sticky='w')
        self.bars = tk.Canvas(self.scorewin, height=h, width=self.scorew, scrollregion=(self.minx,0,self.maxx,0), bg="#ccccee", confine="false")
        self.bars.grid(row=2, column=2, sticky='ew', pady=0)
        scorebg = "#fffff0"
        self.score = tk.Canvas(self.scorewin, width=self.scorew, height=self.scoreh, xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set, scrollregion=(self.minx, self.miny, self.maxx, self.maxy), confine="false", bg=scorebg, cursor=self.scorecursor)
        self.score.rowconfigure(0, weight=1)
        self.score.columnconfigure(0, weight=1)
        self.score.grid(row=3, column=2, sticky='nesw')
        self.cursor = cursor(self)
        self.octaves = tk.Canvas(self.scorewin, width=10, height=self.scoreh, scrollregion=(0, self.miny, 0, self.maxy), bg="#99dd99", confine="false")
        self.octaves.rowconfigure(0, weight=1)
        self.octaves.grid(row=3,column=1, sticky='ns')
        self.xscroll.config(command=self.scorexscroll)
        self.yscroll.config(command=self.scoreyscroll)
        self.scorexscroll("moveto", 0.00242072)
	if sys.platform.count("darwin"):
	    self.score.bind("<Button-3>", self.grab)
	    self.score.bind("<B3-Motion>", self.scoredrag)
	else:
            self.score.bind("<Button-2>", self.grab)
            self.score.bind("<B2-Motion>", self.scoredrag)
        self.score.bind("<Button-4>",
                              lambda
                              event, arg1="scroll", arg2=-1, arg3="units":
                              self.scoreyscroll(arg1, arg2, arg3))
        self.score.bind("<Button-5>",
                              lambda
                              event, arg1="scroll", arg2=1, arg3="units":
                              self.scoreyscroll(arg1, arg2, arg3))
        self.yscroll.bind("<Button-4>",
                              lambda
                              event, arg1="scroll", arg2=-1, arg3="units":
                              self.scoreyscroll(arg1, arg2, arg3))
        self.yscroll.bind("<Button-5>",
                              lambda
                              event, arg1="scroll", arg2=1, arg3="units":
                              self.scoreyscroll(arg1, arg2, arg3))
        self.myparent.bind("<MouseWheel>",
                              lambda
                              event, arg1="scroll", arg3="units": self.scoreyscrollwheel(arg1, event, arg3))

        self.drawoctaves(self.octave11)
        self.drawlines(1000)
        self.hover = hover(self)

### Score Bindings ###
        self.score.bind("<Button-1>", self.buttondown)
        self.score.bind("<B1-Motion>", self.buttonmotion)
        self.score.bind("<Motion>",self.normalmotion)
        self.score.bind("<Shift-Motion>",self.shiftmotion)
        self.score.bind("<Shift-B1-Motion>", self.shiftbuttonmotion)
        self.score.bind("<ButtonRelease-1>",self.buttonup)
	if sys.platform.count("darwin"):
	    self.score.bind("<Button-2>",self.popup)
	    self.score.bind("<Control-1>", self.popup)
	else:
	    self.score.bind("<Button-3>",self.popup)
        self.score.bind("<Key>",self.keypress)
        self.score.bind("<KeyRelease>",self.keyrelease)
        self.scorewin.bind("<Key>",self.keypress)
        self.scorewin.bind("<KeyRelease>",self.keyrelease)
        self.myparent.bind("<Key>",self.keypress)
        self.myparent.bind("<KeyRelease>",self.keyrelease)
#        self.myparent.bind("<Shift-KeyPress-1>", self.shift1)
#        self.myparent.bind("<Shift-KeyPress-2>", self.shift2)
#        self.myparent.bind("<Shift-KeyPress-3>", self.shift3)
#        self.myparent.bind("<Shift-KeyPress-4>", self.shift4)
#        self.myparent.bind("<Shift-KeyPress-5>", self.shift5)
#        self.myparent.bind("<Shift-KeyPress-6>", self.shift6)
#        self.myparent.bind("<Shift-KeyPress-7>", self.shift7)
#        self.myparent.bind("<Shift-KeyPress-8>", self.shift8)
#        self.myparent.bind("<Shift-KeyPress-9>", self.shift9)
#        self.myparent.bind("<Shift-KeyPress-0>", self.shift0)
        self.myparent.bind("<Shift-Right>", self.durmod8up)
        self.myparent.bind("<Shift-Left>", self.durmod8down)
        self.myparent.bind("<Shift-Up>", self.durmod6up)
        self.myparent.bind("<Shift-Down>", self.durmod6down)

###     Keyboard Bindings
	if sys.platform.count("darwin"):
            self.myparent.bind("<Command-q>", self.fileexit)
            self.myparent.bind("<Command-Q>", self.fileexit)
            self.myparent.bind("<Shift-Command-q>", self.exit)
            self.myparent.bind("<Shift-Command-Q>", self.exit)
            self.myparent.bind("<Command-s>", self.filesave)
            self.myparent.bind("<Command-S>", self.filesave)
            self.myparent.bind("<Shift-Command-s>", self.filesaveas)
            self.myparent.bind("<Shift-Command-S>", self.filesaveas)
            self.myparent.bind("<Command-o>", self.fileopen)
            self.myparent.bind("<Command-O>", self.fileopen)
            self.myparent.bind("<Command-r>", self.filereload)
            self.myparent.bind("<Command-R>", self.filereload)
            self.myparent.bind("<Command-i>", self.fileimport)
            self.myparent.bind("<Command-I>", self.fileimport)
            self.myparent.bind("<Command-e>", self.fileexport)
            self.myparent.bind("<Command-E>", self.fileexport)
            self.myparent.bind("<Command-Next>", self.cursor.nextbar)
            self.myparent.bind("<Command-Prior>", self.cursor.previousbar)
            self.myparent.bind("<Command-n>", self.filenew)
            self.myparent.bind("<Command-N>", self.filenew)
            self.myparent.bind("<Command-z>", self.editundo)
            self.myparent.bind("<Command-Z>", self.editundo)
            self.myparent.bind("<Command-y>", self.editredo)
            self.myparent.bind("<Command-Y>", self.editredo)
            self.myparent.bind("<Command-c>", self.editmodecopy)
            self.myparent.bind("<Command-C>", self.editmodecopy)
            self.myparent.bind("<Command-x>", self.editmodecut)
            self.myparent.bind("<Command-X>", self.editmodecut)
            self.myparent.bind("<Command-v>", self.editmodepaste)
            self.myparent.bind("<Command-V>", self.editmodepaste)
            self.myparent.bind("<Command-a>", self.editmodeselectall)
            self.myparent.bind("<Command-A>", self.editmodeselectall)
            self.myparent.bind("<Command-d>", self.optionsaudio)
            self.myparent.bind("<Command-D>", self.optionsaudio)
            self.myparent.bind("<Command-b>", self.opennotebankdialog)
            self.myparent.bind("<Command-B>", self.opennotebankdialog)
	else:
            self.myparent.bind("<Control-q>", self.fileexit)
            self.myparent.bind("<Control-Q>", self.fileexit)
            self.myparent.bind("<Shift-Control-q>", self.exit)
            self.myparent.bind("<Shift-Control-Q>", self.exit)
            self.myparent.bind("<Control-s>", self.filesave)
            self.myparent.bind("<Control-S>", self.filesave)
            self.myparent.bind("<Shift-Control-s>", self.filesaveas)
            self.myparent.bind("<Shift-Control-S>", self.filesaveas)
            self.myparent.bind("<Control-o>", self.fileopen)
            self.myparent.bind("<Control-O>", self.fileopen)
            self.myparent.bind("<Control-r>", self.filereload)
            self.myparent.bind("<Control-R>", self.filereload)
            self.myparent.bind("<Control-i>", self.fileimport)
            self.myparent.bind("<Control-I>", self.fileimport)
            self.myparent.bind("<Control-e>", self.fileexport)
            self.myparent.bind("<Control-E>", self.fileexport)
            self.myparent.bind("<Control-Next>", self.cursor.nextbar)
            self.myparent.bind("<Control-Prior>", self.cursor.previousbar)
            self.myparent.bind("<Control-n>", self.filenew)
            self.myparent.bind("<Control-N>", self.filenew)
            self.myparent.bind("<Control-z>", self.editundo)
            self.myparent.bind("<Control-Z>", self.editundo)
            self.myparent.bind("<Control-y>", self.editredo)
            self.myparent.bind("<Control-Y>", self.editredo)
            self.myparent.bind("<Control-c>", self.editmodecopy)
            self.myparent.bind("<Control-C>", self.editmodecopy)
            self.myparent.bind("<Control-x>", self.editmodecut)
            self.myparent.bind("<Control-X>", self.editmodecut)
            self.myparent.bind("<Control-v>", self.editmodepaste)
            self.myparent.bind("<Control-V>", self.editmodepaste)
            self.myparent.bind("<Control-a>", self.editmodeselectall)
            self.myparent.bind("<Control-A>", self.editmodeselectall)
            self.myparent.bind("<Control-d>", self.optionsaudio)
            self.myparent.bind("<Control-D>", self.optionsaudio)
            self.myparent.bind("<Control-b>", self.opennotebankdialog)
            self.myparent.bind("<Control-B>", self.opennotebankdialog)
        
        self.myparent.bind("<Next>", self.cursor.nextbeat)
        self.myparent.bind("<Prior>", self.cursor.previousbeat)
        self.myparent.bind("<Home>", self.cursor.home)
        self.myparent.bind("<End>", self.cursor.end)
        self.myparent.bind("<n>", self.openregiondialog)
        self.myparent.bind("<N>", self.openregiondialog)
        self.myparent.bind("<p>", self.opentempodialog)
        self.myparent.bind("<P>", self.opentempodialog)
        self.myparent.bind("<m>", self.openmeterdialog)
        self.myparent.bind("<M>", self.openmeterdialog)
        self.myparent.bind("<c>", self.setconnect)
        self.myparent.bind("<C>", self.setconnect)
        self.myparent.bind("<x>", self.disconnect)
        self.myparent.bind("<X>", self.disconnect)
        self.myparent.bind("<FocusIn>", self.globalcancel)
#        self.myparent.bind("<FocusOut>", self.globalcancel)
#        self.myparent.bind("<o>", self.openoutputdialog)
#        self.myparent.bind("<O>", self.openoutputdialog)
        self.myparent.bind("<Delete>", self.editmodedelete)
        self.myparent.bind_all("<Alt-Escape>", self.globalcancel)
        self.myparent.bind_all("<Escape>", self.globalcancel)
#        self.myparent.bind("<n>", self.noteeditlistnew)
#        self.myparent.bind("<N>", self.noteeditlistnew)


### Score Menus ###
        self.menumain = tk.Menu(self.myparent)
        self.myparent.config(menu=self.menumain)
#        self.menumain.add_command(image=self.icon, command=self.helpabout)
        self.menufile = tk.Menu(self.menumain, tearoff=0)
        self.menufile.add_command(label="New", command=self.filenew, underline=0, accelerator="%s-N" % self.ctlacc)
        self.menufile.add_command(label="Open...", command=self.fileopen, underline=0, accelerator="%s-O" % self.ctlacc)
        self.menufile.add_command(label="Save...", command=self.filesave, underline=0, accelerator="%s-S" % self.ctlacc)
        self.menufile.add_command(label="Save As...", command=self.filesaveas, underline=1, accelerator="Sh-%s-S" % self.ctlacc)
        self.menufile.add_command(label="Reload", command=self.filereload, underline=0, accelerator="%s-R" % self.ctlacc)
        self.menufile.add_command(label="Import .ji...", command=self.fileimport, underline=0, accelerator="%s-I" % self.ctlacc, state="disabled")
        self.menufile.add_command(label="Export Csound...", command=self.fileexport, underline=0, accelerator="%s-E" % self.ctlacc)
        self.menufile.add_command(label="Exit Rationale", command=self.fileexit, underline=1, accelerator="%s-Q" % self.ctlacc)
        self.menumain.add_cascade(label="File", menu=self.menufile, underline=0)
        self.menuedit = tk.Menu(self.menumain, tearoff=0)
        self.menuedit.add_command(label="Can't Undo", command=self.editundo, accelerator="%s-Z" % self.ctlacc, state="disabled")
        self.menuedit.add_command(label="Can't Redo", command=self.editredo, accelerator="%s-Y" % self.ctlacc, state="disabled")
        self.menumode = tk.Menu(self.menuedit, tearoff=0)
        self.menumode.add_radiobutton(label="Add", value=0, variable=self.mode, underline=0, command=self.modeannounce, accelerator="A")
        self.menumode.add_radiobutton(label="Edit", value=1, variable=self.mode, underline=0, command=self.modeannounce, accelerator="E")
        self.menumode.add_radiobutton(label="Delete", value=2, variable=self.mode, underline=0, command=self.modeannounce, accelerator="D")
        self.menumode.add_radiobutton(label="Scrub", value=3, variable=self.mode, underline=0, command=self.modeannounce, accelerator="S")
        self.menumode.invoke(0)
        self.menuselect = tk.Menu(self.menuedit, tearoff=0)
        self.menuselect.add_command(label="All", command=self.editmodeselectall, accelerator="%s-A" % self.ctlacc)
        self.menuselect.add_command(label="None", command=self.editmodeselectnone)
        self.menuselect.add_command(label="Start to Cursor", command=self.editmodeselecttocursor)
        self.menuselect.add_command(label="Cursor to End", command=self.editmodeselectfromcursor)
        self.menuselect.add_command(label="Filter...", state="disabled")
        self.menuedit.add_cascade(label="Mode", menu=self.menumode, underline=0)
        self.menuedit.add_cascade(label="Select", menu=self.menuselect, underline=0)
        self.menuedit.add_separator()
        self.menuedit.add_command(label="Output...", command=self.openoutputdialog, underline=0, accelerator="O")
        self.menuedit.add_command(label="Tempos...", command=self.opentempodialog, underline=0, accelerator="P")
        self.menuedit.add_command(label="Meters...", command=self.openmeterdialog, underline=1, accelerator="M")
        self.menuedit.add_command(label="Regions...", command=self.openregiondialog, underline=0, accelerator="R")
        self.menuedit.add_command(label="Notebanks", command=self.opennotebankdialog, underline=0, accelerator="%s-B" % self.ctlacc)
        self.menuedit.add_separator()
        self.menuedit.add_command(label="Cut", command=self.editmodecut, accelerator="%s-X" % self.ctlacc)
        self.menuedit.add_command(label="Copy", command=self.editmodecopy, underline=0, accelerator="%s-C" % self.ctlacc)
        self.menuedit.add_command(label="Paste...", command=self.editmodepaste, underline=0, accelerator="%s-V" % self.ctlacc)
        self.menuedit.add_command(label="Delete", command=self.editmodedelete, underline=0, accelerator="Delete")
        self.menumain.add_cascade(label="Edit", menu=self.menuedit, underline=0)
        self.statusshow = tk.BooleanVar()
        self.statusshow.set(True)
        self.statusshow.trace("w", self.statusgrid)
        self.menuview = tk.Menu(self.menumain, tearoff=0)
        self.menuview.add_command(label="Maximize", command=lambda arg1= self.myparent: self.max(arg1), underline=0)
        self.menuview.add_checkbutton(label="Status Bar", variable=self.statusshow)
        self.menuview.add_separator()
        self.menuview.add_command(label="Show All", command=self.showall, accelerator="%s-S" % self.altacc)
        self.createhidemenu()
        self.menumain.add_cascade(label="View", menu=self.menuview, underline=0)
        self.menuoptions = tk.Menu(self.menumain, tearoff=0)
        self.menuoptions.add_command(label="Audio", command=self.optionsaudio, underline=0, accelerator="%s-D" % self.ctlacc)
        self.menumain.add_cascade(label="Options", menu=self.menuoptions, underline=0)
        self.menuhelp = tk.Menu(self.menumain, tearoff=0)
        self.menuhelp.add_command(label="Manual", underline=0, command=self.helpManual)
        self.menuhelp.add_command(label="About", underline=0, command=self.helpabout)
        self.menumain.add_cascade(label="Help", menu=self.menuhelp, underline=0)
        self.poppedup = False
        self.menupopup = tk.Menu(self.myparent, tearoff=0)
        self.menupopupregion = tk.Menu(self.menupopup, tearoff=0)
        for region in range(0, len(self.regionlist)):
            self.menupopupregion.add_command(label='%d' % region, command=lambda arg1=region: self.editregionassign(arg1))
        self.menupopupinst = tk.Menu(self.menupopup, tearoff=0)
        for inst in range(1, len(self.instlist)):
            self.menupopupinst.add_command(label='%d' % inst, command=lambda arg1=inst: self.editinstassign(arg1))
        self.menupopupvoice = tk.Menu(self.menupopup, tearoff=0)
        for voice in range(0, 9):
            self.menupopupvoice.add_command(label='%d' % voice, command=lambda arg1=voice: self.editvoiceassign(arg1))
        self.menupopuparb = tk.Menu(self.menupopup, tearoff=0)
        self.menupopup.add_cascade(label="Region", menu=self.menupopupregion)
        self.menupopup.add_cascade(label="Instrument", menu=self.menupopupinst)
        self.menupopup.add_cascade(label="Voice", menu=self.menupopupvoice)
        self.menupopup.add_command(label="Connect", command=self.editmodeconnect)
        self.menupopup.add_command(label="Disconnect", command=self.editmodedisconnect)
        self.menupopup.add_command(label="Arbitrary", command=self.editmodearb)
        self.menupopup.add_command(label="Cut", command=self.editmodecut)
        self.menupopup.add_command(label="Copy", command=self.editmodecopy)
        self.menupopup.add_command(label="Delete", command=self.editmodedelete)

        if len(sys.argv) > 1:
            try:
                self.fileopenwork(sys.argv[1])
            except:
                self.filesave()
                self.write('File Created: %s' % sys.argv[1])
#                self.write('%s: File Not Found' % sys.argv[1])

    def statusgrid(self, *args):
        if self.statusbar.winfo_ismapped() and not self.statusshow.get():
            self.statusbar.grid_remove()
        elif self.statusshow.get() and not self.statusbar.winfo_ismapped():
            self.statusbar.grid(row=5, column=0, columnspan=4, sticky='ew')

    def ratioreduce(self, num, den, lim):
        for factor in range(2,lim+1):
            for i in range(0,15):
                if num % factor == 0 and den % factor == 0:
                    num /= factor
                    den /= factor
                else:
                    pass
        ret = (num,den)
        return ret

### Draw the barlines and beatlines ###
    def drawlines(self, bars):
        beats = 4
        count = 4
        ml = self.meterlist
        i = [(s.bar) for s in ml]
        x = 0
        barnum = 1
	if sys.platform.count("darwin"):
	    y, anch, size = 5, "n", 9
	else: y, anch, size = -1, "n", 7
        for m in range(1, bars+1):
            if (m in i):
                ind = i.index(m)
                if ml[ind].top != 0:
                    beats = ml[ind].top
                if ml[ind].bottom != 0:
                    count = ml[ind].bottom
                self.meters.create_text(x, y, anchor=anch, fill="#555522", text='%d/%d' % (beats, count), font=("Times", size), tags="x")
            bar = self.score.create_line(x, self.miny, x, self.maxy, width=2, fill="#999999", tags=("barline", "x"))
            barnumdisp = self.bars.create_text(x, y, anchor=anch, fill="#222222", text=str(barnum), font=("Times", size), tags="x")
            self.barlist.append(bar)
            x += self.xperquarter * 4 / count
            barnum = barnum + 1
            for b in range(1, beats):
                bar = self.score.create_line(x, self.miny, x, self.maxy, width=1, fill="#aaaaaa", tags=("beatline", "all"))
                self.barlist.append(bar)
                x += self.xperquarter * 4 / count

    def redrawlines(self, *args):
        self.meters.delete("all")
        self.bars.delete("all")
        self.score.delete("barline")
        self.score.delete("beatline")
        self.barlist[:] = []
        self.drawlines(1000)

    def drawoctaves(self, new11, resdelta=0):
        y = self.octave11 - 5 * self.octaveres
        num = 32
        den = 1
        coloroctnum = "#228822"
        linelength = 1000 * self.xperquarter * 4
        try:
            line = self.line11
            ydelta = new11 - self.octave11
            if ydelta:
    #            if abs(ydelta) > 240:
                if abs(ydelta) > self.octaveres:
                    ydiv = 64
    #            elif abs(ydelta) > 120:
                elif abs(ydelta) > self.octaveres/2.0:
                    ydiv = 32
                else:
                    ydiv = 16
                yincr = float(ydelta)/ydiv
                for incr in range(0, ydiv):
                    self.score.move("octaveline", 0, yincr)
                    self.octaves.move("octavetext", 0, yincr)
                    self.scorewin.update_idletasks()
            else:
                for item in self.score.find_withtag("octaveline"):
                    coords = self.score.coords(item)
                    cury = coords[1]
                    diff = (coords[1] - self.octave11)/(self.octaveres - resdelta)
                    self.score.move(item, 0, (diff * resdelta))
                for item in self.octaves.find_withtag("octavetext"):
                    coords = self.octaves.coords(item)
                    cury = coords[1]
                    diff = (coords[1] - self.octave11)/(self.octaveres - resdelta)
                    self.octaves.move(item, 0, (diff * resdelta))
                self.scorewin.update_idletasks()
        except:
            self.perm11 = self.score.create_line(-60, self.octave11, linelength, self.octave11, width=4, fill="#aaaaaa", tags=("all", "perm11"))
            for up in range(0,5):
                self.score.create_line(-60,y,linelength,y,width=2,fill="#bbbbbb",tags=("octaveline", "all"))
                self.octaves.create_text(6,y,anchor="s",text=str(num),fill=coloroctnum,tags=("octavetext", "y"),font=("Times",9))
                self.octaves.create_text(6,y,anchor="n",text=str(den),fill=coloroctnum,tags=("octavetext", "y"),font=("Times",9))
                num /= 2
                y += self.octaveres
            self.line11 = self.score.create_line(-60,y,linelength,y,width=2,fill="#7777bb",tags=("octaveline", "y"))
            self.octaves.create_text(6,y,anchor="s",text=str(num),fill=coloroctnum,tags=("octavetext", "y"),font=("Times",14))
            self.octaves.create_text(6,y,anchor="n",text=str(den),fill=coloroctnum,tags=("octavetext", "y"),font=("Times",14))
            for down in range(0,6):
                y += self.octaveres
                den *= 2
                self.score.create_line(-60,y,linelength,y,width=2,fill="#bbbbbb",tags=("octaveline", "y"))
                self.octaves.create_text(6,y,anchor="s",text=str(num),fill=coloroctnum,tags=("octavetext", "y"),font=("Times",9))
                self.octaves.create_text(6,y,anchor="n",text=str(den),fill=coloroctnum,tags=("octavetext", "y"),font=("Times",9))

    def beatstoseconds(self, beat):
        pass

    def constructline(self, note, line, lineguide, volume):
        pnum = include = 1
        for pfield in range(1,len(lineguide)):
            line += ' '
            if lineguide[pfield] == 'freq':
                line += '[$RATBASE * %d/%d * %d/%d]' % (note.dict['num'], note.dict['den'], self.regionlist[note.region].num, self.regionlist[note.region].den)
            elif lineguide[pfield] == 'db':
                line += '%f' % (float(note.dict['db']) + float(volume))
            elif lineguide[pfield] == '[':
                line += lineguide[pfield]
                include = 0
            elif lineguide[pfield] == ']':
                line += lineguide[pfield]
                include = 1
            else:
                try:
                    line += str(note.dict[lineguide[pfield]])
                except:
                    line += str(lineguide[pfield])
            if include == 1: pnum += 1
        return (line, pnum)

######## prepare csd file
    def preparecsd(self, instlist, sf2list, method, sr, ksmps, nchnls, amodule, dac, b, B, aifffile, wavfile, commandline, commandlineuse):
        self.scsort()
        if self.outautoload == True:
            self.csdreload()

        playscore = self.notelist
        proglist = []
        todict = {}

#########CsScore
        self.csdsco = ''
        if self.tempolist:
            self.csdsco = 't'
            for t in self.tempolist:
                self.csdsco += ' %f %f' % (t.scobeat, t.bpm*t.unit/4.0)
            self.csdsco += os.linesep
        else:
            self.csdsco = ''
        last = playscore[-1]
        tottime = last.time + abs(last.dur)
        if method == 0:
            self.csdsco += 'f0 %f%s' % (tottime+.125, os.linesep)
        if self.cursor.beat == 0:
            self.ratstart = 0
        else:
#            self.ratstart = float(self.score.coords(self.barlist[self.cursor.beat])[0])/self.xperquarter
            self.ratstart = float(self.cursor.center)/self.xperquarter
        astring = 'a 0 0 %f%s' % (self.ratstart, os.linesep)
        self.csdsco += astring
        self.csdsco += '#define RATSTART #%f#%s' % (self.ratstart, os.linesep)
        self.csdsco += '#define RATBASE #%f#%s' % (self.basefreq, os.linesep)
        if self.csdimported.count("<CsScore>"):
            scostart = self.csdimported.find("<CsScore>") + 9
            scoend = self.csdimported.find("</CsScore>")
            self.csdsco += self.csdimported[scostart:scoend]
        ondict = {}
        for i, note in enumerate(playscore):
#            region = note.region
#            rnum = self.regionlist[region].num
#            rden = self.regionlist[region].den
#            freq = (float(rnum * note.num))/(float(rden * note.den)) * self.basefreq
            if int(note.inst) < len(instlist):
#                instr = float(note.inst) + .001 * float(note.voice)
                if instlist[note.inst].solo >= instlist[0] and not instlist[note.inst].mute:
                    for outline in instlist[note.inst].outlist:
                        if outline.solo >= instlist[note.inst].gsolo and not outline.mute:
                            if outline.__class__.__name__ == 'csdout':
                                lineguide = outline.string.split()
                                pnum = include = 1
                                if not lineguide[0].isdigit() and note.voice:
                                    ## named instruments need a turn-on instrument to supply the voice parameter
                                    line = 'i "rat%son" %f %f %d' % (lineguide[0].strip('"'), note.time, note.dur, note.voice)

                                elif note.voice:
                                    line = 'i %s.%.3d' % (lineguide[0], note.voice)
                                elif not lineguide[0].isdigit():
                                    line = 'i "' + lineguide[0].strip('"') + '"'
				else:
				    line = 'i ' + lineguide[0].strip('"')
#####################3
                                constructed = self.constructline(note, line, lineguide, outline.volume)
                                line = constructed[0]
                                pnum = constructed[1]

                                line += os.linesep
                                self.csdsco += line
                                if not lineguide[0].isdigit() and not lineguide[0] == ('"ratdefault"'):
                                    if lineguide[0] not in todict.keys() or todict[lineguide[0]][0] < pnum:
                                        toinst = '%sinstr +rat%son%s' % (os.linesep, lineguide[0].strip('"'), os.linesep)
                                        toinst += 'instnum nstrnum "%s"%s' % (lineguide[0].strip('"'), os.linesep)
                                        toinst += '''inum = instnum + (p4/1000)
al, ar	subinstr	inum, p7, p8'''
                                        for p in range(7, pnum+7):
                                            toinst += ', p%d' % p
                                        toinst += '''
	outc	al, ar
        endin
'''
                                        todict[lineguide[0]] = (pnum, toinst)

                            elif outline.__class__.__name__ == 'sf2out':
                                try: fullpath = outline.file.filename
                                except: fullpath = None
                                if (outline.program, outline.bank, outline.file) not in proglist:
                                    proglist.append((outline.program, outline.bank, outline.file))
                                try:
                                    A = note.dict['a1']
                                except:
                                    A = outline.A
                                try:
                                    D = note.dict['a2']
                                except:
                                    D = outline.D
                                try:
                                    S = note.dict['a3']
                                except:
                                    S = outline.S
                                try:
                                    R = note.dict['a4']
                                except:
                                    R = outline.R
                                line = 'i "ratratsf2defaulton" %f %f %d %f %f [$RATBASE * %d/%d * %d/%d] %d %s %s %s %s%s' % (note.time, note.dur, note.voice, note.dur, float(note.db)+float(outline.volume), note.num, note.den, self.regionlist[note.region].num, self.regionlist[note.region].den, proglist.index((outline.program, outline.bank, outline.file)), A, D, S, R, os.linesep)
                                self.csdsco += line
                            elif outline.__class__.__name__ == 'oscout':
                                lineguide = outline.string.split()
                                line = 'i "ratoscdefault%drat%don" %f %f' % (note.inst, instlist[note.inst].outlist.index(outline), note.time, abs(note.dur))
                                #include = 1
                                for pfield in range(len(lineguide)):
                                    line += ' '
                                    if lineguide[pfield] == 'freq':
                                        line += '[$RATBASE * %d/%d * %d/%d]' % (note.dict['num'], note.dict['den'], self.regionlist[note.region].num, self.regionlist[note.region].den)
                                    elif lineguide[pfield] == 'db':
                                        line += '%f' % (float(note.dict['db']) + float(outline.volume))
                                    else:
                                        try:
                                            line += str(note.dict[lineguide[pfield]])
                                        except:
                                            line += str(lineguide[pfield])
                                line += os.linesep
                                self.csdsco += line
                                if outline.noff:
                                    lineguide = outline.noffstring.split()
                                    line = 'i "ratoscdefault%drat%doff" %f 0.01' % (note.inst, instlist[note.inst].outlist.index(outline), note.time+abs(note.dur))
                                    for pfield in range(len(lineguide)):
                                        line += ' '
                                        if lineguide[pfield] == 'freq':
                                            line += '[$RATBASE * %d/%d * %d/%d]' % (note.dict['num'], note.dict['den'], self.regionlist[note.region].num, self.regionlist[note.region].den)
                                        elif lineguide[pfield] == 'db':
                                            line += '%f' % (float(note.dict['db']) + float(outline.volume))
                                        else:
                                            try:
                                                line += str(note.dict[lineguide[pfield]])
                                            except:
                                                line += str(lineguide[pfield])
                                    line += os.linesep
                                    self.csdsco += line
                    if not instlist[note.inst].outlist:
#                        line = 'i "ratratdefaulton" %f %f %f [$RATBASE * %d/%d * %d/%d] %d%s' % (note.time, note.dur, note.db, note.num, note.den, self.regionlist[note.region].num, self.regionlist[note.region].den, note.voice, os.linesep)
                        line = 'i "ratratdefaulton" %f %f %d 0 %f %f [$RATBASE * %d/%d * %d/%d]%s' % (note.time, note.dur, note.voice, note.dur, note.db, note.num, note.den, self.regionlist[note.region].num, self.regionlist[note.region].den, os.linesep)
#                        print line
                        self.csdsco += line
            else:
#                line = 'i "ratratdefaulton" %f %f %f [$RATBASE * %d/%d * %d/%d] %d%s' % (note.time, note.dur, note.db, note.num, note.den, self.regionlist[note.region].num, self.regionlist[note.region].den, note.voice, os.linesep)
                line = 'i "ratratdefaulton" %f %f %d 0 %f %f [$RATBASE * %d/%d * %d/%d]%s' % (note.time, note.dur, note.voice, note.dur, note.db, note.num, note.den, self.regionlist[note.region].num, self.regionlist[note.region].den, os.linesep)
                self.csdsco += line


#############TIME CURSOR
        if len(playscore) and method == 0:
            icounter = self.ratstart
#            last = playscore[-1]
            while icounter <= tottime:
                self.csdsco += 'i "ratcounter" %f .125%s' % (icounter, os.linesep)
                icounter += .125

#########CsOptions
########    (self, instlist, method, sr, ksmps, nchnls, amodule, dac, b, B, aifffile, wavfile, commandline, commandlineuse)
        if commandlineuse == 1:
            if commandline.startswith('csound '):
                self.csdopt = commandline
            else:
                self.csdopt = 'csound ' + commandline
            if not self.csdopt.count('.orc'):
                self.csdopt += ' test.orc'
            if not self.csdopt.count('.sco'):
                self.csdopt += ' test.sco'

        else:
            self.csdopt = 'csound -m0d'
            if method == 0:
                ##realtime
                self.csdopt += ' -+rtaudio=%s' % amodule
                if amodule == 'portaudio' or amodule == 'mme':
#		    print dac
                    self.csdopt += ' -odac%s' % dac.strip().split(':')[0] 
                elif amodule == 'alsa' or amodule == 'jack':
                ## everything between first two sets of double-quotes
                    slicestart = dac.find('"') + 1
                    sliceend = dac.find('"', slicestart)
                    self.csdopt += ' -odac:%s' % dac[slicestart:sliceend]
                elif amodule == 'coreaudio':
                    self.csdopt += ' -odac'
                if b > 0:
                    self.csdopt += ' -b%d' % b
                if B > 0:
                    self.csdopt += ' -B%d' % B
            elif method == 1:
                ##aiff
                if aifffile.endswith('.aiff'):
                    self.csdopt += ' -Ao %s' % aifffile
                else:
                    self.csdopt += ' -Ao %s.aiff' % aifffile
            elif method == 2:
                ##wav
                if wavfile.endswith('.wav'):
                    self.csdopt += ' -Wo %s' % wavfile
                else:
                    self.csdopt += ' -Wo %s.wav' % wavfile
            self.csdopt += ' test.orc test.sco'

#########CsInstruments
        csdinstreplace = 'sr = %d%sksmps = %d%snchnls = %d%s%s' % (sr, os.linesep, ksmps, os.linesep, nchnls, os.linesep, os.linesep)
        if self.csdimported.count("<CsInstruments>"):
            orcstart = self.csdimported.find("<CsInstruments>") + 15
            orcend = self.csdimported.find("</CsInstruments>")
            csdimportinst = self.csdimported[orcstart:orcend]
            flag = 1
            permaflag = 1
            for line in csdimportinst.splitlines(True):
                if permaflag == 1:
                    if flag == 1:
                        if line.strip().startswith('opcode'):
                            csdinstreplace += line
                            flag = 0
                        elif line.strip().startswith('instr '):
                            csdinstreplace += line
                            permaflag = 0
                        elif line.strip().startswith('sr') or line.strip().startswith('kr') or line.strip().startswith('ksmps') or line.strip().startswith('nchnls'):
                            pass
                        else:
                            csdinstreplace += line
                    else:
                        csdinstreplace += line
                        if line.strip().startswith('endop'):
                            flag = 1
                else:
                    csdinstreplace += line

        self.csdinst = '''
giratdefaulttable  ftgen   0, 0, 2048, 10, 1, .2, .1
girattcursor init ''' + str(self.ratstart) + '''
girattcursor chnexport "rattime", 2
girattimeskip init 0
girattimeskip chnexport "rattimeskip", 1
'''
######add sf2 loading opcodes in orc header
        for ind, tempfile in enumerate(sf2list):
            self.csdinst += 'giratsf2file%d sfload "%s"%s' % (ind, tempfile.filename, os.linesep)
        for ind, tempitem in enumerate(proglist):
            for sf2 in sf2list:
                if sf2.basename == tempitem[2].basename:
                    sf2no = sf2list.index(sf2)
            self.csdinst += 'giratsf2preset%d sfpreset %s, %s, giratsf2file%d, %d%s' % (ind, tempitem[0].split()[0], tempitem[1], sf2no, ind, os.linesep)

        self.csdinst = self.csdinst + csdinstreplace + '''
instr +ratdefault
;iact	active	p1
;	print p1, iact, p3
iamp1   =       ampdb(p4) * .7
iamp2   =       iamp1
iamp3   =       iamp1
iamp4   =       iamp1
idur    =       abs(p3)
iporttime = idur/16
;iporttime = 1
ifreq   =       p5
iphs = -1
tigoto tiedin
iamp1 = 0
iamp2 = ampdb(p4)
iphs = 0
kfreq init ifreq
kfreq port ifreq, iporttime, ifreq
tiedin:
if p3 < 0 igoto tiedout
iamp4 = 0
tiedout:
;        printk2 kfreq
;print   ifreq
;aamp    transeg 0, .004, 1, iamp, idur-.01, 1, iamp * .4, .006, 1, 0
aamp    transeg iamp1, .004, 1, iamp2, .004, 1, iamp3, idur-.014, 1, iamp3, .006, 1, iamp4
aosc    oscil   1, kfreq, giratdefaulttable, iphs
aflt    lowpass2 aosc, 1200, 5
aenv    =       aflt * aamp
aout    =       aenv
outc    aout, aout
endin

instr +ratratdefaulton
instnum nstrnum "ratdefault"
inum = instnum + (p4/1000)
;event_i "i", inum, 0, p6, p7, p8
al, ar	subinstr	inum, p7, p8
	outc	al, ar
endin

instr +ratsf2default
;idur    =       p3
isus    =       p9
iamp1   =       ampdb(p4) * isus/0dbfs
iamp2   =       iamp1
iamp3   =       iamp1
iamp4	=	iamp1
idur    =       abs(p3)
iporttime = idur/16
;iamp	=	ampdb(p4)
;kamp	init	iamp/0dbfs
;kamp	init	1
ivel	=	127 * ampdb(p4)/0dbfs
inotenum=	1
ifreq   =       p5
iphs = -1
iatt	=	0
idec	=	0
irel	=	0
tigoto tiedin
iamp1	=	0
iamp2	=	ampdb(p4)/0dbfs
iphs = 0
kfreq init ifreq
kfreq port ifreq, iporttime, ifreq
iatt    =       p7/1000 + .001
idec    =       p8/1000 + .001
tiedin:
if p3 < 0 igoto tiedout
iamp4	=	0
irel	=	p10/1000 + .001
tiedout:
;kfreq	init	p5
ipreindex=	p6
iflag	=	1
ioffset	=	0
ienv	=	0
;aenv    transeg 0, iatt, 1, 1, idec, 1, isus, idur-(iatt+idec+irel), 0, isus, irel, 1, 0
kamp    transeg iamp1, iatt, 1, iamp2, idec, 1, iamp3, idur-(iatt+idec+irel), 1, iamp3, irel, 1, iamp4
;print   iamp3
;printk2  kamp
al, ar	sfplay	ivel, inotenum, kamp, kfreq, ipreindex, iflag, ioffset, ienv
al      =       al; * aenv
ar      =       ar; * aenv
	outc	al, ar
endin

instr +ratratsf2defaulton
instnum nstrnum "ratsf2default"
inum = instnum + (p4/1000)
;event_i "i", inum, 0, p5, p6, p7, p8, p9, p10, p11, p12
al, ar	subinstr	inum, p6, p7, p8, p9, p10, p11, p12
	outc	al, ar
endin
'''
        nothing = '''
instr +ratsf2default
;idur    =       p3
iamp1   =       ampdb(p4)
iamp2   =       iamp1
iamp3   =       iamp1
idur    =       abs(p3)
iporttime = idur/16
;iamp	=	ampdb(p4)
kamp	init	iamp/0dbfs
ivel	=	127 * iamp/0dbfs
inotenum=	1
ifreq   =       p5
iphs = -1
tigoto tiedin
iamp1 = 0
iphs = 0
kfreq init ifreq
kfreq port ifreq, iporttime, ifreq
tiedin:
if p3 < 0 igoto tiedout
iamp3 = 0
tiedout:
;kfreq	init	p5
ipreindex=	p6
iatt    =       p7/1000
idec    =       p8/1000
isus    =       p9
irel    =       p10/1000
iflag	=	1
ioffset	=	0
ienv	=	0
;aenv    transeg 0, iatt, 1, 1, idec, 1, isus, idur-(iatt+idec+irel), 0, isus, irel, 1, 0
aenv    transeg iamp1, iatt, 1, iamp2, idur-.01, 1, iamp2, .006, 1, iamp3
al, ar	sfplay	ivel, inotenum, kamp, kfreq, ipreindex, iflag, ioffset, ienv
al      =       al * aenv
ar      =       ar * aenv
	outc	al, ar
endin
'''

        for toinst in todict.values():
            self.csdinst += toinst[1]
        for ind1, instrument in enumerate(instlist):
            if ind1:  # avoid instlist[0], which is a placeholder
                for ind2, outline in enumerate(instrument.outlist):
                    if outline.__class__.__name__ == 'oscout':
                        oscinst = '%sinstr +ratoscdefault%drat%d%son' % (os.linesep, ind1, ind2, os.linesep)
                        oscinst += 'Shost strcpy "%s"%siport = %d%sSpath strcpy "%s"%sOSCsend 1, Shost, iport, Spath, "' % (outline.host, os.linesep, outline.port, os.linesep, outline.path, os.linesep)
                        include, pnum = 1, 0
                        for element in outline.string.split():
                            if element.startswith('[') and not element.endswith(']'):
                                include = 0
                            elif element.endswith(']') and not element.startswith('['):
                                pnum += 1
                                include = 1
                            elif include == 1:
                                pnum += 1
#                            oscinst += 'f'
                        for i in range(0, pnum):
                            oscinst += 'f'
                        oscinst += '"'
#                        last = len(outline.string.split()) + 4
#                        for pnumber in range(4, last):
                        for pnumber in range(4, pnum + 4):
                            oscinst += ', p%d' % pnumber
                        oscinst += '%sendin%s' % (os.linesep, os.linesep)
                        self.csdinst += oscinst

                ## add note-off instrument for OSC instance, if required
                        if outline.noff:
                            oscinst = '%sinstr +ratoscdefault%drat%d%soff' % (os.linesep, ind1, ind2, os.linesep)
                            oscinst += 'Shost strcpy "%s"%siport = %d%sSpath strcpy "%s"%sOSCsend 1, Shost, iport, Spath, "' % (outline.host, os.linesep, outline.port, os.linesep, outline.noffpath, os.linesep)
                            include, pnum = 1, 0
                            for element in outline.noffstring.split():
                                if element.startswith('[') and not element.endswith(']'):
                                    include = 0
                                elif element.endswith(']') and not element.startswith('['):
                                    pnum += 1
                                    include = 1
                                elif include == 1:
                                    pnum += 1
#                            oscinst += 'f'
                            for i in range(0, pnum):
                                oscinst += 'f'
                            oscinst += '"'
#                        last = len(outline.string.split()) + 4
#                        for pnumber in range(4, last):
                            for pnumber in range(4, pnum + 4):
                                oscinst += ', p%d' % pnumber
                            oscinst += '%sendin%s' % (os.linesep, os.linesep)
                            self.csdinst += oscinst

        self.csdinst += '''
instr +ratcounter
girattcursor = girattcursor + .125
endin
'''
        return tottime

    def csdreload(self):
        if self.outautoload == True and self.csdimport != None:
            file = open(self.csdimport)
            self.csdimported = ''
            for line in file:
                self.csdimported += line
            try:
                self.out.csdtext.delete(1.0, "end")
                self.out.csdtext.insert("end", self.csdimported)
            except:
                pass

    def waitforconnect(self, sock, q):
        conn = sock.accept()
        q.put(conn)

    def delegatecallbacks(self, sock):
        cbtext = ''
        while self.playing == 1:
#            if select.select((sock,),(),())[0]:
            try:
                cbtext += sock.recv(32)
                while cbtext.count('CB'):
                    cb, cbtext = cbtext.split('CB', 1)
                    if cb == 'END':
#                    self.playing = 0
#                    print "END received"
#                        print "END received"
                        self.stop()
                    elif self.outputmethod == 0:
#                        print 'cb', cb
                        if self.playing == 1:
                            self.cursor.scrollabs(float(cb))
            except:
                print "Callback Socket Unavailable"

    def delegatescrubcallbacks(self, sock):
#        print sock.__class__.__name__
#        print sock
        cbtext = ''
        flag = 1
        while flag == 1:
#            if select.select((sock,),(),())[0]:
            cbtext += sock.recv(32)
            while cbtext.count('CB'):
                cb, cbtext = cbtext.split('CB', 1)
                if cb == 'END':
                    flag = 0
                    sock.close()
                    del sock

    def messagesend(self, dest, msg):
        dest.write(msg.replace(msg.replace(os.linesep, '$RATNEWLINE')))

### Play ###
    def play(self, instlist, sf2list, method, sr, ksmps, nchnls, amodule, dac, b, B, aifffile, wavfile, commandline, commandlineuse):
        '''A hot mess...

        Lots of workarounds added that could probably be replaced by more efficient code, but it appears to work as expected at this point, and there's music to be written.'''

        if len(self.notelist) and self.mode.get() != 3 and self.allowed2play:
            self.allowed2play = 0
            cstart = 1
#            for instno in range(1, len(instlist)):
#                if not instlist[instno].mute:
#                    for out in instlist[instno].outlist:
#                        if not out.mute:
#                            cstart = 1
#                            break
            if cstart:
                tottime = self.preparecsd(instlist, sf2list, method, sr, ksmps, nchnls, amodule, dac, b, B, aifffile, wavfile, commandline, commandlineuse)
#                print self.csdsco

        #create socket to receive callbacks to move the time cursor
                cbwait = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                count = 0
                while count < 30000:
                    try:
                        cbwait.bind(('127.0.0.1', self.cbport))
                        print 'Callback Port: %s' % str(self.cbport)
                        count = 30000
                    except:
                        self.cbport += 1
                        count += 1
                        if count == 30000:
                            print "NO PORTS AVAILABLE FOR CALLBACK"

                cbwait.listen(2)
#                self.outsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #thread to wait for rataudio to connect
                q = Queue.Queue()
                wait = threading.Thread(target=self.waitforconnect, args=(cbwait, q))
                wait.start()

                count = 0
#                while count < 10000:
#                    tmpsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                    try:
#                        tmpsoc.bind(('127.0.0.1', self.outport))
#			print 'outport:', self.outport
#                        count = 10000
#                        del tmpsoc
#                    except:
#                        self.outport += 1
#                        count += 1
#			print "count:", count
#                        del tmpsoc
#            #Rationale AUdio engine
#		print "final countdown:", count
                self.rau = subprocess.Popen((sys.executable, 'rataudio.py', str(self.cbport)))
                if sys.platform.count("linux"):
                    try:
                        os.nice(-1)
                        os.nice(6)
                    except: pass

#            success = self.rau.poll()
            #if success:
#            print success

#                connected = False
#                while not connected:
#                    try:
#                        self.outsock.connect(('127.0.0.1', self.outport))
#			print 'outsock connected to:', self.outport
#                        connected = True
#                    except:
##			print "outsock failed to connect to:", self.outport
#                        time.sleep(.1)
#

                wait.join()
                self.cbsock = q.get()[0]
#		waitflag = True
#		while waitflag:
#                    try:
#			self.cbsock = q.get()[0]
#			waitflag = False
#			print 'cb connected'
#                    except: pass

                try: self.audiodialog.playbutton.configure(text='Stop', command=self.audiodialog.stop)
                except: pass
                try: self.out.playbutton.configure(text='Stop', command=self.stop)
                except: pass
                self.playing = 1
                self.statusplay.configure(text="Playing")
                threading.Thread(target=self.delegatecallbacks, args=(self.cbsock,)).start()

                self.cbsock.sendall('csdopt:%sRATENDMESSAGE' % self.csdopt)
                self.cbsock.sendall('csdorc:%sRATENDMESSAGE' % self.csdinst)
                self.cbsock.sendall('csdsco:%sRATENDMESSAGE' % self.csdsco)
                self.cbsock.sendall('csdgozRATENDMESSAGE')


    def stop(self):
        if self.playing == 1:
            try:
                self.playing = 0
                self.statusplay.configure(text="Stopped")
#                print "Stop"
#                self.cbsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGEcsdclnRATENDMESSAGE')
                self.cbsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGE')
                ended = self.rau.communicate()
                self.cbsock.close()


#                self.cbsock.shutdown(socket.SHUT_RD)
#                del self.cbsock
            except: print "Unable to Close Audio Engine"
            self.internalstop()

#            if len(self.notelist):
#                coords = self.score.coords(self.barlist[self.cursor.beat])
#                self.score.coords(self.cursor.widget, coords[0]-3, self.miny, coords[0]+3, self.maxy)
#                self.cursor.center = coords[0]
#            self.playing = 0

    def internalstop(self):
        if self.playing == 0:
            if sys.platform.count("linux"):
                try:
                    os.nice(-5)
                except: pass
            if len(self.notelist):
                self.cursor.scrollabs(float(self.score.coords(self.barlist[self.cursor.beat])[0])/self.xperquarter)
                
#            try: self.audiodialog.buttons.subwidget('play').configure(text='Play', command=self.audiodialog.play)
            try: self.audiodialog.playbutton.configure(text='Play', command=self.audiodialog.play)
            except: pass
#            try: self.out.outputbuttons.subwidget('play').configure(text='Play', command=self.out.audition)
            try: self.out.playbutton.configure(text='Play', command=self.out.audition)
            except: pass
            self.playing = 0
            self.statusplay.configure(text="Stopped")
        self.allowed2play = 1

### Tonality Change###
#    def tonchange(self, innum, inden):
    def tonchange(self, innum, inden, yadj):
        com = comtonchange(self, self.hover.hregion, innum, inden, self.octave11, yadj)
        if self.dispatcher.push(com):
            self.dispatcher.do()

        return

### Sort extant score notes ###
    def scsort(self):
        '''Sort notes according to note-off time!

        Rationale sorts notes according to their end time, so that the last note's end time marks the end of the score.  It simplifies certain things.'''
        sc = self.notewidgetlist
#        sorter=[(s.purex,s) for s in sc]
#        sorter.sort()
        sc.sort(key=lambda nw:(nw.note.time+abs(nw.note.dur), nw.note.time))
#        for nw in sc:
#            print nw.note.num
#        self.notewidgetlist[:]=[t[1] for t in sorter]
        self.notewidgetlist[:] = [t for t in sc]
        self.notelist = [nw.note for nw in self.notewidgetlist]

    def buttondown(self, event):
        if self.mode.get() == 1 and not self.poppedup:
            if self.overdur == 0:
                if self.editreference != None:
                    if self.editreference.note.sel:
                        if self.shiftkey:
                            com = comedittime(self, [nw.note.id for nw in self.notewidgetlist if nw.note.sel], 0)
                        else:
                            com = comeditnumden(self, [nw.note.id for nw in self.notewidgetlist if nw.note.sel], 1, 1)

                        if self.dispatcher.push(com):
                            self.dispatcher.do()
                    else:
                        com = comselect(self, (self.editreference.note.id,), [nw.note.id for nw in self.notewidgetlist if nw.note.sel==1])
                        com.do()
#                        if self.dispatcher.push(com):
#                            self.dispatcher.do()

                        if self.shiftkey:
                            com = comedittime(self, (self.editreference.note.id,), 0)
                        else:
                            com = comeditnumden(self, (self.editreference.note.id,), 1, 1)
                        if self.dispatcher.push(com):
                            self.dispatcher.do()

                else:
                    self.selectbox = selectbox(self, event)
            else:
                self.durgrab(event)
        elif self.mode.get() == 3 and not self.poppedup:
            try:
                self.scrubber.buttondown(event)
            except: pass

    def durgrab(self, event):
        self.dragcoords = self.score.coords("durdrag")
        self.startinit = self.dragcoords[4]
#        self.leninit = self.dragcoords[8]-self.dragcoords[4]
#        self.durinit = self.leninit/self.xperquarter
        noteid = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in self.score.find_withtag("durdrag")]
#        com = comeditdurmouse(self, noteid)
#        if self.dispatcher.push(com):
#            self.dispatcher.do()

    def durdrag(self, event):
        if self.dispatcher.comlist and self.dispatcher.comlist[-1].__class__.__name__ == 'comeditdurmouse' and not self.dispatcher.comlist[-1].finalized:
            self.dispatcher.increment('comeditdurmouse', self.score.canvasx(event.x))
        else:
            com = comeditdurmouse(self, [nw.note.id for nw in self.notewidgetlist if nw.notewidget in self.score.find_withtag("durdrag")], self.score.canvasx(event.x))
            if self.dispatcher.push(com):
                self.dispatcher.do()

    def shiftbuttonmotion(self, event):
        if self.mode.get() == 1:
            if self.overdur == 0:
                if self.editreference != None: #over note
                    widget = event.widget
                    realx = widget.canvasx(event.x)
                    quantizedx = int(realx/self.xpxquantize) * self.xpxquantize
                    xdelta = quantizedx - self.editreference.purex
                    self.dispatcher.increment("comedittime", xdelta)
                else: #not over note
                    try: self.selectbox.adjust(event)
                    except: pass
            else: #overdur
                self.durdrag(event)

    def buttonmotion(self, event):
        if self.mode.get() == 1:
            if self.overdur == 0:
                if self.editreference == None:
                    self.selectbox.adjust(event)
#                    try: self.selectbox.adjust(event)
#                    except: pass
                else:
##############
                    widget = event.widget
                    realy = widget.canvasy(event.y)
                    yloc = self.regionlist[self.editreference.note.region].octave11 - realy
##                    ynotestorage = int(yloc * 240 / self.octaveres) % self.octaveres
#                    ynotestorage = int(240 * (yloc % self.octaveres) / self.octaveres)
                    index = 2**((yloc % self.octaveres) / self.octaveres)
                    distance = 10
                    closest = (0, 1, 1)
                    for ratio in self.notebanklist[self.notebankactive].numdenlist:
        #                print "ratio =", float(ratio[1])/ratio[2]
                        closeness = (float(ratio[0])/ratio[1]) - index
        #                print "closeness:", closeness
                        if abs(closeness) <= distance:
                            distance = abs(closeness)
                            closest = ratio
                        else:
                            break
#        #            print 'ynotestorage', self.ynotestorage
#        #            prenum = self.notebank[self.ynotestorage][1]
#        #            preden = self.notebank[self.ynotestorage][2]
                    prenum, preden = closest[0], closest[1]
##                    prenum = self.notebank[ynotestorage][1]
##                    preden = self.notebank[ynotestorage][2]
                    if yloc >= self.octaveres:
                        prenum *= 2**int((yloc)/self.octaveres)
                    elif yloc < 0:
                        preden *= 2**(0-((int(yloc)/self.octaveres)))
                    numdelta = prenum * self.editreference.note.den
                    dendelta = preden * self.editreference.note.num
                    ids = [nw.note.id for nw in self.notewidgetlist if nw.note.sel == 1]
                    self.dispatcher.increment("comeditnumden", numdelta, dendelta)
#                    if not self.unsaved:
#                        self.unsaved = True
#                        if self.filetosave:
#                            file = os.path.basename(self.filetosave)
#                        else:
#                            file = 'New Score'
#                        self.myparent.title('*Rationale %s: %s' % (vs, file))

##############
            else:
                self.durdrag(event)
        elif self.mode.get() == 3:
            self.scrubber.scroll(event)

    def normalmotion(self, event):
#        self.scoredrag(event)
        if self.mode.get() == 0:
            self.hover.hovermotion(event)
            self.otherseek(event)
        elif self.mode.get() == 1:
            self.editseek(event)
        elif self.mode.get() == 2:
            self.deleteseek(event)
        else:
            self.scrubber.seek(event)
#            self.otherseek(event)
#        self.editseek(event)

    def shiftmotion(self, event):
        if self.mode.get() == 1:
            self.editseek(event)

    def otherseek(self, event):
        self.score.itemconfig("note", stipple="", activefill='', activeoutline='', activewidth=1)
        self.score.dtag("note", "edit")
        widget = event.widget
        realx = widget.canvasx(event.x)
        realy = widget.canvasy(event.y)
        notes = self.score.find_overlapping(realx-10, realy-10, realx+10, realy+10)
        note = 0
        absall = 10
        tempflag = 0
        flag = 0
        for match in notes:
            if "note" in self.score.gettags(match):
                coords = self.score.coords(match)
                mainxy = (coords[0], coords[1])
                maindist = math.sqrt((mainxy[0]-realx)**2 + (mainxy[1]-realy)**2)
                if maindist < absall:
                    absall = maindist
                    note = match
		if sys.platform.count("darwin"):
		    self.score.itemconfig(note, activefill="#888888", activeoutline="#552222", activewidth=3)
		else:
	            self.score.itemconfig(note, stipple="gray50")
                self.score.addtag_withtag("edit", note)

    def editseek(self, event):
        self.score.itemconfig("note", stipple="", activefill='', activeoutline='', activewidth=1)
        self.score.dtag("note", "edit")
        widget = event.widget
        realx = widget.canvasx(event.x)
        realy = widget.canvasy(event.y)
        notes = self.score.find_overlapping(realx-10, realy-10, realx+10, realy+10)
        note = 0
        absall = 10
        tempflag = 0
        flag = 0
        for match in notes:
            if "note" in self.score.gettags(match):
                coords = self.score.coords(match)
                mainxy = (coords[0], coords[1])
                durxy = (coords[8], coords[9])
                maindist = math.sqrt((mainxy[0]-realx)**2 + (mainxy[1]-realy)**2)
                durdist = math.sqrt((durxy[0]-realx)**2 + (durxy[1]-realy)**2)
                if durdist < maindist:
                    abs = durdist
                    tempflag = 1
                else:
                    abs = maindist
                    tempflag = 0
                if abs < absall:
                    absall = abs
                    note = match
                    flag = tempflag
        if note == 0:
            self.overdur = 0
            self.score.configure(cursor="pencil")
            self.score.dtag("note", "durdrag")
            self.editreference = None
        else:
            if flag == 1:
                self.overdur = 1
                self.score.configure(cursor="right_side")
                self.score.addtag_withtag("durdrag", note)
            if flag == 0:
                self.overdur = 0
                if self.shiftkey == 0:
                    self.score.configure(cursor="sb_v_double_arrow")
                else:
                    self.score.configure(cursor="sb_h_double_arrow")
		if sys.platform.count("darwin"):
		    self.score.itemconfig(note, activefill="#888888", activeoutline="#552222", activewidth=3)
		else:
	            self.score.itemconfig(note, stipple="gray50")
#                self.score.itemconfig(note, stipple="gray50")
                self.score.addtag_withtag("edit", note)
                for notewidget in self.notewidgetlist:
                    if notewidget.notewidget == note:
                        self.editreference = notewidget

#                self.score.addtag_withtag("editreference", note)
#                self.selectbox = selectbox(self, event)

### Add a Note ###
    def buttonup(self, event):
        winfo = (str(self.scorewin.winfo_name()))
        winfocus = (str(self.scorewin.focus_get()))
        if self.poppedup:
            self.menupopup.unpost()
            self.poppedup = False
# conditional based on whether window is active #
#        if (winfocus.endswith(winfo)):
        elif winfocus != None and self.mode.get() == 0 and self.hover.hinst not in self.hidden:
            ### Add Note ###
            inst = self.hover.hinst
            time = self.hover.posx/self.xperquarter
            dur = self.hover.entrydur
            db = self.hover.hdb
            num = self.hover.hnum
            den = self.hover.hden
            voice = self.hover.hvoice
            if voice == 0:
                held = 0
            else:
                held = 1
            region = self.hover.hregion
            rnum = self.regionlist[region].num
            rden = self.regionlist[region].den
            rcolor = self.regionlist[region].color
            sel = 0
            arb = []
            yloc = self.yadj
            locy2 = yloc
            locy0 = yloc - self.hover.hyoff
            locy1 = yloc + self.hover.hyoff
            ry0 = yloc - 15
            ry1 = yloc + 15
            noteinfo = [(self.noteid, self.hover.hinst, self.hover.hvoice, time, dur, db, num, den, region, sel)]
            com = comaddnotes(self, noteinfo)
            if self.dispatcher.push(com):
                self.dispatcher.do()
            self.noteid += 1
#            if not self.unsaved:
#                self.unsaved = True
#                if self.filetosave:
#                    file = os.path.basename(self.filetosave)
#                else:
#                    file = 'New Score'
#                self.myparent.title('*Rationale %s: %s' % (vs, file))

        elif winfocus != None and self.mode.get() == 1:
            if self.overdur == 0 and self.editreference == None:
                self.selectbox.lift(event)
                self.score.delete(self.selectbox.widget)
                del self.selectbox
            elif self.overdur:
                if self.dispatcher.comlist[-1].__class__.__name__ == "comeditdurmouse" and not self.dispatcher.comlist[-1].finalized:
                    self.dispatcher.comlist[-1].finalized = True

        elif winfocus != None and self.mode.get() == 2:
            ### Delete Note ###
            deletematch = self.score.find_withtag("delete")
            if deletematch:
                todel = deletematch[0]
                ids = [nw.note.id for nw in self.notewidgetlist if nw.notewidget == todel]
                com = comdeletenotes(self, ids)
                if self.dispatcher.push(com):
                    self.dispatcher.do()

        elif winfocus != None and self.mode.get() == 3:
            try:
                self.scrubber.release()
            except: pass

    def write(self,s):
        self.stdouttxt.configure(state='normal')
        self.stdouttxt.insert('end', '%s%s%s' % (s, os.linesep, os.linesep))
        self.stdouttxt.configure(state='disabled')
        self.stdouttxt.update_idletasks()
        if self.stdscroll.winfo_ismapped():
            pass
        else:
            if self.stdscroll.get() != (0.0, 1.0):
                self.stdscroll.grid(row=0, column=1, rowspan=1, sticky='ns')
        self.stdouttxt.see('end')

    def opennotebankdialog(self, *args):
        try:
            self.notebanks.lift()
            self.notebanks.focus_set()
        except:
            self.notebanks = ndialog.notebankdialog(self)
            self.notebanks.lift()
            self.notebanks.focus_set()
        self.bkey = self.ctlkey = 0

    def openoutputdialog(self, *args):
        try:
            self.out.outputfr.lift()
            self.out.outputfr.focus_set()
        except:
            self.out = odialog.outputdialog(self)
            self.out.outputfr.lift()
            self.out.outputfr.focus_set()
        self.ctlkey = 0

    def openregiondialog(self, *args):
        try:
            self.regiondialog.regionfr.lift()
            self.regiondialog.regionfr.focus_set()
        except:
            self.regiondialog = rdialog.regiondialog(self)
            self.regiondialog.regionfr.lift()
            self.regiondialog.regionfr.focus_set()
        self.ctlkey = 0

    def opentempodialog(self, *args):
        try:
            self.tempodialog.tempofr.lift()
            self.tempodialog.tempofr.focus_set()
        except:
            self.tempodialog = tdialog.tempodialog(self)
            self.tempodialog.tempofr.lift()
            self.tempodialog.tempofr.focus_set()
        self.ctlkey = 0

    def openmeterdialog(self, *args):
        try:
            self.meterdialog.meterfr.lift()
            self.meterdialog.meterfr.focus_set()
        except:
            self.meterdialog = mdialog.meterdialog(self)
            self.meterdialog.meterfr.lift()
            self.meterdialog.meterfr.focus_set()
        self.ctlkey = 0

    def globalcancel(self, event):
        self.ctlkey = self.shiftkey = self.altkey = self.numkey = self.rkey = self.vkey = self.bkey = 0

    def shift1(self, event):
        print "shift1"
        self.hinstch = self.hinstch * 10 + 1

    def shift2(self, event):
        self.hinstch = self.hinstch * 10 + 2

    def shift3(self, event):
        self.hinstch = self.hinstch * 10 + 3

    def shift4(self, event):
        self.hinstch = self.hinstch * 10 + 4

    def shift5(self, event):
        self.hinstch = self.hinstch * 10 + 5

    def shift6(self, event):
        self.hinstch = self.hinstch * 10 + 6

    def shift7(self, event):
        self.hinstch = self.hinstch * 10 + 7

    def shift8(self, event):
        self.hinstch = self.hinstch * 10 + 8

    def shift9(self, event):
        self.hinstch = self.hinstch * 10 + 9

    def shift0(self, event):
        self.hinstch = self.hinstch * 10 + 0

    def shifttest(self, event):
        print "shifttest", event.keysym

    def keypress(self, event):
#        print event.char
#        if event.keysym.isdigit():
#            print "isdigit", event.keysym
#        print event.keysym, event.keycode, event.keysym_num
#        print 'ctl %d shift %d alt %d num %d v %d r %d%s' % (self.ctlkey, self.shiftkey, self.altkey, self.numkey, self.vkey, self.rkey, os.linesep)
#        print event.keysym
#        print event.keycode
#        print event.keysym_num
#        print "event.serial:", event.serial, event.keysym
#        print "event.type:", event.type
        if event.keysym.count("Shift"):
            self.hinstch = 0
            self.editinst = 0
            self.shiftkey = 1
            if self.mode.get() == 1 and self.editreference != None:
                self.score.configure(cursor="sb_h_double_arrow")
        elif event.keysym.count(self.control):
            self.ctlkey = 1
            self.quant = 0
        elif event.keysym.count(self.alt):
            self.hide = 0
            self.altkey = 1
        elif self.shiftkey == self.ctlkey == self.rkey == self.vkey == self.bkey == 0 and self.altkey == 1:
            if event.keycode in self.shiftnum1:
                self.hide = self.hide * 10 + self.shiftnum1.index(event.keycode)
            elif event.keycode in self.shiftnum2:
                self.hide = self.hide * 10 + self.shiftnum2.index(event.keycode)
            elif event.keysym in "1234567890":
		self.hide = self.hide * 10 + int(event.keysym)
            elif event.keysym == "s" or event.keysym == "S":
                self.showall()
        elif self.shiftkey == self.ctlkey == self.altkey == self.rkey == self.bkey == 0 and self.vkey == 1:
            if event.keysym in "1234567890":
                if self.mode.get() == 0:
                    self.hover.hvoice = 10 * self.hover.hvoice + int(event.keysym)
                    self.score.itemconfigure(self.hover.hvoicedisp, text=str(self.hover.hvoice))
                    self.statusvoice.configure(text='Voice %d' % self.hover.hvoice)
                    self.write(str(self.hover.hvoice))
                elif self.mode.get() == 1:
                    self.editvoice = 10 * self.editvoice + int(event.keysym)
        elif self.shiftkey == self.ctlkey == self.altkey == self.rkey == self.vkey and self.bkey == 1:
            if self.mode.get() == 0 or self.mode.get() == 1:
                if event.keysym in "1234567890":
                    self.notebankactive = self.notebankactive * 10 + int(event.keysym)
                    self.statusbank.configure(text='Bank %d' % self.notebankactive)
                elif event.keycode in self.shiftnum1:
                    self.notebankactive = self.notebankactive * 10 + self.shiftnum1.index(event.keycode)
                    self.statusbank.configure(text='Bank %d' % self.notebankactive)
                elif event.keycode in self.shiftnum2:
                    self.notebankactive = self.notebankactive * 10 + self.shiftnum2.index(event.keycode)
                    self.statusbank.configure(text='Bank %d' % self.notebankactive)
        elif self.shiftkey == 1 and self.ctlkey == self.altkey == self.rkey == self.vkey == self.bkey == 0:
            if event.keycode in self.shiftnum1:
#############################################
#                print "shiftnum1", event.keycode
                if self.mode.get() == 0:
                    self.hinstch = self.hinstch * 10 + self.shiftnum1.index(event.keycode)
                elif self.mode.get() == 1:
                    self.editinst = self.editinst * 10 + self.shiftnum1.index(event.keycode)
            elif event.keycode in self.shiftnum2:
#                print event.keycode
                if self.mode.get() == 0:
                    self.hinstch = self.hinstch * 10 + self.shiftnum2.index(event.keycode)
                elif self.mode.get() == 1:
                    self.editinst = self.editinst * 10 + self.shiftnum2.index(event.keycode)
        elif self.shiftkey == self.rkey == self.vkey == self.bkey == self.altkey == 0 and self.ctlkey == 1:
            if event.keysym in "1234567890":
		self.quant = self.quant * 10.0 + int(event.keysym)
        elif self.ctlkey == self.shiftkey == self.rkey == self.vkey == self.bkey == self.altkey == 0:
            if event.keysym == "comma" or event.keysym == "less":
                self.xquantize = 1/6.0
                self.xpxquantize = self.xquantize * self.xperquarter
            elif event.keysym == "period" or event.keysym == "greater":
                self.xquantize = .25
                self.xpxquantize = self.xquantize * self.xperquarter
            elif event.serial != self.norepeat and event.keysym == "r" or event.keysym == "R":
                if self.hover.hregion:
                    self.hover.hregion = 0
                self.editregion = 0
                self.rkey = 1
            elif event.serial != self.norepeat and event.keysym == "v" or event.keysym == "V":
                if self.mode.get() == 0:
                    # the hover is no longer part of the tied-note process; maybe later
                    #oldinst = self.hover.hinst
                    #oldvoice = self.hover.hvoice
                    self.hover.hvoice = 0
                    self.statusvoice.configure(text='Voice ')
#                    self.statusvoice.configure(text="Voice 0")
                    #self.tiedraw(oldinst, oldvoice)
                elif self.mode.get() == 1:
                    self.editvoice = 0
                self.vkey = 1
            elif event.serial != self.norepeat and event.keysym == "b" or event.keysym == "B":
                if self.mode.get() == 0 or self.mode.get() == 1:
                    self.notebankactive = 0
                    self.statusbank.configure(text='Bank ')
                self.bkey = 1
    # Score Modes #
            if event.serial != self.norepeat and event.keysym == "a" or event.keysym == "A":
                self.menumode.invoke(0)
            elif event.serial != self.norepeat and event.keysym == "e" or event.keysym == "E":
                self.menumode.invoke(1)
            elif event.serial != self.norepeat and event.keysym == "d" or event.keysym == "D":
                self.menumode.invoke(2)
            elif event.serial != self.norepeat and event.keysym == "s" or event.keysym == "S":
                self.menumode.invoke(3)
            if event.keysym == "space" and event.serial != self.norepeat:
                if self.numkey == 0:
                    if self.playing == 0:
                        self.play(self.instlist, self.sf2list, self.outputmethod, self.sr, self.ksmps, self.nchnls, self.audiomodule, self.dac, self.b, self.B, self.aifffile, self.wavfile, self.csdcommandline, self.csdcommandlineuse)
                    else:
                        self.stop()
            # "space" while holding number sets dotted value of duration #
                elif self.numkey == 1:
                    if self.mode.get() == 0:
                        self.durupdate(self.hover.entrydur*1.5)
                    elif self.mode.get() == 1:
                        self.dispatcher.increment("comeditdurset", 1.5)

    # Durations #
            #32nd note#
            if event.keysym == "1":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(.125)
                    elif self.mode.get() == 1:
                        self.editmodedur(.125)
            #16th note#
            elif event.keysym == "2":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(.25)
                    elif self.mode.get() == 1:
                        self.editmodedur(.25)
            #8th note#
            elif event.keysym == "3":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(.5)
                    elif self.mode.get() == 1:
                        self.editmodedur(.5)
            #quarter note#
            elif event.keysym == "4":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(1)
                    elif self.mode.get() == 1:
                        self.editmodedur(1)
            #half note#
            elif event.keysym == "5":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(2)
                    elif self.mode.get() == 1:
                        self.editmodedur(2)
            #whole note#
            elif event.keysym == "6":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(4)
                    elif self.mode.get() == 1:
                        self.editmodedur(4)
            #double whole note#
            elif event.keysym == "7":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(8)
                    elif self.mode.get() == 1:
                        self.editmodedur(8)
            #and so on#
            elif event.keysym == "8":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(16)
                    elif self.mode.get() == 1:
                        self.editmodedur(16)
            elif event.keysym == "9":
                self.numkey = 1
                if event.serial != self.norepeat:
                    if self.mode.get() == 0:
                        self.durupdate(32)
                    elif self.mode.get() == 1:
                        self.editmodedur(32)
            # "t" while holding number sets triplet of duration #
            elif event.serial != self.norepeat and event.keysym == "t" or event.keysym == "T":
                if self.mode.get() == 0:
                    if self.numkey == 1:
                        self.durupdate(self.hover.entrydur*(2.0/3.0))
                    else:
                        self.tonchange(self.hover.hnum, self.hover.hden, self.yadj)
                elif self.mode.get() == self.numkey == 1:
                    self.dispatcher.increment("comeditdurset", 2.0/3.0)

            elif event.serial != self.norepeat and event.keysym == "g" or event.keysym == "G":
                if self.mode.get() < 2:
                    self.yadj = 240
                    self.tonchange(self.curden, self.curnum, self.yadj)

            elif event.keysym == "y" or event.keysym == "Y":
                if self.mode.get() == 0:
                    self.hover.increase(self.hover)
                elif self.mode.get() == 1:
                    self.editmodedbup()
            elif event.keysym == "h" or event.keysym == "H":
                if self.mode.get() == 0:
                    self.hover.decrease(self.hover)
                elif self.mode.get() == 1:
                    self.editmodedbdown()

            elif event.keysym == "o" or event.keysym == "O":
                self.openoutputdialog()

    # Region change #
        if self.rkey == 1 and self.ctlkey == self.altkey == self.shiftkey == 0 and event.keysym.isdigit():#str.isdigit(event.keysym):
            if self.mode.get() == 0:
                self.hover.hregion = self.hover.hregion * 10 + int(event.keysym)
            elif self.mode.get() == 1:
                self.editregion = self.editregion * 10 + int(event.keysym)
        if event.keysym.count("equal") or event.keysym.count("plus"):
            if self.ctlkey:
                self.zoom("in", vert=True)
            else:
                self.zoom("in")
        elif event.keysym.count("underscore") or event.keysym.count("minus"):
            if self.ctlkey:
                self.zoom("out", vert=True)
            else:
                self.zoom("out")
        elif event.keysym.count("BackSpace"):
            if self.ctlkey:
                self.zoom("reset", vert=True)
            else:
                self.zoom("reset")

    def keyrelease(self, event):
#        self.write(str(event.keysym))
#        print event.keysym
        self.norepeat = event.serial
        if event.keysym.count("Shift"):
            if self.mode.get() == 0:
                oldinst = self.hover.hinst
                if self.hinstch >= len(self.instlist):
                    self.hinstch = len(self.instlist)
                    com = cominstnew(self, self.hinstch)
                    if self.dispatcher.push(com):
                        self.dispatcher.do()
                if self.hinstch > 0:
                    self.hover.hinst = self.hinstch
                    self.tiedraw(oldinst, self.hover.hvoice)
                    self.tiedraw(self.hover.hinst, self.hover.hvoice)
                    self.statusinst.configure(text='Inst %d' % self.hover.hinst)
                    self.write(str(self.hover.hinst))
                    self.hover.colorupdate(self)
            elif self.mode.get() == 1:
                self.editinstassign(self.editinst)
                if self.editreference != None:
                    self.score.configure(cursor="sb_v_double_arrow")
                if self.dispatcher.comlist:
                    lastcom = self.dispatcher.comlist[-1]
                    if lastcom.__class__.__name__ == 'comeditdurarrows':
                        lastcom.finalized = True
            self.shiftkey = 0
        elif event.keysym.count(self.control):
            self.ctlkey = 0
            if self.quant == 0:
                self.quant = 1/self.xquantize
            self.xquantize = 1/self.quant
            self.xpxquantize = float(self.xquantize * self.xperquarter)
        elif event.keysym.count(self.alt):
            if self.hide:
                self.hideshow()
#            else:
#                self.showall()
            self.altkey = 0
        elif event.keysym == "r" or event.keysym == "R":
            self.regionchange()
            self.rkey = 0
            if self.mode.get() == 1:
                self.editregionassign(self.editregion)
        elif event.keysym == "v" or event.keysym == "V":
            if self.mode.get() == 0:
                #self.tiedraw(self.hover.hinst, self.hover.hvoice)
                self.score.itemconfigure(self.hover.hvoicedisp, text=str(self.hover.hvoice))
                self.voicechange()
                self.statusvoice.configure(text='Voice %d' % self.hover.hvoice)
            elif self.mode.get() == 1:
                self.editvoiceassign(self.editvoice)
            self.vkey = 0
        elif event.keysym == "b" or event.keysym == "B":
            if self.mode.get() == 0 or self.mode.get() == 1:
                if self.notebankactive >= len(self.notebanklist):
                    self.notebankactive = len(self.notebanklist) - 1
                self.statusbank.configure(text='Bank %d' % self.notebankactive)
            self.bkey = 0
        elif event.keysym in "1234567890":
            self.numkey = 0

    def hideshow(self):
#        print "hideshow"
        if self.hide >= len(self.instlist):
            return
#            self.hide = len(self.instlist) - 1
        inst = self.instlist[self.hide]
        if self.hide not in self.hidden:
            for nw in self.notewidgetlist:
                if nw.note.inst == self.hide:
                    nw.undraw()
            self.hidden.append(self.hide)
            self.hidden.sort()
            menutext = "Show"
        else:
            voicelist = []
            for nw in self.notewidgetlist:
                if nw.note.inst == self.hide:
                    nw.draw()
                    if nw.note.voice not in voicelist:
                        voicelist.append(nw.note.voice)
#            print "voicelist", voicelist
            for voice in voicelist:
                self.tiedraw(self.hide, voice)
            self.hidden.remove(self.hide)
#            inst.show = 1
            menutext = "Hide"
#        print "self.hidden", self.hidden
        text = ''
        for i in self.hidden:
            text += 'i%d  ' % i
        if not text: text = 'None '
        text += 'Hidden'
        self.statushidden.configure(text=text)
        ind = self.hide + 3
        self.menuview.entryconfigure(ind, label='%s i%d' % (menutext, self.hide), command=lambda arg1=self.hide: self.hidethis(arg1), accelerator='%s-%d' % (self.altacc, self.hide))
        self.hide = 0

    def hidethis(self, number):
        self.hide = number
        if self.hide in self.hidden:
            label = "Hide"
        else:
            label = "Show"
        self.hideshow()
        self.menuview.entryconfigure(number+3, label="%s %d" % (label, number))

    def showall(self):
#        print self.hidden
        for i in self.hidden:
#            print 'showall', i
            voicelist = []
            for nw in self.notewidgetlist:
                if nw.note.inst == i:
                    nw.draw()
                    if nw.note.voice not in voicelist:
                        voicelist.append(nw.note.voice)
            for voice in voicelist:
                self.tiedraw(i, voice)
            self.menuview.entryconfigure(i+3, label="Hide i%d" % i)
        self.hidden = []
#            inst.show = 1
        self.hide = 0
        text = 'None Hidden'
        self.statushidden.configure(text=text)

    def regionchange(self):
        if self.hover.hregion >= len(self.regionlist):
            self.hover.hregion = len(self.regionlist)
            num = self.regionlist[self.hover.oldhregion].num
            den = self.regionlist[self.hover.oldhregion].den
            color = self.regionlist[self.hover.oldhregion].color
            octave11 = self.regionlist[self.hover.oldhregion].octave11
            com = comregionnew(self, num, den, color, octave11)
            if self.dispatcher.push(com):
                self.dispatcher.do()
            self.score.itemconfigure(self.hover.hregiondisp, text='r'+str(self.hover.hregion))

        elif self.hover.hregion != self.hover.oldhregion:
            region = self.regionlist[self.hover.hregion]
            oldregion = self.regionlist[self.hover.oldhregion]
            hnum = self.hover.hnum * region.den * oldregion.num
            hden = self.hover.hden * region.num * oldregion.den
            hratio = self.ratioreduce(hnum, hden, self.primelimit)
            rcolor = region.color
            self.hover.hnum = hratio[0]
            self.hover.hden = hratio[1]
            self.statusrat.configure(text='Hover %3d:%d' % hratio)
            self.curnum = region.num
            self.curden = region.den
            self.score.itemconfigure(self.hover.hnumdisp, text=str(self.hover.hnum))
            self.score.itemconfigure(self.hover.hdendisp, text=str(self.hover.hden))
            self.score.itemconfigure(self.hover.hrnumdisp, text=str(region.num), fill=rcolor)
            self.score.itemconfigure(self.hover.hrdendisp, text=str(region.den), fill=rcolor)
            self.score.itemconfigure(self.hover.hregiondisp, text='r'+str(self.hover.hregion), fill=rcolor)
            self.drawoctaves(region.octave11)
            self.octave11 = region.octave11
            self.hover.log1 = math.log(float(self.hover.hnum)/float(self.hover.hden))
            self.hover.logged = self.hover.log1/self.log2
            self.yadj = self.octave11 - (self.hover.logged * self.octaveres)
        else:
            region = self.regionlist[self.hover.hregion]
        self.hover.oldhregion = self.hover.hregion
#        self.write('%s%d =' % ("Region: ",self.hregion))
#        self.write('%d/%d' % (self.regionlist[self.hregion][0],self.regionlist[self.hregion][1]))
        self.textsize = 24
        rtext = 'Region %d%s= %d/%d' % (self.hover.hregion, os.linesep, self.regionlist[self.hover.hregion].num, self.regionlist[self.hover.hregion].den)
        self.statusregion.configure(text='Region %d = %d:%d' % (self.hover.hregion, self.regionlist[self.hover.hregion].num, self.regionlist[self.hover.hregion].den))
        self.write(rtext)

    def voicechange(self):
        pass

    def modeannounce(self):
        mode = self.mode.get()
        # ADD
        if mode == 0:
            if [nw for nw in self.notewidgetlist if nw.note.sel]:
                self.editselectcancel()
            self.score.config(cursor="ur_angle")
#            self.score.unbind("<Motion>")
#            self.score.bind("<Motion>", self.hover.hovermotion)
#            self.score.itemconfigure("note", activewidth=0, activeoutline=None)
            self.statusmode.configure(text="ADD mode")
            if not self.statusrat.winfo_ismapped():
                self.statusinst.grid(row=0, column=2, sticky='w')
                self.statusvoice.grid(row=0, column=3, sticky='w')
                self.statusregion.grid(row=0, column=4, sticky='w')
                self.statusbank.grid(row=0, column=5, sticky='w')
                self.statusrat.grid(row=0, column=6, sticky='w', padx=5)
            if self.score.itemcget(self.hover.widget, 'state') != 'normal':
                self.score.itemconfigure(self.hover.widget, state='normal')
                self.score.itemconfigure(self.hover.hcross1, state='normal')
                self.score.itemconfigure(self.hover.hcross2, state='normal')
                self.score.itemconfigure(self.hover.hnumdisp, state='normal')
                self.score.itemconfigure(self.hover.hdendisp, state='normal')
                self.score.itemconfigure(self.hover.hrnumdisp, state='normal')
                self.score.itemconfigure(self.hover.hrdendisp, state='normal')
                self.score.itemconfigure(self.hover.hregiondisp, state='normal')
                self.score.itemconfigure(self.hover.hvoicedisp, state='normal')
            self.tiedraw(self.hover.hinst, self.hover.hvoice)
            try:
                self.cbscrubsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGE')
                ended = self.rauscrub.communicate()
                self.cbscrubsock.close()
            except: pass
            try:
                self.score.delete(self.scrubber.widget)
                del self.scrubber
                del self.scrubtimelist
            except: pass
            self.write("Now in ADD Mode")
        # EDIT
        elif mode == 1:
            self.statusmode.configure(text="EDIT mode")
            self.score.config(cursor="pencil")
            if self.statusrat.winfo_ismapped():
                self.statusinst.grid_remove()
                self.statusvoice.grid_remove()
                self.statusregion.grid_remove()
                self.statusbank.grid_remove()
                self.statusrat.grid_remove()
            if self.score.itemcget(self.hover.widget, 'state') != 'hidden':
                self.score.itemconfigure(self.hover.widget, state='hidden')
                self.score.itemconfigure(self.hover.hcross1, state='hidden')
                self.score.itemconfigure(self.hover.hcross2, state='hidden')
                self.score.itemconfigure(self.hover.hnumdisp, state='hidden')
                self.score.itemconfigure(self.hover.hdendisp, state='hidden')
                self.score.itemconfigure(self.hover.hrnumdisp, state='hidden')
                self.score.itemconfigure(self.hover.hrdendisp, state='hidden')
                self.score.itemconfigure(self.hover.hregiondisp, state='hidden')
                self.score.itemconfigure(self.hover.hvoicedisp, state='hidden')
            self.tiedraw(self.hover.hinst, self.hover.hvoice)
            try:
                self.cbscrubsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGE')
                ended = self.rauscrub.communicate()
                self.cbscrubsock.close()
            except: pass
            try:
                self.score.delete(self.scrubber.widget)
                del self.scrubber
                del self.scrubtimelist
            except: pass
            self.write("Now in EDIT Mode")
        # DELETE
        elif mode == 2:
            if [nw for nw in self.notewidgetlist if nw.note.sel]:
                self.editselectcancel()
            self.statusmode.configure(text="DELETE mode")
            self.score.config(cursor="X_cursor")
            if self.statusrat.winfo_ismapped():
                self.statusinst.grid_remove()
                self.statusvoice.grid_remove()
                self.statusregion.grid_remove()
                self.statusbank.grid_remove()
                self.statusrat.grid_remove()
#            self.score.unbind("<Motion>")
#            self.score.bind("<Motion>", self.deleteseek)
#            self.score.itemconfigure("note", activeoutline="#664444", activewidth=2)
            if self.score.itemcget(self.hover.widget, 'state') != 'hidden':
                self.score.itemconfigure(self.hover.widget, state='hidden')
                self.score.itemconfigure(self.hover.hcross1, state='hidden')
                self.score.itemconfigure(self.hover.hcross2, state='hidden')
                self.score.itemconfigure(self.hover.hnumdisp, state='hidden')
                self.score.itemconfigure(self.hover.hdendisp, state='hidden')
                self.score.itemconfigure(self.hover.hrnumdisp, state='hidden')
                self.score.itemconfigure(self.hover.hrdendisp, state='hidden')
                self.score.itemconfigure(self.hover.hregiondisp, state='hidden')
                self.score.itemconfigure(self.hover.hvoicedisp, state='hidden')
            self.tiedraw(self.hover.hinst, self.hover.hvoice)
            try:
                self.cbscrubsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGE')
                ended = self.rauscrub.communicate()
                self.cbscrubsock.close()
            except: pass
            try:
                self.score.delete(self.scrubber.widget)
                del self.scrubber
                del self.scrubtimelist
            except: pass
            self.write("Now in DELETE Mode")
        # SCRUB
        elif mode == 3:
            if [nw for nw in self.notewidgetlist if nw.note.sel]:
                self.editselectcancel()
            self.statusmode.configure(text="SCRUB mode")
            self.score.config(cursor="crosshair")
            if self.statusrat.winfo_ismapped():
                self.statusinst.grid_remove()
                self.statusvoice.grid_remove()
                self.statusregion.grid_remove()
                self.statusbank.grid_remove()
                self.statusrat.grid_remove()
            if self.score.itemcget(self.hover.widget, 'state') != 'hidden':
                self.score.itemconfigure(self.hover.widget, state='hidden')
                self.score.itemconfigure(self.hover.hcross1, state='hidden')
                self.score.itemconfigure(self.hover.hcross2, state='hidden')
                self.score.itemconfigure(self.hover.hnumdisp, state='hidden')
                self.score.itemconfigure(self.hover.hdendisp, state='hidden')
                self.score.itemconfigure(self.hover.hrnumdisp, state='hidden')
                self.score.itemconfigure(self.hover.hrdendisp, state='hidden')
                self.score.itemconfigure(self.hover.hregiondisp, state='hidden')
                self.score.itemconfigure(self.hover.hvoicedisp, state='hidden')
            self.tiedraw(self.hover.hinst, self.hover.hvoice)
#            self.preparescrub()
            try:
                self.cbscrubsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGE')
                ended = self.rauscrub.communicate()
                self.cbscrubsock.close()
            except: pass
            try:
                self.score.delete(self.scrubber.widget)
                del self.scrubber
                del self.scrubtimelist
            except: pass
            x = 0
            ind = 0
            self.scrubber = scrubcursor(self, x, ind)
            self.scrubplay()
            self.write("Now in SCRUB Mode")

    def popup(self,event):
        self.menupopupinst.delete(0, "end")
        for inst in range(1, len(self.instlist)):
            self.menupopupinst.add_command(label='%d' % inst, command=lambda arg1=inst: self.editinstassign(arg1))
        self.menupopupregion.delete(0, "end")
        for region in range(0, len(self.regionlist)):
            self.menupopupregion.add_command(label='%d' % region, command=lambda arg1=region: self.editregionassign(arg1))
        self.menupopup.post(event.x_root,event.y_root)
        self.poppedup = True

    def editregionassign(self, region):
        if region >= len(self.regionlist):
            self.poppedup = False
	    self.altkey = 0
            return
#            region = len(self.regionlist)-1
#        color = self.regionlist[region].color
        set = self.score.find_withtag("edit")
        if set and not "selected" in self.score.gettags(set):
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else:
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.note.sel]
        if toedit:
            com = comeditregion(self, toedit, region)
            if self.dispatcher.push(com):
                self.dispatcher.do()
        self.poppedup = False
	self.altkey = 0

    def editvoiceassign(self, voice):
        if voice == 0:
            self.editmodedisconnect()
        set = self.score.find_withtag("edit")
        if set and not "selected" in self.score.gettags(set):
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else:
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.note.sel]
        if toedit:
            com = comeditvoice(self, toedit, voice)
            if self.dispatcher.push(com):
                self.dispatcher.do()
        self.poppedup = False
	self.altkey = 0

    def editinstassign(self, inst):
        if inst < 1 or inst >= len(self.instlist):
            self.poppedup = False
	    self.altkey = 0
            self.editinst = 0
            self.ctlkey = 0
            return
#        elif inst >= len(self.instlist):
#            inst = len(self.instlist)-1
        set = self.score.find_withtag("edit")
        if set and not "selected" in self.score.gettags(set):
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else:
            toedit = [note.id for note in self.notelist if note.sel]
        if toedit:
            com = comeditinst(self, toedit, inst)
            if self.dispatcher.push(com):
                self.dispatcher.do()

        self.ctlkey = 0
        self.editinst = 0
	self.altkey = 0
        self.poppedup = False

    def editselect(self):
        self.write("Edit->Select")

    def editselectcancel(self, *args):
        '''a shameless workaround

        to record mode change selection cancel as a command'''
        selids = []
        deselids = [nw.note.id for nw in self.notewidgetlist if nw.note.sel]
        com = comselect(self, selids, deselids)
#        self.dispatcher.push(com)
        for notewidget in self.notewidgetlist:
            notewidget.note.sel = 0
            outline = self.score.itemcget(notewidget.notewidget, "fill")
            self.score.itemconfig(notewidget.notewidget, outline=outline, width=1)
            self.score.dtag("selected", notewidget.notewidget)

    def editcut(self, *args):
        self.write("Edit->Cut")

    def editcopy(self, *args):
        self.write("Edit->Copy")

    def editpaste(self, *args):
        self.write("Edit->Paste")

    def optionsaudio(self, *args):
        try:
            self.audiodialog.destroy()
            del self.audiodialog
        except:
            pass
        self.audiodialog = audiodialog(self)
        self.altkey = self.ctlkey = 0

    def removehidemenu(self):
        for ind, i in enumerate(self.instlist):
            if ind:
                self.menuview.delete(ind+3)

    def createhidemenu(self):
        for ind, inst in enumerate(self.instlist):
            if ind:
                if ind in self.hidden:
                    text='Show'
                else:
                    text='Hide'
                self.menuview.add_command(label='%s i%d' % (text, ind), command=lambda arg1=ind: self.hidethis(arg1), accelerator='%s-%d' % (self.altacc, ind))
                    

    def filenew(self, *args):
        if not self.allowed2play:
            return
        if self.unsaved:
#            print "UNSAVED"
            if self.filetosave:
                confirm = tkmb.askquestion("Save File?", message='Save %s?' % os.path.basename(self.filetosave), type=tkmb.YESNOCANCEL, icon=tkmb.QUESTION, default=tkmb.CANCEL)
            else:
                confirm = tkmb.askquestion("Save File?", message="Save Current File?", type=tkmb.YESNOCANCEL, icon=tkmb.QUESTION, default=tkmb.CANCEL)
            if confirm == 'yes':
                saved = self.filesaveas()
                if not saved:
                    self.ctlkey = 0
                    return
            elif confirm.__class__.__name__ != 'str' or confirm == 'cancel':
                self.ctlkey = 0
                return

        for i in range(len(self.notewidgetlist)):
            self.notewidgetlist[0].undraw()
            del self.notewidgetlist[0]
        for i in range(len(self.notelist)):
            del self.notelist[0]
        self.notelist = []
        self.notewidgetlist = []
        self.noteid = 0
        initregion = rdialog.region(self, 1, 1, '#999999', 240)
        for i in range(len(self.regionlist)):
            del self.regionlist[0]
        self.regionlist = [initregion]
        self.removehidemenu()
        for i in range(len(self.instlist)):
            del self.instlist[0]
        self.instlist = [0]
        self.instlist.append(odialog.instrument(self, 1, '#999999'))
        self.createhidemenu()
        for i in range(len(self.tempolist)):
            del self.tempolist[0]
        self.tempolist = []
        self.tempos.delete("bpm")
        self.tempos.delete("unit")
        for i in range(len(self.meterlist)):
            del self.meterlist[0]
        self.meterlist = []
        self.meters.delete("all")
        self.redrawlines()
        self.filetosave = None
        self.csdimport = None
        self.csdimported = ''
        self.outautoload = False
        if self.mode.get() == 3:
            try:
                self.cbscrubsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGE')
                ended = self.rauscrub.communicate()
                self.cbscrubsock.close()
                self.scrubtimelist = []
            except:
                print "Problems closing SCRUB engine..."
        self.ctlkey = 0
        ####
        self.hover.oldhregion = self.hover.hregion = 0
        self.regionchange()
        self.hover.hinst = 1
        self.hover.colorupdate(self)
        self.hover.hvoice = 0
        self.score.itemconfigure(self.hover.hvoicedisp, text=str(self.hover.hvoice))
        region = self.regionlist[0]
        rcolor = region.color

        self.curnum = region.num
        self.curden = region.den
        self.score.itemconfigure(self.hover.hrnumdisp, text=str(region.num), fill=rcolor)
        self.score.itemconfigure(self.hover.hrdendisp, text=str(region.den), fill=rcolor)
        self.score.itemconfigure(self.hover.hregiondisp, text='r'+str(self.hover.hregion), fill=rcolor)
        self.drawoctaves(region.octave11)
        self.octave11 = region.octave11
        self.hover.log1 = math.log(float(self.hover.hnum)/float(self.hover.hden))
        self.hover.logged = self.hover.log1/self.log2
        self.yadj = self.octave11 - (self.hover.logged * self.octaveres)
        self.cursor.home()
        ####
        self.myparent.title('Rationale %s: New Score' % vs)
        self.unsaved = 0
        del self.dispatcher
        self.dispatcher = dispatcher(self)
        self.titleset()
        self.write("File->New")

    def fileopen(self, *args):
        if not self.allowed2play:
            return
        if self.unsaved:
#            print "UNSAVED"
            
            if self.filetosave:
                confirm = tkmb.askquestion("Save File?", message='Save %s?' % os.path.basename(self.filetosave), type=tkmb.YESNOCANCEL, icon=tkmb.QUESTION, default=tkmb.CANCEL)
            else:
                confirm = tkmb.askquestion("Save File?", message="Save Current File?", type=tkmb.YESNOCANCEL, icon=tkmb.QUESTION, default=tkmb.CANCEL)
            if confirm == 'yes':
                saved = self.filesaveas()
                if not saved:
                    self.ctlkey = 0
                    return
#                self.filesaveas()
            elif confirm.__class__.__name__ != 'str' or confirm == 'cancel':
                self.ctlkey = 0
                return

        file = tkfd.askopenfilename(title="Open", filetypes=[('Rationale %s' % self.version, ".rat"), ("All", "*")])
        if file:
            self.fileopenwork(file)
#        else:
        self.ctlkey = 0
#        self.unsaved = False

    def fileopenwork(self, file):
#        self.unsaved = 0
#        self.titleset()
        self.filenew()
        self.filetosave = file
        self.myparent.title('Rationale %s: %s' % (vs, os.path.basename(file)))
        self.write('File->Open: %s' % str(file))
        input = open(file, 'rb')
        regionlistin = pickle.load(input)
        instlistin = pickle.load(input)
        notelistin = pickle.load(input)
        meterlistin = pickle.load(input)
        tempolistin = pickle.load(input)
        self.csdimport = pickle.load(input)
        if self.csdimport:
            self.write('Loaded Csound File: %s' % str(self.csdimport))
        self.csdimported = pickle.load(input)
        self.outautoload = pickle.load(input)
        self.sf2list = pickle.load(input)
        for scoreitem in self.score.find_all():
            tags = self.score.gettags(scoreitem)
            if "octaveline" not in tags and "perm11" not in tags and "timecursor" not in tags and "hover" not in tags and "scrubcursor" not in tags:
                self.score.delete(scoreitem)
#        self.drawoctaves(self.octave11)
        self.regionlist = []
        self.notelist = []
        self.meterlist = []
        self.tempolist = []
#            for region in regionlistin:
#                newregion = rdialog.region(self, region[0], region[1], region[2], region[3])
#                self.regionlist.append(newregion)
        self.regionlist = regionlistin
#            for reg in self.regionlist:
#                reg.color = '#' + str(reg.color)
        self.removehidemenu()
        self.instlist = instlistin
        self.createhidemenu()
#        self.yadj = 240
#        self.tonchange(self.curden, self.curnum, self.yadj)
#        self.yadj = self.regionlist[self.hover.hregion].octave11
#        self.tonchange(self.regionlist[self.hover.hregion].num, self.regionlist[self.hover.hregion].den, self.regionlist[self.hover.hregion].octave11)
        self.regionchange()
        self.hover.colorupdate(self)
        region = self.regionlist[0]
        rcolor = region.color
        self.curnum = region.num
        self.curden = region.den
        self.score.itemconfigure(self.hover.hrnumdisp, text=str(region.num), fill=rcolor)
        self.score.itemconfigure(self.hover.hrdendisp, text=str(region.den), fill=rcolor)
        self.score.itemconfigure(self.hover.hregiondisp, text='r'+str(self.hover.hregion), fill=rcolor)
        self.drawoctaves(region.octave11)
        self.octave11 = region.octave11
        self.hover.log1 = math.log(float(self.hover.hnum)/float(self.hover.hden))
        self.hover.logged = self.hover.log1/self.log2
        self.yadj = self.octave11 - (self.hover.logged * self.octaveres)

        for test in notelistin:
            if len(test) == 9:
                id = self.noteid
                self.noteid += 1
                inst = test[0]
                voice = test[1]
                time = test[2]
                dur = test[3]
                db = test[4]
                num = test[5]
                den = test[6]
                region = test[7]
                sel = test[8]
            elif len(test) == 10:
                id = test[0]
                if self.noteid <= id:
                    self.noteid = id + 1
                inst = test[1]
                voice =test[2] 
                time =test[3] 
                dur =test[4] 
                db = test[5]
                num = test[6]
                den = test[7]
                region = test[8]
                sel = test[9]
                
            entrycolor = '#888888'
            if inst < len(self.instlist):
                entrycolor = str(self.instlist[inst].color)
            rnum = self.regionlist[region].num
            rden = self.regionlist[region].den
            rcolor = str(self.regionlist[region].color)
            posx = time * self.xperquarter
            yadj = self.regionlist[region].octave11 - ((math.log((float(num)/float(den))*(float(rnum)/rden))/self.log2) * self.octaveres)
            x2 = posx + db/12
            y2 = yadj
            x0 = posx
            y0 = yadj - db/6
            x1 = posx
            y1 = yadj + db/6
            crossx3 = posx + dur * self.xperquarter
            ry0 = yadj - 15
            ry1 = yadj + 15

            noteinstance = note(self, id, inst, voice, time, dur, db, num, den, region, sel)
            self.notelist.append(noteinstance)
            notewidgetinstance = notewidgetclass(self, noteinstance)
            self.notewidgetlist.append(notewidgetinstance)
            try:
                self.tiedraw(inst, voice)
            except:
                print "Unable to draw ties!"
        for i in meterlistin:
            test = mdialog.meter(self, i[0], i[1], i[2])
            self.meterlist.append(test)
        self.redrawlines()
        for i in tempolistin:
            test = tdialog.tempo(self, i[0], i[1], i[2], i[3])
            self.tempolist.append(test)
            test.makewidget(self)
#            tdialog.tempowidgetclass(self, test)
        if self.mode.get() == 3:
            self.scrubtimelist = []
            self.scrubplay()


    def filesave(self, *args):
        if not self.filetosave or self.filetosave == None:
            self.filetosave = tkfd.asksaveasfilename(master=self.myparent, title="Save As", defaultextension=".rat")
        if self.filetosave:
            self.ctlkey = 0
            self.myparent.title('Rationale %s: %s' % (vs, os.path.basename(self.filetosave)))
            output = open(self.filetosave, 'wb')
            regionlist = self.regionlist
            instlist = self.instlist
            notelist = [(note.id, note.inst, note.voice, note.time, note.dur, note.db, note.num, note.den, note.region, note.sel) for note in self.notelist]
            meterlist = [(meter.bar, meter.top, meter.bottom) for meter in self.meterlist]
            tempolist = [(tempo.bar, tempo.beat, tempo.bpm, tempo.unit) for tempo in self.tempolist]
            pickle.dump(regionlist, output)
            pickle.dump(instlist, output)
            pickle.dump(notelist, output)
            pickle.dump(meterlist, output)
            pickle.dump(tempolist, output)
            pickle.dump(self.csdimport, output)
            pickle.dump(self.csdimported, output)
            pickle.dump(self.outautoload, output)
            pickle.dump(self.sf2list, output)
#            if self.unsaved:
            self.unsaved = 0
#            print "filesave:", self.unsaved
            file = os.path.basename(self.filetosave)
            self.myparent.title('Rationale %s: %s' % (vs, file))
            self.write('File->Save: %s' % self.filetosave)
            output.close()

    def filesaveas(self, *args):
        filetosave = tkfd.asksaveasfilename(master=self.myparent, title="Save As", filetypes=[('Rationale %s: New Score' % self.version, ".rat")])
        if filetosave:
            output = open(filetosave, 'wb')
            self.myparent.title('Rationale %s: %s' % (vs, os.path.basename(self.filetosave)))
            regionlist = self.regionlist
            instlist = self.instlist
            notelist = [(note.id, note.inst, note.voice, note.time, note.dur, note.db, note.num, note.den, note.region, note.sel) for note in self.notelist]
            meterlist = [(meter.bar, meter.top, meter.bottom) for meter in self.meterlist]
            tempolist = [(tempo.bar, tempo.beat, tempo.bpm, tempo.unit) for tempo in self.tempolist]
            pickle.dump(regionlist, output)
            pickle.dump(instlist, output)
            pickle.dump(notelist, output)
            pickle.dump(meterlist, output)
            pickle.dump(tempolist, output)
            pickle.dump(self.csdimport, output)
            pickle.dump(self.csdimported, output)
            pickle.dump(self.outautoload, output)
            pickle.dump(self.sf2list, output)
#            if self.unsaved:
            self.unsaved = 0
            file = os.path.basename(self.filetosave)
            self.myparent.title('*Rationale %s: %s' % (vs, file))
            self.write('File->Save As: %s' % filetosave)
            self.filetosave = filetosave
            self.myparent.title('Rationale %s: %s' % (vs, os.path.basename(self.filetosave)))
            output.close()
            self.ctlkey = 0
            return True
        else:
            self.ctlkey = 0
            return False
        self.ctlkey = 0

    def filereload(self, *args):
        if not self.allowed2play:
            return
        if self.filetosave:
            if tkmb.askokcancel("Reload", "Reload File?"):
                self.unsaved = 0
                del self.dispatcher
                self.dispatcher = dispatcher(self)
                self.fileopenwork(self.filetosave)
#                if self.unsaved:
#                    self.unsaved = 0
#                    self.myparent.title('Rationale %s: %s' % (vs, os.path.basename(self.filetosave)))

    def fileimport(self, *args):
        if not self.allowed2play:
            return
        self.write("File->Import .ji")
        file = tkfd.askopenfilename(title="Import .ji", filetypes=[("JIsequencer", ".ji")])
        if file:
            input = open(file, 'rb')
            notelistin = []
            flag1 = 0
            for line in input:
                if flag1 == 1:
                    split = line.split()
                    if split[-1][-1] == ';':
                        split[-1] = split[-1][:-1]
                    bothlines = fstline + split
                    notelistin.append(bothlines)
                    flag1 = 0
                if line.split()[0] == "notes":
                    split = line.split()
                    if split[-1][-1] == ';':
                        split[-1] = split[-1][:-1]
                    fstline = split
                    flag1 = 1
#            meterlistin = pickle.load(input)
#            tempolistin = pickle.load(input)
            self.filenew()
#            for scoreitem in self.score.find_all():
#                tags = self.score.gettags(scoreitem)
#                if "octaveline" not in tags and "perm11" not in tags and "timecursor" not in tags and "hover" not in tags:
#                    self.score.delete(scoreitem)
#            initregion = rdialog.region(self, 1, 1, '#999999', 240)
#            for i in range(len(self.regionlist)):
#                del self.regionlist[i]
#            self.regionlist = [initregion]
##            self.regionlist = [[1,1,999999,240]]
#            self.notelist = []
#            self.meterlist = []
#            self.tempolist = []
            instset = [0]
            for test in notelistin:
                id = self.noteid
                self.noteid += 1
                jiinst = test[8]
                if jiinst in instset:
                    inst = instset.index(jiinst)
                else:
                    instset.append(jiinst)
                    inst = instset.index(jiinst)
                voice = 0
                time = (float(test[1]) - 30)/30
                dur = float(test[5])/30
                widgetdur = dur * self.xperquarter
                db = int(test[-2]) * 6
                num = int(test[3])
                den = int(test[4])
                region = 0
                sel = 0
                entrycolor = '#888888'
                if inst < len(self.instlist):
                    entrycolor = str(self.instlist[inst].color)
                rnum = self.regionlist[region].num
                rden = self.regionlist[region].den
                rcolor = str(self.regionlist[region].color)
                posx = time * self.xperquarter
                yadj = self.octave11 - ((math.log(float(num)/float(den))/self.log2) * self.octaveres)
                x2 = posx + db/12
                y2 = yadj
                x0 = posx
                y0 = yadj - db/6
                x1 = posx
                y1 = yadj + db/6
                crossx3 = posx + widgetdur
                ry0 = yadj - 15
                ry1 = yadj + 15

                noteinstance = note(self, id, inst, voice, time, dur, db, num, den, region, sel)
                self.notelist.append(noteinstance)
                notewidgetinstance = notewidgetclass(self, noteinstance)
                self.notewidgetlist.append(notewidgetinstance)

                self.tiedraw(inst, voice)
#            for i in meterlistin:
#                test = meter(self, i[0], i[1], i[2])
#                self.meterlist.append(test)
            self.redrawlines()
#            for i in tempolistin:
#                test = tempo(self, i[0], i[1], i[2], i[3])
#                self.tempolist.append(test)

    def fileexport(self, *args):
        filetoexport = tkfd.asksaveasfilename(master=self.myparent, title="Export Csound", filetypes=[("Csound Unified Format", ".csd")])
        if filetoexport:
            self.preparecsd(self.instlist, self.sf2list, self.outputmethod, self.sr, self.ksmps, self.nchnls, self.audiomodule, self.dac, self.b, self.B, self.aifffile, self.wavfile, self.csdcommandline, self.csdcommandlineuse)
            csdcsd = '<CsoundSynthesizer>%s<CsOptions>%s%s%s</CsOptions>%s<CsInstruments>%s%s%s</CsInstruments>%s<CsScore>%s%s%s</CsScore>%s</CsoundSynthesizer>' % (os.linesep, os.linesep, self.csdopt, os.linesep, os.linesep, os.linesep, self.csdinst, os.linesep, os.linesep, os.linesep, self.csdsco, os.linesep, os.linesep)
            csdexport = open(filetoexport, 'w')
            csdexport.write(csdcsd)
            csdexport.close()
            self.write('File->Export: %s' % filetoexport)

    def fileexit(self, *args):
        if not self.allowed2play:
            return
        # to confirm save before exiting
        if self.unsaved:
#            print "UNSAVED"
            
            if self.filetosave:
                confirm = tkmb.askquestion("Save File?", message='Save %s?' % os.path.basename(self.filetosave), type=tkmb.YESNOCANCEL, icon=tkmb.QUESTION, default=tkmb.CANCEL)
            else:
                confirm = tkmb.askquestion("Save File?", message="Save Current File?", type=tkmb.YESNOCANCEL, icon=tkmb.QUESTION, default=tkmb.CANCEL)
            if confirm == 'yes':
                saved = self.filesaveas()
                if not saved:
                    self.ctlkey = 0
                    return
            elif confirm.__class__.__name__ != 'str' or confirm == 'cancel':
                self.ctlkey = 0
                return
        self.exit(self, *args)

    def exit(self, *args):
        #exit without confirmation
        if self.mode.get() == 3:
            try:
                self.cbscrubsock.sendall('RATENDMESSAGEcsdstpRATENDMESSAGE')
                ended = self.rauscrub.communicate()
                self.cbscrubsock.close()
            except:
                print "Problems with SCRUB..."
        self.write("File->Exit")
        self.myparent.destroy()

    def durupdate(self,dur):
        if self.mode.get() == 0:
            self.hover.entrydur = dur
            self.hover.hdur = self.xperquarter * self.hover.entrydur
            self.hover.hcrossx3 = self.hover.posx + self.hover.hdur
            self.score.coords(self.hover.hcross2,self.hover.hovx0,self.hover.hcrossy2,self.hover.hcrossx3,self.hover.hcrossy3)
        elif self.mode.get() == 1:
            self.selectdur = dur * self.xperquarter

    def durmod8up(self, event):
        if self.mode.get() == 0:
            tempdur = (int(self.hover.entrydur * 8) + 1)/8.0
            self.durupdate(tempdur)
        elif self.mode.get() == 1:
            if self.dispatcher.comlist and self.dispatcher.comlist[-1].__class__.__name__ == 'comeditdurarrows' and not self.dispatcher.comlist[-1].finalized:
                self.dispatcher.increment('comeditdurarrows', 8.0)
            else:
                com = comeditdurarrows(self, [note.id for note in self.notelist if note.sel], 8.0)
                if self.dispatcher.push(com):
                    self.dispatcher.do()
                
    def durmod8down(self, event):
        if self.mode.get() == 0 and self.hover.entrydur > 1/8.0:
            tempdur = (int(self.hover.entrydur * 8) - 1)/8.0
            self.durupdate(tempdur)
        elif self.mode.get() == 1:
            if self.dispatcher.comlist and self.dispatcher.comlist[-1].__class__.__name__ == 'comeditdurarrows' and not self.dispatcher.comlist[-1].finalized:
                self.dispatcher.increment('comeditdurarrows', -8.0)
            else:
                com = comeditdurarrows(self, [note.id for note in self.notelist if note.sel], -8.0)
                if self.dispatcher.push(com):
                    self.dispatcher.do()
        
    def durmod6up(self, event):
        if self.mode.get() == 0:
#            tempdur = (int(self.hover.entrydur * 6) + 1)/6.0
            tempdur = (int(self.hover.entrydur * self.quant) + 1)/self.quant
            self.durupdate(tempdur)
        elif self.mode.get() == 1:
            if self.dispatcher.comlist and self.dispatcher.comlist[-1].__class__.__name__ == 'comeditdurarrows' and not self.dispatcher.comlist[-1].finalized:
                self.dispatcher.increment('comeditdurarrows', self.quant)
            else:
                com = comeditdurarrows(self, [note.id for note in self.notelist if note.sel], self.quant)
                if self.dispatcher.push(com):
                    self.dispatcher.do()
                
    def durmod6down(self, event):
        if self.mode.get() == 0 and self.hover.entrydur > 1/self.quant:
#            tempdur = (int(self.hover.entrydur * 6) - 1)/6.0
            tempdur = (int(self.hover.entrydur * self.quant) - 1)/self.quant
            self.durupdate(tempdur)
        elif self.mode.get() == 1:
            if self.dispatcher.comlist and self.dispatcher.comlist[-1].__class__.__name__ == 'comeditdurarrows' and not self.dispatcher.comlist[-1].finalized:
                self.dispatcher.increment('comeditdurarrows', -self.quant)
            else:
                com = comeditdurarrows(self, [note.id for note in self.notelist if note.sel], -self.quant)
                if self.dispatcher.push(com):
                    self.dispatcher.do()

    def setconnect(self, *args):
        if self.mode.get() == 0:
            self.hover.entrydur = -abs(self.hover.entrydur)
        elif self.mode.get() == 1:
            self.editmodeconnect()

    def disconnect(self, *args):
        if self.mode.get() == 0:
            self.hover.entrydur = abs(self.hover.entrydur)
        elif self.mode.get() == 1:
            self.editmodedisconnect()

    def tiedraw(self, inst, voice):
        if voice != 0:
            self.scsort()
            for nw in self.notewidgetlist:
                if nw.note.inst == inst and nw.note.voice == voice:
                    nw.updateconnect()

    def hupdate(self):
        pass

    def scorexscroll(self, *args):
#        print args
        self.score.xview(*args)
        self.meters.xview(*args)
        self.tempos.xview(*args)
        self.bars.xview(*args)

    def scoreyscroll(self, *args):
#        print args
        self.score.yview(*args)
        self.octaves.yview(*args)

    def scoreyscrollwheel(self, arg1, event, arg3):
#        print args
	if event.delta > 0:
            self.score.yview(arg1, -1, arg3)
            self.octaves.yview(arg1, -1, arg3)
	else:
            self.score.yview(arg1, 1, arg3)
            self.octaves.yview(arg1, 1, arg3)



    def inserttempo(self, event):
        pass

    def grab(self, event):
        self.xdrag = event.x
        self.ydrag = event.y
        xscroll = self.xscroll.get()
        yscroll = self.yscroll.get()
        self.xscrwas = xscroll[0]
        self.yscrwas = yscroll[0]
        self.xrange = self.maxx - self.minx
        self.yrange = self.maxy - self.miny

    def zoom(self, which, vert=False):
        if vert:
            if which == "in":
                self.octaveres += 20
                resdelta = 20
            elif which == "out":
                if self.octaveres <= 70:
                    return
                self.octaveres -= 20
                resdelta = -20
            elif which == "reset":
                resdelta = 240 - self.octaveres
                self.octaveres = 240
            self.drawoctaves(self.octave11, resdelta)
#                    self.score.move("octaveline", 0, yincr)
#                    self.octaves.move("octavetext", 0, yincr)
#                    self.scorewin.update_idletasks()
            for nw in self.notewidgetlist:
                nw.updatedb()
                nw.updateheight()
        else:
            if which == "in":
                self.xperquarter = self.xperquarter + 5
            elif which == "out":
                if self.xperquarter <= 5:
                    return
                self.xperquarter = self.xperquarter - 5
            elif which == "reset":
                self.xperquarter = 30
            self.xpxquantize = float(self.xquantize * self.xperquarter)
            self.tempos.delete("bpm")
            self.tempos.delete("unit")
            for t in self.tempolist:
                t.makewidget(self)
            for nw in self.notewidgetlist:
                nw.updatetime()
            self.durupdate(self.hover.entrydur)

        self.drawoctaves(self.octave11)
        self.redrawlines()
#        for item in self.score.find_withtag("all"):
#            coords = list(self.score.coords(item))
#            for xcoord in range(len(coords)/2):
#                coords[xcoord*2] = int(coords[xcoord*2] * (float(newxperquarter)/self.xperquarter))
#            newcoords = '%d' % coords[0]
#            for i in range(1, len(coords)):
#                newcoords = '%s %d' % (newcoords, coords[i])
#            self.score.coords(item, newcoords)
#        self.xperquarter = newxperquarter

    def deleteseek(self, event):
        self.score.itemconfig("note", stipple="", activefill='', activeoutline='', activewidth=1)
        self.score.dtag("note", "delete")
        self.score.dtag("note", "edit")
        widget = event.widget
        realx = widget.canvasx(event.x)
        realy = widget.canvasy(event.y)
        notes = self.score.find_overlapping(realx-21, realy-21, realx+21, realy+21)
        note = 0
        absall = 20
        for match in notes:
            if "note" in self.score.gettags(match):
                coords = self.score.coords(match)
                xy = (coords[2], coords[1])
                abs = math.sqrt((xy[0]-realx)**2 + (xy[1]-realy)**2)
                if abs < absall:
                    absall = abs
                    note = match
        if note != 0:
	    if sys.platform.count("darwin"):
		self.score.itemconfig(note, activefill="#888888", activeoutline="#552222", activewidth=3)
	    else:
	    	self.score.itemconfig(note, stipple="gray50")
#            self.score.itemconfig(note, stipple="gray50")
            self.score.addtag_withtag("delete", note)
            self.score.addtag_withtag("edit", note)

    def meteradd(self, event):
        self.meteraddwindow = tk.Toplevel(self.myparent)
        self.meteraddwindow.title("Add Meter Change")
        self.meteraddwindow.rowconfigure(0, weight=0)
        self.meteraddwindow.rowconfigure(1, weight=0)
        self.meteraddwindow.rowconfigure(2, weight=0)
        self.meteraddwindow.rowconfigure(3, weight=1)
        self.meteraddwindow.columnconfigure(1, weight=0)
        self.meteraddwindow.columnconfigure(2, weight=0)
        self.meteraddwindow.columnconfigure(3, weight=0)
        self.meteraddwindow.columnconfigure(4, weight=1)
        self.meteraddbar = tk.IntVar()
        self.meteraddtop = tk.IntVar()
        self.meteraddbottom = tk.IntVar()
        barwidget = tk.Entry(self.meteraddwindow, textvariable=self.meteraddbar, width=4)
        barwidget.grid(row=0, column=0)
        topwidget = tk.Entry(self.meteraddwindow, textvariable=self.meteraddtop, width=4)
        topwidget.grid(row=0, column=1)
        bottomwidget = tk.Entry(self.meteraddwindow, textvariable=self.meteraddbottom, width=4)
        bottomwidget.grid(row=1, column=1)
        ok = tk.Button(self.meteraddwindow, text="OK")
        ok.grid(row=2, column=0)
        cancel = tk.Button(self.meteraddwindow, text="Cancel", command=self.cancel)
        cancel.grid(row=2, column=1)

    def meteredit(self, event):
        tempwindow = tk.Toplevel(self.myparent)
        tempwindow.title("Edit Meter Changes")
        rowcount = 0
        for meter in self.meterlist:
            tempwindow.rowconfigure(rowcount, weight=0)
            tk.Entry(tempwindow, text=str(meter.bar)).grid(row=rowcount, column=0)            

    def tempoinit(self, event):
        print 'tempo init: %d %d' % (event.x, event.y)

    def tempoadjust(self, event):
        print 'tempo adjust'

    def tempoadd(self, event):
        print 'tempo add: %d %d' % (event.x, event.y)

    def editmodearb(self, *args):
        for nw in self.notewidgetlist:
            if "edit" in self.score.gettags(nw.notewidget):
                arbdialog(self, nw.note)

    def editmodeselectall(self, *args):
        self.mode.set(1)
        self.modeannounce()
        selids = [nw.note.id for nw in self.notewidgetlist if not nw.note.sel]
        deselids = []
        com = comselect(self, selids, deselids)
        com.do()
#        if self.dispatcher.push(com):
#            self.dispatcher.do()

    def editmodeselectnone(self, *args):
        self.mode.set(1)
        self.modeannounce()
        selids = []
        deselids = [nw.note.id for nw in self.notewidgetlist if nw.note.sel]
        com = comselect(self, selids, deselids)
        com.do()
#        if self.dispatcher.push(com):
#            self.dispatcher.do()

    def editmodeselecttocursor(self, *args):
        self.mode.set(1)
        self.modeannounce()
        selids = [nw.note.id for nw in self.notewidgetlist if nw.note.time < float(self.cursor.center)/self.xperquarter and not nw.note.sel]
        deselids = [nw.note.id for nw in self.notewidgetlist if nw.note.time >= float(self.cursor.center)/self.xperquarter and nw.note.sel]
        com = comselect(self, selids, deselids)
        com.do()
#        if self.dispatcher.push(com):
#            self.dispatcher.do()

    def editmodeselectfromcursor(self, *args):
        self.mode.set(1)
        self.modeannounce()
        selids = [nw.note.id for nw in self.notewidgetlist if nw.note.time >= float(self.cursor.center)/self.xperquarter and not nw.note.sel]
        deselids = [nw.note.id for nw in self.notewidgetlist if nw.note.time < float(self.cursor.center)/self.xperquarter and nw.note.sel]
        com = comselect(self, selids, deselids)
        com.do()
#        if self.dispatcher.push(com):
#            self.dispatcher.do()

    def editmodecopy(self, *args):
#        self.clipboard = []
        set = self.score.find_withtag("edit")
        if set and "selected" not in self.score.gettags(set):
            noteids = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else:
            noteids = [nw.note.id for nw in self.notewidgetlist if nw.note.sel]

        if noteids:
            com = comcopy(self, noteids)
            com.do()
#            if self.dispatcher.push(com):
#                self.dispatcher.do()
##      BROKEN
#        flag = 0
#        for nw in self.notewidgetlist:
#            if nw.notewidget in toedit:
#                if flag == 0:
#                    self.clipboard = []
#                self.clipboard.append(copy.copy(nw.note))
#                flag = 1
#        self.clipboard.sort(key=lambda n: n.time)
#        if len(self.clipboard):
#            basetime = self.clipboard[0].time
#        for note in self.clipboard:
#            note.time -= basetime
        self.poppedup = False
	self.altkey = 0
#        print 'copy'

    def editmodecut(self, *args):
        set = self.score.find_withtag("edit")
        if set and "selected" not in self.score.gettags(set):
            noteids = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else:
            noteids = [nw.note.id for nw in self.notewidgetlist if nw.note.sel]

        if noteids:
            com = comcopy(self, noteids)
            com.do()
            com = comdeletenotes(self, noteids)
            if self.dispatcher.push(com):
                self.dispatcher.do()


#        self.editmodecopy(*args)
#        self.editmodedelete(*args)
#        print 'cut'

    def editmodepaste(self, *args):
#        print self.clipboard
        self.pastedialog = pastedialog(self)
#        print 'paste'

    def editmodedelete(self, *args):
        set = self.score.find_withtag("edit")
        if set and not "selected" in self.score.gettags(set):
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else:
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.note.sel == 1]
        if toedit:
            com = comdeletenotes(self, toedit)
            if self.dispatcher.push(com):
                self.dispatcher.do()
        self.poppedup = False
	self.altkey = 0

    def editmodedur(self, dur):
        noteids = [note.id for note in self.notelist if note.sel]
        com = comeditdurset(self, noteids, dur)
        if self.dispatcher.push(com):
            self.dispatcher.do()

    def editmodetranspose(self, num, den):
        print 'notes transposed'

    def editmoderegion(self, region):
        print 'notes assigned to region %d' % region

    def editmodeinst(self, inst):
        print 'assigned to inst %d' % inst

    def editmodevoice(self, voice):
        for nw in self.notewidgetlist:
            if nw.note.sel == 1:
                nw.note.updatevoice(voice)
                nw.updatevoice()
        print 'assigned to voice %d' % voice

    def editmodeslide(self, bars, beats, ticks):
        print 'slid'

    def editmodedbup(self):
        noteids = []
        for nw in self.notewidgetlist:
            if nw.note.sel == 1:
                if nw.note.db <= 84:
                    noteids.append(nw.note.id)
        if noteids:
            com = comeditdb(self, noteids, 6)
            if self.dispatcher.push(com):
                self.dispatcher.do()

    def editmodedbdown(self):
        noteids = []
        for nw in self.notewidgetlist:
            if nw.note.sel == 1:
                if nw.note.db >= 6:
                    noteids.append(nw.note.id)
        if noteids:
            com = comeditdb(self, noteids, -6)
            if self.dispatcher.push(com):
                self.dispatcher.do()

    def editmodedbset(self, db):
        for nw in self.notewidgetlist:
            if nw.note.sel == 1:
                nw.note.updatedb(db)
                nw.updatedb()

    def editmodeconnect(self):
        set = self.score.find_withtag("edit")
        if set and not "selected" in self.score.gettags(set):
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else: toedit = [note.id for note in self.notelist if note.sel == 1]
        if not toedit: return

        com = comeditconnect(self, toedit, -1)
        if self.dispatcher.push(com):
            self.dispatcher.do()
#        if not self.unsaved: self.unsaved = True
        self.poppedup = False
	self.altkey = 0

    def editmodedisconnect(self):
        set = self.score.find_withtag("edit")
        if set and not "selected" in self.score.gettags(set):
            toedit = [nw.note.id for nw in self.notewidgetlist if nw.notewidget in set]
        else: toedit = [note.id for note in self.notelist if note.sel == 1]
        if not toedit: return

        com = comeditconnect(self, toedit, 1)
        if self.dispatcher.push(com):
            self.dispatcher.do()
#        if not self.unsaved: self.unsaved = True
        self.poppedup = False
	self.altkey = 0

    def noteeditlistnew(self, *args):
        self.noteeditlist = noteeditlist(self)

    def scoredrag(self, event):
        winfocus = (str(self.scorewin.focus_get()))
        if winfocus != None:
            xdrag = self.xdrag - event.x
            ydrag = self.ydrag - event.y
            xfrac = float(xdrag) / self.xrange + self.xscrwas
            yfrac = float(ydrag) / self.yrange + self.yscrwas
            self.scorexscroll('moveto', xfrac)
            self.scoreyscroll('moveto', yfrac)

    def getaudiodevices(self, module):
        rau = subprocess.Popen((sys.executable, 'rataudiotester.py', module), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = rau.communicate()
#	print 'res0:', res[0], os.linesep, os.linesep
#	print 'res1:', res[1], os.linesep, os.linesep
        if sys.platform.count('win32'):
            lines = res[0].split(os.linesep)[:-1]
        else:
            lines = res[1].split(os.linesep)[:-1]

#        print [fstr for fstr in os.listdir(os.getcwd()) if fstr.count('rataudiotester')]
#        rau = subprocess.Popen((os.path.join(os.getcwd(), 'rataudiotester'), module), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#        err = rau.communicate()[1]
#        lines = err.split(os.linesep)
#        print "lines:", lines
        startflag = '#&*@$!'
        endflag = 'WHAT ME WORRY?'

        if module == 'portaudio':
            startflag = 'PortAudio: available'
            endflag = 'error'
        if module == 'alsa':
            startflag = '*** ALSA:'
            endflag = 'Failed to initialise'
        if module == 'jack':
            startflag = 'available JACK'
            endflag = '*** rtjack:'
        if module == 'mme':
            return module + os.linesep
        if module == 'coreaudio':
            return module + os.linesep

#        csdout.seek(0)
        flag = 0
        result = []
        for line in lines:
            line = line.strip("\x1b[m")
            if line.count(startflag):
                flag = 1
            elif flag == 1:
                if line.count(endflag):
                    flag = 0
                    break
                elif not line.count('detected'):
                    result.append(line)

        return result
#        return rau.communicate()[0].split(os.linesep)[:-1]
###     portaudio: 0:... 1:...
###     alsa: "hw:..."
###     jack: "...."
###     coreaudio: nothing
###     mme: same as portaudio

    def helpabout(self, *args):
        file = open('about.txt', 'r')
        ab = ''
        for line in file:
            ab += line
        about = ab % self.version
        win = tk.Toplevel()
        win.title("About Rationale")
        if sys.platform.count("win32"):
            try: win.iconbitmap('img/rat32.ico')
            except: pass
        win.grid_propagate(1)
        tk.Label(win, image=self.icon).grid(row=0, column=0)
        text = tk.Text(win, height=11, width=50, bd=0, relief="flat")
        text.insert("end", about, "about")
        text.tag_configure("about", justify="center", wrap="word")
        text.grid(row=1, column=0, sticky='nesw')
        win.bind("<Return>", lambda event: win.destroy())
        win.bind("<Escape>", lambda event: win.destroy())
        button = tk.Button(win, text="OK", command=win.destroy)
        button.focus_set()
        button.grid(row=2, column=0, pady=10)

    def helpManual(self, *args):
        file = open('manual.txt', 'r')
        tut = ''
        for line in file:
            tut += line
        win = tk.Toplevel()
        win.title("Rationale Manual")
        if sys.platform.count("win32"):
            try: win.iconbitmap('img/rat32.ico')
            except: pass
        win.grid_propagate(1)
        scroll = tk.Scrollbar(win)
        scroll.grid(row=0, column=1, sticky='ns')
        text = tk.Text(win, height=50, width=100, bd=2, yscrollcommand=scroll.set)
        text.insert("end", tut, "tut")
        text.tag_configure("tut", justify="left", wrap="word")
        text.grid(row=0, column=0, sticky='nesw')
        scroll.configure(command=text.yview)
        win.bind("<Return>", lambda event: win.destroy())
        win.bind("<Escape>", lambda event: win.destroy())
        button = tk.Button(win, text="OK", command=win.destroy)
        button.focus_set()
        button.grid(row=1, column=0, pady=10)

    def keyreset(self, *args):
        self.altkey = 0

    def editundo(self, *args):
        self.dispatcher.undo()

    def editredo(self, *args):
        self.dispatcher.do()

    def titleset(self):
        if self.filetosave:
            file = os.path.basename(self.filetosave)
        else:
            file = 'New Score'
        if self.unsaved:
            self.myparent.title('*Rationale %s: %s' % (vs, file))
        else:
            self.myparent.title('Rationale %s: %s' % (vs, file))

    def max(self, win):
        maxx = win.wm_maxsize()[0]
        x = (win.winfo_screenwidth()-maxx)/2
        y = win.winfo_screenheight()-win.wm_maxsize()[1]
        maxy = win.wm_maxsize()[1] - y
        str = '%dx%d+%d+%d' % (maxx, maxy, x, y)
        win.geometry(str)

    def preparescrub(self):
        self.scsort()
        if self.outautoload == True:
            self.csdreload()

        playscore = self.notelist
        proglist = []
        scrubdict = {}
        self.scrubber.scrubbits = []
        self.scrubtimelist = []
        ## assemble scrubdict, to find # pfields for all outs
        ## ("ratdefault" and "ratsf2default" have fixed numbers)
        ## (osc outs with note-off selected have on and off entries)
        for ind, inst in enumerate(self.instlist):
            if ind:
                for outline in inst.outlist:
                    if outline.__class__.__name__ == 'csdout':
                        if not outline.instnum.isdigit():
                            include = 1
                            ptotal = 1
                            ptemp = outline.string.split()
                            for pfield in ptemp:
                                if pfield.startswith('[') and not pfield.endswith(']'):
                                    include = 0
                                elif pfield.endswith(']'):
                                    ptotal += 1
                                    include = 1
                                elif include == 1:
                                    ptotal += 1
                            if scrubdict.has_key(outline.instnum) and ptotal <= scrubdict[outline.instnum]:
                                pass
                            else:
                                scrubdict[outline.instnum] = ptotal

                    elif outline.__class__.__name__ == 'oscout':
                        include = 1
                        ptotal = 4
                        ptemp = outline.string.split()
                        for pfield in ptemp:
                            if pfield.startswith('[') and not pfield.endswith(']'):
                                include = 0
                            elif pfield.endswith(']'):
                                ptotal += 1
                                include = 1
                            elif include == 1:
                                ptotal += 1
                        ind = 'rat%don%d' % (self.instlist.index(inst), inst.outlist.index(outline))
                        if scrubdict.has_key(ind) and ptotal <= scrubdict[ind]:
                            pass
                        else:
                            scrubdict[ind] = ptotal
                        if outline.noff:
                            include = 1
                            ptotal = 4
                            ptemp = outline.noffstring.split()
                            for pfield in ptemp:
                                if pfield.startswith('[') and not pfield.endswith(']'):
                                    include = 0
                                elif pfield.endswith(']'):
                                    ptotal += 1
                                    include = 1
                                elif include == 1:
                                    ptotal += 1
                            ind = 'rat%doff%d' % (self.instlist.index(inst), inst.outlist.index(outline))
                            if scrubdict.has_key(ind) and ptotal <= scrubdict[ind]:
                                pass
                            else:
                                scrubdict[ind] = ptotal


#########CsScore
        self.csdscrubsco = 'f0 3600%s' % os.linesep
        self.csdscrubsco += 'i "ratdefault" 3600 .1 0 0%s' % os.linesep
        self.csdscrubsco += '#define RATBASE #%f#%s' % (self.basefreq, os.linesep)
        if self.csdimported.count("<CsScore>"):
            scostart = self.csdimported.find("<CsScore>") + 9
            scoend = self.csdimported.find("</CsScore>")
            scolines = self.csdimported[scostart:scoend].splitlines(True)
            #
            # remove all user 'i' statements from score
            # except those marked with "; ratalways"-style comments
            # seems like score macros should be preserved,
            # but they don't seem to be?
            #
            for scoline in scolines:
                if scoline.count("ratalways") or not scoline.strip().startswith("i"):
                    self.csdscrubsco += scoline

        id = 0
        instance = 0
        for i, note in enumerate(playscore):
            if instance == 999: instance = 0
            instance += 1
            if int(note.inst) < len(self.instlist):
                if self.instlist[note.inst].solo >= self.instlist[0] and not self.instlist[note.inst].mute:
                    for outline in self.instlist[note.inst].outlist:
                        if outline.solo >= self.instlist[note.inst].gsolo and not outline.mute:
#                        if outline.solo >= self.instlist[0] and not outline.mute:
                            if outline.__class__.__name__ == 'csdout':
                                lineguide = outline.string.split()
#                                if note.voice:
#                                    line = 'i %s.%.3d' % (lineguide[0], note.voice)
#                                else:
#                                    line = 'i ' + lineguide[0]
                                if lineguide[0].isdigit():
                                    inum = int(lineguide[0]) + (instance/1000.0)
                                    offstring = 'i -%f 0 .1' % inum
                                    onstring = 'i %f 0 -%f' % (inum, abs(note.dur))
                                else:
                                    offstring = 'i "ratscrub%soff" 0 .1 %d' % (lineguide[0].strip('"'), instance)
                                    onstring = 'i "ratscrub%son" 0 .1 %d -%f' % (lineguide[0].strip('"'), instance, abs(note.dur))
#                                    print 'lineguide', lineguide[0].strip('"')
                                for pfield in range(3,len(lineguide)):
                                    onstring += ' '
                                # so that the resulting Csound file can be transposed/read:
#                                    if lineguide[pfield] == 'freq':
#                                        onstring += '[$RATBASE * %d/%d * %d/%d]' % (note.dict['num'], note.dict['den'], self.regionlist[note.region].num, self.regionlist[note.region].den)
                                    if lineguide[pfield] == 'db':
                                        onstring += '%f' % (float(note.dict['db']) + float(outline.volume))
                                    else:
                                        try:
                                            onstring += str(note.dict[lineguide[pfield]])
                                    # pass on non-keyword entries
                                        except:
                                            onstring += str(lineguide[pfield])
#                                onstring += os.linesep
#                                offstring = 'i "ratscrubturneroffer" 0 .1'
                            elif outline.__class__.__name__ == 'sf2out':
                                offstring = ''
                                try: fullpath = outline.file.filename
                                except: fullpath = None
                                if (outline.program, outline.bank, outline.file) not in proglist:
                                    proglist.append((outline.program, outline.bank, outline.file))
                                try:
                                    A = note.dict['a1']
                                except:
                                    A = outline.A
                                try:
                                    D = note.dict['a2']
                                except:
                                    D = outline.D
                                try:
                                    S = note.dict['a3']
                                except:
                                    S = outline.S
                                try:
                                    R = note.dict['a4']
                                except:
                                    R = outline.R
                                onstring = 'i "ratsf2defaulton" 0 .1 %d %f %f %d %s %s %s %s' % (instance, float(note.db)+float(outline.volume), note.freq, proglist.index((outline.program, outline.bank, outline.file)), A, D, S, R)
                                offstring = 'i "ratsf2defaultoff" 0 .1 %d' % instance
#                                offstring = 'i "ratscrubturneroffer" 0 .1'
                            elif outline.__class__.__name__ == 'oscout':
                                lineguide = outline.string.split()
                                onstring = 'i "ratoscdefault%drat%donon" 0 .1 %d' % (instance, note.inst, self.instlist[note.inst].outlist.index(outline))
                                for pfield in range(len(lineguide)):
                                    onstring += ' '
#                                    if lineguide[pfield] == 'freq':
#                                        onstring += '[$RATBASE * %d/%d * %d/%d]' % (note.dict['num'], note.dict['den'], self.regionlist[note.region].num, self.regionlist[note.region].den)
                                    if lineguide[pfield] == 'db':
                                        onstring += '%f' % (float(note.dict['db']) + float(outline.volume))
                                    else:
                                        try:
                                            onstring += str(note.dict[lineguide[pfield]])
                                        except:
                                            onstring += str(lineguide[pfield])
#                                offstring = ''
                                if outline.noff:
#                                    offstring += os.linesep
                                    lineguide = outline.noffstring.split()
                                    offstring += '%si "ratoscdefault%drat%doff" 0 0.01' % (os.linesep, note.inst, self.instlist[note.inst].outlist.index(outline))
                                    for pfield in range(len(lineguide)):
                                        offstring += ' '
#                                        if lineguide[pfield] == 'freq':
#                                            offstring += '[$RATBASE * %d/%d * %d/%d]' % (note.dict['num'], note.dict['den'], self.regionlist[note.region].num, self.regionlist[note.region].den)
                                        if lineguide[pfield] == 'db':
                                            offstring += '%f' % (float(note.dict['db']) + float(outline.volume))
                                        else:
                                            try:
                                                offstring += str(note.dict[lineguide[pfield]])
                                            except:
                                                offstring += str(lineguide[pfield])
#                                    offstring += ' 0%s' % os.linesep
#                                offstring += 'i "ratscrubturneroffer" 0 .1'
                                else:
                                    pass
                            #problems with muted/soloed
                    if not self.instlist[note.inst].outlist:
                        onstring = 'i "ratscrubratdefaulton" 0 .1 %d -%f %f %f' % (instance, abs(note.dur), note.db, note.freq)
                        offstring = 'i "ratscrubratdefaultoff" 0 .1 %d' % instance
#                        offstring = 'i "ratscrubturneroffer" 0 .1'
            else:
                onstring = 'i "ratscrubratdefaulton" 0 .1 %d -%f %f %f' % (instance, abs(note.dur), note.db, note.freq)
                offstring = 'i "ratscrubratdefaultoff" 0 .1 %d' % instance
#                offstring = 'i "ratscrubturneroffer" 0 .1'

            if onstring:
                son = scrubonscruboff(self, onstring, offstring, id)
                soff = scrubonscruboff(self, onstring, offstring, id)
                onflag = 0
                offflag = 0
                for st in self.scrubtimelist:
                    if st.x == (note.time * self.xperquarter):
                        st.sosolist.insert(0, son)
                        onflag = 1
                    if st.x == (note.time + abs(note.dur)) * self.xperquarter:
                        st.sosolist.append(soff)
                        offflag = 1
                if onflag == 0:
                    st = scrubtime(self, note.time*self.xperquarter)
                    st.sosolist.append(son)
                    self.scrubtimelist.append(st)
                if offflag == 0:
                    st = scrubtime(self, (note.time + abs(note.dur))*self.xperquarter)
                    st.sosolist.append(soff)
                    self.scrubtimelist.append(st)
            id += 1
        self.scrubtimelist.sort(key=lambda n: n.x)
        # scrubtimelist is now assembled


####FIX FIX FIX
#        tempbits = []
#        tempids = {}
#        for st in self.scrubtimelist:
#            for soso in st.sosolist:
#                if soso.id not in tempids.keys():
#                    bit = 1
#                    while bit in tempbits:
#                        bit += 1
##                        if bit == 2147483648:
##                            raise UserWarning("Time to fix SCRUB mode.")
#                    soso.bit = bit
#                    tempids[soso.id] = bit
#                    tempbits.append(bit)
#            for soso in st.sosolist:
#                if soso.bit == 0:
#                    soso.bit = tempids[soso.id]
#                    tempbits.pop(tempbits.index(soso.bit))
#                    pass
##                soso.onstring += ' %d' % soso.bit
##                soso.offstring += ' %d' % soso.bit
#                del soso.id

#########CsOptions
########    (self, instlist, method, sr, ksmps, nchnls, amodule, dac, b, B, aifffile, wavfile, commandline, commandlineuse)
        if self.csdcommandlineuse == 1:
            if self.csdcommandline.startswith('csound '):
                self.csdscrubopt = self.csdcommandline
            else:
                self.csdscrubopt = 'csound ' + self.csdcommandline
            if not self.csdscrubopt.count('.orc'):
                self.csdscrubopt += ' test.orc'
            if not self.csdscrubopt.count('.sco'):
                self.csdscrubopt += ' test.sco'

        else:
            self.csdscrubopt = 'csound -m0d'
#            if method == 0:
                ##realtime
            self.csdscrubopt += ' -+rtaudio=%s' % self.audiomodule
            if self.audiomodule == 'portaudio' or self.audiomodule == 'mme':
                self.csdscrubopt += ' -odac%s' % self.dac.strip().split(':')[0] 
            elif self.audiomodule == 'alsa' or self.audiomodule == 'jack':
                ## everything between first two sets of double-quotes
                slicestart = self.dac.find('"') + 1
                sliceend = self.dac.find('"', slicestart)
                self.csdscrubopt += ' -odac:%s' % self.dac[slicestart:sliceend]
            elif self.audiomodule == 'coreaudio':
                self.csdscrubopt += ' -odac'
            if self.b > 0:
                self.csdscrubopt += ' -b%d' % self.b
            if self.B > 0:
                self.csdscrubopt += ' -B%d' % self.B
            self.csdscrubopt += ' test.orc test.sco'

#########CsInstruments
        csdinstreplace = 'sr = %d%sksmps = %d%snchnls = %d%s%s' % (self.sr, os.linesep, self.ksmps, os.linesep, self.nchnls, os.linesep, os.linesep)
        if self.csdimported.count("<CsInstruments>"):
            orcstart = self.csdimported.find("<CsInstruments>") + 15
            orcend = self.csdimported.find("</CsInstruments>")
            csdimportinst = self.csdimported[orcstart:orcend]

            permaflag = 1
            flag = 1
            for line in csdimportinst.splitlines(True):
                if permaflag:
                    if flag:
                        if line.strip().startswith('opcode'):
                            csdinstreplace += line
                            flag = 0
                        elif line.strip().startswith('instr '):
                            csdinstreplace += line
#                            ind = line.split()[1]
                            flag = permaflag = 0
                        elif line.strip().startswith('sr') or line.strip().startswith('kr') or line.strip().startswith('ksmps') or line.strip().startswith('nchnls'):
                            pass
                        else:
                            csdinstreplace += line
                    else:
                        if line.strip().startswith('endop'):
                            flag = 1
                        csdinstreplace += line
        # put scrubturneroffer clause into each user instrument... I hope #
#                        elif line.strip().startswith('endin'):
#                            flag = 1
#                            try:
#                                csdinstreplace += 'iratidentifier = p%d%s' % (scrubdict[ind], os.linesep)
#                                csdinstreplace += '''
#iratidentifier = p6
#kratidentifier init iratidentifier
#if (gkratscrubturnoff & kratidentifier) != kratidentifier goto nevermind
#turnoff
#nevermind:
#'''                        
#                        except: pass
#                        flag = 1
                else:
                    csdinstreplace += line


        self.csdscrubinst = '''
giratdefaulttable  ftgen   0, 0, 2048, 10, 1, .2, .1
girattcursor init ''' + str(self.cursor.beat) + '''
girattcursor chnexport "rattime", 2
girattimeskip init 0
girattimeskip chnexport "rattimeskip", 1
'''
######add sf2 loading opcodes in orc header
        for ind, tempfile in enumerate(self.sf2list):
            self.csdscrubinst += 'giratsf2file%d sfload "%s"%s' % (ind, tempfile.filename, os.linesep)
        for ind, tempitem in enumerate(proglist):
            for sf2 in self.sf2list:
                if sf2.basename == tempitem[2].basename:
                    sf2no = self.sf2list.index(sf2)
            self.csdscrubinst += 'giratsf2preset%d sfpreset %s, %s, giratsf2file%d, %d%s' % (ind, tempitem[0].split()[0], tempitem[1], sf2no, ind, os.linesep)

        self.csdscrubinst = self.csdscrubinst + csdinstreplace + '''
instr +ratdefault
;iact active p1
;print p1, iact, p3
iamp = ampdb(p4)
ifreq   =       p5
idur    =       p3
;print   ifreq
;aamp    transeg 0, .004, 1, iamp, idur-.01, 1, iamp * .4, .006, 1, 0
aamp    expsegr 0.001, .004, iamp, .004, iamp * .7, 0, iamp * .7, .006, 0.001
aosc    oscil   1, ifreq, giratdefaulttable
aflt    lowpass2 aosc, 1200, 5
aenv    =       aflt * aamp
aout    =       aenv
outrg 1, aout, aout
endin

instr +ratsf2default
idur    =       p3
iamp	=	ampdb(p4)
kamp	init	iamp/0dbfs
ivel	=	127 * iamp/0dbfs
inotenum=	1
kfreq	init	p5
ipreindex=	p6
iatt    =       p7/1000
idec    =       p8/1000
isus    =       p9
irel    =       p10/1000
iflag	=	1
ioffset	=	0
ienv	=	0
;aenv    transeg 0, iatt, 1, 1, idec, 1, isus, idur-(iatt+idec+irel), 0, isus, irel, 1, 0
aenv    expsegr 0.001, iatt, 1, idec, isus, -1, isus, irel, 0.001
al, ar	sfplay	ivel, inotenum, kamp, kfreq, ipreindex, iflag, ioffset, ienv
al      =       al * aenv
ar      =       ar * aenv
	outc	al, ar
endin
'''

        for ind1, instrument in enumerate(self.instlist):
            if ind1:  # avoid instlist[0], which is a placeholder
                for ind2, outline in enumerate(instrument.outlist):
                    if outline.__class__.__name__ == 'oscout':
                        oscinst = '%sinstr +ratoscdefault%drat%don%s' % (os.linesep, ind1, ind2, os.linesep)
                        oscinst += 'Shost strcpy "%s"%siport = %d%sSpath strcpy "%s"%sOSCsend 1, Shost, iport, Spath, "' % (outline.host, os.linesep, outline.port, os.linesep, outline.path, os.linesep)
                        include, pnum = 1, 0
                        for element in outline.string.split():
                            if element.startswith('[') and not element.endswith(']'):
                                include = 0
                            elif element.endswith(']') and not element.startswith('['):
                                pnum += 1
                                include = 1
                            elif include == 1:
                                pnum += 1
#                            oscinst += 'f'
                        for i in range(0, pnum):
                            oscinst += 'f'
                        oscinst += '"'
#                        last = len(outline.string.split()) + 4
#                        for pnumber in range(4, last):
                        for pnumber in range(4, pnum + 4):
                            oscinst += ', p%d' % pnumber
                        sind = '%don%d' % (ind1, ind2)
                        oscinst += '%sendin%s' % (os.linesep, os.linesep)
                        self.csdscrubinst += oscinst

                        if outline.noff:
                            oscinst = '%sinstr +ratoscdefault%drat%doff%s' % (os.linesep, ind1, ind2, os.linesep)
                            oscinst += 'Shost strcpy "%s"%siport = %d%sSpath strcpy "%s"%sOSCsend 1, Shost, iport, Spath, "' % (outline.host, os.linesep, outline.port, os.linesep, outline.noffpath, os.linesep)
                            include, pnum = 1, 0
                            for element in outline.noffstring.split():
                                if element.startswith('[') and not element.endswith(']'):
                                    include = 0
                                elif element.endswith(']') and not element.startswith('['):
                                    pnum += 1
                                    include = 1
                                elif include == 1:
                                    pnum += 1
#                            oscinst += 'f'
                            for i in range(0, pnum):
                                oscinst += 'f'
                                oscinst += '"'
#                        last = len(outline.string.split()) + 4
#                        for pnumber in range(4, last):
                            for pnumber in range(4, pnum + 4):
                                oscinst += ', p%d' % pnumber
                            sind = '%don%d' % (ind1, ind2)
                            oscinst += '%sendin%s' % (os.linesep, os.linesep)
                            self.csdscrubinst += oscinst
                        onner = '%sinstr +ratoscdefault%drat%donon%s' % (os.linesep, ind1, ind2, os.linesep)
                        onner += 'instnum nstrnum "ratoscdefault%drat%don"%s' % (ind1, ind2, os.linesep)
                        onner += '''inum = instnum + (p4/1000)
event_i "i", inum, 0, -1'''

                        pnum = scrubdict['rat%don%d' % (ind1, ind2)]
                        for p in range(5, pnum+5):
                            onner += ', p%d' % p

                        onner += '''
endin
'''
                        offer = '%sinstr +ratoscdefault%drat%donoff%s' % (os.linesep, ind1, ind2, os.linesep)
                        offer += 'instnum nstrnum "ratoscdefault%drat%don"%s' % (ind1, ind2, os.linesep)
                        offer += '''inum = -instnum - (p4/1000)
event_i "i", inum, 0, .1
endin
'''
                        self.csdscrubinst += onner
                        self.csdscrubinst += offer

                    elif outline.__class__.__name__ == 'csdout':
                        if not outline.instnum.isdigit():
                            pnum = scrubdict[outline.instnum]
#                            onner = '%sinstr +ratscrub%son%s' % (os.linesep, outline.instnum[1:-2], os.linesep)
                            onner = '%sinstr +ratscrub%son%s' % (os.linesep, outline.instnum.strip('"'), os.linesep)
                            onner += 'instnum nstrnum "%s"%s' % (outline.instnum.strip('"'), os.linesep)
                            onner += '''inum = instnum + (p4/1000)
event_i "i", inum, 0, p5'''
                            for p in range(6, pnum+6):
                                onner += ', p%d' % p
                            onner += '''
endin
'''
#                            offer = '%sinstr +ratscrub%soff%s' % (os.linesep, outline.instnum[1:-2], os.linesep)
                            offer = '%sinstr +ratscrub%soff%s' % (os.linesep, outline.instnum.strip('"'), os.linesep)
                            offer += 'instnum nstrnum "%s"%s' % (outline.instnum.strip('"'), os.linesep)
                            offer += '''inum = -instnum - (p4/1000)
event_i "i", inum, 0, .1
endin
'''
                            self.csdscrubinst += onner
                            self.csdscrubinst += offer

        self.csdscrubinst += '''
instr +ratsf2defaulton
instnum nstrnum "ratsf2default"
inum = instnum + (p4/1000)
event_i "i", inum, 0, -1, p5, p6, p7, p8, p9, p10, p11
endin

instr +ratsf2defaultoff
instnum nstrnum "ratsf2default"
inum = -instnum - (p4/1000)
event_i "i", inum, 0, .1
endin

instr +ratscrubratdefaulton
instnum nstrnum "ratdefault"
inum = instnum + (p4/1000)
event_i "i", inum, 0, p5, p6, p7
endin

instr +ratscrubratdefaultoff
instnum nstrnum "ratdefault"
inum = -instnum - (p4/1000)
event_i "i", inum, 0, .1
endin
'''
#        print [soso.onstring for soso in st.sosolist for st in self.scrubtimelist]
        print [st.x for st in self.scrubtimelist]

    def scrubplay(self):
        '''Copied from play().

        Updated to reflect the changing needs of our customers.'''

        if len(self.notelist):
            cstart = 1
#            for instno in range(1, len(self.instlist)):
#                if not self.instlist[instno].mute:
#                    for out in self.instlist[instno].outlist:
#                        if not out.mute:
#                            cstart = 1

            if cstart:
                self.preparescrub()

        #create socket to receive callbacks to move the time cursor
        #well not necessary in SCRUB mode, but let's leave the code in place
                cbwait = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                count = 0
                while count < 30000:
                    try:
                        cbwait.bind(('127.0.0.1', self.cbscrubport))
                        print 'Callback Port: %s' % str(self.cbscrubport)
                        count = 30000
                    except:
                        self.cbscrubport += 1
                        count += 1
                        if count == 30000:
                            print "NO PORTS AVAILABLE FOR CALLBACK"

                cbwait.listen(2)
#                self.outscrubsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #thread to wait for rataudio to connect
                r = Queue.Queue()
                wait = threading.Thread(target=self.waitforconnect, args=(cbwait, r))
                wait.start()

                count = 0
#                while count < 10000:
#                    tmpsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                    try:
#                        tmpsoc.bind(('127.0.0.1', self.outscrubport))
#                        count = 10000
#                        del tmpsoc
#                    except:
#                        self.outscrubport += 1
#                        count += 1
#                        del tmpsoc
#            #Rationale SCRUB AUdio engine
                self.rauscrub = subprocess.Popen((sys.executable, 'ratscrubaudio.py', str(self.cbscrubport)))
                if sys.platform.count("linux"):
                    try:
                        os.nice(-1)
                        os.nice(6)
                    except: pass

                wait.join()
                self.cbscrubsock = r.get()[0]

                self.scrubbing = 1
                threading.Thread(target=self.delegatescrubcallbacks, args=(self.cbscrubsock,)).start()

                self.cbscrubsock.sendall('csdopt:%sRATENDMESSAGE' % self.csdscrubopt)
                self.cbscrubsock.sendall('csdorc:%sRATENDMESSAGE' % self.csdscrubinst)
                self.cbscrubsock.sendall('csdsco:%sRATENDMESSAGE' % self.csdscrubsco)
                self.cbscrubsock.sendall('csdgozRATENDMESSAGE')
        else:
            self.scrubtimelist = []

class scrubonscruboff(object):
    def __init__(self, parent, onstring, offstring, id):
        self.myparent = parent
        self.onstring = onstring
        self.offstring = offstring
        self.bit = str(id)
#        self.id = str(id)

class scrubtime(object):
    def __init__(self, parent, x):
        self.myparent = parent
        self.x = x
        self.sosolist = []

class scrubcursor(object):
    def __init__(self, parent, x, ind):
        self.myparent = parent
        self.x = x
        self.ind = ind
        self.bits = []
        self.slowdown = 0
        self.widget = self.myparent.score.create_rectangle(self.x-1,self.myparent.miny,self.x+1,self.myparent.maxy, fill="#cccccc", outline="#888888", stipple="gray25", tags=("scrubcursor", "all"))

    def seek(self, event):
        self.find(self.myparent.score.canvasx(event.x))

    def find(self, x):
        ind = 0
        scrubbits = []
        self.scrubinitdict = {}
#        eventx = self.myparent.score.canvasx(event.x)
#        self.x = self.myparent.score.canvasx(event.x)
        self.x = x
        self.myparent.score.coords(self.widget, self.x-1,self.myparent.miny,self.x+1,self.myparent.maxy)
        while ind < len(self.myparent.scrubtimelist) and self.myparent.scrubtimelist[ind].x <= self.x:
#            print 'x:', self.scrubtimelist[ind].x
            for soso in self.myparent.scrubtimelist[ind].sosolist:
#                print 'global scrubbits:', self.scrubbits
#                print 'scrubbits:', scrubbits
#                print 'bit:', soso.bit
                if soso.bit in scrubbits:
                    scrubbits.pop(scrubbits.index(soso.bit))
                    del self.scrubinitdict[str(soso.bit)]
                else:
                    scrubbits.append(soso.bit)
                    self.scrubinitdict[str(soso.bit)] = soso.onstring
            ind += 1
#        if self.scrubtimelist[-1].x <= self.score.canvasx(event.x):
#            scrubbits = 0
#        self.scrubbits = scrubbits
#        self.x = eventx
        self.bits = self.initbits = scrubbits
#        self.scrubinitdict = scrubinitdict
        self.ind = ind
#        print ind

    def buttondown(self, event):
#        print "starting to scrub"
#        print self.scrubinitdict
        for line in self.scrubinitdict.values():
            try: self.myparent.cbscrubsock.sendall('csdadd:%sRATENDMESSAGE' % line)
            except: print "Unable to send notes"
#            print line

    def scroll(self, event):
        offbits = []
        eventx = self.myparent.score.canvasx(event.x)
        # going down
#        print self.x, self.myparent.score.canvasx(event.x)
        if eventx < self.x and self.ind > 0:
            stind = self.ind - 1
            flag = 1
            while flag == 1:
                if stind == -1:
#                    for soso in self.myparent.scrubtimelist[0].sosolist:
#                        print 'dammit:', soso.offstring
#                        pass
                    self.bits = []
                    flag = 0
                elif self.myparent.scrubtimelist[stind].x >= eventx:
#                    print "down"
                    for soso in self.myparent.scrubtimelist[stind].sosolist:
#                       if on: off
                        if soso.bit in self.bits:
                            offbits.append(soso.bit)
                            if soso.offstring:
                                try: self.myparent.cbscrubsock.sendall('csdadd:%sRATENDMESSAGE' % soso.offstring)
                                except: print "String failed:", soso.offstring
#                                print soso.offstring
#                            print 'bits', self.bits
#                            print soso.bit
                            self.bits.pop(self.bits.index(soso.bit))
#                            print 'bits', self.bits
#                       if off: on
                        elif not soso.bit in self.bits:
                            try: self.myparent.cbscrubsock.sendall('csdadd:%sRATENDMESSAGE' % soso.onstring)
                            except: print "String failed:", soso.onstring
#                            print soso.onstring
#                            print soso.bit
                            self.bits.append(soso.bit)
#                            print 'bits', self.bits
                    stind -= 1
                    self.ind -= 1
                else:
                    flag = 0
        # going up
        elif eventx > self.x and self.ind <= len(self.myparent.scrubtimelist):
            stind = self.ind
            flag = 1
            while flag == 1:
                if stind == len(self.myparent.scrubtimelist):
#                    for soso in self.myparent.scrubtimelist[-1].sosolist:
#                        print soso.offstring
#                        pass
                    self.bits = []
                    flag = 0
                elif self.myparent.scrubtimelist[stind].x <= eventx:
#                    print "up"
                    for soso in self.myparent.scrubtimelist[stind].sosolist:
#                       if on: off
                        if soso.bit in self.bits:
                            offbits.append(soso.bit)
                            if soso.offstring:
                                try: self.myparent.cbscrubsock.sendall('csdadd:%sRATENDMESSAGE' % soso.offstring)
                                except: print "String failed:", soso.offstring
#                                print soso.offstring
#                            print 'bits', self.bits
#                            print soso.bit
                            self.bits.pop(self.bits.index(soso.bit))
#                            print 'bits', self.bits
#                       if off: on
                        elif not soso.bit in self.bits:
                            try:
                                self.myparent.cbscrubsock.sendall('csdadd:%sRATENDMESSAGE' % soso.onstring)
#                                print "note sent..."
                            except:
                                print "String failed:", soso.onstring
#                                print "Unexpected error:", sys.exc_info()[0]
#                                raise
#                            print soso.onstring
#                            print soso.bit
                            self.bits.append(soso.bit)
#                            print 'bits', self.bits
                    stind += 1
                    self.ind += 1
                else:
                    flag = 0
#        if offbits:
##            try: self.myparent.outscrubsock.sendall('csdadd:i "ratscrubturneroffer" 0 .1 %dRATENDMESSAGE' % offbits)
#            try:
#                self.myparent.outscrubsock.sendall('csdadd:%sRATENDMESSAGE' % soso.offstring)
#                print soso.offstring
#            except: pass
##            print 'i "ratscrubturneroffer" 0 .1 %d' % offbits
        self.x = eventx
        self.autoscroll(eventx)
#            if self.slowdown >= 10:
#                self.myparent.scorexscroll('scroll', '1', "units")
#                self.slowdown = 0
#            else:
#                self.slowdown += 1
        self.myparent.score.coords(self.widget, self.x-1,self.myparent.miny,self.x+1,self.myparent.maxy)

    def autoscroll(self, x):
        realw = self.myparent.score.winfo_width()
        relw = self.myparent.score.canvasx(realw)
        rel0 = self.myparent.score.canvasx(0)
        scrollreg = self.myparent.score.cget("scrollregion").split()
        scrw = int(scrollreg[2]) - int(scrollreg[0])
        reall = self.myparent.score.canvasx(0) - int(scrollreg[0])
        newl = reall + 10.0
        newr = reall - 10.0
#        print "reall:", reall, newl
#        print "scrw:", scrw
        newloc = newl/scrw
        bacloc = newr/scrw
#        print "newloc:", newloc
        if relw-x < 50 or x > relw:
            self.myparent.scorexscroll('moveto', newloc)
        elif -30 < rel0 and (x-rel0 < 50 or x < rel0):
            self.myparent.scorexscroll('moveto', bacloc)

    def release(self):
#        print "release"
#        try:
#            self.myparent.outscrubsock.sendall('csdadd:i "ratscrubturneroffer" 0 .1 8388607 RATENDMESSAGE')
#        except: pass
#        print 'i "ratscrubturneroffer" 0 .1 8388607'

#        oscoffdict = {}
#        print self.bits
        for stind in range(0, self.ind):
            for soso in self.myparent.scrubtimelist[stind].sosolist:
                if soso.bit in self.bits:
                    try: self.myparent.cbscrubsock.sendall('csdadd:%sRATENDMESSAGE' % soso.offstring)
                    except: print "String failed:", soso.offstring
        self.bits = []
        self.find(self.x)
#                    oscoffdict[str(soso.bit)] = soso.offstring
#        for offstring in oscoffdict.values():
#            if offstring:
#                try: self.myparent.outscrubsock.sendall('csdadd:%sRATENDMESSAGE' % offstring)
#                except: print "String failed:", offstring
#                print offstring

class audiodialog(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.myparent = parent
        if sys.platform.count("win32"):
            try: self.iconbitmap('img/rat32.ico')
            except: pass
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        if sys.platform.count("win32"):
            self.amodules = ['portaudio', 'mme']
        elif sys.platform.count("linux"):
            self.amodules = ['portaudio', 'alsa', 'jack']
        elif sys.platform.count("darwin"):
            self.amodules = ['portaudio']
        self.modulevar = tk.StringVar()
        self.modulevar.set(self.myparent.audiomodule)
        self.modulevar.trace("w", self.dacreset)
        self.dacvar = tk.StringVar()
        self.dacvar.set(self.myparent.dac)
        self.bvar = tk.IntVar()
        self.bvar.set(self.myparent.b)
        self.Bvar = tk.IntVar()
        self.Bvar.set(self.myparent.B)
        self.aiffvar = tk.StringVar()
        self.aiffvar.set(self.myparent.aifffile)
        self.wavvar = tk.StringVar()
        self.wavvar.set(self.myparent.wavfile)
        self.overridevar = tk.IntVar()
        self.overridevar.set(self.myparent.csdcommandlineuse)
        self.csdcommandlinevar = tk.StringVar()
        self.csdcommandlinevar.set(self.myparent.csdcommandline)
        self.srvar = tk.IntVar()
        self.srvar.set(self.myparent.sr)
#        self.srvar.trace("w", self.srverify)
        self.krvar = tk.DoubleVar()
        self.krvar.set(self.myparent.kr)
#        self.krvar.trace("w", self.krverify)
        self.ksmpsvar = tk.IntVar()
        self.ksmpsvar.set(self.myparent.ksmps)
#        self.ksmpsvar.trace("w", self.ksmpsverify)
        self.nchnlsvar = tk.IntVar()
        self.nchnlsvar.set(self.myparent.nchnls)
#        self.widget = tk.Toplevel(self.myparent.myparent, width=340, height=400)
        self.title("Audio Options")
        self.rowconfigure(4, weight=1)
        self.columnconfigure(0, weight=1)
        self.banner = tk.Label(self, text="Audio Options")
#        self.banner.grid(row=0, column=0, sticky='ew')
        self.outputfr = tk.Frame(self, bd=2, relief="ridge")
        self.outputfr.rowconfigure(0, weight=1)
        self.outputfr.columnconfigure(0, weight=0)
        self.outputfr.columnconfigure(1, weight=1)
        self.outputfr.grid(row=1, column=0, sticky='ew')
        self.manualfr = tk.Frame(self, bd=2, relief="ridge")
        self.manualfr.grid(row=2, column=0, sticky='ew')
        self.ratefr = tk.Frame(self, bd=2, relief="ridge")
        self.ratefr.columnconfigure(0, weight=0)
        self.ratefr.columnconfigure(4, weight=1)
        self.ratefr.grid(row=3, column=0, sticky='ew')
#--------------------------outputfr
        tk.Label(self.outputfr, text="Output", bg="#aaaaaa").grid(row=0, column=0, sticky='w')
        self.outputmethod = tk.IntVar()
        self.outputmethod.set(self.myparent.outputmethod)
        self.playback = tk.Radiobutton(self.outputfr, text="Real-Time: ", variable=self.outputmethod, value=0)
        self.playback.grid(row=1, column=0, sticky='w')
        self.audiomodulefr = tk.Frame(self.outputfr)
        self.audiomodulefr.grid(row=1, column=1, sticky='w')
#        self.audiomoduleselector = tk.ComboBox(self.audiomodulefr, editable=0, variable=self.modulevar, listwidth=25, label="Module")
#        self.audiomoduleselector.entry.configure(width=10)
#        self.audiomoduleselector.subwidget("listbox").configure(height=6)
#        self.audiomoduleselector.grid(row=0, column=0, sticky='w')
        tk.Label(self.audiomodulefr, text="Module:").grid(row=0, column=0, sticky='e')
#        self.downarrow = tk.BitmapImage(file="downarrow.xbm")
        self.audiomoduleselector = tk.Menubutton(self.audiomodulefr, textvariable=self.modulevar, bg="#aa9999", activebackground="#bbaaaa", width=10, relief="raised", padx=0, indicatoron=1)
        self.audiomoduleselectormenu = tk.Menu(self.audiomoduleselector, tearoff=0)

#        self.outputfr.grid_propagate()
        for module in self.amodules:
#            self.audiomoduleselector.append_history(module)
            self.audiomoduleselectormenu.add_command(label=module, command=lambda arg1=module: self.changemodule(arg1))
        self.audiomoduleselector['menu'] = self.audiomoduleselectormenu
        self.audiomoduleselector.grid(row=0, column=1, sticky='w')
#        self.downarrow.grid(row=0, column=2, sticky='w', padx=0)
        self.getparentaudiodevices()
        self.bfr = tk.Frame(self.outputfr)
        self.bfr.grid(row=2, column=1, sticky='w')
        self.blabel = tk.Label(self.bfr, text="-b")
        self.blabel.grid(row=0, column=0, sticky='w')
        self.bfield = tk.Entry(self.bfr, width=7, textvariable=self.bvar)
        self.bfield.grid(row=0, column=1, sticky='w')
        self.bdesc = tk.Label(self.bfr, text="Samples per Software Buffer")
        self.bdesc.grid(row=0, column=2, sticky='w')
        self.bdef = tk.Button(self.bfr, text="default", command=self.bdefault)
        self.bdef.grid(row=0, column=3, sticky='w')
        self.Bfr = tk.Frame(self.outputfr)
        self.Bfr.grid(row=3, column=1, sticky='w')
        self.Blabel = tk.Label(self.Bfr, text="-B")
        self.Blabel.grid(row=0, column=0, sticky='w')
        self.Bfield = tk.Entry(self.Bfr, width=7, textvariable=self.Bvar)
        self.Bfield.grid(row=0, column=1, sticky='w')
        self.Bdesc = tk.Label(self.Bfr, text="Samples per Hardware Buffer")
        self.Bdesc.grid(row=0, column=2, sticky='w')
        self.Bdef = tk.Button(self.Bfr, text="default", command=self.Bdefault)
        self.Bdef.grid(row=0, column=3, sticky='w')

        self.aiff = tk.Radiobutton(self.outputfr, text="AIFF", variable=self.outputmethod, value=1)
        self.aiff.grid(row=4, column=0, sticky='w')
        self.aifffr = tk.Frame(self.outputfr)
        self.aifffr.grid(row=4, column=1, sticky='w', pady=10)
        self.aifflb = tk.Label(self.aifffr, text="File: ")
        self.aifflb.grid(row=0, column=0, sticky='w')
        self.aifffield = tk.Entry(self.aifffr, width=15, textvariable=self.aiffvar)
        self.aifffield.grid(row=0, column=1, sticky='w')
        self.aiffbrowse = tk.Button(self.aifffr, text="Browse...", command=self.aiffchoose)
        self.aiffbrowse.grid(row=0, column=2, sticky='w', padx=10)
        self.wav = tk.Radiobutton(self.outputfr, text="WAV", variable=self.outputmethod, value=2)
        self.wav.grid(row=5, column=0, sticky='w')
        self.wavfr = tk.Frame(self.outputfr)
        self.wavfr.grid(row=5, column=1, sticky='w')
        self.wavlb = tk.Label(self.wavfr, text="File: ")
        self.wavlb.grid(row=0, column=0, sticky='w')
        self.wavfield = tk.Entry(self.wavfr, width=15, textvariable=self.wavvar)
        self.wavfield.grid(row=0, column=1, sticky='w')
        self.wavbrowse = tk.Button(self.wavfr, text="Browse...", command=self.wavchoose)
        self.wavbrowse.grid(row=0, column=2, sticky='w', padx=10)
#----------------------manualfr
        self.manualfr.columnconfigure(2, weight=1)
        self.manualselector = tk.Checkbutton(self.manualfr, text="Override Command Line", variable=self.overridevar)
        self.manualselector.grid(row=0, column=0, sticky='w')
        self.manualfield = tk.Entry(self.manualfr, width=50, textvariable=self.csdcommandlinevar)
        self.manualfield.grid(row=0, column=1, sticky='w')
#----------------------ratefr
        tk.Label(self.ratefr, text="Orchestra Header", bg="#aaaaaa").grid(row=0, column=0, sticky='w', columnspan=4)
        self.srfield = tk.Entry(self.ratefr, width=8, textvariable=self.srvar)
        self.srfield.grid(row=1, column=1, sticky='w')
        self.srfield.bind("<FocusOut>", self.srverify)
        self.srlb = tk.Label(self.ratefr, text="Sample Rate (sr)")
        self.srlb.grid(row=1, column=3, sticky='w')
        tk.Label(self.ratefr, text="/").grid(row=2, column=0, sticky='w')
        self.krfield = tk.Entry(self.ratefr, width=8, textvariable=self.krvar)
        self.krfield.grid(row=2, column=1, sticky='w')
        self.krfield.bind("<FocusOut>", self.krverify)
        self.krlb = tk.Label(self.ratefr, text="Control Rate (kr)")
        self.krlb.grid(row=2, column=3, sticky='w')
        tk.Label(self.ratefr, text="=").grid(row=3, column=0, sticky='w')
        self.ksmpsfield = tk.Entry(self.ratefr, width=8, textvariable=self.ksmpsvar)
        self.ksmpsfield.grid(row=3, column=1, sticky='w', pady=4)
        self.ksmpsfield.bind("<FocusOut>", self.ksmpsverify)
        self.ksmpslb = tk.Label(self.ratefr, text="Samples per Control Period (ksmps)")
        self.ksmpslb.grid(row=3, column=3, sticky='w')

        self.nchnlsfr = tk.Frame(self.ratefr)
        self.nchnlsfr.grid(row=4, column=0, sticky='w', columnspan=4)
        self.nchnlsfield = tk.Spinbox(self.nchnlsfr, width=3, from_=1, to=64, repeatinterval=100, repeatdelay=500, textvariable=self.nchnlsvar)
        self.nchnlsfield.grid(row=0, column=0, sticky='w')
        self.nchnlslb = tk.Label(self.nchnlsfr, text="Number of Audio Channels")
        self.nchnlslb.grid(row=0, column=1, sticky='w')

#----------------------buttons
        self.buttons = tk.Frame(self, width=300, height=80, borderwidth=1, relief="raised")
        tk.Button(self.buttons, text="OK", command=self.ok).grid(row=0, column=0, padx=10)
        tk.Button(self.buttons, text="Cancel", command=self.cancel).grid(row=0, column=1, padx=10)
#        tk.Button(self.buttons, text="Test Tone", command=self.test).grid(row=0, column=2, padx=10)
        self.playbutton = tk.Button(self.buttons, text="Play", command=self.play)
        self.playbutton.grid(row=0, column=3, padx=10)
        self.buttons.grid(row=5, column=0, columnspan=6, sticky='s', ipady=20)
        self.lift()
        self.focus_set()

    def aiffchoose(self):
        aiffname = tkfd.asksaveasfilename(master=self, title="Output AIFF", defaultextension=".aif")
        if aiffname:
            self.aiffvar.set(aiffname)
            self.aifffield.xview("end")

    def wavchoose(self):
        wavname = tkfd.asksaveasfilename(master=self, title="Output wav", defaultextension=".wav")
        if wavname:
            self.wavvar.set(wavname)
            self.wavfield.xview("end")

    def changemodule(self, module):
        if self.modulevar.get() != module:
            self.modulevar.set(module)

    def changedac(self, dac):
        self.dacvar.set(dac)

    def ok(self, *args):
        self.myparent.outputmethod = self.outputmethod.get()
        self.myparent.audiomodule = self.modulevar.get()
        self.myparent.dac = self.dacvar.get()
        self.myparent.b = self.bvar.get()
        self.myparent.B = self.Bvar.get()
        self.myparent.aifffile = self.aiffvar.get()
        self.myparent.wavfile = self.wavvar.get()
        self.myparent.csdcommandlineuse = self.overridevar.get()
        self.myparent.csdcommandline = self.csdcommandlinevar.get()
        self.krvar.set(float(self.srvar.get())/self.ksmpsvar.get())
        self.myparent.sr = self.srvar.get()
        self.myparent.kr = self.krvar.get()
        self.myparent.ksmps = self.ksmpsvar.get()
        self.myparent.nchnls = self.nchnlsvar.get()
        self.cancel()

    def bdefault(self, *args):
        self.bvar.set(-1)

    def Bdefault(self, *args):
        self.Bvar.set(-1)

    def cancel(self, *args):
        self.destroy()

    def test(self, *args):
        pass

    def play(self, *args):
        self.myparent.play(self.myparent.instlist, self.myparent.sf2list, self.outputmethod.get(), self.srvar.get(), self.ksmpsvar.get(), self.nchnlsvar.get(), self.modulevar.get(), self.dacvar.get(), self.bvar.get(), self.Bvar.get(), self.aiffvar.get(), self.wavvar.get(), self.csdcommandlinevar.get(), self.overridevar.get())
        self.playbutton.configure(text="Stop", command=self.stop)

    def stop(self, *args):
        self.myparent.stop()
        self.playbutton.configure(text="Play", command=self.play)

    def getparentaudiodevices(self, *args):
        self.dacselector = tk.Menubutton(self.audiomodulefr, textvariable=self.dacvar, bg="#99aa99", activebackground="#aabbaa", width=10, relief="raised", anchor="w", indicatoron=1)
        self.dacselectormenu = tk.Menu(self.dacselector, tearoff=0)

        daclist = self.myparent.getaudiodevices(self.modulevar.get())
        if daclist:
            for dac in daclist:
                if not dac.count('detected'):
                    self.dacselectormenu.add_command(label=str(dac).strip(), command=lambda arg1=dac: self.changedac(arg1))
        else: self.dacvar.set('')
        self.dacselector['menu'] = self.dacselectormenu
        tk.Label(self.audiomodulefr, text="DAC:").grid(row=0, column=2, sticky='e')
        self.dacselector.grid(row=0, column=3, sticky='w')

    def dacreset(self, *args):
        self.dacselector.destroy()
        self.getparentaudiodevices()
        self.dacselectormenu.invoke(0)

    def srverify(self, *args):
        self.srvar.set(int(self.srvar.get()))
        self.krvar.set(float(self.srvar.get())/self.ksmpsvar.get())

    def krverify(self, *args):
        self.ksmpsvar.set(int(self.srvar.get()/self.krvar.get()))
        self.krvar.set(float(self.srvar.get())/self.ksmpsvar.get())

    def ksmpsverify(self, *args):
        self.ksmpsvar.set(int(self.ksmpsvar.get()))
        self.krvar.set(float(self.srvar.get())/self.ksmpsvar.get())

class notewidgetclass(object):
    def __init__(self, parent, note):
        self.myparent = parent
        self.note = note
        self.connect = None
        self.purex = self.note.time * self.myparent.xperquarter
        self.purey = self.myparent.regionlist[self.note.region].octave11 - ((math.log(float(self.note.num)/float(self.note.den))/self.myparent.log2) * self.myparent.octaveres)
#        print self.purey
        self.yoff = self.note.db/6.0
        self.xoff = self.yoff/2.0
        self.durx = self.purex + abs(self.note.dur) * self.myparent.xperquarter
        if self.note.inst >= len(self.myparent.instlist):
            self.color = '#888888'
        else:
            self.color = self.myparent.instlist[self.note.inst].color
        self.rcolor = self.myparent.regionlist[self.note.region].color
        self.rnum = self.myparent.regionlist[self.note.region].num
        self.rden = self.myparent.regionlist[self.note.region].den
        self.rstring = 'r ' + str(self.note.region)
        if self.note.voice == 0:
            self.vstring = ''
        else:
            self.vstring = str(self.note.voice)
        self.draw()

    def updatetime(self):
        self.purex = self.note.time * self.myparent.xperquarter
        self.durx = self.purex + abs(self.note.dur) * self.myparent.xperquarter
        self.myparent.score.coords(self.notewidget, self.purex+self.xoff,self.purey,self.purex,self.purey-self.yoff,self.purex,self.purey+self.yoff,self.purex+self.xoff,self.purey,self.durx,self.purey)
        self.myparent.score.coords(self.numwidget, self.purex,self.purey)
        self.myparent.score.coords(self.denwidget, self.purex,self.purey)
        self.myparent.score.coords(self.rnumwidget, self.purex+6,self.purey-12)
        self.myparent.score.coords(self.rdenwidget, self.purex+6,self.purey+12)
        self.myparent.score.coords(self.regiondisp, self.purex+6,self.purey)
        self.myparent.score.coords(self.voicedisp, self.purex+6,self.purey)
#        self.note.setsdur()

    def updateheight(self):
        self.purey = self.myparent.regionlist[self.note.region].octave11 - ((math.log(float(self.note.num)/float(self.note.den))/self.myparent.log2) * self.myparent.octaveres)
        self.myparent.score.coords(self.notewidget, self.purex+self.xoff,self.purey,self.purex,self.purey-self.yoff,self.purex,self.purey+self.yoff,self.purex+self.xoff,self.purey,self.durx,self.purey)
        self.myparent.score.coords(self.numwidget, self.purex,self.purey)
        self.myparent.score.coords(self.denwidget, self.purex,self.purey)
        self.myparent.score.coords(self.rnumwidget, self.purex+6,self.purey-12)
        self.myparent.score.coords(self.rdenwidget, self.purex+6,self.purey+12)
        self.myparent.score.coords(self.regiondisp, self.purex+6,self.purey)
        self.myparent.score.coords(self.voicedisp, self.purex+6,self.purey)

    def updatedb(self):
        self.yoff = self.note.db/6.0
        self.xoff = self.yoff/2.0
        self.myparent.score.coords(self.notewidget, self.purex+self.xoff,self.purey,self.purex,self.purey-self.yoff,self.purex,self.purey+self.yoff,self.purex+self.xoff,self.purey,self.durx,self.purey)

    def updatedur(self):
        self.durx = self.purex + abs(self.note.dur) * self.myparent.xperquarter
        self.myparent.score.coords(self.notewidget, self.purex+self.xoff,self.purey,self.purex,self.purey-self.yoff,self.purex,self.purey+self.yoff,self.purex+self.xoff,self.purey,self.durx,self.purey)
#        self.note.setsdur()

    def updateinst(self):
        if self.note.inst < len(self.myparent.instlist):
            self.color = self.myparent.instlist[self.note.inst].color
        else:
            self.color = '#888888'
        if self.note.sel:
            outline = "#ff6670"
        else:
            outline = self.color
        self.myparent.score.itemconfigure(self.notewidget, fill=self.color, outline=outline)
        self.myparent.score.itemconfigure(self.numwidget, fill=self.color)
        self.myparent.score.itemconfigure(self.denwidget, fill=self.color)
        self.myparent.score.itemconfigure(self.voicedisp, fill=self.color)

    def updateregion(self):
        self.rcolor = self.myparent.regionlist[self.note.region].color
        self.rnum = self.myparent.regionlist[self.note.region].num
        self.rden = self.myparent.regionlist[self.note.region].den
        self.rstring = 'r ' + str(self.note.region)
        self.myparent.score.itemconfigure(self.numwidget, text=self.note.num)
        self.myparent.score.itemconfigure(self.denwidget, text=self.note.den)
        self.myparent.score.itemconfigure(self.rnumwidget, text=self.rnum, fill=self.rcolor)
        self.myparent.score.itemconfigure(self.rdenwidget, text=self.rden, fill=self.rcolor)
        self.myparent.score.itemconfigure(self.regiondisp, text=self.rstring, fill=self.rcolor)

    def updatevoice(self):
        if self.note.voice == 0:
            self.vstring = ''
        else:
            self.vstring = str(self.note.voice)
        self.myparent.score.itemconfigure(self.voicedisp, text=self.vstring)

    def updateconnect(self):
#        print self.connect, self.note.voice
        if self.note.dur < 0:
#            flag = 1
            endx = None
            for nw in sorted(self.myparent.notewidgetlist, key=lambda x: (x.purex)):
                if nw.note.inst == self.note.inst and nw.note.voice == self.note.voice and nw.note.time > self.note.time and not endx:
                    endx, endy = nw.purex, nw.purey
#                    flag = 0
#            print "endx", endx, self.connect
            if self.connect and self.note.voice == 0:
                self.myparent.score.delete(self.connect)
                self.connect = None
            elif self.connect and endx:
                self.myparent.score.coords(self.connect, self.purex, self.purey, endx, endy)
#                self.myparent.score.itemconfig(self.connect, fill="#ffcccc")
            elif endx:
                self.connect = self.myparent.score.create_line(self.purex, self.purey, endx, endy, fill="#ffcccc", width=5, tags="all")
#                print self.connect
                self.myparent.score.tag_lower(self.connect)
            elif self.connect:
                self.myparent.score.delete(self.connect)
                self.connect = None
        else:
            if self.connect:
                self.myparent.score.delete(self.connect)
                self.connect = None

    def undraw(self):
        self.myparent.score.delete(self.notewidget)
        self.myparent.score.delete(self.numwidget)
        self.myparent.score.delete(self.denwidget)
        self.myparent.score.delete(self.rnumwidget)
        self.myparent.score.delete(self.rdenwidget)
        self.myparent.score.delete(self.regiondisp)
        self.myparent.score.delete(self.voicedisp)
        try: self.myparent.score.delete(self.connect)
        except: pass
        self.connect = None

    def draw(self):
#        print self.note.dur, self.note.voice
        if self.note.sel:
            outline = "#ff6670"
            border = 3
        else:
            outline = self.color
            border = 1

        self.notewidget = self.myparent.score.create_polygon(self.purex+self.xoff, self.purey, self.purex, self.purey-self.yoff, self.purex, self.purey+self.yoff, self.purex+self.xoff, self.purey, self.durx, self.purey, fill=self.color, outline=outline, width=border, tags=("note", "all"))
        self.numwidget = self.myparent.score.create_text(self.purex, self.purey, anchor="se", fill=self.color, text=str(self.note.num), tags="all")
        self.denwidget = self.myparent.score.create_text(self.purex, self.purey, anchor="ne", fill=self.color, text=str(self.note.den), tags="all")
        self.rnumwidget = self.myparent.score.create_text(self.purex+6, self.purey-12, anchor="se", fill=self.rcolor, text=str(self.rnum), font=("Times",10), tags="all")
        self.rdenwidget = self.myparent.score.create_text(self.purex+6, self.purey+12, anchor="ne", fill=self.rcolor, text=str(self.rden), font=("Times",10), tags="all")
        self.regiondisp = self.myparent.score.create_text(self.purex+6, self.purey, anchor="sw", fill=self.rcolor, text=self.rstring, font=("Times",10,"bold"), tags="all")
        self.voicedisp = self.myparent.score.create_text(self.purex+6, self.purey, anchor="nw", fill=self.color, text=self.vstring, font=("Times",10), tags="all")

    def remove(self):
        pass

class note(object):
    def __init__(self, parent, id, inst, voice, time, dur, db, num, den, region, sel):
        self.myparent = parent
        self.id = id
        self.inst = inst
        self.voice = voice
        self.time = time
        self.dur = dur
        self.db = db
        self.num = num
        self.den = den
        self.region = region
        self.sel = sel
        self.arb = ()
        self.scrubonscruboff = None
        rnum = self.myparent.regionlist[self.region].num
        rden = self.myparent.regionlist[self.region].den
        self.freq = (float(rnum * self.num))/(float(rden * self.den)) * self.myparent.basefreq
        self.sdur = 0
        self.dict = {'inst': self.inst, 'voice': self.voice, 'time': self.time, 'dur': self.dur, 'sdur': self.sdur, 'db': self.db, 'num': self.num, 'den': self.den, 'region': self.region, 'freq': self.freq}

    def updateinst(self, inst):
        self.inst = inst
        self.dict['inst'] = inst
#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def updatevoice(self, voice):
        self.voice = voice
        self.dict['voice'] = voice
#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def updatetime(self, time):
        self.time = time
        self.dict['time'] = time
#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def updatedur(self, dur):
        self.dur = dur
        self.dict['dur'] = dur
#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def updatedb(self, db):
        self.db = db
        self.dict['db'] = db
#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def updatenum(self, num):
        self.num = num
        self.dict['num'] = num
        rnum = self.myparent.regionlist[self.region].num
        rden = self.myparent.regionlist[self.region].den
        self.freq = (float(rnum * self.num))/(float(rden * self.den)) * self.myparent.basefreq
        self.dict['freq'] = self.freq
#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def updateden(self, den):
        self.den = den
        self.dict['den'] = den
        rnum = self.myparent.regionlist[self.region].num
        rden = self.myparent.regionlist[self.region].den
        self.freq = (float(rnum * self.num))/(float(rden * self.den)) * self.myparent.basefreq
        self.dict['freq'] = self.freq
#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def updateregion(self, region):
        self.region = region
        self.dict['region'] = region
#        if not self.myparent.unsaved: self.myparent.unsaved = True

class noteeditlist(object):
    def __init__(self, parent):
        self.myparent = parent
        self.myparent.scsort()
        self.widget = tk.Toplevel(self.myparent.myparent)
        self.widget.title("Note List")
        self.widget.rowconfigure(0, weight=0)
        self.widget.rowconfigure(1, weight=0)
        self.widget.rowconfigure(2, weight=1)
        self.notesfr = tk.Frame(self.widget)
        self.notesfr.grid(row=0, column=0, sticky='ew')
        self.buttonfr = tk.Frame(self.widget)
        self.buttonfr.grid(row=1, column=0, sticky='ew')
        self.ok = tk.Button(self.buttonfr, text="OK")
        self.ok.grid(row=0, column=0)
        self.cancel = tk.Button(self.buttonfr, text="Cancel")
        self.cancel.grid(row=0, column=1)
        row = 0
        for note in self.myparent.notelist:
            note.fr = tk.Frame(self.notesfr)
            note.fr.grid(row=row, column=0)
            note.instwidget = tk.Entry(note.fr, width=5)
            note.instwidget.grid(row=0, column=0, rowspan=2)
            note.instwidget.insert("end", str(note.inst))
            note.voicewidget = tk.Entry(note.fr, width=3)
            note.voicewidget.grid(row=0, column=1, rowspan=2)
            note.voicewidget.insert("end", str(note.voice))
            note.timewidget = tk.Entry(note.fr, width=6)
            note.timewidget.grid(row=0, column=2, rowspan=2)
            note.timewidget.insert("end", str(note.time))
            note.durwidget = tk.Entry(note.fr, width=6)
            note.durwidget.grid(row=0, column=3, rowspan=2)
            note.durwidget.insert("end", str(note.dur))
            note.dbwidget = tk.Entry(note.fr, width=2)
            note.dbwidget.grid(row=0, column=4, rowspan=2)
            note.dbwidget.insert("end", str(note.db))
            note.numwidget = tk.Entry(note.fr, width=4)
            note.numwidget.grid(row=0, column=5)
            note.numwidget.insert("end", str(note.num))
            note.denwidget = tk.Entry(note.fr, width=4)
            note.denwidget.grid(row=1, column=5)
            note.denwidget.insert("end", str(note.den))
            note.regionwidget = tk.Entry(note.fr, width=2)
            note.regionwidget.grid(row=0, column=6, rowspan=2)
            note.regionwidget.insert("end", str(note.region))

            row += 1

class marker(object):
    def __init__(self, parent, name, bar, beat, widget):
        self.myparent = parent
        self.name = name
        self.bar = bar
        self.beat = beat
        self.widget = widget

class hover(object):
    def __init__(self, parent):
        '''This is the surrogate mouse cursor in ADD mode.  It always shows the current region's tonality, as well as the potential note's dynamic, duration, color, voice, and ratio to the current tonality.  If you click, the note that is added will be a copy of this hover.'''
        self.myparent = parent
        self.hnum = 1
        self.hden = 1
        self.hdb = 78
        self.hyoff = self.hdb / 6
        self.hxoff = self.hyoff/2
        self.hinst = 1
        self.hvoice = 0
        self.hinstch = 0
        self.hregion = 0
        self.oldhregion = 0
        self.hoffsetx = 10
        self.hoffsety = -30
        self.entrydur = 2
        self.entrycolor = "#888888"
        self.hdur = self.myparent.xperquarter * abs(self.entrydur)
        self.posx = 120
        self.hovx0 = 120# + self.hoffsetx
        self.hovy0 = 225# + self.hoffsety
        self.hovx1 = 120# + self.hoffsetx
        self.hovy1 = 255# + self.hoffsety
        self.hovx2 = 120 + self.hxoff# + self.hoffsetx
        self.hovy2 = 240# + self.hoffsety
        self.hovx3 = 120# + self.hoffsetx
        self.hovy3 = 225# + self.hoffsety
        self.hcrossx0 = self.hovx0 + 1
        self.hcrossy0 = self.hovy2 - 16
        self.hcrossx1 = self.hovx0 + 1
        self.hcrossy1 = self.hovy2 + 16
        self.hcrossx2 = self.hovx0
        self.hcrossy2 = self.hovy2
        self.hcrossx3 = self.hovx0 + self.hdur
        self.hcrossy3 = self.hovy2
        self.hcrossx4 = self.hovx0
        self.hcrossy4 = self.hovy2
        self.widget = self.myparent.score.create_polygon(self.hovx0,self.hovy0,self.hovx1,self.hovy1,self.hovx2,self.hovy2,self.hovx3,self.hovy3,fill=self.entrycolor, tags=("hover", "all"))
        self.hcross1 = self.myparent.score.create_line(self.hcrossx0,self.hcrossy0,self.hcrossx0,self.hcrossy1,width=2, tags=("hover", "all"))
        self.hcross2 = self.myparent.score.create_line(self.hcrossx0,self.hcrossy2,self.hcrossx3,self.hcrossy3,width=2, tags=("hover", "all"))
        self.hnumdisp = self.myparent.score.create_text(120,240,anchor="se",fill=self.entrycolor,text=str(self.hnum), font=("Helvetica",12), tags=("hover", "all"))
        self.hdendisp = self.myparent.score.create_text(120,240,anchor="ne",fill=self.entrycolor,text=str(self.hden), font=("Helvetica",12), tags=("hover", "all"))
        region = self.hregion
        rnum = self.myparent.regionlist[region].num
        rden = self.myparent.regionlist[region].den
        rcolor = self.myparent.regionlist[region].color
        self.hrnumdisp = self.myparent.score.create_text(125,225,anchor="se",fill=rcolor,text=str(rnum),font=("Times",10), tags=("hover", "all"))
        self.hrdendisp = self.myparent.score.create_text(125,255,anchor="ne",fill=rcolor,text=str(rden),font=("Times",10), tags=("hover", "all"))
        self.hregiondisp = self.myparent.score.create_text(125, 240, anchor="sw", fill=rcolor, text='r ' + str(region), font=("Times",10,"bold"), tags=("hover", "all"))
        self.hvoicedisp = self.myparent.score.create_text(125, 240, anchor="nw", fill=self.entrycolor, text=str(self.hvoice), font=("Times",10), tags=("hover", "all"))

    ### Move the Hover ###
    def hovermotion(self,event):
        '''Called every time the mouse moves over the score in ADD mode.'''
        winfo = (str(self.myparent.scorewin.winfo_name()))
        winfocus = (str(self.myparent.scorewin.focus_get()))
        # conditional based on whether window is active #
        #if (winfocus.endswith(winfo)):
        if winfocus != None and self.myparent.mode.get() == 0:
            canv = event.widget
            x = canv.canvasx(event.x)
            y = canv.canvasy(event.y)
            self.posx = self.myparent.xpxquantize * math.floor((x + self.hoffsetx)/self.myparent.xpxquantize)
            self.hovx0 = self.posx
            self.hovx1 = self.posx
            self.hovx2 = self.posx + self.hxoff
            self.hovx3 = self.posx
            self.hovy0 = (y + self.hoffsety - self.hyoff)
            self.hovy1 = (y + self.hoffsety + self.hyoff)
            self.hovy2 = (y + self.hoffsety + 0)
            self.hovy3 = (y + self.hoffsety - self.hyoff)
            self.myparent.score.coords(self.widget,self.posx,self.hovy0,self.posx,self.hovy1,self.posx+self.hxoff,self.hovy2,self.posx,self.hovy3)
            self.hcrossx0 = self.posx
            self.hcrossy0 = self.hovy2 - 16
            self.hcrossx1 = self.posx
            self.hcrossy1 = self.hovy2 + 16
            self.hcrossx2 = self.posx
            self.hcrossy2 = self.hovy2
            self.hcrossx3 = self.posx + self.hdur
            self.hcrossy3 = self.hovy2
            self.hcrossx4 = self.posx
            self.hcrossy4 = self.hovy2
            self.myparent.score.coords(self.hcross1,self.hovx0,self.hcrossy0,self.hovx0,self.hcrossy1)
            self.myparent.score.coords(self.hcross2,self.hovx0,self.hcrossy2,self.hcrossx3,self.hcrossy3)
            self.yloc = self.myparent.octave11 - self.hovy2
##            self.ynotestorage = int(self.yloc * 240 / self.myparent.octaveres) % self.myparent.octaveres
#            self.ynotestorage = int(240 * (self.yloc % self.myparent.octaveres) / self.myparent.octaveres)
            index = 2**((self.yloc % self.myparent.octaveres) / self.myparent.octaveres)
            distance = 10
            closest = (0, 1, 1)
            for ratio in self.myparent.notebanklist[self.myparent.notebankactive].numdenlist:
#                print "ratio =", float(ratio[1])/ratio[2]
                closeness = (float(ratio[0])/ratio[1]) - index
#                print "closeness:", closeness
                if abs(closeness) <= distance:
                    distance = abs(closeness)
                    closest = ratio
                else:
                    break
##            print 'ynotestorage', self.ynotestorage
##            prenum = self.myparent.notebank[self.ynotestorage][1]
##            preden = self.myparent.notebank[self.ynotestorage][2]
            prenum, preden = closest[0], closest[1]
#            print closest[1], closest[2], prenum, preden
            ### Here's where I fixed the 1/1 vs. 2/1 problem with "="
            if self.yloc >= self.myparent.octaveres:
                prenum *= 2**int((self.yloc)/self.myparent.octaveres)
            elif self.yloc < 0:
                preden *= 2**(0-((int(self.yloc)/self.myparent.octaveres)))
            hratio = self.myparent.ratioreduce(prenum,preden,self.myparent.primelimit)
            self.hnum = hratio[0]
            self.hden = hratio[1]
            self.myparent.statusrat.configure(text='Hover %3d:%d' % hratio)
            self.log1 = math.log(float(self.hnum)/float(self.hden))
            self.logged = self.log1/self.myparent.log2
            self.myparent.yadj = self.myparent.octave11 - (self.logged * self.myparent.octaveres)
            self.myparent.score.coords(self.hnumdisp,self.hovx0-2,self.hovy2)
            self.myparent.score.coords(self.hdendisp,self.hovx0-2,self.hovy2)
            self.myparent.score.itemconfigure(self.hnumdisp,text=str(self.hnum))
            self.myparent.score.itemconfigure(self.hdendisp,text=str(self.hden))
            ry0 = (y + self.hoffsety - 15)
            ry1 = (y + self.hoffsety + 15)
            self.myparent.score.coords(self.hrnumdisp,self.hovx2,ry0)
            self.myparent.score.coords(self.hrdendisp,self.hovx2,ry1)
            self.myparent.score.coords(self.hregiondisp,self.hovx2, self.hovy2)
            self.myparent.score.coords(self.hvoicedisp, self.hovx2, self.hovy2)
            self.myparent.tiedraw(self.hinst, self.hvoice)

    def colorupdate(self, *args):
        try:
            self.entrycolor = str(self.myparent.instlist[self.hinst].color)
            self.myparent.score.itemconfigure(self.widget, fill=self.entrycolor)
            self.myparent.score.itemconfigure(self.widget+3, fill=self.entrycolor)
            self.myparent.score.itemconfigure(self.widget+4, fill=self.entrycolor)
            self.myparent.score.itemconfigure(self.widget+8, fill=self.entrycolor)
        except:
            pass

    def increase(self, event):
        if self.hdb <= 84:
            self.hdb = self.hdb + 6
            self.hyoff = self.hdb / 6
            self.hxoff = self.hyoff/2
            self.hovx2 = self.posx + self.hxoff
            self.hovy0 -= 1
            self.hovy1 += 1
            self.hovy3 -= 1
            self.myparent.score.coords(self.widget,self.posx,self.hovy0,self.posx,self.hovy1,self.posx+self.hxoff,self.hovy2,self.posx,self.hovy3)
            self.hcrossy0 = self.hovy2 - 16
            self.hcrossy1 = self.hovy2 + 16
            self.myparent.score.coords(self.hcross1,self.hovx0,self.hcrossy0,self.hovx0,self.hcrossy1)

    def decrease(self, event):
        if self.hdb >= 6:
            self.hdb = self.hdb - 6
            self.hyoff = self.hdb / 6
            self.hxoff = self.hyoff/2
            self.hovx2 = self.posx + self.hxoff
            self.hovy0 += 1
            self.hovy1 -= 1
            self.hovy3 += 1
            self.myparent.score.coords(self.widget,self.posx,self.hovy0,self.posx,self.hovy1,self.posx+self.hxoff,self.hovy2,self.posx,self.hovy3)
            self.hcrossy0 = self.hovy2 - 16
            self.hcrossy1 = self.hovy2 + 16
            self.myparent.score.coords(self.hcross1,self.hovx0,self.hcrossy0,self.hovx0,self.hcrossy1)


class cursor(object):
    def __init__(self, parent):
        self.myparent = parent
        self.beat = 0
        self.center = 0
        self.widget = self.myparent.score.create_rectangle(-3,self.myparent.miny,3,self.myparent.maxy, fill="#99cccc", outline="#555555", stipple="gray25", tags=("timecursor", "all"))

    def checkautoscroll(self, x):
        realw = self.myparent.score.winfo_width()
        relw = self.myparent.score.canvasx(realw)
        rel0 = self.myparent.score.canvasx(0)
        if relw-x < 40:
            self.myparent.scorexscroll('scroll', '1', "pages")
        elif x-rel0 < 40 and rel0 > 0:
            self.myparent.scorexscroll('scroll', '-1', "pages")
        rel0 = self.myparent.score.canvasx(0)
        if rel0 < -30:
#            print 'rel0', rel0
            self.myparent.scorexscroll('moveto', 0.00242072)

    def scrollabs(self, time):
        pos = float(time) * self.myparent.xperquarter
#        print pos
        self.center = pos
        self.myparent.score.coords("timecursor", pos-3, self.myparent.miny, pos+3, self.myparent.maxy)
#        print 'pos', pos
        self.checkautoscroll(pos)
#        print pos
#        print self.myparent.score.canvasx(pos)
#        print relw, pos

    def scroll(self, time):
        pos = float(time) * self.myparent.xperquarter + self.center
        self.myparent.score.coords("timecursor", pos-3, self.myparent.miny, pos+3, self.myparent.maxy)
        self.center = pos
#        x = self.myparent.score.coords(self.widget)[2] - 3
#        if x - self.myparent.viewwidthtotal > self.myparent.viewwidth:
#            toscroll = x/self.myparent.scrolltotal
#            print toscroll
#            self.myparent.scorexscroll('moveto', toscroll)

    def nextbar(self, event):
        for i in range(int(self.beat), len(self.myparent.barlist)):
            self.beat = int(self.beat + 1)
            if "barline" in self.myparent.score.gettags(self.myparent.barlist[self.beat]):
                oldcoords = self.myparent.score.coords(self.myparent.barlist[self.beat])
                self.center = oldcoords[0]
                self.myparent.score.coords(self.widget, self.center-3, self.myparent.miny, self.center+3, self.myparent.maxy)
                self.checkautoscroll(self.center)
                break

    def previousbar(self, event):
        for i in range(0, int(self.beat)):
            self.beat = int(self.beat - 1)
            if "barline" in self.myparent.score.gettags(self.myparent.barlist[self.beat]):
                oldcoords = self.myparent.score.coords(self.myparent.barlist[self.beat])
                self.center = oldcoords[0]
                self.myparent.score.coords(self.widget, self.center-3, self.myparent.miny, self.center+3, self.myparent.maxy)
                self.checkautoscroll(self.center)
                break

    def nextbeat(self, event):
        if self.beat < len(self.myparent.barlist)-1:
            self.beat = int(self.beat + 1)
            oldcoords = self.myparent.score.coords(self.myparent.barlist[self.beat])
            self.center = oldcoords[0]
            self.myparent.score.coords(self.widget, self.center-3, self.myparent.miny, self.center+3, self.myparent.maxy)
            self.checkautoscroll(self.center)

    def previousbeat(self, event):
        if self.beat > 0:
            self.beat = int(self.beat - 1)
            oldcoords = self.myparent.score.coords(self.myparent.barlist[self.beat])
            self.center = oldcoords[0]
            self.myparent.score.coords(self.widget, self.center-3, self.myparent.miny, self.center+3, self.myparent.maxy)
            self.checkautoscroll(self.center)

    def home(self, *args):
        self.beat = 0
        self.center = 0
        self.myparent.score.coords(self.widget, -3, self.myparent.miny, 3, self.myparent.maxy)
        self.myparent.scorexscroll("moveto", 0.00242072)

    def end(self, event):
        if len(self.myparent.notelist):
            self.myparent.scsort()
            loc = (self.myparent.notelist[-1].time + abs(self.myparent.notelist[-1].dur)) * self.myparent.xperquarter
            for bar in self.myparent.barlist:
                if self.myparent.score.coords(bar)[0] >= loc:
                    self.beat = self.myparent.barlist.index(bar)
                    self.center = self.myparent.score.coords(bar)[0]
                    break
#            self.center = self.beat * self.myparent.xperquarter
            self.myparent.score.coords(self.widget, self.center-3, self.myparent.miny, self.center+3, self.myparent.maxy)
            while self.center > self.myparent.score.canvasx(self.myparent.score.winfo_reqwidth()):
                self.myparent.scorexscroll('scroll', '1', 'pages')

class selectbox(object):
    def __init__(self, parent, event):
#        print "init"
        self.myparent = parent
        self.selected = []
        self.deselected = []
        x = self.myparent.score.canvasx(event.x)
        y = self.myparent.score.canvasy(event.y)
        self.corners = (x, y, x, y)
        self.widget = self.myparent.score.create_rectangle(self.corners, outline="#888888", tags="selectbox")
        selectall = self.myparent.score.find_overlapping(self.corners[0], self.corners[1], self.corners[2], self.corners[3])
        for nw in self.myparent.notewidgetlist:
            if nw.notewidget in selectall:
                if self.myparent.ctlkey == 0 and not nw.note.sel:
#                    nw.note.sel = 1
                    if nw not in self.selected:
                        self.selected.append(nw)
#                    if nw in self.deselected:
#                        self.deselected.remove(nw)
#                        print 'remove 1'
                    self.myparent.score.itemconfig(nw.notewidget, outline="#ff6670", width=3)
                    self.myparent.score.addtag_withtag("selected", nw.notewidget)
                elif self.myparent.ctlkey == 1:
                    # deselect if ctl-clicked
#                    nw.note.sel = 0
                    if nw in self.selected:
                        self.selected.remove(nw)
                    if nw not in self.deselected:
                        self.deselected.append(nw)
                    outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                    self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                    self.myparent.score.dtag(nw.notewidget, "selected")
            elif self.myparent.shiftkey == self.myparent.ctlkey == 0:
                # not clicked, no mods
#                nw.note.sel = 0
                if nw.note.sel == 1:# and nw not in self.deselected:
                    self.deselected.append(nw)
#                if nw in self.selected:
#                    self.selected.remove(nw)
#                nw.note.sel = 0
                    outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                    self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                    self.myparent.score.dtag(nw.notewidget, "selected")
#                print nw.note.sel, self.myparent.score.itemcget(nw.notewidget, "outline")

    def adjust(self, event):
#        print "self.deselected", self.deselected
#        print "adjust"
        x = self.myparent.score.canvasx(event.x)
        y = self.myparent.score.canvasy(event.y)
        self.corners = (self.corners[0], self.corners[1], x, y)
        self.myparent.score.coords(self.widget, self.corners)
        selectall = self.myparent.score.find_overlapping(self.corners[0], self.corners[1], self.corners[2], self.corners[3])
#        print 'selectall:', selectall
#        print 'nwlist:', [nw.notewidget for nw in self.myparent.notewidgetlist]
        for nw in self.myparent.notewidgetlist:
#            print 'nw:', nw.notewidget
#            note = notewidget.note
            if nw.notewidget in selectall:
#                print nw.notewidget, 'in selectall'
                if self.myparent.ctlkey == 0:
#                    print 'in selectall:', nw.note.num, nw.note.den
                    if nw not in self.selected:
                        self.selected.append(nw)
                        self.myparent.score.itemconfig(nw.notewidget, outline="#ff6670", width=3)
                        self.myparent.score.addtag_withtag("selected", nw.notewidget)
                    if nw in self.deselected:
#                        ######
                        self.deselected.remove(nw)
                else:
                    if nw in self.selected:
                        self.selected.remove(nw)
                        outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                        self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                        self.myparent.score.dtag(nw.notewidget, "selected")
                    if nw not in self.deselected:
                        self.deselected.append(nw)
                        outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                        self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                        self.myparent.score.dtag(nw.notewidget, "selected")
            else:
                ###BROKEN SELECT
                # note outside selection box
                if self.myparent.ctlkey == 1:
                    if nw in self.deselected:
                        self.deselected.remove(nw)
#                    print 'remove 3'
                        if nw.note.sel:
                            # restore selected note when ctl-dragging back
                            self.myparent.score.itemconfig(nw.notewidget, outline="#ff6670", width=3)
                            self.myparent.score.addtag_withtag("selected", nw.notewidget)
                elif self.myparent.shiftkey == 1:
                    if not nw.note.sel:
                        outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                        self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                        self.myparent.score.dtag(nw.notewidget, "selected")
                    if nw in self.selected:
                        self.selected.remove(nw)
                else:
                    ## note outside box, old selection discarded
                    outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                    self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                    self.myparent.score.dtag(nw.notewidget, "selected")
                    if nw in self.selected:
                        self.selected.remove(nw)

    def lift(self, event):
        flag = 0
        for nw in self.selected:
            if nw.note.sel == 0:
                flag = 1
        for nw in self.deselected:
            if nw.note.sel == 1:
                flag = 1
        if flag == 0: return
        com = comselect(self.myparent, [nw.note.id for nw in self.selected], [nw.note.id for nw in self.deselected])
        com.do()
#        if self.myparent.dispatcher.push(com):
#            self.myparent.dispatcher.do()

class pastedialog(tk.Toplevel):
    ## bar beat tick
    ## times
    ## quarters
    def __init__(self, parent, *args):
        tk.Toplevel.__init__(self, parent.myparent)
        self.myparent = parent
        self.title("Paste Notes")
        if sys.platform.count("win32"):
            try: self.iconbitmap('img/rat32.ico')
            except: pass
#        for note in self.myparent.clipboard:
#            print note.time
        self.bar = 0
        self.beat = 0
        for ind, beatline in enumerate(self.myparent.barlist):
            beatlinex = self.myparent.score.coords(beatline)[0]
            if beatlinex <= self.myparent.cursor.center and "barline" in self.myparent.score.gettags(beatline):
                self.bar += 1
                self.beat = self.myparent.cursor.beat - ind
#        print self.bar, self.beat
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
#        self.columnconfigure(1, weight=1)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        self.top = tk.Frame(self, bd=1, relief="raised")
        self.top.grid(row=0, column=0, sticky='we')
        self.middle = tk.Frame(self, bd=1, relief="raised")
        self.middle.grid(row=1, column=0, sticky='we')
        self.bottom = tk.Frame(self, bd=1, relief="raised")
        self.bottom.grid(row=2, column=0, sticky='we')
        self.buttons = tk.Frame(self, width=300, height=80, borderwidth=1, relief="raised")
        tk.Button(self.buttons, text="OK", command=self.ok).grid(row=0, column=0, padx=10)
        tk.Button(self.buttons, text="Cancel", command=self.cancel).grid(row=0, column=1, padx=10)
        tk.Button(self.buttons, text="Apply", command=self.apply).grid(row=0, column=2, padx=10)
        self.buttons.grid(row=4, column=0, sticky='s', ipady=20)
        tk.Label(self.top, text="Bar").grid(row=0, column=0)
        tk.Label(self.top, text="Beat").grid(row=0, column=1)
        tk.Label(self.top, text="Tick (1/120 Quarter)").grid(row=0, column=2)
        self.barvar = tk.IntVar(value=self.bar)
        self.barfield = tk.Spinbox(self.top, width=5, textvariable=self.barvar, from_=0, to=100000)
        self.barfield.grid(row=1, column=0, sticky='')
        self.beatvar = tk.IntVar(value=self.beat)
        self.beatfield = tk.Spinbox(self.top, width=5, textvariable=self.beatvar, from_=0, to=40, wrap=1)
        self.beatfield.grid(row=1, column=1, sticky='')
        self.tickvar = tk.IntVar(value=0)
        self.tickfield = tk.Spinbox(self.top, width=5, textvariable=self.tickvar, from_=0, to=119, wrap=1)
        self.tickfield.grid(row=1, column=2, sticky='')
        tk.Label(self.middle, text="Number of Repetitions").grid(row=0, column=0)
        self.timesvar = tk.IntVar(value=1)
        self.timesfield = tk.Spinbox(self.middle, width=5, textvariable=self.timesvar, from_=1, to=100, wrap=1)
        self.timesfield.grid(row=1, column=0, sticky='')
#        tk.Label(self.bottom, text="Gap Between Repetitions:").grid(row=0, column=0, columnspan=3)
        tk.Label(self.bottom, text="Gap Between Repetitions:").grid(row=0, column=0, columnspan=2)
#        tk.Label(self.bottom, text="Bars").grid(row=1, column=0)
        tk.Label(self.bottom, text="Quarter Notes").grid(row=1, column=0)
#        tk.Label(self.bottom, text="Beats").grid(row=1, column=1)
        self.gapbeatvar = tk.IntVar(value=0)
        self.gapbeatfield = tk.Spinbox(self.bottom, width=5, textvariable=self.gapbeatvar, from_=0, to=40, wrap=1)
#        self.gapbeatfield.grid(row=2, column=1, sticky='w')
        self.gapbeatfield.grid(row=2, column=0, sticky='')
#        tk.Label(self.bottom, text="Ticks").grid(row=1, column=2)
        tk.Label(self.bottom, text="Ticks").grid(row=1, column=1)
        self.gaptickvar = tk.IntVar(value=0)
        self.gaptickfield = tk.Spinbox(self.bottom, width=5, textvariable=self.gaptickvar, from_=0, to=40, wrap=1)
#        self.gaptickfield.grid(row=2, column=2, sticky='w')
        self.gaptickfield.grid(row=2, column=1, sticky='')
        self.lift()
        self.focus_set()

    def ok(self, *args):
        self.apply()
        self.cancel()

    def apply(self):
        '''Here's the hard part.'''
        self.myparent.menumode.invoke(1)
        bar = self.barvar.get()
        beat = self.beatvar.get()
        tick = self.tickvar.get()
        barcount = 1
        beatcount = 1
        pastex = 0
        for beatline in self.myparent.barlist:
            if "barline" in self.myparent.score.gettags(beatline) and barcount <= bar:
                pastex = self.myparent.score.coords(beatline)[0]
                barcount += 1
            elif barcount > bar and beatcount <= beat:
                pastex = self.myparent.score.coords(beatline)[0]
                beatcount += 1
        pastebeat = pastex/self.myparent.xperquarter + tick/120.0
        noteinfo = []
        for rep in range(self.timesvar.get()):
            for orig in self.myparent.clipboard:
                noteinstance = (self.myparent.noteid, orig.inst, orig.voice, orig.time+pastebeat, orig.dur, orig.db, orig.num, orig.den, orig.region, orig.sel)
                self.myparent.noteid += 1
                noteinfo.append(noteinstance)
#                self.myparent.notelist.append(noteinstance)
#                nw = notewidgetclass(self.myparent, noteinstance)
#                self.myparent.notewidgetlist.append(nw)
#                if not self.myparent.unsaved: self.myparent.unsaved = True
            pastebeat += (self.gapbeatvar.get() + (self.gaptickvar.get()/120.0))
        com = comaddnotes(self.myparent, noteinfo, paste=True)
        if self.myparent.dispatcher.push(com):
            self.myparent.dispatcher.do()
        self.myparent.scsort()

    def cancel(self, *args):
        self.myparent.vkey = self.myparent.ctlkey = 0
        self.destroy()

class arbdialog(tk.Toplevel):
    def __init__(self, parent, note):
        tk.Toplevel.__init__(self)
#        self.geometry("160x50+400+300")
        self.myparent = parent
        self.mynote = note
        if sys.platform.count("win32"):
            try: self.iconbitmap('img/rat32.ico')
            except: pass
        self.string = tk.StringVar()
        self.string.set('')
#        print self.mynote.arb
        for pf in self.mynote.arb:
            if self.string.get():
                temp = self.string.get()
                self.string.set('%s %s' % (temp, pf))
            else:
                self.string.set(str(pf))
#        print self.mynote.arb
        self.arbdisp = tk.Entry(self, textvariable=self.string)
        self.okbutton = tk.Button(self, text="OK", command=self.ok)
        self.cancelbutton = tk.Button(self, text="Cancel", command=self.cancel)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        self.arbdisp.bind("<Return>", self.ok)
        self.arbdisp.bind("<Escape>", self.cancel)
        self.arbdisp.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.okbutton.grid(row=1, column=0)
        self.cancelbutton.grid(row=1, column=1)
        self.lift()
        self.focus_set()

    def ok(self, *args):
#        print "OKAY"
        self.apply()
        self.cancel()

    def cancel(self, *args):
#        print "CANCEL"
        self.myparent.poppedup = False
	self.altkey = 0
        self.destroy()

    def apply(self):
        com = comarbchange(self.myparent, self.mynote.id, self.string.get())
        if self.dispatcher.push(com):
            self.dispatcher.do()
#        if not self.myparent.unsaved: self.myparent.unsaved = True
        self.myparent.poppedup = False
	self.altkey = 0

class dispatcher(object):
    def __init__(self, parent):
        self.myparent = parent
        self.comlist = []
        self.comind = -1

    def push(self, com):
#        flag = False
#        if not self.comlist:
#            flag = True
#        else:
#            if self.comlist[self.comind].__class__.__name__ != com.__class__.__name__:
#                flag = True
#            else:
#                for key in self.comlist[self.comind].__dict__.keys():
#                    if not key=='durdict' and self.comlist[self.comind].__dict__[key] != com.__dict__[key]:
#                        flag = True
        flag = True
        if flag:
            if self.comlist:
                self.comlist = self.comlist[:self.comind+1]
            if self.myparent.unsaved < 0:
                self.myparent.unsaved = len(self.comlist) + 1
            self.comlist.append(com)
        return flag


    def do(self):
#        com.do()
#        print "dispatcher do", self.comind
        if self.comind+1 < len(self.comlist):
            self.comind += 1
            self.comlist[self.comind].do()
            self.myparent.menuedit.entryconfig(0, label='Undo %s' % self.comlist[self.comind].string, state="normal")
            if self.comind+1 < len(self.comlist):
                self.myparent.menuedit.entryconfig(1, label='Redo %s' % self.comlist[self.comind+1].string, state="normal")
            else:
                self.myparent.menuedit.entryconfig(1, label="Can't Redo", state="disabled")
            self.myparent.unsaved += 1
            self.myparent.titleset()

    def undo(self):
#        print "dispatcher undo", self.comind
        if self.comind >= 0:
            self.comlist[self.comind].undo()
            self.myparent.menuedit.entryconfig(1, label='Redo %s' % self.comlist[self.comind].string, state="normal")
            self.comind -= 1
            if self.comind >= 0:
                self.myparent.menuedit.entryconfig(0, label='Undo %s' % self.comlist[self.comind].string, state="normal")
            else:
                self.myparent.menuedit.entryconfig(0, label="Can't Undo", state="disabled")
            self.myparent.unsaved -= 1
            self.myparent.titleset()

    def increment(self, com, *args):
        if self.comlist[-1].__class__.__name__ == com:
            self.comlist[-1].increment(args)

##      COMMAND CLASSES         ##
class comaddnotes(object):
#    def __init__(self, parent, id, inst, voice, time, dur, db, num, den, region, sel):
    def __init__(self, parent, noteinfo, paste=False):
        self.myparent = parent
        self.noteinfo = noteinfo
#        self.id = id
#        self.inst = inst
#        self.voice = voice
#        self.time = time
#        self.dur = dur
#        self.db = db
#        self.num = num
#        self.den = den
#        self.region = region
#        self.sel = sel
        if paste:
            self.string = "Paste Notes"
        else:
            self.string = "Add Note"

    def do(self):
        listtodraw = []
        for ni in self.noteinfo:
            id = ni[0]
            inst = ni[1]
            voice = ni[2]
            time = ni[3]
            dur = ni[4]
            db = ni[5]
            num = ni[6]
            den = ni[7]
            region = ni[8]
            sel = ni[9]
            noteinstance = note(self.myparent, id, inst, voice, time, dur, db, num, den, region, sel)
            self.myparent.notelist.append(noteinstance)
            notewidgetinstance = notewidgetclass(self.myparent, noteinstance)
            self.myparent.notewidgetlist.append(notewidgetinstance)
            if voice and (inst, voice) not in listtodraw:
                listtodraw.append((inst, voice))
            self.noteinfo[self.noteinfo.index(ni)] = id
        for iv in listtodraw:
            self.myparent.tiedraw(iv[0], iv[1])

    def undo(self):
        listtodraw = []
        listtoremove = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteinfo:
                self.noteinfo[self.noteinfo.index(nw.note.id)] = (nw.note.id, nw.note.inst, nw.note.voice, nw.note.time, nw.note.dur, nw.note.db, nw.note.num, nw.note.den, nw.note.region, nw.note.sel)
                inst, voice = nw.note.inst, nw.note.voice
                nw.undraw()
                if nw not in listtoremove:
                    listtoremove.append(nw)
                if (inst, voice) not in listtodraw:
                    listtodraw.append((inst, voice))
#                if not self.myparent.unsaved: self.myparent.unsaved = True
        for nw in listtoremove:
            self.myparent.notelist.remove(nw.note)
            self.myparent.notewidgetlist.remove(nw)
            del nw.note
            del nw
        for iv in listtodraw:
            self.myparent.tiedraw(iv[0], iv[1])

        
class comdeletenotes(object):
    def __init__(self, parent, noteids):
        self.myparent = parent
        self.noteids = noteids
        self.deleted = []
        self.string = "Delete Notes"

    def do(self):
        instvoicelist = []
#        for id in self.noteids:
        nws = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
#                    break
                self.deleted.append(nw.note)
                nws.append(nw)
                inst = nw.note.inst
                voice = nw.note.voice
                if (inst, voice) not in instvoicelist:
                    instvoicelist.append((inst, voice))
        for nw in nws:
            nw.undraw()
            self.myparent.notelist.remove(nw.note)
            self.myparent.notewidgetlist.remove(nw)
#            del nw.note
            del nw
#            self.tiedraw(inst, voice)
        self.noteids = []   
        for iv in instvoicelist:
            self.myparent.tiedraw(iv[0], iv[1])

#        if not self.myparent.unsaved: self.myparent.unsaved = True

    def undo(self):
        self.noteids = []
        instvoicelist = []
        for note in self.deleted:
            nw = notewidgetclass(self.myparent, note)
            self.myparent.notelist.append(note)
            self.myparent.notewidgetlist.append(nw)
            self.noteids.append(nw.note.id)
            if (note.inst, note.voice) not in instvoicelist:
                instvoicelist.append((note.inst, note.voice))
        self.deleted = []
        for iv in instvoicelist:
            self.myparent.tiedraw(iv[0], iv[1])

#        if not self.myparent.unsaved: self.myparent.unsaved = True

class comselect(object):
    def __init__(self, parent, selids, deselids):
        self.myparent = parent
        self.selids = selids
        self.deselids = deselids
        self.string = "Change Selection"

    def do(self):
        if self.myparent.mode.get() != 1:
            self.myparent.mode.set(1)
            self.myparent.modeannounce()
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.selids:
                nw.note.sel = 1
                self.myparent.score.itemconfig(nw.notewidget, outline="#ff6670", width=3)
                self.myparent.score.addtag_withtag("selected", nw.notewidget)
            elif nw.note.id in self.deselids:
                nw.note.sel = 0
                outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                self.myparent.score.dtag(nw.notewidget, "selected")

    def undo(self):
        if self.myparent.mode.get() != 1:
            self.myparent.mode.set(1)
            self.myparent.modeannounce()
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.deselids:
                nw.note.sel = 1
                self.myparent.score.itemconfig(nw.notewidget, outline="#ff6670", width=3)
                self.myparent.score.addtag_withtag("selected", nw.notewidget)
            elif nw.note.id in self.selids:
                nw.note.sel = 0
                outline = self.myparent.score.itemcget(nw.notewidget, "fill")
                self.myparent.score.itemconfig(nw.notewidget, width=1, outline=outline)
                self.myparent.score.dtag(nw.notewidget, "selected")

class comeditnumden(object):
    def __init__(self, parent, noteids, numdelta, dendelta):
        self.myparent = parent
        self.noteids = noteids
        self.numdelta = numdelta
        self.dendelta = dendelta
        self.string = "Drag Notes Vertically"

    def do(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                ratio = self.myparent.ratioreduce(nw.note.num*self.numdelta, nw.note.den*self.dendelta, self.myparent.primelimit)
                nw.note.updatenum(ratio[0])
                nw.note.updateden(ratio[1])
                self.myparent.score.itemconfig(nw.numwidget, text=str(nw.note.num))
                self.myparent.score.itemconfig(nw.denwidget, text=str(nw.note.den))
                nw.updateheight()
                self.myparent.tiedraw(nw.note.inst, nw.note.voice)

    def undo(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                ratio = self.myparent.ratioreduce(nw.note.num*self.dendelta, nw.note.den*self.numdelta, self.myparent.primelimit)
                nw.note.updatenum(ratio[0])
                nw.note.updateden(ratio[1])
                self.myparent.score.itemconfig(nw.numwidget, text=str(nw.note.num))
                self.myparent.score.itemconfig(nw.denwidget, text=str(nw.note.den))
                nw.updateheight()
                self.myparent.tiedraw(nw.note.inst, nw.note.voice)

    def increment(self, args):
        num, den = args[0], args[1]
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                ratio = self.myparent.ratioreduce(nw.note.num*num, nw.note.den*den, self.myparent.primelimit)
                nw.note.updatenum(ratio[0])
                nw.note.updateden(ratio[1])
                self.myparent.score.itemconfig(nw.numwidget, text=str(nw.note.num))
                self.myparent.score.itemconfig(nw.denwidget, text=str(nw.note.den))
                nw.updateheight()
                self.myparent.tiedraw(nw.note.inst, nw.note.voice)
        ratio = self.myparent.ratioreduce(num*self.numdelta, den*self.dendelta, self.myparent.primelimit)
        self.numdelta = ratio[0]
        self.dendelta = ratio[1]

class comedittime(object):
    def __init__(self, parent, noteids, timedelta):
        self.myparent = parent
        self.noteids = noteids
        self.timedelta = timedelta
        self.string = "Drag Notes Horizontally"

    def do(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
#                            print nw.note.inst
                nw.purex += self.timedelta
                nw.note.updatetime(nw.purex/self.myparent.xperquarter)
                nw.updatetime()
                self.myparent.tiedraw(nw.note.inst, nw.note.voice)

    def undo(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
#                            print nw.note.inst
                nw.purex -= self.timedelta
                nw.note.updatetime(nw.purex/self.myparent.xperquarter)
                nw.updatetime()
                self.myparent.tiedraw(nw.note.inst, nw.note.voice)

    def increment(self, args):
        time = float(args[0])
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
#                            print nw.note.inst
                nw.purex += time
                nw.note.updatetime(nw.purex/self.myparent.xperquarter)
                nw.updatetime()
                self.myparent.tiedraw(nw.note.inst, nw.note.voice)
        self.timedelta += time

class comtonchange(object):
    def __init__(self, parent, region, num, den, octave11, yadj):
        self.myparent = parent
        self.region = region
        self.num = num
        self.den = den
        self.octave11 = octave11
        self.yadj = yadj
        self.string = "Change Tonal Center"

    def do(self):
        curnum = self.myparent.regionlist[self.region].num * self.num
        curden = self.myparent.regionlist[self.region].den * self.den
        curratio = self.myparent.ratioreduce(curnum, curden, self.myparent.primelimit)
        self.myparent.regionlist[self.region].num = curratio[0]
        self.myparent.regionlist[self.region].den = curratio[1]
        self.myparent.statusregion.configure(text='Region %d = %d:%d' % (self.region, self.myparent.regionlist[self.region].num, self.myparent.regionlist[self.region].den))
        if self.region == self.myparent.hover.hregion:
            self.myparent.drawoctaves(self.yadj)
            self.myparent.octave11 = self.yadj
            self.myparent.curnum = curratio[0]
            self.myparent.curden = curratio[1]
        # this next assignment has to be after the call to drawoctaves because that function compares yadj and octave11 to move the lines #
        # and at the time that I did this part I didn't know what I was doing... not like now #
        self.myparent.regionlist[self.region].octave11 = self.yadj
        for nw in self.myparent.notewidgetlist:
            if nw.note.region == self.region:
                num = nw.note.num * self.den
                den = nw.note.den * self.num
                ratio = self.myparent.ratioreduce(num, den, self.myparent.primelimit)
                nw.note.updatenum(ratio[0])
                nw.note.updateden(ratio[1])
                nw.updateregion()
        if self.region == self.myparent.hover.hregion:
            self.myparent.score.itemconfigure(self.myparent.hover.hrnumdisp, text=str(self.myparent.curnum))
            self.myparent.score.itemconfigure(self.myparent.hover.hrdendisp, text=str(self.myparent.curden))
            hnum = self.myparent.hover.hnum * self.den
            hden = self.myparent.hover.hden * self.num
            hratio = self.myparent.ratioreduce(hnum, hden, self.myparent.primelimit)
            self.myparent.hover.hnum = hratio[0]
            self.myparent.hover.hden = hratio[1]
            self.myparent.statusrat.configure(text='Hover %3d:%d' % (hratio[0], hratio[1]))
            self.myparent.score.itemconfigure(self.myparent.hover.hnumdisp, text=str(self.myparent.hover.hnum))
            self.myparent.score.itemconfigure(self.myparent.hover.hdendisp, text=str(self.myparent.hover.hden))
            self.myparent.hover.log1 = math.log(float(self.myparent.hover.hnum)/float(self.myparent.hover.hden))
            self.myparent.hover.logged = self.myparent.hover.log1/self.myparent.log2
            self.myparent.yadj = self.myparent.octave11 - (self.myparent.hover.logged * self.myparent.octaveres)
#        self.myparent.write('New Tonality: %d/%d' % (self.myparent.curnum,self.myparent.curden))
        self.myparent.textsize = 24
        rtext = 'Region "%d" x %d/%d%s= %d/%d' % (self.region, self.num, self.den, os.linesep, self.myparent.regionlist[self.region].num, self.myparent.regionlist[self.region].den)
        self.myparent.write(rtext)

    def undo(self):
        curnum = self.myparent.regionlist[self.region].num * self.den
        curden = self.myparent.regionlist[self.region].den * self.num
        curratio = self.myparent.ratioreduce(curnum, curden, self.myparent.primelimit)
        self.myparent.regionlist[self.region].num = curratio[0]
        self.myparent.regionlist[self.region].den = curratio[1]
        self.myparent.statusregion.configure(text='Region %d = %d:%d' % (self.region, self.myparent.regionlist[self.region].num, self.myparent.regionlist[self.region].den))
        if self.region == self.myparent.hover.hregion:
            self.myparent.drawoctaves(self.octave11)
            self.myparent.octave11 = self.octave11
            self.myparent.curnum = curratio[0]
            self.myparent.curden = curratio[1]
        # this next assignment has to be after the call to drawoctaves because that function compares yadj and octave11 to move the lines #
        # and at the time that I did this part I didn't know what I was doing... not like now #
        self.myparent.regionlist[self.region].octave11 = self.octave11
        for nw in self.myparent.notewidgetlist:
            if nw.note.region == self.region:
                num = nw.note.num * self.num
                den = nw.note.den * self.den
                ratio = self.myparent.ratioreduce(num, den, self.myparent.primelimit)
                nw.note.updatenum(ratio[0])
                nw.note.updateden(ratio[1])
                nw.updateregion()
        if self.region == self.myparent.hover.hregion:
            self.myparent.score.itemconfigure(self.myparent.hover.hrnumdisp, text=str(self.myparent.curnum))
            self.myparent.score.itemconfigure(self.myparent.hover.hrdendisp, text=str(self.myparent.curden))
            hnum = self.myparent.hover.hnum * self.num
            hden = self.myparent.hover.hden * self.den
            hratio = self.myparent.ratioreduce(hnum, hden, self.myparent.primelimit)
            self.myparent.hover.hnum = hratio[0]
            self.myparent.hover.hden = hratio[1]
            self.myparent.statusrat.configure(text='Hover %3d:%d' % (hratio[0], hratio[1]))
            self.myparent.score.itemconfigure(self.myparent.hover.hnumdisp, text=str(self.myparent.hover.hnum))
            self.myparent.score.itemconfigure(self.myparent.hover.hdendisp, text=str(self.myparent.hover.hden))
            self.myparent.hover.log1 = math.log(float(self.myparent.hover.hnum)/float(self.myparent.hover.hden))
            self.myparent.hover.logged = self.myparent.hover.log1/self.myparent.log2
            self.myparent.yadj = self.myparent.octave11 - (self.myparent.hover.logged * self.myparent.octaveres)
#        self.myparent.write('New Tonality: %d/%d' % (self.myparent.curnum,self.myparent.curden))
        self.myparent.textsize = 24
        rtext = 'Region "%d" x %d/%d%s= %d/%d' % (self.region, self.den, self.num, os.linesep, self.myparent.regionlist[self.region].num, self.myparent.regionlist[self.region].den)
        self.myparent.write(rtext)

class comregionnew(object):
    def __init__(self, parent, num, den, color, octave11):
        self.myparent = parent
#        self.region = region
        self.num = num
        self.den = den
        self.color = color
        self.octave11 = octave11
        self.string = "New Region"

    def do(self):
        newregion = rdialog.region(self.myparent, self.num, self.den, self.color, self.octave11)
        self.myparent.regionlist.append(newregion)

    def undo(self):
        if self.myparent.hover.hregion >= len(self.myparent.regionlist)-1:
            self.myparent.hover.hregion = len(self.myparent.regionlist)-2
            self.myparent.regionchange()
        self.myparent.regionlist.pop()

class cominstnew(object):
    def __init__(self, parent, instch):
        self.myparent = parent
        self.instch = instch
        self.string = "New Instrument"

    def do(self):
        self.myparent.write('New Instrument: %d' % self.instch)
        newinst = odialog.instrument(self, self.instch, '#999999')
        self.myparent.instlist.append(newinst)
        self.myparent.menuview.add_command(label='Hide i%d' % self.instch, command=lambda arg1=self.instch: self.myparent.hidethis(arg1), accelerator='%s-%d' % (self.myparent.altacc, self.instch))
        try:
###
#                        print "out dialog?"
#                        self.myparent.out.instmaybe = copy.deepcopy(self.myparent.instlist)
            self.myparent.out.instmaybe.append(newinst)
            newinstpage = odialog.instrumentpage(self.myparent.out, newinst)
            self.myparent.out.instpagelist.append(newinstpage)
#                            print "yup"
        except:
#                        print "no out dialog"
            pass

    def undo(self):
        if self.myparent.hover.hinst >= len(self.myparent.instlist)-1:
            self.myparent.tiedraw(self.myparent.hover.hinst, self.myparent.hover.hvoice)
            self.myparent.hover.hinst = len(self.myparent.instlist)-2
            self.myparent.statusinst.configure(text='Inst %d' % self.myparent.hover.hinst)
            self.myparent.write(str(self.myparent.hover.hinst))
            self.myparent.hover.colorupdate(self.myparent)
        self.myparent.instlist.pop()
        ## remove instpage from odialog??

class comarbchange(object):
    def __init__(self, parent, noteid, arbfields):
        self.myparent = parent
        self.noteid = noteid
        self.arbfields = arbfields
        self.string = "Arb Field Change"

    def do(self):
        current = ''
        for note in self.myparent.notelist:
            if note.id == self.noteid:
                for ind in range(1, 10000):
                    if 'a%d' % ind in note.dict:
#                        current += ' a%d' % ind
                        current += str(note.dict['a%d' % ind])
                        current += ' '
                        del note.dict['a%d' % ind]
                    else: break
                break
        for num, field in enumerate(self.arbfields.split()):
            note.dict['a%d' % (num+1)] = field
        note.arb = tuple(self.arbfields.split())
        self.arbfields = current.strip()

    def undo(self):
        self.do()

class comeditdb(object):
    def __init__(self, parent, noteids, dbdelta):
        self.myparent = parent
        self.noteids = noteids
        self.dbdelta = dbdelta
        self.string = "Edit Db"

    def do(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                if 0 <= nw.note.db + self.dbdelta <= 90:
                    nw.note.updatedb(nw.note.db + self.dbdelta)
                    nw.updatedb()
                else:
                    self.noteids.remove(nw.note.id)

    def undo(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                if 0 <= nw.note.db - self.dbdelta <= 90:
                    nw.note.updatedb(nw.note.db - self.dbdelta)
                    nw.updatedb()

class comeditconnect(object):
    def __init__(self, parent, noteids, conn):
        self.myparent = parent
        self.noteids = noteids
        self.conn = conn
        self.string = "Edit Connection"

    def do(self):
        listtodraw = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                ## negative self.conn means connect!
                if nw.note.dur == self.conn * abs(nw.note.dur):
                    self.noteids.remove(nw.note.id)
                else:
                    nw.note.updatedur(self.conn * abs(nw.note.dur))
                    if not (nw.note.inst, nw.note.voice) in listtodraw:
                        listtodraw.append((nw.note.inst, nw.note.voice))
        for pair in listtodraw:
            self.myparent.tiedraw(pair[0], pair[1])

    def undo(self):
        listtodraw = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                ## negative self.conn means connect!
                nw.note.updatedur(-self.conn * abs(nw.note.dur))
                if not (nw.note.inst, nw.note.voice) in listtodraw:
                    listtodraw.append((nw.note.inst, nw.note.voice))
        for pair in listtodraw:
            self.myparent.tiedraw(pair[0], pair[1])

class comeditinst(object):
    def __init__(self, parent, noteids, inst):
        self.myparent = parent
        self.noteids = noteids
        self.inst = inst
        for note in self.myparent.notelist:
            if note.id in self.noteids and note.inst == self.inst:
                self.noteids.remove(note.id)
        self.oldinst = {}
        self.string = "Edit Inst Number"

    def do(self):
        listtodraw = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                inst = nw.note.inst
                voice = nw.note.voice
                if (inst, voice) not in listtodraw:
                    listtodraw.append((inst, voice))
                if (self.inst, voice) not in listtodraw:
                    listtodraw.append((self.inst, voice))
                self.oldinst['n%d' % nw.note.id] = inst
                nw.note.updateinst(self.inst)
                nw.updateinst()
                if self.inst in self.myparent.hidden:
                    nw.undraw()
        for iv in listtodraw:
            self.myparent.tiedraw(iv[0], iv[1])

    def undo(self):
        listtodraw = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                inst = self.oldinst['n%d' % nw.note.id]
                voice = nw.note.voice
                if (inst, voice) not in listtodraw:
                    listtodraw.append((inst, voice))
                if (self.inst, voice) not in listtodraw:
                    listtodraw.append((self.inst, voice))
                nw.note.updateinst(inst)
                nw.updateinst()
                if inst in self.myparent.hidden:
                    nw.undraw()
        for iv in listtodraw:
            self.myparent.tiedraw(iv[0], iv[1])
        self.oldinst = {}

class comeditregion(object):
    def __init__(self, parent, noteids, region):
        self.myparent = parent
        self.noteids = noteids
        self.region = region
        for note in self.myparent.notelist:
            if note.id in self.noteids and note.region == self.region:
                self.noteids.remove(note.id)
        self.oldregion = {}
        self.string = "Edit Region Number"

    def do(self):
        color = self.myparent.regionlist[self.region].color
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                oldrnum = self.myparent.regionlist[nw.note.region].num
                oldrden = self.myparent.regionlist[nw.note.region].den
                self.oldregion['n%d' % nw.note.id] = nw.note.region
                nw.note.updateregion(self.region)
                rnum = self.myparent.regionlist[self.region].num
                rden = self.myparent.regionlist[self.region].den
                ratio = self.myparent.ratioreduce(nw.note.num * oldrnum * rden, nw.note.den * oldrden * rnum, self.myparent.primelimit)
                nw.note.updatenum(ratio[0])
                nw.note.updateden(ratio[1])
                nw.updateregion()

    def undo(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                newr = self.oldregion['n%d' % nw.note.id]
                newrnum = self.myparent.regionlist[newr].num
                newrden = self.myparent.regionlist[newr].den
                color = self.myparent.regionlist[newr].color
                rnum = self.myparent.regionlist[self.region].num
                rden = self.myparent.regionlist[self.region].den
                nw.note.updateregion(newr)
                ratio = self.myparent.ratioreduce(nw.note.num * rnum * newrden, nw.note.den * rden * newrnum, self.myparent.primelimit)
                nw.note.updatenum(ratio[0])
                nw.note.updateden(ratio[1])
                nw.updateregion()
        self.oldregion = {}

class comeditvoice(object):
    def __init__(self, parent, noteids, voice):
        self.myparent = parent
        self.noteids = noteids
        self.voice = voice
        for note in self.myparent.notelist:
            if note.id in self.noteids and note.voice == self.voice:
                self.noteids.remove(note.id)
        self.oldvoice = {}
        self.string = "Edit Voice Number"

    def do(self):
        listtodraw = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                inst = nw.note.inst
                voice = nw.note.voice
                if (inst, voice) not in listtodraw:
                    listtodraw.append((inst, voice))
                if (inst, self.voice) not in listtodraw:
                    listtodraw.append((inst, self.voice))
                self.oldvoice['n%d' % nw.note.id] = voice
                nw.note.updatevoice(self.voice)
                nw.updatevoice()
                if inst in self.myparent.hidden:
                    nw.undraw()
        for iv in listtodraw:
            self.myparent.tiedraw(iv[0], iv[1])

    def undo(self):
        listtodraw = []
        for nw in self.myparent.notewidgetlist:
            if nw.note.id in self.noteids:
                inst = nw.note.inst
                voice = self.oldvoice['n%d' % nw.note.id]
                if (inst, voice) not in listtodraw:
                    listtodraw.append((inst, voice))
                if (inst, self.voice) not in listtodraw:
                    listtodraw.append((inst, self.voice))
                nw.note.updatevoice(voice)
                nw.updatevoice()
                if inst in self.myparent.hidden:
                    nw.undraw()
        for iv in listtodraw:
            self.myparent.tiedraw(iv[0], iv[1])
        self.oldvoice = {}

class comeditdurset(object):
    def __init__(self, parent, noteids, dur):
        self.myparent = parent
        self.durdict = {}
        self.dur = dur
        for id in noteids:
            self.durdict['n%d' % id] = dur
        self.string = "Edit Durations"

    def do(self):
        for nw in self.myparent.notewidgetlist:
            if 'n%d' % nw.note.id in self.durdict.keys():
                tempdur = nw.note.dur
                if nw.note.dur < 0:
                    nw.note.updatedur(-abs(self.durdict['n%d' % nw.note.id]))
                else:
                    nw.note.updatedur(abs(self.durdict['n%d' % nw.note.id]))
                self.durdict['n%d' % nw.note.id] = tempdur
                nw.updatedur()

    def undo(self):
        self.do()

    def increment(self, args):
        delta = args[0]
        for nw in self.myparent.notewidgetlist:
            if 'n%d' % nw.note.id in self.durdict.keys():
                nw.note.updatedur(nw.note.dur * delta)
                nw.updatedur()

class comeditdurarrows(object):
    def __init__(self, parent, noteids, mod):
        self.myparent = parent
        self.durdict = {}
        for note in self.myparent.notelist:
            if note.id in noteids:
##      change this to record *new* durations!
#                tempdur = int(abs(note.dur)*24+.5)
                tempdur = int(abs(note.dur)*mod+.5)
                if mod < 0:
                    tempdur -= 1
#                    while tempdur % mod:
#                        tempdur -= 1
                else:
                    tempdur += 1
#                    while tempdur % mod:
#                        tempdur += 1
#                tempdur /= 24.0
                tempdur /= mod
                if note.dur < 0:
                    tempdur *= -1
                if abs(tempdur) > 0:
                    self.durdict['n%d' % note.id] = tempdur
                else:
                    self.durdict['n%d' % note.id] = note.dur
        self.finalized = False
        self.string = "Edit Durations"

    def do(self):
        for nw in self.myparent.notewidgetlist:
            if 'n%d' % nw.note.id in self.durdict.keys():
                self.durdict['n%d' % nw.note.id], tempdur = nw.note.dur, self.durdict['n%d' % nw.note.id]
                nw.note.updatedur(tempdur)
                nw.updatedur()

    def undo(self):
        self.do()

    def increment(self, args):
        if not self.finalized:
            mod = args[0]
            for nw in self.myparent.notewidgetlist:
                if 'n%d' % nw.note.id in self.durdict.keys():
                    tempdur = int(abs(nw.note.dur)*24+.5)
                    if mod < 0:
                        tempdur -= 1
                        while tempdur % mod:
                            tempdur -= 1
                    else:
                        tempdur += 1
                        while tempdur % mod:
                            tempdur += 1
                    tempdur /= 24.0
                    if nw.note.dur < 0:
                        tempdur *= -1
                    if abs(tempdur) > 0:
                        nw.note.updatedur(tempdur)
                        nw.updatedur()

class comeditdurmouse(object):
    def __init__(self, parent, noteid, x):
        self.myparent = parent
        self.noteid = noteid[0]
        self.dur = 0
        for nw in self.myparent.notewidgetlist:
            if nw.note.id == self.noteid:
                self.dur = nw.note.dur
                diff = (int((x - (nw.note.time * self.myparent.xperquarter))/self.myparent.xpxquantize + .5) * self.myparent.xpxquantize)/self.myparent.xperquarter
                if diff > 0:
                    if self.dur > 0: sign = 1
                    else: sign = -1
                    nw.note.updatedur(sign * diff)
                    nw.updatedur()
                break
        self.finalized = False
        self.string = "Edit Durations"

    def do(self):
        for nw in self.myparent.notewidgetlist:
            if nw.note.id == self.noteid:
                if self.dur < 0:
                    self.dur, tempdur = -abs(nw.note.dur), -abs(self.dur)
                else:
                    self.dur, tempdur = abs(nw.note.dur), abs(self.dur)
                nw.note.updatedur(tempdur)
                nw.updatedur()
                break

    def undo(self):
        self.do()

    def increment(self, args):
        if not self.finalized:
            x = args[0]
            for nw in self.myparent.notewidgetlist:
                if nw.note.id == self.noteid:
                    diff = (int((x - (nw.note.time * self.myparent.xperquarter))/self.myparent.xpxquantize + .5) * self.myparent.xpxquantize)/self.myparent.xperquarter
                    if diff > 0:
                        if self.dur > 0: sign = 1
                        else: sign = -1
                        nw.note.updatedur(sign * diff)
                        nw.updatedur()
                    break
        
### will this ever end??

class comcopy(object):
    def __init__(self, parent, noteids):
        self.myparent = parent
        self.noteids = noteids
        self.clipboard = [copy.copy(note) for note in self.myparent.notelist if note.id in self.noteids]
        self.clipboard.sort(key=lambda n: n.time)
        if len(self.clipboard):
            basetime = self.clipboard[0].time
        for note in self.clipboard:
            note.time -= basetime
        self.string = "Copy Notes"

    def do(self):
        self.clipboard, self.myparent.clipboard = self.myparent.clipboard, self.clipboard

    def undo(self):
        self.do()

class comcut(comcopy, comdeletenotes):
    def __init__(self, parent, noteids):
        comcopy.__init__(self, parent, noteids)
        comdeletenotes.__init__(self, parent, noteids)
        self.string = "Cut Notes"

    def do(self):
        comcopy.do(self)
        comdeletenotes.do(self)

    def undo(self):
        comcopy.undo(self)
        comdeletenotes.undo(self)




if __name__ == "__main__":
    vs = '0.2'
    root = tk.Tk()
    root.geometry('1040x600+200+100')
    root.title('Rationale %s: New Score' % vs)
    if sys.platform.count("win32"):
        try: root.iconbitmap('img/rat32.ico')
        except: pass
    elif sys.platform.count("darwin"):
        root.tk.call('set', '::tk::mac::useCustomMDEF', '1')

    root.lift()
    root.focus_set()
    rat = rationale(root, vs)
    root.protocol("WM_DELETE_WINDOW", rat.fileexit)
    root.mainloop()
