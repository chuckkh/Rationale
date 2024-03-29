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


import tkinter as tk
import tkinter.colorchooser as tkcc
import tkinter.filedialog as tkfd
import copy
import os
import subprocess
import sys

class outputdialog:
    def __init__(self, parent=None):
        self.myparent = parent
        self.myparent.odialogopen = True
        self.myroot = self.myparent.myparent
        self.instmaybe = copy.deepcopy(self.myparent.instlist)
        for i, inst in enumerate(self.instmaybe):
            if i:
                inst.gsolo = 0
        if sys.platform.count("darwin"):
            self.w = 790
        else:
            self.w = 700
        self.outputfr = tk.Toplevel(self.myroot, width=self.w, height=580)
        self.outputfr.grid_propagate(False)
        if sys.platform.count("win32"):
            try: self.outputfr.iconbitmap('rat32.ico')
            except: pass
        self.outputfr.bind("<Return>", self.okcond)
        self.outputfr.bind("<Escape>", self.cancel)
        self.outputfr.title("Output")
        self.outputfr.rowconfigure(0, weight=0)
        self.outputfr.rowconfigure(1, weight=1)
        self.outputfr.columnconfigure(0, weight=1)
#        self.tablist = []
        self.framelist = []
        self.currentframe = 0
        self.tabs = tk.Frame(self.outputfr, width=self.w, height=20)
        for i in range(100):
            self.tabs.columnconfigure(i, minsize=40)
        self.nb = tk.Frame(self.outputfr, width=self.w, height=480, relief="ridge", bd=2)
        self.nb.rowconfigure(0, weight=1)
        self.nb.columnconfigure(0, weight=1)
#        self.nb = tk.NoteBook(self.outputfr, width=self.w, height=480)
#        self.nb.rowconfigure(0, weight=1)
#        self.nb.columnconfigure(0, weight=1)
        self.showframe = tk.Frame(self.nb)
        self.tabs.grid(row=0, column=0, sticky='w', padx=20)
#        self.outputfr.bind("<Configure>", self.tabsreset)
        self.tabs.bind("<Configure>", self.tabsreset)
        self.nb.grid(row=1, column=0, sticky='nesw')
        self.showframe.grid(sticky='nesw')
#        self.outputbuttons = tk.ButtonBox(self.outputfr, width=self.w, height=80)
#        self.outputbuttons.add('ok', text='OK', command=self.ok)
#        self.outputbuttons.add('cancel', text='Cancel', command=self.cancel)
#        self.outputbuttons.add('apply', text='Apply', command=self.apply)
#        self.outputbuttons.add('play', text='Play', command=self.audition)
#        self.outputbuttons.add('newinst', text='New Instrument', command=self.newinstrument)
        self.outputbuttons = tk.Frame(self.outputfr, width=self.w, height=80, borderwidth=1, relief="raised")
        self.outputbuttons.rowconfigure(0, weight=1)
        tk.Button(self.outputbuttons, text="OK", command=self.ok).grid(row=0, column=0, padx=10)
        tk.Button(self.outputbuttons, text="Cancel", command=self.cancel).grid(row=0, column=1, padx=10)
        tk.Button(self.outputbuttons, text="Apply", command=self.apply).grid(row=0, column=2, padx=10)
        self.playbutton = tk.Button(self.outputbuttons, text="Play", command=self.audition)
        self.playbutton.grid(row=0, column=3, padx=10)
        tk.Button(self.outputbuttons, text="New Instrument", command=self.newinstrument).grid(row=0, column=4, padx=10)
##########

        self.outputbuttons.grid(row=2, column=0, sticky='', ipady=20)

        self.instpagelist = []
        self.sf2list = copy.deepcopy(self.myparent.sf2list)
#        self.csdpage = self.nb.add('csd', label='CSD')
        self.timingIn = tk.StringVar()
        self.timingIn.set(self.myparent.midiTimingInDevice.name)
        self.triggerSpaceDev = tk.StringVar()
        self.triggerSpaceDev.set(self.myparent.triggerSpaceKey.devname)
        self.triggerPageUpDev = tk.StringVar()
        self.triggerPageUpDev.set(self.myparent.triggerPageUpKey.devname)
        self.triggerPageDownDev = tk.StringVar()
        self.triggerPageDownDev.set(self.myparent.triggerPageDownKey.devname)
        self.triggerHomeDev = tk.StringVar()
        self.triggerHomeDev.set(self.myparent.triggerHomeKey.devname)
        self.triggerEndDev = tk.StringVar()
        self.triggerEndDev.set(self.myparent.triggerEndKey.devname)
        self.triggerSpaceChannel = tk.IntVar()
        self.triggerSpaceCC = tk.IntVar()
        self.triggerPageUpChannel = tk.IntVar()
        self.triggerPageUpCC = tk.IntVar()
        self.triggerPageDownChannel = tk.IntVar()
        self.triggerPageDownCC = tk.IntVar()
        self.triggerHomeChannel = tk.IntVar()
        self.triggerHomeCC = tk.IntVar()
        self.triggerEndChannel = tk.IntVar()
        self.triggerEndCC = tk.IntVar()
        self.triggerSpaceChannel.set(self.myparent.triggerSpaceKey.channel)
        self.triggerSpaceCC.set(self.myparent.triggerSpaceKey.cc)
        self.triggerPageUpChannel.set(self.myparent.triggerPageUpKey.channel)
        self.triggerPageUpCC.set(self.myparent.triggerPageUpKey.cc)
        self.triggerPageDownChannel.set(self.myparent.triggerPageDownKey.channel)
        self.triggerPageDownCC.set(self.myparent.triggerPageDownKey.cc)
        self.triggerHomeChannel.set(self.myparent.triggerHomeKey.channel)
        self.triggerHomeCC.set(self.myparent.triggerHomeKey.cc)
        self.triggerEndChannel.set(self.myparent.triggerEndKey.channel)
        self.triggerEndCC.set(self.myparent.triggerEndKey.cc)

#        self.timingIn.trace("w", self.timingInDeviceChange)
        self.globalPage = self.add(label='Global')
        self.globalPage.rowconfigure(0, weight=0)
        self.globalPage.rowconfigure(1, weight=0)
        self.globalPage.rowconfigure(2, weight=0)
        self.globalPage.rowconfigure(3, weight=0)
        self.globalPage.rowconfigure(4, weight=0)
        self.globalPage.rowconfigure(5, weight=0)
        self.globalPage.rowconfigure(6, weight=0)
        self.globalPage.rowconfigure(7, weight=0)
        self.globalPage.rowconfigure(8, weight=0)
        self.globalPage.rowconfigure(9, weight=0)
        self.globalPage.rowconfigure(10, weight=0)
        self.globalPage.rowconfigure(11, weight=0)
        self.globalPage.rowconfigure(12, weight=0)
        self.globalPage.rowconfigure(13, weight=1)
        self.globalPage.rowconfigure(14, weight=0)

        self.timingInFrame = tk.Frame(self.globalPage, relief="ridge", bd=2)
        self.timingInFrame.grid(row=1, column=0, sticky='w', padx=10)
        tk.Label(self.timingInFrame, text="MIDI Transport and Timing Input").grid(row=0, column=0, columnspan=2, sticky='w')
        self.timingInSelector = tk.Menubutton(self.timingInFrame, textvariable=self.timingIn, bg="#aa9999", activebackground="#bbaaaa", width=35, relief="raised", padx=0, indicatoron=1)
        self.timingInSelectorMenu = tk.Menu(self.timingInSelector, tearoff=0)
        for devname in self.myparent.midiInDevices:
            self.timingInSelectorMenu.add_command(label=devname, command = lambda arg1=devname: self.changeTimingInDevice(arg1))
        self.timingInSelector['menu'] = self.timingInSelectorMenu
        self.timingInSelector.grid(row=1, column=0, columnspan=2, sticky='w')
#        self.globalPage.columnconfigure(0, weight=1)

        self.triggerSpace = TriggerKeyFrame(self, self.myparent.triggerSpaceKey, "Space", 4)
        self.triggerPageUp = TriggerKeyFrame(self, self.myparent.triggerPageUpKey, "PageUp", 6)
        self.triggerPageDown = TriggerKeyFrame(self, self.myparent.triggerPageDownKey, "PageDown", 8)
        self.triggerHome = TriggerKeyFrame(self, self.myparent.triggerHomeKey, "Home", 10)
        self.triggerEnd = TriggerKeyFrame(self, self.myparent.triggerEndKey, "End", 12)






#        tk.Label(self.globalPage, text="CSD file load/edit: Edit in this space, or load with the button below.").grid(row=0, column=0, columnspan=2, sticky='w')
#        if self.myparent.csdimport:
#            lab = os.path.split(self.myparent.csdimport)
#        else:
#        lab = ('', 'No Csound File Loaded')
#        self.csdpathlabel = tk.Label(self.globalPage, text=lab[0]+os.sep, relief="ridge", bg="#aaaaaa")
#        self.csdpathlabel.grid(row=1, column=0, sticky='w')
#        self.csdlabel = tk.Label(self.globalPage, text=lab[1], relief="ridge", bg="#eeeeee")
#        self.csdlabel.grid(row=1, column=1, sticky='w')
#        scroll = tk.Scrollbar(self.globalPage)
#        scroll.grid(row=2, column=2, sticky='ns')
 #       self.csdtext = tk.Text(self.globalPage, yscrollcommand=scroll.set)
 #       self.csdtext.grid(row=2, column=0, columnspan=2, sticky='nesw')
#        self.csdtext.insert('0.0', self.myparent.csdimported)
 #       self.csdtext.insert('0.0', '')
#        if self.myparent.outautoload:
#            self.csdloadwork(self.myparent.csdimport)
#        scroll.config(command=self.csdtext.yview)
        for i in range(1, len(self.instmaybe)):
            inst = self.instmaybe[i]
            newpage = self.addinstpage(inst)
            for out in inst.outlist:
                if len(newpage.linelist) == 0:
                    if out.__class__.__name__ == 'csdout':
                        newline = csdline(newpage, out)
                    elif out.__class__.__name__ == 'sf2out':
                        newline = sf2line(newpage, out)
                    elif out.__class__.__name__ == 'oscout':
                        newline = oscline(newpage, out)
                    elif out.__class__.__name__ == 'midout':
                        print("line 125")
                        newline = midline(newpage, out)
                    newpage.linelist.append(newline)
                    newpage.scrolladjust()
                    newpage.canvas.yview_moveto(1.0)
