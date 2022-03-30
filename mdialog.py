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


#import Tix as tk
import tkinter as tk
import copy
import math
import sys

class meterdialog:
    def __init__(self, parent=None):
        self.myparent = parent
        self.myroot = self.myparent.myparent
        self.metermaybe = copy.deepcopy(self.myparent.meterlist)
        self.meterfr = tk.Toplevel(self.myroot, width=400, height=300)
        self.meterfr.title("Meter Changes")
        if sys.platform.count("win32"):
            try: self.meterfr.iconbitmap('rat32.ico')
            except: pass
        self.meterfr.rowconfigure(0, weight=1)
        self.meterfr.rowconfigure(1, weight=0)
        self.meterfr.columnconfigure(0, weight=1)
#        self.meterbuttons = tk.ButtonBox(self.meterfr, width=400, height=300)
#        self.meterbuttons.add('ok', text='OK', command=self.ok)
#        self.meterbuttons.add('cancel', text='Cancel', command=self.cancel)
#        self.meterbuttons.add('apply', text='Apply', command=self.apply)
#        self.meterbuttons.add('sort', text='Sort', command=self.reorder)
#        self.meterbuttons.grid(row=1, column=0, sticky='')
        self.meterbuttons = tk.Frame(self.meterfr, width=400, height=300, relief="raised", bd=1)
        self.meterbuttons.rowconfigure(0, weight=1)
        tk.Button(self.meterbuttons, text="OK", command=self.ok).grid(row=0, column=0, padx=10)
        tk.Button(self.meterbuttons, text="Cancel", command=self.cancel).grid(row=0, column=1, padx=10)
        tk.Button(self.meterbuttons, text="Apply", command=self.apply).grid(row=0, column=2, padx=10)
        tk.Button(self.meterbuttons, text="Sort", command=self.reorder).grid(row=0, column=3, padx=10)

        self.meterbuttons.grid(row=1, column=0, sticky='', ipady=20)
        self.canvas = tk.Canvas(self.meterfr, width=400, height=300)
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
        self.meterlinelist = []

#        print self.metermaybe
        self.scroll = tk.Scrollbar(self.meterfr, orient='vertical', takefocus=0)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scroll.config(command=self.canvas.yview)
        self.meterfr.bind("<Button-4>",
                              lambda
                              event, arg1="scroll", arg2=-1, arg3="units":
                              self.canvas.yview(arg1, arg2, arg3), "+")
        self.meterfr.bind("<Button-5>",
                              lambda
                              event, arg1="scroll", arg2=1, arg3="units":
                              self.canvas.yview(arg1, arg2, arg3), "+")
        self.meterfr.bind("<MouseWheel>",
                          lambda
                          event, arg1="scroll", arg3="units":
                              self.canvaswheel(arg1, event, arg3))
        for meter in self.metermaybe:
            number = self.metermaybe.index(meter)
            newline = self.addmeterline(meter, number)

        self.addbar = tk.IntVar(value=1)
#        self.addbar.set(1)
        self.addtop = tk.IntVar(value=4)
#        self.addtop.set(4)
        self.addbottom = tk.IntVar(value=4)
#        self.addbottom.set(4)
        tk.Label(self.botrow, text="Bar:", bg=bg).grid(row=0, column=0, sticky='w')
#        self.blankbar = tk.Entry(self.botrow, width=4, textvariable=self.addbar)
        self.blankbar = tk.Spinbox(self.botrow, width=4, textvariable=self.addbar, from_=1, to=999999, bg=bg)
        self.blankbar.focus_set()
#        self.blankbar.select_range(0, "end")
        self.blankbar.selection_adjust(6)
        self.blankbar.grid(row=0, column=1, padx=4, sticky='')
        tk.Label(self.botrow, text="Top:", bg=bg).grid(row=0, column=2, sticky='w')
#        self.blanktop = tk.Entry(self.botrow, width=3, textvariable=self.addtop)
        self.blanktop = tk.Spinbox(self.botrow, width=3, textvariable=self.addtop, from_=1, to=40, bg=bg)
        self.blanktop.grid(row=0, column=3, padx=4, sticky='')
        tk.Label(self.botrow, text="Bottom:", bg=bg).grid(row=0, column=4, sticky='w')
