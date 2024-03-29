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
#import tkFileDialog as tkfd
import tkinter.filedialog as tkfd
import copy
import os
import sys
import pickle
import math

class NoteBankNoteInfo(object):
    def __init__(self, fractionOfOctave, name):
        self.fractionOfOctave = fractionOfOctave
        self.name = name
    def setFraction(self, fractionOfOctave):
        self.fractionOfOctave = fractionOfOctave
    def setName(self, name):
        self.name = name
    def getFraction(self):
        return self.fractionOfOctave
    def getName(self):
        return self.name

class NoteBankNote(object):
    def __init__(self, name=None):
        self.name = name
        self.centOffset = None
        self.num = None
        self.den = None
        self.fractionOfOctave = 0
    def setName(self, name):
        self.name = name
    def getName(self):
        if self.name:
            return self.name
        elif self.num and self.den:
            return str(self.num)+"/"+str(self.den)
        elif self.centOffset:
            return str(self.centOffset)
            
    def getFractionOfOctave(self):
        return self.fractionOfOctave

class RatioNote(NoteBankNote):
    def __init__(self, num=1, den=1, name=None):
        super().__init__(name)
        self.num = num
        self.den = den
        self.centOffset = None
        self.setFractionOfOctave()
    def getCents(self):
        cent = pow(2,(1/1200))
        return math.log(num/den)/math.log(cent)
    def setFractionOfOctave(self):
        if self.num > 0 and self.den > 0:
            self.fractionOfOctave = math.log2(self.num/self.den)
        else:
            print("Error setting fractionOfOctave:", self.num, self.den)
    def getInfo(self):
        if self.name == None:
            return NoteBankNoteInfo(self.fractionOfOctave, [str(self.num), str(self.den)])
        else:
            return NoteBankNoteInfo(self.fractionOfOctave, [self.name])

class CentNote(NoteBankNote):
    def __init__(self, centOffset=0, name=None):
        super().__init__(name)
        self.centOffset = centOffset
        self.num = self.den = None
        self.setFractionOfOctave()
    def getCents(self):
        return centOffset
    def setFractionOfOctave(self):
        self.fractionOfOctave = self.centOffset/1200
    def getInfo(self):
        if self.name == None:
            return NoteBankNoteInfo(self.fractionOfOctave, [str(self.centOffset)])
        else:
            return NoteBankNoteInfo(self.fractionOfOctave, [self.name])

class NoteBank(object):
    def __init__(self):
        self.notes = []
        self.repeat = True
    def addNote(self, note):
        self.notes.append(note)
    def getClosestTo(self, fractionOfOctave):
        self.sort()
        noteBankIndex = -1
        currentNote = RatioNote(1, 1)
        targetValue = [1, 1, 0] # num, den, cents
        register = 0
        repeatFraction = 0
        # the vertical position in fractions of octaves; the label; and the register (which octave, et al)
        # the note bank assumes 1/1, so its members go from the next note until the top
        if self.repeat:
            repeatFraction = self.notes[-1].getFractionOfOctave()
            # 1/1 = 0
            # 2/1 = 1
            # 4/1 = 2
            # 1/2 = -1
            register = fractionOfOctave // repeatFraction
            fractionOfOctave -= register
        else:
            repeatFraction = 0
        while noteBankIndex < len(self.notes)-1 and abs(self.notes[noteBankIndex+1].getFractionOfOctave() - fractionOfOctave) < abs(currentNote.getFractionOfOctave - fractionOfOctave):
            noteBankIndex += 1
            currentNote = self.notes[noteBankIndex]
        if self.repeat and noteBankIndex == len(self.notes)-1:
            register += 1
        # return the note in  question, the number of "octaves" from 1/1, and the "octave" note
        return (currentNote, register, self.notes[-1])

#        closestInfo = currentInfo = self.notes[noteBankIndex].getInfo()
#        min = -math.inf
        
        
    def sort(self):
        self.notes.sort(key=lambda note: note.getFractionOfOctave())