#        self.loadfr = tk.Frame(self.globalPage)
#        self.loadfr.grid(row=3, column=0, sticky='ew', columnspan=2)
#        self.csdloadbutton = tk.Button(self.loadfr, text="Load", command=self.csdload)
#        self.csdloadbutton.grid(row=0, column=0, sticky='e')
#        self.csdreloadbutton = tk.Button(self.loadfr, text="Reload", command=lambda arg1 = self.myparent.csdimport: self.csdloadwork(arg1))
#        self.csdreloadbutton.grid(row=0, column=1, sticky='e')
#        self.autoload = tk.BooleanVar(value=self.myparent.outautoload)
#        self.autoload.set(self.myparent.outautoload)
#        self.autocheck = tk.Checkbutton(self.loadfr, variable=self.autoload, text="Auto Reload", bg="#77aa77")
#        self.autocheck.grid(row=0, column=2, sticky='w')
        self.tabs.winfo_children()[0].select()
        self.tabs.winfo_children()[0].invoke()
#        self.tablist[0].select()
#        self.tablist[0].invoke()

    def changeTimingInDevice(self, devname):
        if self.timingIn.get() != devname:
            self.timingIn.set(devname)

    def changeTriggerSpaceDevice(self, devname):
        if self.triggerSpaceDev.get() != devname:
            self.triggerSpaceDev.set(devname)

    def changeTriggerSpaceChannel(self, channel):
        if self.triggerSpaceChannel.get() != channel:
            self.triggerSpaceChannel.set(channel)

    def changeTriggerSpaceCC(self, cc):
        if self.triggerSpaceCC.get() != cc:
            self.triggerSpaceCC.set(cc)


    def changeTriggerPageUpDevice(self, devname):
        if self.triggerPageUpDev.get() != devname:
            self.triggerPageUpDev.set(devname)

    def changeTriggerPageUpChannel(self, channel):
        if self.triggerPageUpChannel.get() != channel:
            self.triggerPageUpChannel.set(channel)

    def changeTriggerPageUpCC(self, cc):
        if self.triggerPageUpCC.get() != cc:
            self.triggerPageUpCC.set(cc)


    def changeTriggerPageDownDevice(self, devname):
        if self.triggerPageDownDev.get() != devname:
            self.triggerPageDownDev.set(devname)

    def changeTriggerPageDownChannel(self, channel):
        if self.triggerPageDownChannel.get() != channel:
            self.triggerPageDownChannel.set(channel)

    def changeTriggerPageDownCC(self, cc):
        if self.triggerPageDownCC.get() != cc:
            self.triggerPageDownCC.set(cc)


    def changeTriggerHomeDevice(self, devname):
        if self.triggerHomeDev.get() != devname:
            self.triggerHomeDev.set(devname)

    def changeTriggerHomeChannel(self, channel):
        if self.triggerHomeChannel.get() != channel:
            self.triggerHomeChannel.set(channel)

    def changeTriggerHomeCC(self, cc):
        if self.triggerHomeCC.get() != cc:
            self.triggerHomeCC.set(cc)


    def changeTriggerEndDevice(self, devname):
        if self.triggerEndDev.get() != devname:
            self.triggerEndDev.set(devname)

    def changeTriggerEndChannel(self, channel):
        if self.triggerEndChannel.get() != channel:
            self.triggerEndChannel.set(channel)

    def changeTriggerEndCC(self, cc):
        if self.triggerEndCC.get() != cc:
            self.triggerEndCC.set(cc)








    def timingInDeviceChange(self, *args):
        self.myparent.midiTimingInDevice.set(self.timingIn.get())

    def add(self, label):
        ####tablist, framelist
        number = len(self.tabs.winfo_children())
#        self.tabs.update_idletasks()
        if len(self.tabs.winfo_children()):
            self.outputfr.update_idletasks()
            self.tabs.update_idletasks()
            last = self.tabs.winfo_children()[-1]
#            print last.winfo_width()
            edge = last.winfo_x() + last.winfo_width()
#            print abs(self.outputfr.winfo_width() - edge)
            if abs(self.outputfr.winfo_width() - edge) <= 78:
                row = int(last.grid_info()['row']) + 1
                column = 0
            else:
                row = int(last.grid_info()['row'])
                column = int(last.grid_info()['column']) + 1
        else: edge = row = column = 0

        button = tk.Radiobutton(self.tabs, text=label, indicatoron=False, command=lambda arg1=number: self.frameselect(arg1), value=number, variable=self.currentframe, padx=5, selectcolor="#9999bb")
#        row, column = 0, number
#        self.tablist.append(button)
#        width = 10
#        while column >= width:
#            row += 1
#            column -= width
#        print row, column
        button.grid(row=row, column=column, sticky='ew')
#        self.tabs.update_idletasks()
#        print button.winfo_x(), button.winfo_width()
#        print button.winfo_geometry(), button.winfo_parent()
        frame = tk.Frame(self.nb)
#        frame.grid(row=0, column=0, sticky='nesw')
        self.framelist.append(frame)
        return frame

    def tabsreset(self, event):
#        print "Tabs Reset"
#        print event.width
        row = column = 0
        for index, button in enumerate(self.tabs.winfo_children()):
            self.outputfr.update_idletasks()
            if index:
                last = self.tabs.winfo_children()[index-1]
                if abs(last.winfo_x() + last.winfo_width() - event.width) <= 38:
#                    row = int(last.grid_info()['row']) + 1
                    row += 1
                    column = 0
                else:
#                    row = int(last.grid_info()['row'])
#                    column = int(last.grid_info()['column']) + 1
                    column += 1
            else:
                row = column = 0
            button.grid(row=row, column=column)

    def frameselect(self, index):
        self.showframe.grid_remove()
        self.showframe = self.framelist[index]
        self.showframe.grid(row=0, column=0, sticky='nesw')

    def newinstrument(self):
        number = len(self.instmaybe)
        newinst = instrument(self.myparent, number, '#999999')
        self.addinstpage(newinst)
        self.instmaybe.append(newinst)

    def csdload(self):
        if self.myparent.csdimport:
            base = os.path.dirname(self.myparent.csdimport)
        else:
            base = False
        if base and os.path.realpath(base):
            filetoopen = tkfd.askopenfilename(filetypes=[('Csound', ".csd"), ("All", "*")], initialdir=base)
        else:
            filetoopen = tkfd.askopenfilename(filetypes=[('Csound', ".csd"), ("All", "*")])
        if filetoopen:
            self.myparent.csdimport = filetoopen
            self.csdloadwork(filetoopen)
            lab = os.path.split(filetoopen)
            self.csdpathlabel.configure(text=lab[0]+os.sep)
            self.csdlabel.configure(text=lab[1])

    def csdloadwork(self, filetoopen):
        if filetoopen and os.path.exists(filetoopen):
            file = open(filetoopen)
            if file:
                self.myparent.csdimported = ''
                for line in file:
                    self.myparent.csdimported += line
                self.csdtext.delete(1.0, "end")
                self.csdtext.insert("end", self.myparent.csdimported)

    def addinstpage(self, inst):
        newpage = instrumentpage(self, inst)
        self.instpagelist.append(newpage)
        return newpage

    def removeinstpage(self, inst):
        pass

    def save(self):
        print("Save")

    def okcond(self, event):
        if not event.widget.__class__.__name__.count("Text"):
            self.ok()

    def ok(self, *args):
        self.apply()
        self.cancel()

    def cancel(self, *args):
        self.outputfr.destroy()
        self.myparent.odialogopen = False
        del self.myparent.out

    def audition(self):
        self.myparent.play(instlist = self.instmaybe)
        #self.myparent.play(self.instmaybe, self.sf2list, self.myparent.outputmethod, self.myparent.sr, self.myparent.ksmps, self.myparent.nchnls, self.myparent.audiomodule, self.myparent.dac, self.myparent.b, self.myparent.B, self.myparent.aifffile, self.myparent.wavfile, self.myparent.csdcommandline, self.myparent.csdcommandlineuse)

    def apply(self):
        self.timingInDeviceChange()
        self.triggerSpace.apply()
        self.triggerPageUp.apply()
        self.triggerPageDown.apply()
        self.triggerHome.apply()
        self.triggerEnd.apply()

#        self.myparent.outautoload = self.autoload.get()
#        self.myparent.csdimported = self.csdtext.get(0.0, "end")

        flag = False
        if len(self.instmaybe) != len(self.myparent.instlist):
            flag = True
        else:
            for iind, inst in enumerate(self.instmaybe):
                if iind and len(inst.outlist) != len(self.myparent.instlist[iind].outlist):
                    flag = True
                    break
                elif iind:
                    for pair in inst.__dict__.items():
                        if pair[0] != "outlist" and pair not in self.myparent.instlist[iind].__dict__.items():
                            flag = True
                            break
                    for oind, out in enumerate(inst.outlist):
                        if out.__class__.__name__ != self.myparent.instlist[iind].outlist[oind].__class__.__name__:
                            flag = True
                            break
                        else:
                            if len(out.__dict__.keys()) != len(self.myparent.instlist[iind].outlist[oind].__dict__.keys()):
                                flag = True
                                break
                            else:
                                for pair in out.__dict__.items():
#				    print pair
#				    print self.myparent.instlist[iind].outlist[oind].__dict__.items()
                                    if pair[0] != "instrument" and pair not in self.myparent.instlist[iind].outlist[oind].__dict__.items():
                                        flag = True
                                        break
        if flag:
#            self.myparent.removehidemenu()
            com = comodialog(self.myparent, self.instmaybe)
            if self.myparent.dispatcher.push(com):
                self.myparent.dispatcher.do()
#            self.myparent.instlist = copy.deepcopy(self.instmaybe)
#            self.myparent.createhidemenu()
#        self.myparent.sf2list = copy.deepcopy(self.sf2list)
        for nw in self.myparent.notewidgetlist:
            nw.updateinst()
        color = self.myparent.instlist[self.myparent.hover.hinst].color
        self.myparent.hover.entrycolor = color
        self.myparent.score.itemconfigure(self.myparent.hover.widget, fill=color)
        self.myparent.score.itemconfigure(self.myparent.hover.hnumdisp, fill=color)
        self.myparent.score.itemconfigure(self.myparent.hover.hdendisp, fill=color)
        self.myparent.score.itemconfigure(self.myparent.hover.hvoicedisp, fill=color)

class TriggerKeyInfo:
    def __init__(self, parent):
        self.myparent = parent
        self.devname = ''
        self.channel = 0
        self.cc = 0
        self.value = 127
    def setDevname(self, devname):
        if self.devname != '':
            self.myparent.engine.sendToEngine("triggerDevRemove:"+self.devname)
        self.devname = devname
        self.myparent.engine.sendToEngine("triggerDevAdd:"+devname)
    def setChannel(self, channel):
        self.channel = channel
    def setCC(self, cc):
        self.cc = cc
    def setValue(self, val):
        self.value = val
    def getDevname(self):
        return self.devname
    def getChannel(self):
        return self.channel
    def getCC(self):
        return self.cc
    def getValue(self):
        return self.value
    def trigger(self):
        if self.devname != '' and -1<self.channel<16 and -1<self.cc<127 and -1<self.value<128:
            self.myparent.engine.sendToEngine("trigger:"+self.devname+":"+str(self.channel)+":"+str(self.cc)+":"+str(self.value))