#        self.blankbottom = tk.Entry(self.botrow, width=5, textvariable=self.addbottom, bg=bg)
        self.blankbottom = tk.Menubutton(self.botrow, bd=1, takefocus=1, textvariable=self.addbottom, relief="sunk")

        self.blankbottommenu = tk.Menu(self.blankbottom, tearoff=0)
        self.blankbottommenu.add_command(label="1", command=lambda val=1: self.bottomreplace(val), underline=0)
        self.blankbottommenu.add_command(label="2", command=lambda val=2: self.bottomreplace(val), underline=0)
        self.blankbottommenu.add_command(label="4", command=lambda val=4: self.bottomreplace(val), underline=0)
        self.blankbottommenu.add_command(label="8", command=lambda val=8: self.bottomreplace(val), underline=0)
        self.blankbottommenu.add_command(label="16", command=lambda val=16: self.bottomreplace(val), underline=1)
        self.blankbottommenu.add_command(label="32", command=lambda val=32: self.bottomreplace(val), underline=0)
        self.blankbottommenu.add_command(label="64", command=lambda val=64: self.bottomreplace(val))

        self.blankbottom['menu'] = self.blankbottommenu

###
        self.blankbottom.grid(row=0, column=5, padx=4, sticky='')

        self.blankaddmeter = tk.Button(self.botrow, text="Add Meter", command=self.newmeter)
        self.blankaddmeter.grid(row=0, column=6, padx=4, rowspan=1)

        self.meterfr.update_idletasks()
        self.meterfr.bind("<Return>", self.ok)
        self.meterfr.bind("<Escape>", self.cancel)

    def canvaswheel(self, arg1, event, arg3):
        if event.delta > 0:
            self.canvas.yview(arg1, -1, arg3)
        else:
            self.canvas.yview(arg1, 1, arg3)

    def bottomreplace(self, val):
        self.addbottom.set(val)

    def newmeter(self):
        number = len(self.metermaybe)
        bar = self.addbar.get()
        top = self.addtop.get()
        bottom = self.addbottom.get()
        if bar > 0 and top > 0 and bottom > 0 and not math.log(bottom)/math.log(2) % 1:
            if bar in (existingmeter.bar for existingmeter in self.metermaybe):
                for existingmline in self.meterlinelist:
                    if bar == existingmline.bar.get():
                        existingmline.top.set(top)
                        existingmline.bottom.set(bottom)
                        existingmline.meter.top = top
                        existingmline.meter.bottom = bottom
                        break
            else:
                newmeter = meter(self.myparent, bar, top, bottom)
#        print bar, top, bottom
                self.addmeterline(newmeter, number)
                self.metermaybe.append(newmeter)
#        self.addbar.set(0)
#        self.addtop.set(0)
#        self.addbottom.set(0)
        self.blankbar.focus_set()
        self.blankbar.selection_adjust(6)

    def addmeterline(self, meter, number):
        newline = meterline(self, meter, meter.bar, meter.top, meter.bottom, number)
        self.meterlinelist.append(newline)
        self.scrolladjust()
        self.canvas.yview_moveto(1.0)
#        self.meterfr.update_idletasks()
#        bottomy = self.toprow.winfo_reqheight()
#        print bottomy
#        self.botrowoncanvas
#        self.meterfr.grid_propagate()
        return newline

    def ok(self, *args):
        self.apply()
        self.cancel()

    def cancel(self, *args):
        self.meterfr.destroy()
        del self.myparent.meterdialog

    def apply(self, *args):
        self.reorder()
#        self.myparent.meterlist = copy.deepcopy(self.metermaybe)
        flag = 0
        if len(self.myparent.meterlist) == len(self.metermaybe):
            for ind, m in enumerate(self.metermaybe):
                mparent = self.myparent.meterlist[ind]
                if m.bar == mparent.bar and m.top == mparent.top and m.bottom == mparent.bottom:
                    pass
                else:
                    flag = 1
        else:
            flag = 1
        if flag:
            com = commdialog(self.myparent, self.metermaybe)
            if self.myparent.dispatcher.push(com):
                self.myparent.dispatcher.do()