#    def createScalaFileText(self):
        

        
class ScalaFileText(object):
    def __init__(self, path=None):
        self.setPath(path)
        self.lines = []
 #       self.file = None
        if path and os.path.exists(path):
            try:
                self.readFromDisk()
            except:
                print("Unable to open Scala file:", self.path, file=sys.stderr)
    def setPath(self, path):
        self.path = path
    def readFromText(self, txt):
        self.lines = txt.split(os.linesep)
#        print(self.lines, file=sys.stderr)
    def readFromDisk(self):
        if self.path == None:
            return
        file = open(self.path)
        file.seek(0)
        self.lines = file.readlines()
        file.close()
    def writeToDisk(self, targetPath=None):
        if self.path == None:
            return
        if targetPath == None:
            targetPath = self.path
        if os.path.exists(targetPath):
            fileContentCheck = open(targetPath, 'r')
            fileContentCheckText = fileContentCheck.readlines()
            if fileContentCheckText == self.lines:
                fileContentCheck.close()
                return 1
        fileToWrite = open(targetPath, 'w')
        for ln in self.lines:
            fileToWrite.write(ln + os.linesep)
        fileToWrite.close()
        return 0
    def parseToNoteBank(self):
        notes = [ln.split('!')[0] for ln in self.lines if len(ln) and ln[0] != '!'][2:]
        newNoteBank = NoteBank()
        negativeCentNotes = []
        for note in notes:
            if note == '' or len(note) == 0:
                continue

            splt = note.split()
            if len(splt) == 0:
                continue
            val = splt[0]
            name = None
            for s in splt[1:]:
                if s:
                    name = s
                    break
            valid = True
            if val.count('-'):
                if not val.count('.'):
                    continue
                if val.count('-')>1:
                    continue
                if val.index('-') != 0:
                    continue
            if val.count('/') > 1 or val.count('.') > 1 or (val.count('/') and val.count('.')):
                continue
            for c in val:
                if not c.isdigit() and c != '-' and c != '/' and c != '.':
                    valid = False
                    break
            if not valid:
                continue
            if val.count('.'):
                ## I still have to decide how to handle negative cent values (which seem ludicrous to me, but are allowed in the specification)
                ## I suppose I check the highest note value, and insert a note so many cents down from that; but if that note is a ratio, I have not
                ## included any way of handling a note with both ratio and cent values.
                ## I suppose if the repeat note were a ratio, I would convert it to cents!
                centOffset = float(val)
                if centOffset > 0:
                    newNoteBank.addNote(CentNote(centOffset, name))
                elif centOffset < 0:
                    negativeCentNotes.append((centOffset, name))
            elif val[0] != '/' and val[-1] != '/':
                if val.count('/'):
                    numden = val.split('/')
                    num = int(numden[0])
                    den = int(numden[1])
                    if num < 1 or den < 1:
                        continue
                else:
                    num = int(val)
                    den = 1
                newNoteBank.addNote(RatioNote(num, den, name))
        newNoteBank.sort()
        if len(negativeCentNotes):
            maxNote = newNoteBank.notes[-1]
            maxCents = maxNote.getCents()
            for negativeCentNote in negativeCentNotes:
                cents = negativeCentNote[0]
                name = negativeCentNote[1]
                # Make sure it's not higher than the maximum cents (the repeat point)
                while cents > maxCents:
                    cents -= maxCents
                if cents != maxCents:
                    newNoteBank.addNote(CentNote(cents, name))
            newNoteBank.sort()
        return newNoteBank

# This class will probably be removed, or at least not implemented yet:
#class nnotebankline(tk.Toplevel):
#    def __init__(self, note):
#        self.myNote = note
#        self.text = TkStringVar()
#        self.text.set(note.getName())
        