class TriggerKeyFrame:
    def __init__(self, parent, info, name, row_):
        # parent is outputdialog
        self.myparent = parent
        self.name = name
        self.info = info
        self.row = row_
        self.devname = tk.StringVar(value=info.getDevname())
#        self.devname.trace("w", self.devnameChange)
        self.channel = tk.IntVar(value=info.getChannel())
#        self.channel.trace("w", self.channelChange)
        self.cc = tk.IntVar(value=info.getCC())
#        self.cc.trace("w", self.ccChange)
        self.value = tk.IntVar(value=info.getValue())
#        self.value.trace("w", self.valueChange)

        self.triggerFrame = tk.Frame(self.myparent.globalPage, relief="ridge", bd=2)
        self.triggerFrame.rowconfigure(0, weight=0)
        self.triggerFrame.rowconfigure(1, weight=0)
        self.triggerFrame.rowconfigure(2, weight=1)
        self.triggerFrame.columnconfigure(0, weight=0)
        self.triggerFrame.columnconfigure(1, weight=0)
        self.triggerFrame.columnconfigure(2, weight=0)
        self.triggerFrame.columnconfigure(3, weight=0)
        self.triggerFrame.columnconfigure(4, weight=0)
        self.triggerFrame.columnconfigure(5, weight=0)
        self.triggerFrame.columnconfigure(6, weight=0)
        self.triggerFrame.columnconfigure(7, weight=0)
        self.triggerFrame.columnconfigure(8, weight=0)
        self.triggerFrame.columnconfigure(9, weight=0)
        self.triggerFrame.columnconfigure(10, weight=0)
        self.triggerFrame.columnconfigure(11, weight=0)
        self.triggerFrame.columnconfigure(12, weight=0)
        self.triggerFrame.columnconfigure(13, weight=0)
        self.triggerFrame.columnconfigure(14, weight=0)
        self.triggerFrame.columnconfigure(15, weight=0)
        self.triggerFrame.columnconfigure(16, weight=1)
        self.triggerFrame.columnconfigure(17, weight=0)

        self.triggerFrame.grid(row=row_, column=0, sticky='w', padx=10)
        tk.Label(self.triggerFrame, text="MIDI Trigger for {}".format(self.name)).grid(row=0, column=0, columnspan=2, sticky='w')
        self.triggerSelector = tk.Menubutton(self.triggerFrame, textvariable=self.devname, bg="#aa9999", activebackground="#bbaaaa", width=35, relief="raised", padx=0, indicatoron=1)
        self.triggerSelectorMenu = tk.Menu(self.triggerSelector, tearoff=0)
        for devname in self.myparent.myparent.midiOutDevices:
            self.triggerSelectorMenu.add_command(label=devname, command = lambda arg1=devname: self.changeTriggerDevice(arg1))
        self.triggerSelector['menu'] = self.triggerSelectorMenu
        self.triggerSelector.grid(row=1, column=0, columnspan=2, sticky='w')

#        self.channelSelector = tk.Spinbox(self.triggerFrame, width=6, textvariable=self.channel, from_=1, to=16)
#        tk.Label(self.triggerFrame, text="Channel:").grid(row=0, column=3, sticky='w', columnspan=3)
#        self.channelSelector.grid(row=1, column=2, padx=3, sticky='')

        self.channelSelector = tk.Spinbox(self.triggerFrame, width=6, textvariable=self.channel, from_=0, to=127)
        tk.Label(self.triggerFrame, text="Channel:").grid(row=0, column=2, sticky='w', columnspan=2)
        self.channelSelector.grid(row=1, column=2, padx=3, sticky='')

        self.ccSelector = tk.Spinbox(self.triggerFrame, width=6, textvariable=self.cc, from_=0, to=127)
        tk.Label(self.triggerFrame, text="CC:").grid(row=0, column=7, sticky='w', columnspan=2)
        self.ccSelector.grid(row=1, column=7, padx=3, sticky='')

        self.valueSelector = tk.Spinbox(self.triggerFrame, width=6, textvariable=self.value, from_=0, to=127)
        tk.Label(self.triggerFrame, text="Value:").grid(row=0, column=9, sticky='w', columnspan=2)
        self.valueSelector.grid(row=1, column=9, padx=3, sticky='')

    def changeTriggerDevice(self, arg1):
        if self.devname.get() != arg1:
            self.devname.set(arg1)

    def devnameChange(self, *args):
        self.info.setDevname(self.devname.get())

    def channelChange(self, *args):
        self.info.setChannel(self.channel.get())

    def ccChange(self, *args):
        self.info.setCC(self.cc.get())

    def valueChange(self, *args):
        self.info.setValue(self.value.get())

    def apply(self):
        self.devnameChange()
        self.channelChange()
        self.ccChange()
        self.valueChange()

class instrument:
    def __init__(self, parent, number, color):
#        self.myparent = parent
        self.number = number
        self.color = color
        self.outlist = []
        self.mute = 0
        self.solo = 0
        self.gsolo = 0
        self.show = 1

class instrumentpage:
    def __init__(self, parent, inst):
        self.myparent = parent
        self.myinst = inst
        number = self.myinst.number
        self.linelist = []
        self.mute = tk.BooleanVar()
        self.mute.set(self.myinst.mute)
        self.mute.trace("w", self.mutechange)
        self.solo = tk.BooleanVar()
        self.solo.set(self.myinst.solo)
        self.solo.trace("w", self.solochange)
#        self.widget = self.myparent.nb.add('inst%.4d' % number, label='i%d' % number, raisecmd=lambda arg1=0.0: self.canvas.yview_moveto(arg1))
        self.widget = self.myparent.add('i%d' % number)
        self.widget.rowconfigure(0, weight=0)
        self.widget.rowconfigure(1, weight=1)
#        self.widget.rowconfigure(2, weight=1)
#        self.widget.rowconfigure(3, weight=1)
        self.widget.columnconfigure(0, weight=1)
#        self.widget.columnconfigure(1, weight=1)
        self.toprow = tk.Frame(self.widget)
        self.toprow.grid(row=0, column=0, sticky='we')
        self.toprow.columnconfigure(0, weight=0)
        self.toprow.columnconfigure(1, weight=0)
        self.toprow.columnconfigure(2, weight=0)
        self.toprow.columnconfigure(3, weight=1)
        self.canvas = tk.Canvas(self.widget, bd=2, relief="ridge")
        self.canvas.grid(row=1, column=0, sticky='nesw')
        self.canvas.rowconfigure(2, weight=1)
        self.canvas.columnconfigure(0, weight=1)
        self.canvas.bind("<Configure>", self.scrolladjust)
        self.midrow = tk.Frame(self.canvas)
#        self.midrow.grid(row=0, column=0, sticky='we')
        self.midrowoncanvas = self.canvas.create_window(0, 0, window=self.midrow, anchor="nw")
        self.midrow.columnconfigure(0, weight=0)
        self.midrow.columnconfigure(1, weight=1)
        if sys.platform.count("darwin"):
            self.midrow.columnconfigure(0, minsize=self.myparent.w-30)
        else:
            self.midrow.columnconfigure(0, minsize=self.myparent.w-50)
        self.botrow = tk.Frame(self.canvas, bd=5, relief="ridge")
#        self.botrow.grid(row=1, column=0, sticky='we')
        self.botrow.columnconfigure(0, weight=0)
        self.botrow.columnconfigure(1, weight=1)
#        self.scroll = tk.Scrollbar(self.widget, orient='vertical', takefocus=0, troughcolor="#ccaaaa", activebackground="#cc7777", bg="#cc8f8f")
        self.scroll = tk.Scrollbar(self.widget, orient='vertical', takefocus=0)
        self.canvas.config(yscrollcommand=self.scroll.set)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scroll.config(command=self.canvas.yview)
#        self.myparent.outputfr.bind("<Button-4>",
#                              lambda
#                              event, arg1="scroll", arg2=-1, arg3="units":
#                              self.canvas.yview(arg1, arg2, arg3), "+")
#        self.myparent.outputfr.bind("<Button-5>",
#                              lambda
#                              event, arg1="scroll", arg2=1, arg3="units":
#                              self.canvas.yview(arg1, arg2, arg3), "+")
#        self.myparent.outputfr.bind("<MouseWheel>",
#                          lambda
#                          event, arg1="scroll", arg3="units":
#                              self.canvaswheel(arg1, event, arg3), "+")
        self.myparent.outputfr.bind("<Button-4>",
                                    lambda
                                    event, arg1="scroll", arg3="units":
                                    self.canvaswheel(arg1, event, arg3), "+")
        self.myparent.outputfr.bind("<Button-5>",
                                    lambda
                                    event, arg1="scroll", arg3="units":
                                    self.canvaswheel(arg1, event, arg3), "+")
        self.myparent.outputfr.bind("<MouseWheel>",
                                    lambda
                                    event, arg1="scroll", arg3="units":
                                    self.canvaswheel(arg1, event, arg3), "+")
#        self.scroll.grid(row=1, column=1, sticky='ns')
        self.color = tk.StringVar()
        self.color.set(self.myinst.color)
        self.color.trace("w", self.colorchange)
        tk.Label(self.toprow, text='Instrument %d' % number, bd=2, relief="ridge").grid(row=0, column=0, columnspan=3, sticky='w')
        tk.Label(self.toprow, text="Color").grid(row=1, column=0)
        tk.Label(self.toprow, text="Mute").grid(row=1, column=1)
        tk.Label(self.toprow, text="Solo").grid(row=1, column=2)
        self.colorwidget = tk.Frame(self.toprow, width=40, height=40, bg=self.color.get())
        self.colorwidget.grid(row=2, column=0, padx=10)
        self.colorwidget.bind("<Button-1>", self.colorchoose)
        self.mutewidget = tk.Checkbutton(self.toprow, bg='#ffaaaa', text='M', variable=self.mute, indicatoron=1, activebackground='#ffaaaa', selectcolor='#ff0000', width=1, height=1, bd=2, highlightthickness=0)
        self.mutewidget.grid(row=2, column=1, padx=4)
        self.solowidget = tk.Checkbutton(self.toprow, bg='#00aa00', text='S', variable=self.solo, indicatoron=1, activebackground='#00aa00', selectcolor='#00ff00', width=1, height=1, bd=2, highlightthickness=0)
        self.solowidget.grid(row=2, column=2)