#            if self.myparent.comlist:
#                self.myparent.comlist = self.myparent.comlist[:self.myparent.comind+1]
#            self.myparent.comlist.append(com)
#            com.do()
#            self.myparent.menuedit.entryconfig(0, label='Undo %s' % self.myparent.comlist[-1].string, state="normal")
#            self.myparent.menuedit.entryconfig(1, label="Can't Redo", state="disabled")
#            self.myparent.comind += 1
        
#        self.myparent.redrawlines()
#        for tempo in self.myparent.tempolist:
#            tempo.findcsdbeat(self.myparent)
#        self.myparent.tempos.delete("bpm")
#        self.myparent.tempos.delete("unit")
#        for t in self.myparent.tempolist:
#            t.makewidget(self.myparent)
##            tdialog.tempowidgetclass(self.myparent, t)

    def reorder(self, *args):
        self.meterlinelist.sort(key=self.sortextract)
        for meterline in self.meterlinelist:
            meterline.number = self.meterlinelist.index(meterline)
            meterline.frame.grid(row=meterline.number, column=0, sticky='ew')
        self.metermaybe = [line.meter for line in self.meterlinelist]
        self.myparent.redrawlines()

    def sortextract(self, item):
        if item.bar.get() != '':
            bar = int(item.bar.get())
        else: bar = '0'
        return bar

    def scrolladjust(self, *args):
        self.meterfr.update_idletasks()
        if len(self.toprow.winfo_children()):
            topy = self.toprow.winfo_reqheight()
        else:
            topy = 0
        self.canvas.coords(self.botrowoncanvas, 0, topy)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.meterfr.update_idletasks()
        if self.scroll.get() == (0.0, 1.0):
            self.canvas.yview_moveto(0.0)
            if self.scroll.winfo_ismapped():
                self.scroll.grid_remove()
        else:
            if not self.scroll.winfo_ismapped():
                self.scroll.grid(row=0, column=1, sticky='ns')
        self.canvas.config(scrollregion=(0, 0, 0, self.toprow.winfo_reqheight()+self.botrow.winfo_reqheight()))


class meter:
    def __init__(self, parent, bar, top, bottom):

        self.bar = bar
        self.top = top
        self.bottom = bottom

class meterline:
    def __init__(self, parent, meter, bar, top, bottom, number):
        self.myparent = parent
        self.meter = meter
        self.number = number
        self.frame = tk.Frame(self.myparent.toprow, bd=4, relief='ridge')
        self.frame.grid(row=self.number, column=0, sticky='ew')
        self.bar = tk.IntVar()
        self.bar.set(bar)
        self.bar.trace("w", self.barchange)
        tk.Label(self.frame, text="Bar:").grid(row=0, column=0, padx=4, sticky='e')
#        self.barwidget = tk.Control(self.frame, min=1, max=99999, width=4, variable=self.bar)
        self.barwidget = tk.Spinbox(self.frame, from_=1, to=99999, width=4, textvariable=self.bar)
        self.barwidget.grid(row=0, column=1, padx=4, sticky='')
        self.top = tk.IntVar(value=top)
#        self.top.set(top)
        self.top.trace("w", self.topchange)
        tk.Label(self.frame, text="Top:").grid(row=0, column=2, padx=4, sticky='e')
#        self.topwidget = tk.Control(self.frame, min=1, max=32, width=2, variable=self.top)
        self.topwidget = tk.Spinbox(self.frame, from_=1, to=32, width=2, textvariable=self.top)
        self.topwidget.grid(row=0, column=3, padx=4, sticky='')
        self.bottom = tk.IntVar(value=bottom)
#        self.bottom.set(bottom)
        self.bottom.trace("w", self.bottomchange)
        tk.Label(self.frame, text="Bottom:").grid(row=0, column=4, padx=4, sticky='e')