class nnotebankdialog(tk.Toplevel):
    # The new version requires:
    # Load SCL button (file dialog)
    # Load into (merge) (file dialog)
    # Save SCL (file dialog if no filename)
    # Save as SCL (file dialog)
    # Filename (label)
    # SCL text field
    # Scroll for SCL text field
    # List of notes (text field disabled)
    # Scroll for List of notes
    # Tabs for different banks
    # OK / Apply / Cancel
        # Add ratio (entry field, button)
        # Add cent value (entry field, button)
        # Optional name field for each degree (entry field)
        # X button to remove each degree
        # Scale info field (label and edit button)
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent.myparent, width=640, height=480)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.myparent = parent
        if sys.platform.count("win32"):
            try: self.iconbitmap('rat32.ico')
            except: pass
#        self.bind("<Return>", self.indirectok)
        self.bind("<Escape>", self.cancel)
        self.title("Edit Notebanks")
        self.notebankmaybe = copy.deepcopy(self.myparent.notebanklist)
        self.noteBankListMaybe = copy.deepcopy(self.myparent.noteBankList)
        self.scalaFileListMaybe = copy.deepcopy(self.myparent.scalaFileList)
        defnotebank = [(1, 1), (33, 32), (21, 20), (16, 15), (15, 14), (14, 13), (13, 12), (12, 11), (11, 10), (10, 9), (9, 8), (8, 7), (7, 6), (13, 11), (32, 27), (6, 5), (11, 9), (16, 13), (5, 4), (81, 64), (14, 11), (9, 7), (13, 10), (21, 16), (4, 3), (11, 8), (18, 13), (7, 5), (10, 7), (13, 9), (16, 11), (3, 2), (32, 21), (20, 13), (14, 9), (11, 7), (128, 81), (8, 5), (13, 8), (18, 11), (5, 3), (27, 16), (22, 13), (12, 7), (7, 4), (16, 9), (9, 5), (20, 11), (11, 6), (24, 13), (13, 7), (28, 15), (15, 8), (40, 21), (64, 33), (2, 1)]
        self.defnotebank = parent.scalaFileList[0].parseToNoteBank()
#        for ratio in defnotebank[1:]:
#            self.defnotebank.addNote(RatioNote(ratio[0], ratio[1]))
        self.grid_propagate(0)
        row = column = ht = 0
        numdenlist = []
        notincluded = []
        self.selectfr = tk.Frame(self)
        for i in range(100):
            self.selectfr.columnconfigure(i, minsize=30)
        self.selectfr.bind("<Configure>", self.selectfrreset)
        self.selectfr.grid(row=0, column=0, columnspan=1, sticky='w', padx=20)
        self.mainfr = tk.Frame(self)
        self.mainfr.bind("<Return>", self.indirectok)
        self.mainfr.rowconfigure(0, weight=1)
        self.mainfr.rowconfigure(1, weight=0)
        self.mainfr.rowconfigure(2, weight=0)
        self.mainfr.rowconfigure(3, weight=0)
        self.mainfr.rowconfigure(4, weight=0)
        self.mainfr.rowconfigure(5, weight=0)
        self.mainfr.rowconfigure(6, weight=0)
        self.mainfr.rowconfigure(7, weight=0)
        self.mainfr.rowconfigure(8, weight=1)
        self.mainfr.columnconfigure(0, weight=1)
        self.mainfr.columnconfigure(8, weight=1)
        self.mainfr.grid(row=1, column=0, sticky='nesw')
        self.current = tk.IntVar(value=0)
        self.primelist = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
        self.primelimit = tk.IntVar(value=self.myparent.primelimit)
        self.availableratios = self.unusedratios = []
        for scl in self.scalaFileListMaybe:
            self.bankadd(scl)
#        for ind, nb in enumerate(self.notebankmaybe):
#            self.bankadd(nb)
#            tk.Button(self.selectfr, text="%s" % ind, command=lambda arg1=ind: self.choosebank(arg1)).grid(row=0, column=ind)

        tk.Button(self.mainfr, text="Save...", command=self.save).grid(row=4, column=0)
        tk.Button(self.mainfr, text="Load", command=self.load).grid(row=5, column=0)

        tk.Label(self.mainfr, text="Current Scala File").grid(row=1, column=1, columnspan=1)
        self.sclTextScroll = tk.Scrollbar(self.mainfr)
        self.sclTextScroll.grid(row=2, column=2, rowspan=5, sticky='ns')
        self.inratios = tk.Listbox(self.mainfr, height=15, width=10, yscrollcommand=self.sclTextScroll.set, selectmode="extended")