#        self.blank = tk.Entry(self.botrow, width=2)
#        self.blank.grid(row=0, column=0, pady=6, padx=20, sticky='w')
#        self.blank.bind("<Tab>", self.outputselect)
#        tk.Label(self.botrow, text="c/s/o").grid(row=1, column=0)
        self.widget.update_idletasks()
        bottomy = self.midrow.winfo_reqheight()
#        print bottomy
        self.botrowoncanvas = self.canvas.create_window(0, bottomy, window=self.botrow, anchor="nw")
#        self.myparent.outputfr.bind("<Return>", self.myparent.ok)
#        self.myparent.outputfr.bind("<Escape>", self.myparent.cancel)
        self.outputselect('m')

    def canvaswheel(self, arg1, event, arg3):
#        print self.myinst.number, self.myparent.currentframe
#        print self.myparent.framelist.index(self.myparent.showframe)
        if self.myinst.number == self.myparent.framelist.index(self.myparent.showframe):
            try:
                if event.delta > 0:
                    self.canvas.yview(arg1, -1, arg3)
                elif event.delta < 0:
                    self.canvas.yview(arg1, 1, arg3)
                elif event.num == 4:
                    self.canvas.yview(arg1, -1, arg3)
                elif event.num == 5:
                    self.canvas.yview(arg1, 1, arg3)
            except:
                try:
                    if event.num == 4:
                        self.canvas.yview(arg1, -1, arg3)
                    elif event.num == 5:
                        self.canvas.yview(arg1, 1, arg3)
                except: pass

#    def canvaswheel(self, arg1, event, arg3):
#        print "Canvas Wheel", event.widget
#        self.canvas.yview(arg1, -event.delta/120, arg3)

    def scrolladjust(self, *args):
        self.widget.update_idletasks()
        if len(self.midrow.winfo_children()):
            midy = self.midrow.winfo_reqheight()
        else:
            midy = 0
        self.canvas.coords(self.botrowoncanvas, 0, midy)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.widget.update_idletasks()
        if self.scroll.get() == (0.0, 1.0):
            self.canvas.yview_moveto(0.0)
            if self.scroll.winfo_ismapped():
                self.scroll.grid_remove()
        else:
            if not self.scroll.winfo_ismapped():
                self.scroll.grid(row=1, column=1, sticky='ns')
        self.canvas.config(scrollregion=(0, 0, 0, self.midrow.winfo_reqheight()+self.botrow.winfo_reqheight()))

    def mutechange(self, *args):
        self.myinst.mute = self.mute.get()

    def solochange(self, *args):
        self.myinst.solo = self.solo.get()
        if self.myinst.solo == 0:
            s = 0
            for i in range(1, len(self.myparent.instmaybe)):
                if self.myparent.instmaybe[i].solo:
                    s = 1
                    break
            self.myparent.instmaybe[0] = s
        else:
            self.myparent.instmaybe[0] = 1

    def colorchange(self, *args):
        self.myinst.color = self.color.get()

    def colorchoose(self, event):
        tempcolor = tkcc.askcolor(self.color.get(), parent=self.widget, title="Select Color")
        if None not in tempcolor:
#            self.myinst.color = '#%02x%02x%02x' % (tempcolor[0][0], tempcolor[0][1], tempcolor[0][2])
            self.myinst.color = tempcolor[1]
            self.color.set(self.myinst.color)
            self.colorwidget.configure(bg=self.color.get())
#            self.myparent.myparent.hover.colorupdate(self.myparent.myparent.hover)
#            for note in self.myparent.myparent.notelist:
#                if note.inst == self.myparent.instmaybe.index(self):
#                    reference = note.widget
#                    self.myparent.myparent.score.itemconfigure(reference, fill=self.color.get(), outline=self.color.get())
#                    for i in range(1, 3):
#                        self.myparent.myparent.score.itemconfigure(reference+i, fill=self.color.get())
#                    self.myparent.myparent.score.itemconfigure(reference+6, fill=self.color.get())

    def lineremove(self, line):
        pass

    def lineadd(self, type):
        pass

    def outputselect(self, event):
#        type = event.widget.get()
#        if event.widget == self.blank:
        if self.myinst.outlist == []:
            type = 'm'
            newout = newline = 0
#            if type == 's' or type == 'S':
#                newout = sf2out(self.myinst)
#                newline = sf2line(self, newout)
#            elif type == 'c' or type == 'C':
#                newout = csdout(self.myinst)
#                newline = csdline(self, newout)
#            elif type == 'o' or type == 'O':
#                newout = oscout(self.myinst)
#                newline = oscline(self, newout)
            if type == 'm' or type == 'M':
                newout = midout(self.myinst)
                print("line 526")
                newline = midline(self, newout)
#                newline = midline(self, newout)
            if newout:
                self.myinst.outlist.append(newout)
                self.linelist.append(newline)
                self.scrolladjust()
                self.canvas.yview_moveto(1.0)

#            self.blank.delete(0,last='end')

class sf2out:
    '''Created only by 's' type selection.

    ...Implemented, but untested!
    '''
    def __init__(self, parent, file=None, bank=None, program=None):
        self.instrument = parent
        self.file = file
        self.bank = bank
        self.program = program
        self.mute = 0
        self.solo = 0
        self.volume = 0
        self.A = 0
        self.D = 0
        self.S = 1
        self.R = 0

class sf2line:
    def __init__(self, parent, out):
        self.page = parent
        self.out = out
        self.flag = 's'
        self.place = self.out.instrument.outlist.index(self.out)
        self.mute = tk.BooleanVar()
        self.mute.set(self.out.mute)
        self.mute.trace("w", self.mutechange)
        self.solo = tk.BooleanVar()
        self.solo.set(self.out.solo)
        self.solo.trace("w", self.solochange)
        self.volume = tk.DoubleVar()
        self.volume.set(self.out.volume)
        self.volume.trace("w", self.volumechange)
        self.sf2file = tk.StringVar()
        try:
            self.sf2file.set(self.out.file.basename)
        except:
            self.sf2file.set("None")
        self.sf2file.trace("w", self.filechange)
        self.bank = tk.StringVar()
        try:
            self.bank.set(self.out.bank)
        except: pass
        self.bank.trace("w", self.bankchange)
        self.program = tk.StringVar()
        try: self.program.set(self.out.program)
        except: pass
        self.program.trace("w", self.programchange)
        self.A = tk.IntVar()
        self.A.set(self.out.A)
        self.A.trace("w", self.Achange)
        self.D = tk.IntVar()
        self.D.set(self.out.D)
        self.D.trace("w", self.Dchange)
        self.S = tk.DoubleVar()
        self.S.set(self.out.S)
        self.S.trace("w", self.Schange)
        self.R = tk.IntVar()
        self.R.set(self.out.R)
        self.R.trace("w", self.Rchange)
        self.csdstring = tk.StringVar()
        self.string = ''
        self.frame = tk.Frame(self.page.midrow, bd=5, relief="ridge")
        self.frame.grid(row=self.place, column=0, columnspan=2, sticky='ew')
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(3, weight=0)
        self.frame.columnconfigure(4, weight=0)
        self.frame.columnconfigure(5, weight=0)
        self.frame.columnconfigure(6, weight=0)
        self.frame.columnconfigure(7, weight=0)
        self.frame.columnconfigure(8, weight=0)
        self.frame.columnconfigure(9, weight=1)
        self.frame.columnconfigure(10, weight=0)
        self.field1 = tk.Entry(self.frame, width=2)
        self.field1.grid(row=0, column=0, sticky='w', pady=10, padx=20)
        self.field1.insert(0, 's')
        self.field1.configure(state='disabled')
        self.mutewidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.mute, bg='#ffaaaa', selectcolor='#996666', padx=2, pady=0, indicatoron=0, activebackground='#ff8888')
        self.mutewidget.grid(row=0, column=1, rowspan=1)
        self.solowidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.solo, bg='#aaffaa', selectcolor='#669966', padx=2, pady=0, indicatoron=0, activebackground='#88ff88')
        self.solowidget.grid(row=0, column=2, rowspan=1)
        tk.Label(self.frame, text="sf2:").grid(row=0, column=3, rowspan=1, columnspan=1, sticky='w')

## FUBAR from here...

        self.field2 = tk.Menubutton(self.frame, textvariable=self.sf2file, width=12, relief="raised", padx=0, indicatoron=1, anchor='w')
        self.field2menu = tk.Menu(self.field2, tearoff=0)
        #### sf2list elements are sf2file instances
        self.field2menu.add_command(label="Load", command=self.load)
        for sf2 in self.page.myparent.sf2list:
            self.field2menu.add_command(label=sf2.basename, command=lambda arg1=sf2: self.changefield2(arg1))

        self.field2['menu'] = self.field2menu
        self.field2.grid(row=0, column=4, rowspan=1, columnspan=1, sticky='w', padx=0)
        self.field2.focus_set()

        tk.Label(self.frame, text="   bank:").grid(row=0, column=5, rowspan=1, columnspan=1, sticky='w')

        self.field3 = tk.Menubutton(self.frame, textvariable=self.bank, width=8, relief="raised", padx=0, indicatoron=1)
        self.field3menu = tk.Menu(self.field3, tearoff=0)
        self.field3['menu'] = self.field3menu
        self.field3.grid(row=0, column=6, rowspan=1, columnspan=1, sticky='w')
        self.setbanks(self.out.file)

        tk.Label(self.frame, text="   prog:").grid(row=0, column=7, rowspan=1, columnspan=1, sticky='w')

        self.field4 = tk.Menubutton(self.frame, textvariable=self.program, width=8, relief="raised", padx=0, indicatoron=1, anchor='w')
        self.field4menu = tk.Menu(self.field4, tearoff=0)
        self.field4['menu'] = self.field4menu
        self.field4.grid(row=0, column=8, rowspan=1, columnspan=1, sticky='w')
        self.setpresets(self.out.file)

## ...TO HERE
        self.x = tk.Button(self.frame, text="x", command=self.remove)
        self.x.grid(row=0, column=10, sticky='e', padx=40)

        self.adsrfr = tk.Frame(self.frame)
        self.adsrfr.grid(row=1, column=0, columnspan=9, sticky='w')
        tk.Label(self.adsrfr, text="Soundfont Output").grid(row=0, column=0, sticky='w')
        tk.Label(self.adsrfr, text="             ADSR (milliseconds)", font=("Times", 9)).grid(row=0, column=1, sticky='w')
        tk.Entry(self.adsrfr, width=6, textvariable=self.A).grid(row=0, column=2, sticky='w')
        tk.Entry(self.adsrfr, width=6, textvariable=self.D).grid(row=0, column=3, sticky='w')
        tk.Entry(self.adsrfr, width=6, textvariable=self.S).grid(row=0, column=4, sticky='w')
        tk.Entry(self.adsrfr, width=6, textvariable=self.R).grid(row=0, column=5, sticky='w')
