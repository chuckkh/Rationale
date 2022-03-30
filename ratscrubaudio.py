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


import ctcsound as csnd
import os
import sys
import socket
import threading
#import StringIO
if sys.platform.count('win32'):
    import win32api, win32process, win32con
    pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    try: win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)
    except: win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
elif sys.platform.count('linux') or sys.platform.count('darwin'):
    meaner = True
    while meaner:
        try:
            os.nice(-1)
        except:
            meaner = False
    del meaner

#csdout = StringIO.StringIO()

class ratscrubaudioengine(csnd.CppSound):
    def __init__(self, cbport):
        csnd.CppSound.__init__(self)
#        self.csdout = stdout
#        self.inport = inport
#        self.initsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.initsock.bind(('127.0.0.1', int(inport)))
#        self.initsock.listen(5)

#        threading.Thread(target=self.waitforconnect).start()
        self.inputflag = 1
        self.cbport = int(cbport)
        self.cbsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cbsock.connect(('127.0.0.1', self.cbport))

        self.inputloopthread = threading.Thread(target=self.inputloop)
        self.inputloopthread.start()

    def waitforconnect(self):
        self.insock = self.initsock.accept()[0]
        print("Input Socket Connected")
        self.inputflag = 1
        self.inputloop()

    def inputloop(self):
        string = ''
        while self.inputflag == 1:
            string += self.cbsock.recv(64)
            while string.count('RATENDMESSAGE'):
                cmd, string = string.split('RATENDMESSAGE', 1)
                self.cmddelegate(cmd)

    def cmddelegate(self, cmd):
        if cmd.startswith('csdopt:'):
            self.setCommand(cmd[7:])
        elif cmd.startswith('csdorc:'):
            self.setOrchestra(cmd[7:])
        elif cmd.startswith('csdsco:'):
            self.setScore(cmd[7:])
        elif cmd.startswith('csdadd:'):
            try:
                self.perf.InputMessage(cmd[7:])
#                print 'Input:', cmd[7:]
            except: print("Message failed:", cmd[7:])
        elif cmd.startswith('csdgoz'):
            self.exportForPerformance()
            self.compile()
            if self.getIsGo():
                self.perf = csnd.CsoundPerformanceThread(self)
                self.perf.Play()
            else:
                print("Csound Error")
                self.cbsock.sendall('ENDCB')
        elif cmd.startswith('csdstp'):
#            print "stopping scrub..."
            self.inputflag = 0
            try:
                self.perf.Stop()
                self.perf.Join()
                self.cbsock.sendall('ENDCB')
#		print "stopped"
            except: print("No Performance Thread")
            self.cleanup()
        elif cmd.startswith('csdcln'):
            try:
                self.cleanup()
                print("Csound Cleaned Up")
            except:
                print("Unable to Cleanup Csound Instance")

ra = ratscrubaudioengine(sys.argv[1])