#        self.inratios.grid(row=2, column=1, rowspan=5)
        self.sclText = tk.Text(self.mainfr, height=20, width=25, yscrollcommand=self.sclTextScroll.set, spacing3=3, wrap='word')
        self.sclText.grid(row=2, column=1, rowspan=5)
        self.sclTextScroll.config(command=self.sclText.yview)

        tk.Label(self.mainfr, text="Just the Notes").grid(row=1, column=5, columnspan=1)
        self.noteListScroll = tk.Scrollbar(self.mainfr)
        self.noteListScroll.grid(row=2, column=6, rowspan=5, sticky='ns')
        self.outratios = tk.Listbox(self.mainfr, height=15, width=10, yscrollcommand=self.noteListScroll.set, selectmode="extended")
#        self.outratios.grid(row=2, column=5, rowspan=5)
        self.noteList = tk.Text(self.mainfr, height=20, width=15, yscrollcommand=self.noteListScroll.set, state='disabled', spacing3=3, relief='groove')
        self.noteList.grid(row=2, column=5, rowspan=5)
        self.noteListScroll.config(command=self.noteList.yview)
        self.setScalaText()
        self.setNoteList()
        self.sclText.bind("<KeyRelease>", self.updateNoteList)
                                            




        for ratio in self.notebankmaybe[0].numdenlist:
            self.inratios.insert("end", '%4d : %d' % (ratio[0], ratio[1]))

        self.setratiosfromprime(self.primelimit.get())

#        tk.Label(self.mainfr, text="Prime Limit").grid(row=2, column=7, sticky='s')
        self.primeselector = tk.Menubutton(self.mainfr, textvariable=self.primelimit, width=4, relief="raised", padx=0, indicatoron=1, anchor='w')
        self.primemenu = tk.Menu(self.primeselector, tearoff=0)
        for prime in self.primelist:
            self.primemenu.add_command(label=prime, command=lambda arg1=prime: self.setprimelimit(arg1))

        self.primeselector['menu'] = self.primemenu
#        self.primeselector.grid(row=3, column=7, sticky='n')

#        tk.Button(self.mainfr, text="->", command=self.ratioremove).grid(row=3, column=3, columnspan=2)
#        tk.Button(self.mainfr, text="<-", command=self.ratioadd).grid(row=4, column=3, columnspan=2)
        self.toadd = tk.StringVar()
        self.toadd.trace("w", self.findinverse)
#        tk.Label(self.mainfr, text="Enter Ratio").grid(row=5, column=3, sticky='s')
        self.addbox = tk.Entry(self.mainfr, textvariable=self.toadd, width=6)
#        self.addbox.grid(row=6, column=3, sticky='n')
        self.addbox.bind("<Return>", self.addjust)
#        tk.Button(self.mainfr, text="Just Ratio", command=self.addjust).grid(row=7, column=3)
#        tk.Label(self.mainfr, text='Ratio & Inverse').grid(row=6, column=4, sticky='s')
        self.inverse = tk.Button(self.mainfr, text="", command=self.addinverse)