#        tk.Button(self.adsrfr, text="Test")

        self.volumewidget = tk.Scale(self.frame, orient="horizontal", width=7, fg='#552288', sliderlength=10, sliderrelief='raised', tickinterval=10, from_=-90, to=10, resolution=.1, variable=self.volume)
        self.volumewidget.grid(row=2, column=0, columnspan=11, sticky='ew', pady=2)

## and FUBAR from here...

    def changefield2(self, arg1):
        if self.sf2file.get() != arg1.basename:
            self.sf2file.set(arg1.basename)
            self.bank.set(None)
            self.program.set(None)
            self.field4menu.delete(0, "end")
            try:
                self.setbanks(arg1)
            except: print("Rationale Error: changefield2() failed")

    def changefield3(self, sf2, bank):
        if self.bank.get() != bank:
            self.bank.set(bank)
            self.program.set(None)
            try: self.setpresets(sf2)
            except: print("Rationale Error: changefield3() failed")

    def changefield4(self, prog):
        self.program.set(prog)

    def load(self):
        if self.page.myparent.sf2list:
            base = os.path.dirname(self.page.myparent.sf2list[-1])
        else:
            base = False
        if base and os.path.realpath(base):
            newfile = tkfd.askopenfilename(title="Load Soundfont", filetypes=[("Soundfont 2", ".sf2")], initialdir=base)
        else:
            newfile = tkfd.askopenfilename(title="Load Soundfont", filetypes=[("Soundfont 2", ".sf2")])
#            print newfile
        if newfile and os.path.basename(newfile) != self.sf2file.get():
            base = os.path.basename(newfile)
#            print base
            flag = True
            for element in self.page.myparent.sf2list:
                if element.filename == newfile and flag:
                    flag = False
                    break
            if flag:
                element = sf2file(newfile)
                self.page.myparent.sf2list.append(element)
                self.field2menu.add_command(label=base, command=lambda arg1=element: self.changefield2(arg1))
            self.sf2file.set(base)
            self.bank.set(None)
            self.program.set(None)
            self.setbanks(element)

    def checkforload(self, value):
##      if file is new, add to list, add to history, and parse presets;
##      add presets to another list and to histories for bank and progs
#            print value
        for sf2 in self.page.myparent.sf2list:
            if sf2.basename == value:
                element = sf2
        try:
            self.setbanks(element)
        except: pass

    def setbanks(self, sf2file):
#        print "setbanks:", sf2file
        if sf2file != None:
            keys = [int(key) for key in sf2file.proglist.keys()]
            keys.sort()
            self.field3menu.delete(0, "end")
            for ind, key in enumerate(keys):
                if ind % 30 == 0: colbrk = 1
                else: colbrk = 0
                self.field3menu.add_command(label=str(key), command=lambda arg1=sf2file, arg2=key: self.changefield3(arg1, arg2), columnbreak=colbrk)

            self.field3['menu'] = self.field3menu

    def resetpresets(self, sf2file, *args):
        self.field4.destroy()
        self.setpresets(sf2file, *args)

    def setpresets(self, sf2file, *args):
        if sf2file != None and self.bank.get() != "None":
            progs = sf2file.proglist[self.bank.get()]
            self.field4menu.delete(0, "end")
            for ind, prog in enumerate(progs):
                if ind % 30 == 0: colbrk = 1
                else: colbrk = 0
                self.field4menu.add_command(label=prog, columnbreak=colbrk, command=lambda arg1=prog: self.changefield4(arg1))

    def filechange(self, *args):
        for sf2 in self.page.myparent.sf2list:
            if sf2.basename == self.sf2file.get():
                self.out.file = sf2
                break

    def bankchange(self, *args):
        self.out.bank = self.bank.get()

    def programchange(self, *args):
        self.out.program = self.program.get()

## ...to about HERE

    def mutechange(self, *args):
        self.out.mute = self.mute.get()

    def solochange(self, *args):
        self.out.solo = self.solo.get()

        if self.out.solo == 0:
            s = 0
            for o in self.page.myinst.outlist:
                if o.solo:
                    s = 1
                    break
            self.page.myinst.gsolo = s
        else:
            self.page.myinst.gsolo = 1

    def volumechange(self, *args):
        self.out.volume = self.volume.get()

    def Achange(self, *args):
        try:
            self.out.A = self.A.get()
        except: pass

    def Dchange(self, *args):
        try:
            self.out.D = self.D.get()
        except: pass

    def Schange(self, *args):
        try:
            self.out.S = self.S.get()
        except: pass

    def Rchange(self, *args):
        try:
            self.out.R = self.R.get()
        except: pass

    def remove(self):
        index = self.place
        self.frame.destroy()
        for line in self.page.linelist:
            if line.place > index:
                line.place -= 1
                line.frame.grid(row=line.place)
#        print self.page.myinst.outlist
        del self.page.myinst.outlist[index]
#        print self.page.myinst.outlist
        self.page.widget.update_idletasks()
        if len(self.page.linelist) > 1:
            bottomy = self.page.midrow.winfo_reqheight()
        else:
            bottomy=0
        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
        self.page.scrolladjust()

#        print self.page.linelist
#        print index
        del self.page.linelist[index]
#        print self.page.linelist

class oscout:
    '''Created only by 'o' type selection.'''
    def __init__(self, parent):
        self.instrument = parent
        self.host = 'localhost'
        self.port = '0'
        self.path = '/'
#        self.value = ''
        self.mute = 0
        self.solo = 0
        self.volume = 0
        self.string = ''
        self.noff = 0
        self.noffpath = '/'
        self.noffstring = ''

class oscline:
    def __init__(self, parent, out):
        self.page = parent
        self.out = out
        self.flag = 'o'
        self.place = self.out.instrument.outlist.index(self.out)
        self.mute = tk.BooleanVar(value=self.out.mute)
        self.mute.trace("w", self.mutechange)
        self.solo = tk.BooleanVar(value=self.out.solo)
        self.solo.trace("w", self.solochange)
        self.volume = tk.DoubleVar(value=self.out.volume)
        self.volume.trace("w", self.volumechange)
        self.string = tk.StringVar(value=self.out.string)
        self.string.trace("w", self.stringchange)
        self.host = tk.StringVar(value=self.out.host)
        self.host.trace("w", self.hostchange)
        self.port = tk.IntVar(value=self.out.port)
        self.port.trace("w", self.portchange)
        self.path = tk.StringVar(value=self.out.path)
        self.path.trace("w", self.pathchange)
        self.noff = tk.IntVar(value=self.out.noff)
        self.noff.trace("w", self.noffchange)
        self.noffpath = tk.StringVar(value=self.out.noffpath)
        self.noffpath.trace("w", self.noffpathchange)
        self.noffstring = tk.StringVar(value=self.out.noffstring)
        self.noffstring.trace("w", self.noffstringchange)
####
        self.frame = tk.Frame(self.page.midrow, bd=5, relief="ridge")
        self.frame.grid(row=self.place, column=0, columnspan=2, sticky='ew')
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(3, weight=0)
        self.frame.columnconfigure(4, weight=0)
        self.frame.columnconfigure(5, weight=0)
        self.frame.columnconfigure(6, weight=0)
        self.frame.columnconfigure(7, weight=0)
        self.frame.columnconfigure(8, weight=1)
        self.field1 = tk.Entry(self.frame, width=2)
        self.field1.grid(row=0, column=0, sticky='w', pady=10, padx=20)
        self.field1.insert(0, 'o')
        self.field1.configure(state='disabled')

        tk.Label(self.frame, text="OSC Output").grid(row=1, column=0, sticky='w')
        self.mutewidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.mute, bg='#ffaaaa', selectcolor='#996666', padx=2, pady=0, indicatoron=0, activebackground='#ff8888')
        self.mutewidget.grid(row=0, column=1, rowspan=1)
        self.solowidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.solo, bg='#aaffaa', selectcolor='#669966', padx=2, pady=0, indicatoron=0, activebackground='#88ff88')
        self.solowidget.grid(row=0, column=2, rowspan=1)
        tk.Label(self.frame, text="host:").grid(row=0, column=3, sticky='w')
        self.field2 = tk.Entry(self.frame, width=10, textvariable=self.host)
        self.field2.grid(row=0, column=4, sticky='w')
        self.field2.focus_set()
        self.field2.select_range(0, "end")
#        self.field2.bind("<FocusOut>", self.stringupdate)
        tk.Label(self.frame, text="port:").grid(row=0, column=5, sticky='w')
        self.field3 = tk.Entry(self.frame, width=5, textvariable=self.port)
        self.field3.grid(row=0, column=6, sticky='w')
        tk.Label(self.frame, text="send:").grid(row=0, column=9, sticky='w')
        self.field4 = tk.Entry(self.frame, width=20, textvariable=self.string)
        self.field4.grid(row=0, column=10, sticky='w')
        tk.Label(self.frame, text="path:").grid(row=1, column=3, sticky='w')
        self.field5 = tk.Entry(self.frame, width=15, textvariable=self.path)
        self.field5.grid(row=1, column=4, columnspan=2, sticky='w')

#        self.field5.bind("<FocusOut>", self.stringupdate)
        self.nofffield = tk.Checkbutton(self.frame, variable=self.noff, text="Send Noteoff")
        self.nofffield.grid(row=2, column=0, sticky='')
        tk.Label(self.frame, text="path:").grid(row=2, column=3, sticky='w')
        if self.noff.get() == 0:
            state = "disabled"
        else:
            state = "normal"
        self.noffpathfield = tk.Entry(self.frame, width=15, textvariable=self.noffpath, state=state, disabledbackground="#aaaaaa")
        self.noffpathfield.grid(row=2, column=4, columnspan=2, sticky='w')
        tk.Label(self.frame, text="send:").grid(row=2, column=9, sticky='w')
        self.noffstringfield = tk.Entry(self.frame, width=20, textvariable=self.noffstring, state=state, disabledbackground="#aaaaaa")
        self.noffstringfield.grid(row=2, column=10, sticky='w')

        self.x = tk.Button(self.frame, text="x", command=self.remove)
        self.x.grid(row=0, column=11, sticky='e', padx=40)
        tk.Label(self.frame, text="(inst, voice, time, dur, db, freq, region, num, den, a1, a2...)", font=("Times", 9)).grid(row=1, column=9, columnspan=4, sticky='w', pady=1)
        self.volumewidget = tk.Scale(self.frame, orient="horizontal", width=7, fg='#552288', sliderlength=10, sliderrelief='raised', tickinterval=10, from_=-90, to=10, resolution=.1, variable=self.volume)
        self.volumewidget.set(self.out.volume)
        self.volumewidget.grid(row=3, column=0, columnspan=12, sticky='ew', pady=1)
