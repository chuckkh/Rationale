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


#import Tix as tk
import tkinter as tk
import copy
import sys

class tempodialog:
    def __init__(self, parent=None):
        self.myparent = parent
        self.myroot = self.myparent.myparent
        self.tempomaybe = copy.deepcopy(self.myparent.tempolist)
        self.tempofr = tk.Toplevel(self.myroot, width=480, height=360)
        self.tempofr.title("Tempo Changes")
        if sys.platform.count("win32"):
            try: self.tempofr.iconbitmap('rat32.ico')
            except: pass
        self.tempofr.rowconfigure(0, weight=1)
        self.tempofr.rowconfigure(1, weight=0)
        self.tempofr.columnconfigure(0, weight=1)
#        self.tempobuttons = tk.ButtonBox(self.tempofr, width=480, height=360)
#        self.tempobuttons.add('ok', text='OK', command=self.ok)
#        self.tempobuttons.add('cancel', text='Cancel', command=self.cancel)
#        self.tempobuttons.add('apply', text='Apply', command=self.apply)
#        self.tempobuttons.add('sort', text='Sort', command=self.reorder)

        self.tempobuttons = tk.Frame(self.tempofr, width=480, height=360, relief="raised", bd=1)
        self.tempobuttons.rowconfigure(0, weight=1)
        tk.Button(self.tempobuttons, text="OK", command=self.ok).grid(row=0, column=0, padx=10)
        tk.Button(self.tempobuttons, text="Cancel", command=self.cancel).grid(row=0, column=1, padx=10)
        tk.Button(self.tempobuttons, text="Apply", command=self.apply).grid(row=0, column=2, padx=10)
        tk.Button(self.tempobuttons, text="Sort", command=self.reorder).grid(row=0, column=3, padx=10)

        self.tempobuttons.grid(row=1, column=0, sticky='', ipady=20)
        self.canvas = tk.Canvas(self.tempofr, width=480, height=360)
        self.canvas.grid(row=0, column=0, sticky='nesw')
        self.canvas.rowconfigure(2, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.bind("<Configure>", self.scrolladjust)
        self.toprow = tk.Frame(self.canvas)
        self.toprowoncanvas = self.canvas.create_window(0, 0, window=self.toprow, anchor="nw")
        self.toprow.columnconfigure(0, weight=0)
        self.toprow.columnconfigure(1, weight=1)
        bg = "#ccddff"
        self.botrow = tk.Frame(self.canvas, bd=3, relief="ridge", bg=bg)
#        self.botrow.grid(row=1, column=0, sticky='we')
        self.botrow.columnconfigure(0, weight=0)
        self.botrow.columnconfigure(1, weight=1)
        bottomy = self.toprow.winfo_reqheight()
#        print bottomy
        self.botrowoncanvas = self.canvas.create_window(0, bottomy, window=self.botrow, anchor="nw")
        self.tempolinelist = []

#        print self.tempomaybe
        self.scroll = tk.Scrollbar(self.tempofr, orient='vertical', takefocus=0)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scroll.config(command=self.canvas.yview)
        self.tempofr.bind("<Button-4>",
                              lambda
                              event, arg1="scroll", arg2=-1, arg3="units":
                              self.canvas.yview(arg1, arg2, arg3), "+")
        self.tempofr.bind("<Button-5>",
                              lambda
                              event, arg1="scroll", arg2=1, arg3="units":
                              self.canvas.yview(arg1, arg2, arg3), "+")
        self.tempofr.bind("<MouseWheel>",
                          lambda
                          event, arg1="scroll", arg3="units":
                              self.canvaswheel(arg1, event, arg3))
        for tempo in self.tempomaybe:
            number = self.tempomaybe.index(tempo)
            newline = self.addtempoline(tempo, number)

        self.addbar = tk.IntVar(value=1)
        self.addbeat = tk.IntVar(value=1)
        self.addbpm = tk.DoubleVar()
#        self.addunit = tk.IntVar(value=4)
        self.addunit = tk.IntVar(value=4)
        tk.Label(self.botrow, text="Bar:", bg=bg).grid(row=0, column=0, sticky='w')
#        self.blankbar = tk.Entry(self.botrow, width=4, textvariable=self.addbar)
        self.blankbar = tk.Spinbox(self.botrow, width=4, textvariable=self.addbar, from_=1, to=999999, bg=bg)
        self.blankbar.focus_set()
#        self.blankbar.select_range(0, "end")
        self.blankbar.selection_adjust(6)
        self.blankbar.grid(row=0, column=1, padx=4, sticky='')
        tk.Label(self.botrow, text="Beat:", bg=bg).grid(row=0, column=2, sticky='w')
#        self.blankbeat = tk.Entry(self.botrow, width=3, textvariable=self.addbeat)
        self.blankbeat = tk.Spinbox(self.botrow, width=3, textvariable=self.addbeat, from_=1, to=40, bg=bg)
        self.blankbeat.grid(row=0, column=3, padx=4, sticky='')
        tk.Label(self.botrow, text="BPM:", bg=bg).grid(row=0, column=4, sticky='w')
        self.blankbpm = tk.Entry(self.botrow, width=5, textvariable=self.addbpm, bg=bg)
        self.blankbpm.grid(row=0, column=5, padx=4, sticky='')
        tk.Label(self.botrow, text="Unit:", bg=bg).grid(row=0, column=6, sticky='w')
#        self.blankunit = tk.ComboBox(self.botrow, editable=1, variable=self.addunit, listwidth=16)

        self.blankunit = tk.Menubutton(self.botrow, image=self.myparent.n4, bd=4, takefocus=1)

        self.blankunitmenu = tk.Menu(self.blankunit, tearoff=0)
        self.blankunitmenu.add_command(image=self.myparent.n16, command=lambda val=1, bmp=self.myparent.n16: self.unitchange(val, bmp), label="1", underline=0, compound="left")
        self.blankunitmenu.add_command(image=self.myparent.n8, command=lambda val=2, bmp=self.myparent.n8: self.unitchange(val, bmp), label="2", underline=0, compound="left")
        self.blankunitmenu.add_command(image=self.myparent.nd8, command=lambda val=3, bmp=self.myparent.nd8: self.unitchange(val, bmp), label="3", underline=0, compound="left")
        self.blankunitmenu.add_command(image=self.myparent.n4, command=lambda val=4, bmp=self.myparent.n4: self.unitchange(val, bmp), label="4", underline=0, compound="left")
        self.blankunitmenu.add_command(image=self.myparent.nd4, command=lambda val=6, bmp=self.myparent.nd4: self.unitchange(val, bmp), label="5", underline=0, compound="left")
        self.blankunitmenu.add_command(image=self.myparent.n2, command=lambda val=8, bmp=self.myparent.n2: self.unitchange(val, bmp), label="6", underline=0, compound="left")
        self.blankunitmenu.add_command(image=self.myparent.nd2, command=lambda val=12, bmp=self.myparent.nd2: self.unitchange(val, bmp), label="7", underline=0, compound="left")
        self.blankunitmenu.add_command(image=self.myparent.n1, command=lambda val=16, bmp=self.myparent.n1: self.unitchange(val, bmp), label="8", underline=0, compound="left")
        self.blankunit['menu'] = self.blankunitmenu

#        self.blankunit.entry.configure(width=4)
#        self.blankunit.subwidget("listbox").configure(font=("Arial", 10))
#        self.blankunit.append_history(1)
#        self.blankunit.append_history(2)
#        self.blankunit.append_history(3)
#        self.blankunit.append_history(4)
#        self.blankunit.append_history(6)
#        self.blankunit.append_history(8)
#        self.blankunit.append_history(12)
#        self.blankunit.append_history(16)
#        self.blankunit.grid(row=0, column=7, padx=4, sticky='')
#        self.blankunit.append_history('1/16')
#        self.blankunit.append_history('1/8')
#        self.blankunit.append_history('1/8 *')
#        self.blankunit.append_history('d')
#        self.blankunit.append_history('1/4 *')
#        self.blankunit.append_history('1/2')
#        self.blankunit.append_history('1/2 *')
#        self.blankunit.append_history('1')
#        self.blankunit.subwidget("listbox").configure(width=10)
        self.blankunit.grid(row=0, column=7, padx=4, sticky='')

        self.blankaddtempo = tk.Button(self.botrow, text="Add Tempo", command=self.newtempo)
        self.blankaddtempo.grid(row=0, column=8, padx=10, rowspan=1)

        self.tempofr.update_idletasks()
        self.tempofr.bind("<Return>", self.ok)
        self.tempofr.bind("<Escape>", self.cancel)

    def canvaswheel(self, arg1, event, arg3):
        if event.delta > 0:
            self.canvas.yview(arg1, -1, arg3)
        else:
            self.canvas.yview(arg1, 1, arg3)

    def unitchange(self, val, bmp):
        self.addunit.set(val)
        self.blankunit['image'] = bmp

    def unitget(self):
        ustr = self.addunit.get()
        if ustr == '1/16':
            return 1
        elif ustr == '1/8':
            return 2
        elif ustr == '1/8 *':
            return 3
        elif ustr == 'd':
            return 4
        elif ustr == '1/4 *':
            return 6
        elif ustr == '1/2':
            return 8
        elif ustr == '1/2 *':
            return 12
        elif ustr == '1':
            return 16

    def newtempo(self):
        number = len(self.tempomaybe)
        bar = self.addbar.get()
        beat = self.addbeat.get()
        bpm = self.addbpm.get()
        unit = self.addunit.get()
        flag = 0
        for t in self.tempomaybe:
            if t.bar == bar and t.beat == beat:
                flag += 1
        if bar > 0 and beat > 0 and bpm > 0 and unit > 0 and flag < 2:
            newtempo = tempo(self.myparent, bar, beat, bpm, unit)
            self.addtempoline(newtempo, number)
            self.tempomaybe.append(newtempo)
#            self.addbar.set(0)
#            self.addbeat.set(0)
#            self.addbpm.set(0)
#            self.addunit.set(4)
            self.blankbar.focus_set()
#            self.blankbar.select_range(0, "end")
            self.blankbar.selection_adjust(6)

    def addtempoline(self, tempo, number):
        newline = tempoline(self, tempo, tempo.bar, tempo.beat, tempo.bpm, tempo.unit, number)
        self.tempolinelist.append(newline)
        self.scrolladjust()
        self.canvas.yview_moveto(1.0)

#        self.tempofr.update_idletasks()
#        bottomy = self.toprow.winfo_reqheight()
#        print bottomy
#        self.botrowoncanvas
#        self.tempofr.grid_propagate()
        return newline

    def ok(self, *args):
        self.apply()
        self.cancel()

    def cancel(self, *args):
        self.tempofr.destroy()

    def apply(self):
        self.reorder()
#        self.myparent.tempolist = copy.deepcopy(self.tempomaybe)
        flag = 0
        if len(self.myparent.tempolist) == len(self.tempomaybe):
            for ind, t in enumerate(self.tempomaybe):
                tparent = self.myparent.tempolist[ind]
                if t.bar == tparent.bar and t.beat == tparent.beat and t.bpm == tparent.bpm and t.unit == tparent.unit:
                    pass
                else:
                    flag = 1
        else:
            flag = 1
        if flag:
            com = comtdialog(self.myparent, self.tempomaybe)
            if self.myparent.dispatcher.push(com):
                self.myparent.dispatcher.do()
#            if self.myparent.comlist:
#                self.myparent.comlist = self.myparent.comlist[:self.myparent.comind+1]
#            self.myparent.comlist.append(com)
#            com.do()
#            self.myparent.menuedit.entryconfig(0, label='Undo %s' % self.myparent.comlist[-1].string, state="normal")
#            self.myparent.menuedit.entryconfig(1, label="Can't Redo", state="disabled")
#            self.myparent.comind += 1


#            print t.bpm, t.unit
#            print t.bpm*t.unit/4.0
#            tempowidgetclass(self.myparent, t)

    def reorder(self, *args):
        self.tempolinelist.sort(key=self.sortextract)
        for tempoline in self.tempolinelist:
            tempoline.number = self.tempolinelist.index(tempoline)
            tempoline.frame.grid(row=tempoline.number, column=0, sticky='ew')
        self.tempomaybe = [line.tempo for line in self.tempolinelist]

    def sortextract(self, item):
        if item.bar.get() != '':
            bar = int(item.bar.get())
        else: bar = '0'
        if item.beat != '':
            beat = float(item.beat.get())
        else: beat = '0'
        return (bar, beat)

    def scrolladjust(self, *args):
#        print self.canvas.winfo_height()
        self.tempofr.update_idletasks()
        if len(self.toprow.winfo_children()):
            topy = self.toprow.winfo_reqheight()
        else:
            topy = 0
#        if len(self.tempolinelist) > 0:
#            topy = self.toprow.winfo_reqheight()
#        else:
#            topy = 0
##        bottomy = self.toprow.winfo_reqheight()
##        print 'bottomy', bottomy
        self.canvas.coords(self.botrowoncanvas, 0, topy)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.tempofr.update_idletasks()
        if self.scroll.get() == (0.0, 1.0):
            self.canvas.yview_moveto(0.0)
            if self.scroll.winfo_ismapped():
                self.scroll.grid_remove()
        else:
#            if not len(args):
#                self.canvas.yview_moveto(1.0)
            if not self.scroll.winfo_ismapped():
                self.scroll.grid(row=0, column=1, sticky='ns')
        self.canvas.config(scrollregion=(0, 0, 0, self.toprow.winfo_reqheight()+self.botrow.winfo_reqheight()))


class tempo:
    def __init__(self, parent, bar, beat, bpm, unit):
        '''Left-click: add new or edit existing tempo;
                tempo may be dragged left and right,
                and dragging up and down raises or lowers tempo value
           Right-click: edit list of tempos'''
        self.bar = bar
        self.beat = beat
        self.bpm = bpm
        self.unit = unit
#        self.tick = tick
#        self.widget = widget
        self.findcsdbeat(parent)

    def findcsdbeat(self, app):
        sum = m = 0
        top = bottom = 4
        for b in range(1, self.bar):
            if m < len(app.meterlist):
                if app.meterlist[m].bar == b:
                    top, bottom = app.meterlist[m].top, app.meterlist[m].bottom
                    m += 1
            sum += 4.0 * top / bottom
        try:
            if app.meterlist[m].bar == self.bar:
                bottom = app.meterlist[m].bottom
        except: pass
        sum += 4.0 * (self.beat-1) / bottom
        self.scobeat = sum
#        print sum

    def makewidget(self, parent):
        tempowidgetclass(parent, self)

class tempoline:
    def __init__(self, parent, tempo, bar, beat, bpm, unit, number):
        self.myparent = parent
        self.tempo = tempo
        self.number = number
        self.frame = tk.Frame(self.myparent.toprow, bd=4, relief='ridge')
        self.frame.grid(row=self.number, column=0, sticky='ew')
        self.bar = tk.IntVar()
        self.bar.set(bar)
        self.bar.trace("w", self.barchange)
        self.barlabel = tk.Label(self.frame, text="Bar:")
        self.barlabel.grid(row=0, column=0, padx=4, sticky='e')
#        self.barwidget = tk.Control(self.frame, min=1, max=99999, width=4, variable=self.bar)
        self.barwidget = tk.Spinbox(self.frame, width=4, textvariable=self.bar, from_=1, to=99999)
        self.barwidget.grid(row=0, column=1, padx=4, sticky='')
        self.beat = tk.IntVar()
        self.beat.set(beat)
        self.beat.trace("w", self.beatchange)
        self.beatlabel = tk.Label(self.frame, text="Beat:")
        self.beatlabel.grid(row=0, column=2, padx=4, sticky='e')
#        self.beatwidget = tk.Control(self.frame, min=1, max=32, width=2, variable=self.beat)
        self.beatwidget = tk.Spinbox(self.frame, width=2, textvariable=self.beat, from_=1, to=40)
        self.beatwidget.grid(row=0, column=3, padx=4, sticky='')
        self.bpm = tk.DoubleVar()
        self.bpm.set(bpm)
        self.bpm.trace("w", self.bpmchange)
        self.bpmlabel = tk.Label(self.frame, text="BPM:")
        self.bpmlabel.grid(row=0, column=4, padx=4, sticky='e')
        self.bpmwidget = tk.Entry(self.frame, width=4, textvariable=self.bpm)
        self.bpmwidget.grid(row=0, column=5, padx=4)
        self.unit = tk.IntVar(value=unit)
#        self.unit.set(unit)
#        self.unit.trace("w", self.unitchange)
        self.unitlabel = tk.Label(self.frame, text="Unit:")
        self.unitlabel.grid(row=0, column=6, padx=4, sticky='e')
#        self.unitwidget = tk.ComboBox(self.frame, variable=self.unit, editable=0, listwidth=16)
#        self.unitwidget.entry.configure(width=4)
##        self.unitwidget.append_history(1)
##        self.unitwidget.append_history(2)
##        self.unitwidget.append_history(3)
##        self.unitwidget.append_history(4)
##        self.unitwidget.append_history(6)
##        self.unitwidget.append_history(8)
##        self.unitwidget.append_history(12)
##        self.unitwidget.append_history(16)
#        self.unitwidget.append_history('1/16')
#        self.unitwidget.append_history('1/8')
#        self.unitwidget.append_history('1/8 *')
#        self.unitwidget.append_history('d')
#        self.unitwidget.append_history('1/4 *')
#        self.unitwidget.append_history('1/2')
#        self.unitwidget.append_history('1/2 *')
#        self.unitwidget.append_history('1')
#
##        for value in ('Sixteenth', 'Dotted Sixteenth', 'Eighth', 'Dotted Eighth', 'Quarter', 'Dotted Quarter', 'Half', 'Dotted Half', 'Whole'):
##            self.unitwidget.append_history(value)
        if unit == 1: img = self.myparent.myparent.n16
        elif unit == 2: img = self.myparent.myparent.n8
        elif unit == 3: img = self.myparent.myparent.nd8
        elif unit == 4: img = self.myparent.myparent.n4
        elif unit == 6: img = self.myparent.myparent.nd4
        elif unit == 8: img = self.myparent.myparent.n2
        elif unit == 12: img = self.myparent.myparent.nd2
        elif unit == 16: img = self.myparent.myparent.n1
        else: img = self.myparent.myparent.n4
            
        self.unitwidget = tk.Menubutton(self.frame, image=img, bd=4, takefocus=1)

        self.unitmenu = tk.Menu(self.unitwidget, tearoff=0)
        self.unitmenu.add_command(image=self.myparent.myparent.n16, command=lambda val=1, bmp=self.myparent.myparent.n16: self.unitchange(val, bmp), underline=0, compound="left", label="1")
        self.unitmenu.add_command(image=self.myparent.myparent.n8, command=lambda val=2, bmp=self.myparent.myparent.n8: self.unitchange(val, bmp), underline=0, compound="left", label="2")
        self.unitmenu.add_command(image=self.myparent.myparent.nd8, command=lambda val=3, bmp=self.myparent.myparent.nd8: self.unitchange(val, bmp), underline=0, compound="left", label="3")
        self.unitmenu.add_command(image=self.myparent.myparent.n4, command=lambda val=4, bmp=self.myparent.myparent.n4: self.unitchange(val, bmp), underline=0, compound="left", label="4")
        self.unitmenu.add_command(image=self.myparent.myparent.nd4, command=lambda val=6, bmp=self.myparent.myparent.nd4: self.unitchange(val, bmp), underline=0, compound="left", label="5")
        self.unitmenu.add_command(image=self.myparent.myparent.n2, command=lambda val=8, bmp=self.myparent.myparent.n2: self.unitchange(val, bmp), underline=0, compound="left", label="6")
        self.unitmenu.add_command(image=self.myparent.myparent.nd2, command=lambda val=12, bmp=self.myparent.myparent.nd2: self.unitchange(val, bmp), underline=0, compound="left", label="7")
        self.unitmenu.add_command(image=self.myparent.myparent.n1, command=lambda val=16, bmp=self.myparent.myparent.n1: self.unitchange(val, bmp), underline=0, compound="left", label="8")

        self.unitwidget['menu'] = self.unitmenu

        self.unitwidget.grid(row=0, column=7, padx=4, sticky='')
#        self.unitchange(unit)
        self.x = tk.Button(self.frame, text="x", padx=0, pady=0, command=self.remove)
        self.x.grid(row=0, column=8, sticky='e', padx=40)
#        self.myparent.scrolladjust()
#        self.myparent.canvas.yview_moveto(1.0)

#        self.myparent.tempofr.update_idletasks()
#        bottomy = self.myparent.toprow.winfo_reqheight()
##        print bottomy
#
#        self.myparent.canvas.coords(self.myparent.botrowoncanvas, 0, bottomy)
#        if self.myparent.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.myparent.tempofr.update_idletasks()
##            print self.page.scroll.get()
#            if self.myparent.scroll.get() != (0.0, 1.0):
#                self.myparent.scroll.grid(row=0, column=1, sticky='ns')
#
#        self.myparent.canvas.config(scrollregion=self.myparent.canvas.bbox("all"))
#        self.myparent.canvas.yview_moveto(1.0)
#        if self.myparent.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.myparent.tempofr.update_idletasks()
##            print self.page.scroll.get()
#            if self.myparent.scroll.get() != (0.0, 1.0):
#                self.myparent.scroll.grid(row=0, column=1, sticky='ns')

    def unitchange(self, val, bmp):
        self.unit.set(val)
        self.tempo.unit = val
        self.unitwidget['image'] = bmp

    def unitset(self, unit):
        if unit == 1:
            self.unit.set('1/16')
        if unit == 2:
            self.unit.set('1/8')
        if unit == 3:
            self.unit.set('1/8 *')
        if unit == 4:
            self.unit.set('d')
        if unit == 6:
            self.unit.set('1/4 *')
        if unit == 8:
            self.unit.set('1/2')
        if unit == 12:
            self.unit.set('1/2 *')
        if unit == 16:
            self.unit.set('1')

    def unitget(self):
        ustr = self.unit.get()
        if ustr == '1/16':
            return 1
        elif ustr == '1/8':
            return 2
        elif ustr == '1/8 *':
            return 3
        elif ustr == 'd':
            return 4
        elif ustr == '1/4 *':
            return 6
        elif ustr == '1/2':
            return 8
        elif ustr == '1/2 *':
            return 12
        elif ustr == '1':
            return 16

    def barchange(self, *args):
        self.tempo.bar = self.bar.get()

    def beatchange(self, *args):
        self.tempo.beat = self.beat.get()

    def bpmchange(self, *args):
        try:
            self.tempo.bpm = self.bpm.get()
        except: pass

#    def unitchange(self, *args):
#        self.tempo.unit = self.unitget()

    def remove(self):
        num = self.myparent.tempolinelist.index(self)
        self.frame.destroy()
        for tempoline in self.myparent.tempolinelist:
            if tempoline.number > num:
                tempoline.number -= 1
                tempoline.frame.grid(row=tempoline.number, column=0, sticky='ew')
        todel1 = self.myparent.tempomaybe.pop(num)
        todel2 = self.myparent.tempolinelist.pop(num)
        del todel1
        self.myparent.scrolladjust()
#        self.myparent.tempofr.update_idletasks()
#        if len(self.myparent.tempolinelist) > 0:
#            bottomy = self.myparent.toprow.winfo_reqheight()
#        else:
#            bottomy=0
##        bottomy = self.myparent.toprow.winfo_reqheight()
##        print 'bottomy', bottomy
#        self.myparent.canvas.coords(self.myparent.botrowoncanvas, 0, bottomy)
#        self.myparent.tempofr.update_idletasks()
#        topy = self.myparent.toprow.winfo_reqheight()
#        boty = self.myparent.botrow.winfo_reqheight()
#        bottomy = topy + boty
##        print bottomy
##        self.myparent.canvas.coords(self.myparent.botrowoncanvas, 0, bottomy)
#        self.myparent.canvas.config(scrollregion=self.myparent.canvas.bbox("all"))
#        if self.myparent.scroll.winfo_ismapped():
#            self.myparent.tempofr.update_idletasks()
#            if self.myparent.scroll.get() == (0.0, 1.0):
#                print "remove scroll"
#                self.myparent.scroll.grid_remove()
##################
##        else:
##            self.myparent.tempofr.update_idletasks()
###            print self.page.scroll.get()
##            if self.myparent.scroll.get() != (0.0, 1.0):
##                self.myparent.scroll.grid(row=0, column=1, sticky='ns')
##
##        self.myparent.canvas.config(scrollregion=self.myparent.canvas.bbox("all"))
##        self.myparent.canvas.yview_moveto(1.0)
##        if self.myparent.scroll.winfo_ismapped():
###            print self.page.scroll.get()
##            pass
##        else:
##            self.myparent.tempofr.update_idletasks()
###            print self.page.scroll.get()
##            if self.myparent.scroll.get() != (0.0, 1.0):
##                self.myparent.scroll.grid(row=0, column=1, sticky='ns')
##################
        del todel2

    def scrolladjust(self):
        print(self.myparent.scroll.get())
#        self.myparent.tempofr.update_idletasks()
#        if len(self.myparent.tempolinelist) > 0:
#            topy = self.myparent.toprow.winfo_reqheight()
#        else:
#            topy=0
##        bottomy = self.myparent.toprow.winfo_reqheight()
##        print 'bottomy', bottomy
#        self.myparent.canvas.coords(self.myparent.botrowoncanvas, 0, topy)
#
#        self.myparent.tempofr.update_idletasks()
#        topy = self.myparent.toprow.winfo_reqheight()
##        print bottomy
#
#        self.myparent.canvas.coords(self.myparent.botrowoncanvas, 0, bottomy)
#        if self.myparent.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.myparent.tempofr.update_idletasks()
##            print self.page.scroll.get()
#            if self.myparent.scroll.get() != (0.0, 1.0):
#                self.myparent.scroll.grid(row=0, column=1, sticky='ns')
#
#        self.myparent.canvas.config(scrollregion=self.myparent.canvas.bbox("all"))
#        self.myparent.canvas.yview_moveto(1.0)
#        if self.myparent.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.myparent.tempofr.update_idletasks()
##            print self.page.scroll.get()
#            if self.myparent.scroll.get() != (0.0, 1.0):
#                self.myparent.scroll.grid(row=0, column=1, sticky='ns')
#

    def lineremove(self, line):
        pass

    def lineadd(self, type):
        pass

class comtdialog(object):
    def __init__(self, parent, tlist):
        self.myparent = parent
        self.tlist = tlist
        self.string = "Tempo Changes"

    def do(self):
        self.myparent.tempolist, self.tlist = self.tlist, self.myparent.tempolist

        for tempo in self.myparent.tempolist:
            tempo.findcsdbeat(self.myparent)
        self.myparent.tempos.delete("bpm")
        self.myparent.tempos.delete("unit")
        for t in self.myparent.tempolist:
            t.makewidget(self.myparent)

    def undo(self):
        self.do()

class tempowidgetclass:
    def __init__(self, parent, tempo=None):
        self.myparent = parent
        self.tempo = tempo
        ind = self.myparent.tempolist.index(tempo)
        x = self.tempo.scobeat * self.myparent.xperquarter
        if ind > 0:
            if self.myparent.tempolist[ind-1].bar == self.tempo.bar and self.myparent.tempolist[ind-1].beat == self.tempo.beat:
                x += 6
        if ind < len(self.myparent.tempolist)-1:
            if self.myparent.tempolist[ind+1].bar == self.tempo.bar and self.myparent.tempolist[ind+1].beat == self.tempo.beat:
                x -= 8
        if self.tempo.unit == 1:
            unitbmp = self.myparent.nnb16
        elif self.tempo.unit == 2:
            unitbmp = self.myparent.nnb8
        elif self.tempo.unit == 3:
            unitbmp = self.myparent.nnbd8
        elif self.tempo.unit == 4:
            unitbmp = self.myparent.nnb4
        elif self.tempo.unit == 6:
            unitbmp = self.myparent.nnbd4
        elif self.tempo.unit == 8:
            unitbmp = self.myparent.nnb2
        elif self.tempo.unit == 12:
            unitbmp = self.myparent.nnbd2
        elif self.tempo.unit == 16:
            unitbmp = self.myparent.nnb1
        if sys.platform.count("darwin"):
            self.bpmwidget = self.myparent.tempos.create_text((x+3,3), text=str(int(self.tempo.bpm)), anchor="ne", font=("Times", 10), tags=("bpm"))
        else:
            self.bpmwidget = self.myparent.tempos.create_text((x+3,0), text=str(int(self.tempo.bpm)), anchor="ne", font=("Times", 6), tags=("bpm"))
        self.unitwidget = self.myparent.tempos.create_image((x-2,0), image=unitbmp, anchor="nw", tags=("unit"))