#        self.inverse.grid(row=7, column=4, sticky='n')

        self.buttonfr = tk.Frame(self, width=640, height=80, borderwidth=1, relief="raised")
        self.buttonfr.grid(row=4, column=0, sticky='', ipady=20)
        self.buttonfr.rowconfigure(0, weight=1)
        tk.Button(self.buttonfr, text="OK", command=self.ok).grid(row=0, column=0, padx=10)
        tk.Button(self.buttonfr, text="Cancel", command=self.cancel).grid(row=0, column=1, padx=10)
        tk.Button(self.buttonfr, text="Apply", command=self.apply).grid(row=0, column=2, padx=10)
        tk.Button(self.buttonfr, text="Clear", command=self.clear).grid(row=0, column=3, padx=10)
        tk.Button(self.buttonfr, text="New Bank", command=self.bankadd).grid(row=0, column=4, padx=10)
        tk.Button(self.buttonfr, text="Default", command=self.setdefault).grid(row=0, column=5, padx=10)

    def setScalaText(self):
        #sclText
        #noteList
        #self.myparent.scalaFileList
        ind = self.current.get()
        self.sclText.delete('1.0', 'end')
        for line in self.scalaFileListMaybe[ind].lines:
            if len(line) and line[-1] != '\n' and line[-1] != os.linesep:
                line += os.linesep
            self.sclText.insert('end', line)


    def setNoteList(self):
        ind = self.current.get()
        
        self.noteList.config(state='normal')
        self.noteList.delete('1.0', 'end')
        for note in self.noteBankListMaybe[ind].notes:
            self.noteList.insert('end', note.getName() + '\n')
        self.noteList.config(state='disabled')
        
    def updateNoteList(self, *kw):
        ind = self.current.get()
        self.scalaFileListMaybe[ind].readFromText(self.sclText.get('1.0', 'end'))
        self.noteBankListMaybe[ind] = self.scalaFileListMaybe[ind].parseToNoteBank()
        self.setNoteList()

    def selectfrreset(self, event):
        row = column = 0
        for index, button in enumerate(self.selectfr.winfo_children()):
            self.update_idletasks()
            if index:
                last = self.selectfr.winfo_children()[index-1]
                if abs(last.winfo_x() + last.winfo_width() - event.width) <= 28:
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

    def bankadd(self, nb=None):
        number = len(self.selectfr.winfo_children())
        if len(self.selectfr.winfo_children()):
#            self.outputfr.update_idletasks()
            self.selectfr.update_idletasks()
            last = self.selectfr.winfo_children()[-1]
            edge = last.winfo_x() + last.winfo_width()
            if abs(self.winfo_width() - edge) <= 78:
                row = int(last.grid_info()['row']) + 1
                column = 0
            else:
                row = int(last.grid_info()['row'])
                column = int(last.grid_info()['column']) + 1
        else: edge = row = column = 0

        button = tk.Radiobutton(self.selectfr, text=str(number), indicatoron=False, command=lambda arg1=number: self.choosebank(arg1), value=number, variable=self.current, padx=5, selectcolor="#9999bb")
        button.grid(row=row, column=column, sticky='ew')

        if not nb:
            nb = ScalaFileText('Rationale13.scl')
#            nb = notebank(copy.copy(self.defnotebank))
            self.scalaFileListMaybe.append(nb)
            self.noteBankListMaybe.append(nb.parseToNoteBank())
            