#        self.page.scrolladjust()
#        self.page.canvas.yview_moveto(1.0)

#        self.page.widget.update_idletasks()
#        bottomy = self.page.midrow.winfo_reqheight()
#        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
#        self.page.canvas.config(scrollregion=self.page.canvas.bbox("all"))
#        self.page.canvas.yview_moveto(1.0)
#        if self.page.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.page.widget.update_idletasks()
##            print self.page.scroll.get()
#            if self.page.scroll.get() != (0.0, 1.0):
#                self.page.scroll.grid(row=1, column=1, sticky='ns')

    def mutechange(self, *args):
        self.out.mute = self.mute.get()

    def solochange(self, *args):
        self.out.solo = self.solo.get()

        if self.out.solo == 0:
            s = 0
            for o in self.page.myinst.outlist:
                if o.solo:
                    s = 1
                    break
            self.page.myinst.gsolo = s
        else:
            self.page.myinst.gsolo = 1

    def volumechange(self, *args):
        self.out.volume = self.volume.get()

    def hostchange(self, *args):
        self.out.host = self.host.get()

    def portchange(self, *args):
        try: self.out.port = self.port.get()
        except: pass

    def pathchange(self, *args):
        self.out.path = self.path.get()

    def stringchange(self, *args):
        self.out.string = self.string.get()

    def noffchange(self, *args):
        self.out.noff = self.noff.get()
        if self.noff.get():
            self.noffpathfield.configure(state="normal")
            self.noffstringfield.configure(state="normal")
        else:
            self.noffpathfield.configure(state="disabled")
            self.noffstringfield.configure(state="disabled")

    def noffpathchange(self, *args):
        self.out.noffpath = self.noffpath.get()

    def noffstringchange(self, *args):
        self.out.noffstring = self.noffstring.get()

    def remove(self):
        index = self.place
        self.frame.destroy()
        for line in self.page.linelist:
            if line.place > index:
                line.place -= 1
                line.frame.grid(row=line.place)
#        print self.page.myinst.outlist
        del self.page.myinst.outlist[index]
#        print self.page.myinst.outlist
        self.page.widget.update_idletasks()
        if len(self.page.linelist) > 1:
            bottomy = self.page.midrow.winfo_reqheight()
        else:
            bottomy=0
        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
        self.page.scrolladjust()
#        if self.page.scroll.winfo_ismapped():
#            self.page.canvas.config(scrollregion=self.page.canvas.bbox("all"))
#            self.page.widget.update_idletasks()
#            if self.page.scroll.get() == (0.0, 1.0):
#                self.page.scroll.grid_remove()
#        print self.page.linelist
#        print index
        del self.page.linelist[index]

class csdout:
    '''Created only by 'c' type selection.'''
    def __init__(self, parent):
        self.instrument = parent
        self.instnum = '"ratdefault"'
        self.pfields = 'db freq'
        self.mute = 0
        self.solo = 0
        self.volume = 0
        self.string = self.instnum + ' time dur ' + self.pfields

class csdline:
    def __init__(self, parent, out):
        self.page = parent
        self.out = out
        self.flag = 'c'
#        self.place = len(self.page.linelist)
        self.place = self.out.instrument.outlist.index(self.out)
        self.mute = tk.BooleanVar()
        self.mute.set(self.out.mute)
        self.mute.trace("w", self.mutechange)
        self.solo = tk.BooleanVar()
        self.solo.set(self.out.solo)
        self.solo.trace("w", self.solochange)
        self.volume = tk.DoubleVar()
        self.volume.set(self.out.volume)
        self.volume.trace("w", self.volumechange)
        self.instnum = tk.StringVar()
        self.instnum.set(self.out.instnum)
        self.instnum.trace("w", self.instnumchange)
        self.csdstring = tk.StringVar()
        self.csdstring.set(self.out.pfields)
        self.csdstring.trace("w", self.csdstringchange)
        self.frame = tk.Frame(self.page.midrow, bd=5, relief="ridge")
        self.frame.grid(row=self.place, column=0, columnspan=2, sticky='ew')
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(3, weight=0)
        self.frame.columnconfigure(4, weight=0)
        self.frame.columnconfigure(5, weight=0)
        self.frame.columnconfigure(6, weight=0)
        self.frame.columnconfigure(7, weight=0)
        self.frame.columnconfigure(8, weight=1)
        self.field1 = tk.Entry(self.frame, width=2)
        self.field1.grid(row=0, column=0, sticky='w', pady=10, padx=20)
        self.field1.insert(0, 'c')
        self.field1.configure(state='disabled')
        tk.Label(self.frame, text="Csound Instrument Output").grid(row=1, column=0, sticky='w', columnspan=6)
        self.mutewidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.mute, bg='#ffaaaa', selectcolor='#996666', padx=2, pady=0, indicatoron=0, activebackground='#ff8888')
        self.mutewidget.grid(row=0, column=1, rowspan=1)
        self.solowidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.solo, bg='#aaffaa', selectcolor='#669966', padx=2, pady=0, indicatoron=0, activebackground='#88ff88')
        self.solowidget.grid(row=0, column=2, rowspan=1)
        tk.Label(self.frame, text="inst").grid(row=0, column=3, rowspan=1, columnspan=1, sticky='w')
        self.field2 = tk.Entry(self.frame, width=10, textvariable=self.instnum)
        self.field2.grid(row=0, column=4, rowspan=1, columnspan=1, sticky='w')
        self.field2.focus_set()
        self.field2.select_range(0, "end")
        self.field2.bind("<FocusOut>", self.stringupdate)
        tk.Label(self.frame, text="   time dur ").grid(row=0, column=5, rowspan=1, columnspan=1)
        self.field3 = tk.Entry(self.frame, width=30, textvariable=self.csdstring)
        self.field3.grid(row=0, column=6, rowspan=1, columnspan=2, sticky='w')
        self.field3.bind("<FocusOut>", self.stringupdate)
        self.x = tk.Button(self.frame, text="x", command=self.remove)
        self.x.grid(row=0, column=9, sticky='e', padx=40)
        tk.Label(self.frame, text="(inst, voice, time, dur, db, freq, region, num, den, a1, a2...)", font=("Times", 9)).grid(row=1, column=6, rowspan=1, columnspan=4, sticky='w', pady=1)
        self.volumewidget = tk.Scale(self.frame, orient="horizontal", width=7, fg='#552288', sliderlength=10, sliderrelief='raised', tickinterval=10, from_=-90, to=10, resolution=.1, variable=self.volume)
        self.volumewidget.set(self.out.volume)
        self.volumewidget.grid(row=2, column=0, columnspan=11, sticky='ew', pady=1)
#        self.page.scrolladjust()
#        self.page.canvas.yview_moveto(1.0)

#        self.page.widget.update_idletasks()
#        bottomy = self.page.midrow.winfo_reqheight()
#        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
#        self.page.canvas.config(scrollregion=self.page.canvas.bbox("all"))
#        self.page.canvas.yview_moveto(1.0)
#        if self.page.scroll.winfo_ismapped():
##            print self.page.scroll.get()
#            pass
#        else:
#            self.page.widget.update_idletasks()
##            print self.page.scroll.get()
#            if self.page.scroll.get() != (0.0, 1.0):
#                self.page.scroll.grid(row=1, column=1, sticky='ns')

#        self.string = ''

    def mutechange(self, *args):
        self.out.mute = self.mute.get()

    def solochange(self, *args):
        self.out.solo = self.solo.get()

        if self.out.solo == 0:
            s = 0
            for o in self.page.myinst.outlist:
                if o.solo:
                    s = 1
                    break
            self.page.myinst.gsolo = s
        else:
            self.page.myinst.gsolo = 1

    def volumechange(self, *args):
        self.out.volume = self.volume.get()

    def instnumchange(self, *args):
        self.stringupdate(self)
        self.out.instnum = self.instnum.get()

    def csdstringchange(self, *args):
        self.stringupdate(self)
        self.out.pfields = self.csdstring.get()

    def stringupdate(self, *args):
        instnum = self.instnum.get()
        try:
            inst = instnum.split()[0]
            csdstring = self.csdstring.get()
            self.out.string = '%s%s%s' % (inst, ' time dur ', csdstring)
        except:
            pass

    def remove(self):
        index = self.place
        self.frame.destroy()
        for line in self.page.linelist:
            if line.place > index:
                line.place -= 1
                line.frame.grid(row=line.place)
#        print self.page.myinst.outlist
        del self.page.myinst.outlist[index]
#        print self.page.myinst.outlist
        self.page.widget.update_idletasks()
        if len(self.page.linelist) > 1:
            bottomy = self.page.midrow.winfo_reqheight()
        else:
            bottomy=0
        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
        self.page.scrolladjust()
#        if self.page.scroll.winfo_ismapped():
#            self.page.canvas.config(scrollregion=self.page.canvas.bbox("all"))
#            self.page.widget.update_idletasks()
#            if self.page.scroll.get() == (0.0, 1.0):
#                self.page.scroll.grid_remove()
#        print self.page.linelist
#        print index
        del self.page.linelist[index]
#        print self.page.linelist
#    def remove(self):
#        index = self.place
#        self.frame.destroy()
#        for line in self.page.linelist:
#            if line.place > index:
#                line.place -= 1
#                line.frame.grid(row=line.place)
#        del self.page.myinst.outlist[index]
#        self.page.widget.update_idletasks()
#        if len(self.page.linelist) > 1:
#            bottomy = self.page.midrow.winfo_reqheight()
#        else:
#            bottomy=0
#        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
#        if self.page.scroll.winfo_ismapped():
#            self.page.canvas.config(scrollregion=self.page.canvas.bbox("all"))
#            self.page.widget.update_idletasks()
#            if self.page.scroll.get() == (0.0, 1.0):
#                self.page.scroll.grid_remove()
#        print self.page.linelist
#        del self.page.linelist[index]

class ratout:
    def __init__(self, parent):
        self.instrument = parent
        self.mute = 0
        self.solo = 0
        self.volume = 0

class ratline:
    def __init__(self, parent, out):
        self.page = parent
        self.out = out
        self.place = len(self.out.instrument.outlist)