#        self.bottomwidget = tk.Entry(self.frame, width=4, textvariable=self.bottom)
        self.bottomwidget = tk.Menubutton(self.frame, bd=1, takefocus=1, textvariable=self.bottom, relief="sunk")

        self.bottommenu = tk.Menu(self.bottomwidget, tearoff=0)
        self.bottommenu.add_command(label="1", command=lambda val=1: self.bottomreplace(val), underline=0)
        self.bottommenu.add_command(label="2", command=lambda val=2: self.bottomreplace(val), underline=0)
        self.bottommenu.add_command(label="4", command=lambda val=4: self.bottomreplace(val), underline=0)
        self.bottommenu.add_command(label="8", command=lambda val=8: self.bottomreplace(val), underline=0)
        self.bottommenu.add_command(label="16", command=lambda val=16: self.bottomreplace(val), underline=1)
        self.bottommenu.add_command(label="32", command=lambda val=32: self.bottomreplace(val), underline=0)
        self.bottommenu.add_command(label="64", command=lambda val=64: self.bottomreplace(val))

        self.bottomwidget['menu'] = self.bottommenu

        self.bottomwidget.grid(row=0, column=5, padx=4)
        self.x = tk.Button(self.frame, text="x", padx=0, pady=0, command=self.remove)
        self.x.grid(row=0, column=6, sticky='e', padx=40)
#        self.myparent.scrolladjust()
#        self.myparent.canvas.yview_moveto(1.0)

#        self.myparent.meterfr.update_idletasks()
#        bottomy = self.myparent.toprow.winfo_reqheight()
##        print bottomy
#
#        self.myparent.canvas.coords(self.myparent.botrowoncanvas, 0, bottomy)
#        if self.myparent.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.myparent.meterfr.update_idletasks()
##            print self.page.scroll.get()
#            if self.myparent.scroll.get() != (0.0, 1.0):
#                self.myparent.scroll.grid(row=1, column=1, sticky='ns')
#
#        self.myparent.canvas.config(scrollregion=self.myparent.canvas.bbox("all"))
#        self.myparent.canvas.yview_moveto(1.0)
#        if self.myparent.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.myparent.meterfr.update_idletasks()
##            print self.page.scroll.get()
#            if self.myparent.scroll.get() != (0.0, 1.0):
#                self.myparent.scroll.grid(row=0, column=1, sticky='ns')
#

    def barchange(self, *args):
        self.meter.bar = self.bar.get()

    def topchange(self, *args):
        self.meter.top = self.top.get()

    def bottomreplace(self, val):
        self.bottom.set(val)

    def bottomchange(self, *args):
#        self.bottom.set(int(args[0]))
        self.meter.bottom = self.bottom.get()

    def remove(self):
        num = self.myparent.meterlinelist.index(self)
        self.frame.destroy()
        for meterline in self.myparent.meterlinelist:
            if meterline.number > num:
                meterline.number -= 1
                meterline.frame.grid(row=meterline.number, column=0, sticky='ew')
        todel1 = self.myparent.metermaybe.pop(num)
        todel2 = self.myparent.meterlinelist.pop(num)
        del todel1
        self.myparent.scrolladjust()
#        self.myparent.meterfr.update_idletasks()
#        if len(self.myparent.meterlinelist) > 0:
#            bottomy = self.myparent.toprow.winfo_reqheight()
#        else:
#            bottomy=0
#        self.myparent.canvas.coords(self.myparent.botrowoncanvas, 0, bottomy)
#        
        del todel2

    def lineremove(self, line):
        pass

    def lineadd(self, type):
        pass

class commdialog(object):
    def __init__(self, parent, mlist):
        self.myparent = parent
        self.mlist = mlist
        self.string = "Meter Changes"

    def do(self):
        self.myparent.meterlist, self.mlist = copy.deepcopy(self.mlist), copy.deepcopy(self.myparent.meterlist)
        self.myparent.redrawlines()
        for tempo in self.myparent.tempolist:
            tempo.findcsdbeat(self.myparent)
        self.myparent.tempos.delete("bpm")
        self.myparent.tempos.delete("unit")
        for t in self.myparent.tempolist:
            t.makewidget(self.myparent)

    def undo(self):
        self.do()

class meterwidget:
    def __init__(self, meter):
        pass