#        frame = tk.Frame(self.nb)
#        self.framelist.append(frame)
#        return frame


    def addjust(self, *args):
        rat = None
        for char in self.toadd.get():
            if not char.isdigit():
                rat = self.toadd.get().split(char)
                break
        if rat:
            if len(rat)==2 and rat[1].isdigit():
                while float(rat[0])/float(rat[1]) < 1:
                    rat[0] = int(rat[0]) * 2
                while float(rat[0])/float(rat[1]) >= 2:
                    rat[1] = int(rat[1]) * 2
                self.addthis(rat)



    def addthis(self, rat):
        rat = (int(rat[0]), int(rat[1]))
        if rat not in self.notebankmaybe[self.current.get()].numdenlist:
            for i, existing in enumerate(self.notebankmaybe[self.current.get()].numdenlist):
                if float(existing[0])/float(existing[1]) > float(rat[0])/float(rat[1]):
                    self.notebankmaybe[self.current.get()].numdenlist.insert(i, rat)
                    self.inratios.insert(i, '%4d : %d' % (int(rat[0]), int(rat[1])))
                    break
        for i, pair in enumerate(self.outratios.get(0, "end")):
            if pair == '%4d : %d' % (int(rat[0]), int(rat[1])):
                self.outratios.delete(i)
                break

    def findinverse(self, *args):
        self.inverse.config(text="")
        if not self.toadd.get().isdigit():
            for char in self.toadd.get():
                if not char.isdigit():
                    rat = (self.toadd.get().split(char))
                    if len(rat) == 2 and rat[0] and rat[1]:
                        inv = [int(rat[1]), int(rat[0])]
                        while inv[0] < inv[1]:
                            if inv[1] % 2:
                                inv[0] *= 2
                            else:
                                inv[1] /= 2
                        while inv[0] > 2*inv[1]:
                            if inv[0] % 2:
                                inv[1] *= 2
                            else:
                                inv[0] /= 2
                        self.inverse.config(text='%d : %d' % (inv[0], inv[1]))

    def addinverse(self, *args):
        addtup = self.inverse.cget("text").split(':')
        if len(addtup) == 2 and addtup[0].isnumeric and addtup[1].isnumeric:
            self.addjust()
            self.addthis(self.inverse.cget("text").split(':'))

    def ratioadd(self, *args):
        for ind in reversed(self.outratios.curselection()):
            ind = int(ind)
            ratadd = self.outratios.get(ind).split(':')
            for i, rat in enumerate(self.notebankmaybe[self.current.get()].numdenlist):
                if float(rat[0])/rat[1] > float(ratadd[0])/float(ratadd[1]):
                    self.inratios.insert(i, self.outratios.get(ind))
                    self.notebankmaybe[self.current.get()].numdenlist.insert(i, (int(ratadd[0]), int(ratadd[1])))
                    break
            self.outratios.delete(ind)
            ### insert into inratios?

    def ratioremove(self, *args):
        for ind in reversed(self.inratios.curselection()):
            ind = int(ind)
            rat = self.notebankmaybe[self.current.get()].numdenlist[ind]
            if rat in self.availableratios:
                for i, existing in enumerate(self.outratios.get(0, "end")):
                    e = existing.split(':')
                    if float(e[0].strip())/float(e[1].strip()) > float(rat[0])/rat[1]:
                        self.outratios.insert(i, '%4d : %d' % (int(rat[0]), int(rat[1])))
                        break
            self.inratios.delete(ind)
            self.notebankmaybe[self.current.get()].numdenlist.pop(ind)

    def setratiosfromprime(self, limit):
        ratios = []
        powers = []
        powerlimits = []
        primes = [p for p in self.primelist if p <= limit]
        if limit >= 3:
            powers.append(-3)
            powerlimits.append(4)
            if limit >= 5:
                powers.append(-2)
                powerlimits.append(2)
                if limit >= 7:
                    powers.append(-2)
                    powerlimits.append(2)
                    for factor in primes:
                        if factor > 7:
                            powers.append(-1)
                            powerlimits.append(1)
        default = copy.copy(powers)
        length = len(powers)
        while powers[0] <= 3:
            n = d = t = 0
            for i in powers:
                if i > 0:
                    n += i
                    t += 1
                elif i < 0:
                    d -= i
                    t += 1
            if n < 4 and d < 4 and n + d < 4 and t < 4:
                ratios.append(copy.copy(powers))
            powers = self.powerincrement(powers, default, powerlimits)
        for ind, rat in enumerate(ratios):
            num = den = 1
            for i, prime in enumerate(primes):
                if rat[i] > 0:
                    num *= prime**rat[i]
                elif rat[i] < 0:
                    den *= prime**(-rat[i])
            while float(num)/den < 1: num *= 2
            while float(num)/den >= 2: den *= 2
            ratios[ind] = (num, den)
        ratios.sort(key=self.ratiosorter)
        self.availableratios = ratios
        self.outratios.delete(0, "end")
        for rat in self.availableratios:
            if rat not in self.notebankmaybe[self.current.get()].numdenlist:
                self.outratios.insert("end", '%4d : %d' % (rat[0], rat[1]))

    def ratiosorter(self, tup):
        return tup[0]/tup[1]

    def compareratios(self, tup1, tup2):
        if float(tup1[0])/tup1[1] - float(tup2[0])/tup2[1] < 0:
            return -1
        elif float(tup1[0])/tup1[1] - float(tup2[0])/tup2[1] > 0:
            return 1
        else:
            return 0

    def powerincrement(self, powers, default, powerlimits):
        for ind in range(1, len(powers)+1):
            if powers[-ind] < powerlimits[-ind]:
                powers[-ind] += 1
                break
            else:
                powers[-ind] = default[-ind]
        return powers

    def choosebank(self, bank):
        self.sclText.delete('1.0', "end")
        self.noteList.delete('1.0', "end")
        self.current.set(bank)
        self.setScalaText()
        self.setNoteList()