#        self.place = self.out.instrument.outlist.index(self.out)
        print("ratline init run")
        self.mute = tk.BooleanVar()
        self.mute.set(self.out.mute)
        self.mute.trace("w", self.mutechange)
        self.solo = tk.BooleanVar()
        self.solo.set(self.out.solo)
        self.solo.trace("w", self.solochange)
        self.volume = tk.DoubleVar()
        self.volume.set(self.out.volume)
        self.volume.trace("w", self.volumechange)
        self.frame = tk.Frame(self.page.midrow, bd=5, relief="ridge")
        self.frame.grid(row=self.place, column=0, columnspan=2, sticky='ew')
        self.mutewidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.mute, bg='#ffaaaa', selectcolor='#996666', padx=2, pady=0, indicatoron=0, activebackground='#ff8888')
        self.mutewidget.grid(row=0, column=1, rowspan=1)
        self.solowidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.solo, bg='#aaffaa', selectcolor='#669966', padx=2, pady=0, indicatoron=0, activebackground='#88ff88')
        self.solowidget.grid(row=0, column=2, rowspan=1)
#        self.x = tk.Button(self.frame, text="x", command=self.remove)
#        self.x.grid(row=0, column=9, sticky='e', padx=40)
#        tk.Label(self.frame, text="(inst, voice, time, dur, db, freq, region, num, den, a1, a2...)", font=("Times", 9)).grid(row=1, column=6, rowspan=1, columnspan=4, sticky='w', pady=1)
#        self.volumewidget = tk.Scale(self.frame, orient="horizontal", width=7, fg='#552288', sliderlength=16, sliderrelief='raised', tickinterval=16, from_=-128, to=127, resolution=1, variable=self.volume)
#        self.volumewidget.set(self.out.volume)
#        self.volumewidget.grid(row=2, column=0, columnspan=11, sticky='ew', pady=1)
        
    def mutechange(self, *args):
        self.out.mute = self.mute.get()

    def solochange(self, *args):
        self.out.solo = self.solo.get()

        if self.out.solo == 0:
            s = 0
            for o in self.page.myinst.outlist:
                if o.solo:
                    s = 1
                    break
            self.page.myinst.gsolo = s
        else:
            self.page.myinst.gsolo = 1

    def volumechange(self, *args):
        self.out.volume = self.volume.get()


    def remove(self):
        index = self.place
        self.frame.destroy()
        for line in self.page.linelist:
            if line.place > index:
                line.place -= 1
                line.frame.grid(row=line.place)
#        print self.page.myinst.outlist
        del self.page.myinst.outlist[index]
#        print self.page.myinst.outlist
        self.page.widget.update_idletasks()
        if len(self.page.linelist) > 1:
            bottomy = self.page.midrow.winfo_reqheight()
        else:
            bottomy=0
        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
        self.page.scrolladjust()
        del self.page.linelist[index]


class midout(ratout):
    def __init__(self, parent, device='', channel=1):
        self.device = device
        self.channel = channel
        super().__init__(parent)

class midline(ratline):
    def __init__(self, parent, out):
        super().__init__(parent, out)
        self.flag = 'm'
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(3, weight=0)
        self.frame.columnconfigure(4, weight=0)
        self.frame.columnconfigure(5, weight=0)
        self.frame.columnconfigure(6, weight=0)
        self.frame.columnconfigure(7, weight=0)
        self.frame.columnconfigure(8, weight=0)
        self.frame.columnconfigure(9, weight=0)
        self.frame.columnconfigure(10, weight=0)
        self.frame.columnconfigure(11, weight=1)
        self.frame.columnconfigure(12, weight=0)
        tk.Label(self.frame, text="MIDI Tuning Standard Instrument Output").grid(row=1, column=3, sticky='w', columnspan=6)
        self.deviceName = tk.StringVar()
        self.deviceName.set(self.out.device)
        self.deviceName.trace("w", self.deviceChange)
        self.channel = tk.IntVar()
        self.channel.set(self.out.channel)
        self.channel.trace("w", self.channelChange)
        tk.Label(self.frame, text="Device:").grid(row=2, column=4, sticky='w', columnspan=3)
        self.deviceSelector = tk.Menubutton(self.frame, textvariable=self.deviceName, bg="#aa9999", activebackground="#bbaaaa", width=35, relief="raised", padx=0, indicatoron=1)
        self.deviceSelectorMenu = tk.Menu(self.deviceSelector, tearoff=0)
        for devname in self.page.myparent.myparent.midiOutDevices:
            self.deviceSelectorMenu.add_command(label=devname, command = lambda arg1=devname: self.changeMidiOutputDev(arg1))
        self.deviceSelector['menu'] = self.deviceSelectorMenu
        self.deviceSelector.grid(row=3, column=4, sticky='w')
        self.channelSelector = tk.Spinbox(self.frame, width=4, textvariable=self.channel, from_=1, to=16)
        tk.Label(self.frame, text="Channel:").grid(row=2, column=8, sticky='w', columnspan=3)
        self.channelSelector.grid(row=3, column=8, padx=3, sticky='')

    def changeMidiOutputDev(self, devname):
        if self.deviceName.get() != devname:
            self.deviceName.set(devname)

    def deviceChange(self, *args):
        self.out.device = self.deviceName.get()

    def channelChange(self, *args):
        self.out.channel = self.channel.get()


class midoutold:
    '''Created only by 'm' type selection.

    ...Not quite implemented!
    '''
    def __init__(self, parent, et=12, base=60, mpcl=[], msgl=[], pd={}, file=None, bank=None, program=None):
        self.instrument = parent
        self.ET = et
        self.base = base
        self.round = True
        self.mod = 'portmidi'
        self.modportchnlist = mpcl
        self.messagelist = msgl
        self.primedict = pd
        self.mute = 0
        self.solo = 0
        self.volume = 0

class midlineold:
    def __init__(self, parent, out):
        self.page = parent
        self.out = out
        self.flag = 'm'
        self.place = self.out.instrument.outlist.index(self.out)
        self.ET = tk.IntVar()
        self.ET.set(self.out.ET)
        self.base = tk.IntVar()
        self.base.set(self.out.base)
        self.round = tk.BooleanVar()
        self.round.set(self.out.round)
        self.mpcwidgetlist = []
        self.mute = tk.BooleanVar()
        self.mute.set(self.out.mute)
        self.mute.trace("w", self.mutechange)
        self.solo = tk.BooleanVar()
        self.solo.set(self.out.solo)
        self.solo.trace("w", self.solochange)
        self.volume = tk.DoubleVar()
        self.volume.set(self.out.volume)
        self.volume.trace("w", self.volumechange)
        self.frame = tk.Frame(self.page.midrow, bd=5, relief="ridge")
        self.frame.grid(row=self.place, column=0, columnspan=2, sticky='ew')
        self.frame.columnconfigure(0, weight=0)
        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(2, weight=0)
        self.frame.columnconfigure(3, weight=0)
        self.frame.columnconfigure(4, weight=0)
        self.frame.columnconfigure(5, weight=0)
        self.frame.columnconfigure(6, weight=0)
        self.frame.columnconfigure(7, weight=0)
        self.frame.columnconfigure(8, weight=0)
        self.frame.columnconfigure(9, weight=0)
        self.frame.columnconfigure(10, weight=0)
        self.frame.columnconfigure(11, weight=1)
        self.frame.columnconfigure(12, weight=0)
        self.field1 = tk.Entry(self.frame, width=2)
        self.field1.grid(row=0, column=0, sticky='w', pady=10, padx=20)
        self.field1.insert(0, 'm')
        self.field1.configure(state='disabled')
        self.mutewidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.mute, bg='#ffaaaa', selectcolor='#996666', padx=2, pady=0, indicatoron=0, activebackground='#ff8888')
        self.mutewidget.grid(row=0, column=1, rowspan=1)
        self.solowidget = tk.Checkbutton(self.frame, height=1, width=1, variable=self.solo, bg='#aaffaa', selectcolor='#669966', padx=2, pady=0, indicatoron=0, activebackground='#88ff88')
        self.solowidget.grid(row=0, column=2, rowspan=1)

        tk.Label(self.frame, text="Module:").grid(row=0, column=3, rowspan=1, columnspan=1, sticky='w')
        if sys.platform.count("win32"):
            self.midimodules = ['portmidi', 'mme', 'winmm']
        elif sys.platform.count("linux"):
            self.midimodules = ['portmidi', 'alsa']
        elif sys.platform.count("darwin"):
            self.midimodules = ['portmidi']
        self.midimodule = tk.StringVar()
        self.midimodule.set("portmidi")
        self.field2 = tk.Menubutton(self.frame, textvariable=self.midimodule, bg="#bbbbaa", activebackground="#ccccaa", width=8, relief="raised", padx=0, indicatoron=1)
        self.field2menu = tk.Menu(self.field2, tearoff=0)
#	self.field2 = tk.OptionMenu(self.frame, self.midimodule, "portmidi")
        for module in self.midimodules:
            self.field2menu.add_command(label=module, command=lambda arg1=module: self.changemidimodule(arg1))
        self.field2['menu'] = self.field2menu
        self.field2.grid(row=0, column=4, rowspan=1, columnspan=1, sticky='w', padx=0)
        self.field2.focus_set()

        tk.Label(self.frame, text="ET:").grid(row=0, column=5, rowspan=1, columnspan=1, sticky='w')
        self.field3 = tk.Entry(self.frame, width=5, textvariable=self.ET)
        self.field3.grid(row=0, column=6, rowspan=1, columnspan=1, sticky='w', padx=0)

        tk.Label(self.frame, text="  1/1:").grid(row=0, column=7, rowspan=1, columnspan=1, sticky='w')
        self.field4 = tk.Spinbox(self.frame, from_=0, to=127, width=5, textvariable=self.base)
        self.field4.grid(row=0, column=8, rowspan=1, columnspan=1, sticky='w')

        tk.Label(self.frame, text="  1/1 Port/Channel:").grid(row=0, column=9, rowspan=1, columnspan=1, sticky='w')
        self.portdevice11 = tk.StringVar()
        self.portdevice11.set("--")
        self.field5 = tk.OptionMenu(self.frame, self.portdevice11, "--")
        self.field5.grid(row=0, column=10, sticky='w')


        self.x = tk.Button(self.frame, text="x", command=self.remove)
        self.x.grid(row=0, column=12, sticky='e', padx=16)

        tk.Label(self.frame, text="MIDI Output    ").grid(row=1, column=0, sticky='w')