#        for rat in self.notebankmaybe[bank].numdenlist:
#            self.inratios.insert("end", '%4d : %d' % (int(rat[0]), int(rat[1])))
#        self.setratiosfromprime(self.primelimit.get())

    def setprimelimit(self, limit):
        self.primelimit.set(limit)
        self.setratiosfromprime(limit)

    def save(self, *args):
        filetosave = tkfd.asksaveasfilename(master=self, title="Save Scala Tuning File", defaultextension=".scl", filetypes=[('Scala Tuning File', ".scl")])
        if not filetosave:
            return
#        file = open(filetosave, 'wb')
        ind = self.current.get()
        self.scalaFileListMaybe[ind].setPath(filetosave)
        self.scalaFileListMaybe[ind].writeToDisk()
#        pickle.dump(self.scalaFileListMaybe[ind], file)

    def load(self, *args):
        filetoload = tkfd.askopenfilename(title="Open", filetypes=[('Scala Tuning File', ".scl"), ("All", "*")])
        if not filetoload:
            return
#        file = open(filetoload, 'rb')
        ind = self.current.get()
#        self.scalaFileListMaybe[ind] = pickle.load(file)
        self.scalaFileListMaybe[ind].setPath(filetoload)
        self.scalaFileListMaybe[ind].readFromDisk()
        self.noteBankListMaybe[ind] = self.scalaFileListMaybe[ind].parseToNoteBank()
        self.setScalaText()
        self.setNoteList()
#        for sel in self.selectfr.winfo_children():
#            sel.destroy()
#        for bank in self.notebankmaybe:
#            self.bankadd(bank)
#        self.selectfr.winfo_children()[0].select()
#        self.selectfr.winfo_children()[0].invoke()

    def indirectok(self, *args):
#        if self.focus_get() != self.addbox:
        if self.focus_get() != self.sclText:
            self.ok()

    def ok(self, *args):
        self.apply()
        self.cancel()

    def apply(self, *args):
        self.myparent.noteBankList = copy.deepcopy(self.noteBankListMaybe)
        self.myparent.scalaFileList = copy.deepcopy(self.scalaFileListMaybe)
#        primelimit = 3
#        for prime in self.primelist:
#            for bank in self.notebankmaybe:
#                for ratio in bank.numdenlist:
#                    if not ratio[0] % prime or not ratio[1] % prime:
#                        primelimit = prime
#                        break
#        self.myparent.primelimit = primelimit

    def cancel(self, *args):
        self.destroy()

    def clear(self, *args):
        ind = self.current.get()
        self.scalaFileListMaybe[ind] = ScalaFileText()
        self.noteBankListMaybe[ind] = self.scalaFileListMaybe[ind].parseToNoteBank()
        self.setScalaText()
        self.setNoteList()
        #self.inratios.selection_set(0, "end")
        #self.ratioremove()

    def setdefault(self, *args):
        
        self.clear()
        ind = self.current.get()
        self.scalaFileListMaybe[ind] = ScalaFileText('Rationale13.scl')
        self.noteBankListMaybe[ind] = self.scalaFileListMaybe[ind].parseToNoteBank()
        self.setScalaText()
        self.setNoteList()