####### PORT/CHANNEL #######
        self.modportchnfr = tk.Frame(self.frame, bd=2, relief="ridge")
        self.mpcexpand = tk.StringVar()
        self.mpcexpand.set("+")
        self.mpcbox = tk.Button(self.modportchnfr, textvariable=self.mpcexpand, padx=0, pady=0, command=self.mpcexpcon, font=("Times", 6), width=1)
        self.mpcbox.grid(row=0, column=0)
        self.modportchnfr.columnconfigure(6, weight=1)
        tk.Label(self.modportchnfr, text="Port/Channel Combinations", bd=2, relief="ridge", anchor='w').grid(row=0, column=1, columnspan=6, sticky='ew')
        tk.Checkbutton(self.modportchnfr, text="Round Robin", variable=self.round).grid(row=0, column=7)
        nothing = tk.Label(self.modportchnfr, text="Port/Channel combinations go here.", anchor='w')
        nothing.grid(row=1, column=1, columnspan=7, sticky='w')
        nothing.grid_remove()
        for mpc in self.out.modportchnlist:
            temp = midimpcwidget(self, mpc)
            self.mpcwidgetlist.append(temp)
        for mpcw in self.mpcwidgetlist:
            print(mpcw.mpc.port)
        self.mpcrow = 1
        self.mpcpopulate()

####### MESSAGE #######
        self.msgfr = tk.Frame(self.frame, bd=2, relief="ridge")
        self.msgexpand = tk.StringVar()
        self.msgexpand.set("+")
        self.msgbox = tk.Button(self.msgfr, textvariable=self.msgexpand, padx=0, pady=0, command=self.msgexpcon, font=("Times", 6), width=1)
        self.msgbox.grid(row=0, column=0)
        self.msgfr.columnconfigure(6, weight=1)
        tk.Label(self.msgfr, text="MIDI Messages", bd=2, relief="ridge", anchor='w').grid(row=0, column=1, columnspan=7, sticky='ew')
        nothing2 = tk.Label(self.msgfr, text="MIDI messages go here.", anchor='w')
        nothing2.grid(row=1, column=1, columnspan=7, sticky='w')
        nothing2.grid_remove()
        for msg in self.out.messagelist:
            temp = midimsgwidget(self, msg)
        self.msgrow = 1
        self.msgpopulate()


####### PRIME EQUIVALENTS #######
        self.primefr = tk.Frame(self.frame, bd=2, relief="ridge")
        self.primeexpand = tk.StringVar()
        self.primeexpand.set("+")
        self.primebox = tk.Button(self.primefr, textvariable=self.primeexpand, padx=0, pady=0, command=self.primeexpcon, font=("Times", 6), width=1)
        self.primebox.grid(row=0, column=0)
        self.primefr.columnconfigure(6, weight=1)
        tk.Label(self.primefr, text="Prime Equivalents (Advanced)", bd=2, relief="ridge", anchor='w').grid(row=0, column=1, columnspan=7, sticky='ew')

####### GRID 'EM, GET WID 'EM #######
        self.modportchnfr.grid(row=1, column=1, columnspan=9, sticky='ew')
        self.msgfr.grid(row=2, column=1, columnspan=9, sticky='ew')
        self.primefr.grid(row=3, column=1, columnspan=9, sticky='ew')


        self.volumewidget = tk.Scale(self.frame, orient="horizontal", width=7, fg='#552288', sliderlength=10, sliderrelief='raised', tickinterval=10, from_=-90, to=10, resolution=.1, variable=self.volume)
        self.volumewidget.grid(row=4, column=0, columnspan=11, sticky='ew', pady=2)

    def changemidimodule(self, module):
        print("Change MIDI module to", module)
        self.midimodule.set("%s" % module)

    def mpcpopulate(self, *args):
        todestroy = []
        for child in self.modportchnfr.winfo_children():
            try:
                if int(child.grid_info()['row']):
                    child.grid_forget()
                    todestroy.append(child)
            except:
                pass
        for dest in todestroy:
            dest.destroy()
        mpcrow = 0
        for mpc in self.out.modportchnlist:
            temp = midimpcwidget(self, mpc)
            temp.grid(row=row, column=0, sticky='we')
            mpcrow += 1            

    def msgpopulate(self, *args):
        pass

    def primepopulate(self, *args):
        pass

    def mpcexpcon(self, *args):
        if self.mpcexpand.get() == "+":
            self.mpcexpand.set("-")
            for wid in self.modportchnfr.winfo_children():
                try:
                    if int(wid.grid_info()['row']):
                        wid.grid()
                except:
                    wid.grid()
        else:
            self.mpcexpand.set("+")
            for wid in self.modportchnfr.winfo_children():
                if int(wid.grid_info()['row']):
#                    print wid.grid_info()['row']
                    wid.grid_remove()
#	for wid in self.modportchnfr.winfo_children():
#            print wid.grid_info()['row']

    def msgexpcon(self, *args):
        if self.msgexpand.get() == "+":
            self.msgexpand.set("-")
            for wid in self.msgfr.winfo_children():
                try:
                    if int(wid.grid_info()['row']):
                        wid.grid()
                except:
                    wid.grid()
        else:
            self.msgexpand.set("+")
            for wid in self.msgfr.winfo_children():
                if int(wid.grid_info()['row']):
                    wid.grid_remove()

    def primeexpcon(self, *args):
        if self.primeexpand.get() == "+":
            self.primeexpand.set("-")
            for wid in self.primefr.winfo_children():
                try:
                    if int(wid.grid_info()['row']):
                        wid.grid()
                except:
                    wid.grid()
        else:
            self.primeexpand.set("+")
            for wid in self.primefr.winfo_children():
                if int(wid.grid_info()['row']):
                    wid.grid_remove()

    def roundchange(self, *args):
        pass

    def basechange(self, *args):
        pass

    def ETchange(self, *args):
        pass

    def mutechange(self, *args):
        self.out.mute = self.mute.get()

    def solochange(self, *args):
        self.out.solo = self.solo.get()

        if self.out.solo == 0:
            s = 0
            for o in self.page.myinst.outlist:
                if o.solo:
                    s = 1
                    break
            self.page.myinst.gsolo = s
        else:
            self.page.myinst.gsolo = 1

    def volumechange(self, *args):
        self.out.volume = self.volume.get()

    def remove(self):
        index = self.place
        self.frame.destroy()
        for line in self.page.linelist:
            if line.place > index:
                line.place -= 1
                line.frame.grid(row=line.place)
#        print self.page.myinst.outlist
        del self.page.myinst.outlist[index]
#        print self.page.myinst.outlist
        self.page.widget.update_idletasks()
        if len(self.page.linelist) > 1:
            bottomy = self.page.midrow.winfo_reqheight()
        else:
            bottomy=0
        self.page.canvas.coords(self.page.botrowoncanvas, 0, bottomy)
        self.page.scrolladjust()

#        print self.page.linelist
#        print index
        del self.page.linelist[index]
#        print self.page.linelist

class midimpc:
    def __init__(self, module="portmidi", port="0", channel=(1,16), base=False):
        self.module = module
        self.port = port
        self.channel = channel
        self.base = base

class midimpcwidget(tk.Frame):
    def __init__(self, parent, mpc):
        tk.Frame.__init__(self)
        self.myparent = parent
        self.mpc = mpc

class midimsg:
    def __init__(self, code="cc", msb=0, lsb=0, offset=0, pernote=True):
        self.code = code
        self.msb = msb
        self.lsb = lsb
        self.offset = offset
        self.pernote = pernote

class midimsgwidget:
    def __init__(self, parent, msg):
        self.myparent = parent
        self.msg = msg
        self.csdstring = tk.StringVar()
        self.string = ''

    def csdstringchange(self, *args):
        self.stringupdate(self)
        self.out.pfields = self.csdstring.get()

    def stringchange(self, *args):
        self.out.string = self.string.get()

    def stringupdate(self, *args):
        instnum = self.instnum.get()
        try:
            inst = instnum.split()[0]
            csdstring = self.csdstring.get()
            self.out.string = '%s%s%s' % (inst, ' time dur ', csdstring)
        except:
            pass


class sf2file:
    def __init__(self, filename):
        self.filename = filename
        self.basename = os.path.basename(filename)
        self.proglist = {}
        self.getpresets()

    def getpresets(self):
        try:
            result = subprocess.Popen((sys.executable, 'ratsf2list.py', self.filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if sys.platform.count('win32'):
                presets = result[0].split(os.linesep)
            else:
                presets = result[1].split(os.linesep)
            startflag = 'Preset list'
            flag = 0
            result = []
            for line in presets:
                if line.count(startflag):
                    flag = 1
                elif flag == 1:
                    if not line.count('prog:'):
                        flag = 0
                    else:
                        ind = line.split()[0][:-1]
                        name = line.split()[1]
                        for word in line.split()[2:-2]:
                            name += ' %s' % word
                        prog = line.split()[-2].split(':')[1]
                        bank = line.split()[-1].split(':')[1]
                        if bank in self.proglist.keys():
                            self.proglist[bank].append('%s %s' % (prog, name))
                        else:
                            self.proglist[bank] = ['%s %s' % (prog, name)]
#                        result.append((bank, prog, name))
##                        sys.stdout.write('%s"%s %s%s' % (bank, prog, name, os.linesep))
#
#
#            print "presets:", presets
#            for prog in presets[:-1]:
#                tempset = [str for str in prog.split('"')]
#                try: self.proglist[tempset[0]].append(tempset[1])
##                self.proglist.append(tuple(tempset))
#                except: self.proglist[tempset[0]] = [tempset[1]]
##            print self.proglist
        except:
            print("Unable to get presets")


class comodialog(object):
    def __init__(self, parent, instlist):
        self.myparent = parent
        self.instlist = instlist
        self.string = "Output Changes"

    def do(self):
        self.myparent.removehidemenu()
        self.myparent.instlist, self.instlist = self.instlist, self.myparent.instlist
        for ind in range(len(self.instlist), len(self.myparent.instlist)):
            self.myparent.engine.sendToEngine("addInst:"+str(ind))
        self.myparent.engine.sendToEngine("resetOuts")
        for inst in range(1,len(self.myparent.instlist)):
            for out in self.myparent.instlist[inst].outlist:
                self.myparent.engine.sendToEngine("addOut:"+str(inst)+":"+str(out.__class__)[16:-2]+":"+str(out.device)+":"+str(out.channel))
        if self.myparent.mode.get() == 0:
            self.myparent.hover.colorupdate()
        for nw in self.myparent.notewidgetlist:
            nw.updateinst()
        self.myparent.createhidemenu()

    def undo(self):
        self.myparent.removehidemenu()
        self.myparent.instlist, self.instlist = self.instlist, self.myparent.instlist
        for ind in range(len(self.instlist)-1, len(self.myparent.instlist)-1, -1):
            self.myparent.engine.sendToEngine("unAddInst:"+str(ind))
        if self.myparent.mode.get() == 0:
            self.myparent.hover.colorupdate()
        for nw in self.myparent.notewidgetlist:
            nw.updateinst()        
        self.myparent.createhidemenu()

