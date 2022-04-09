##    Copyright 2008, 2009, 2013, 2022 Charles S. Hubbard, Jr.
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


#import ctcsound as csnd
import time
import os
import sys
import socket
import threading
import rtmidi2

#https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setpriorityclass

#import StringIO
#if sys.platform.count('win32'):
#    try:
#        import win32api, win32process, win32con
#        pid = win32api.GetCurrentProcessId()
#        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
#    #    try: win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)
#    #    except: win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
#        win32process.SetPriorityClass(handle, win32process.HIGH_PRIORITY_CLASS)
#    except: print "Unable to Set Windows Process Priorities"
if sys.platform.count('linux'):
    meaner = True
    while meaner:
        try:
            os.nice(-1)
        except:
            meaner = False
    del meaner

#csdout = StringIO.StringIO()

class ratmidiengine():
#    def __init__(self, inport, cbport, stdout):
    def __init__(self, cbport):
        print("Initializing Rationale MIDI Engine.  No flash photography.")
#        self.inport = inport
#        self.initsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	print "binding initsock..."
#        self.initsock.bind(('127.0.0.1', int(inport)))
#	print "done"
#        self.initsock.listen(5)
        self.flag = 0
        self.inputflag = 1
        self.cbport = int(cbport)
        self.cbsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.cbsock.connect(('127.0.0.1', self.cbport))
        except:
            print("Unable to connect audio engine to main program")
            return

        self.inputloopthread = threading.Thread(target=self.inputloop)
        self.inputloopthread.start()

#    def waitforconnect(self):
#	print "waiting for Input Socket to Connect..."
#        self.insock = self.initsock.accept()[0]
#        print "Input Socket Connected"
#        self.inputflag = 1
#        self.inputloop()

    def inputloop(self):
        string = ''
        try:
            while self.inputflag ==1:
                string += self.cbsock.recv(64)
                while string.count('RATENDMESSAGE'):
                    cmd, string = string.split('RATENDMESSAGE', 1)
                    self.cmddelegate(cmd)
        except:
            print("Socket problems in MIDI engine, line 83.")
            print("............................................")
        print("input loop ending")
#        sys.exit(1)

    def scoreloc(self):
        self.flag = 1
        try:
            while self.flag:
#            flag = self.perf.GetStatus()
#            print 'flag:', flag
                if self.perf.isRunning():
#                self.cmddelegate('csdstp')
                    self.flag = 0
#                print "sending endcb"
                    try:
                        self.cbsock.sendall('ENDCB')
#                    print "end sent"
                    except:
                        print("............................................")
                        pass
                else:
                    time.sleep(.125)
                    loc = self.GetChannel("rattime")
                ## prevent score cursor from being reset to beginning when stopped:
                    if loc:

                        self.cbsock.sendall('%fCB' % loc)
        except:
            print("Socket problems in audio engine, line 110.")
            print("............................................")
        print("scoreloc thread ending")

    def cmddelegate(self, cmd):
        if cmd.startswith('csdopt:'):
            self.setCommand(cmd[7:])
        elif cmd.startswith('csdorc:'):
            self.setOrchestra(cmd[7:])
        elif cmd.startswith('csdsco:'):
            self.setScore(cmd[7:])
        elif cmd.startswith('csdadd:'):
            try: self.perf.InputMessage(cmd[7:])
            except: print("No Performance Thread")
        elif cmd.startswith('csdgoz'):
            self.exportForPerformance()
            self.compile()
            if self.getIsGo():
                self.perf = csnd.CsoundPerformanceThread(self)
                self.scorelocthread = threading.Thread(target=self.scoreloc)
#                self.scorelocthread.setDaemon(1)
                self.scorelocthread.start()
                self.perf.Play()
            else:
                print("Csound Error")
                try:
                    self.cbsock.sendall('ENDCB')
                except:
                    print("No end!")
                    print("............................................")
            print("Went")
        elif cmd.startswith('csdstp'):
            self.flag = 0
            self.inputflag = 0
##            try:
#                self.cbsock.sendall('ENDCB')
#            self.scorelocthread.join()
            try:
                self.scorelocthread.join()
                self.perf.Stop()
                self.perf.Join()
                print("Stopped")
#                self.cleanup()
#                print "Cleaned Up"
            except:
                print("Stop/Cleanup Failed")
#            raise SystemExit(0)
#            os._exit(1)

#                self.perf.InputMessage('e')
##                pass
#                del self.perf
#                del self.scorelocthread

##            except: print "No Performance Thread"
#            print 'threads', threading.enumerate()
#            try:
#                self.cleanup()
#            except:
#                "Cleanup Failed"
#            print  'threads2', threading.enumerate()
#            self.insock.close()
#            self.cbsock.close()
        elif cmd.startswith('csdcln'):
            try:
                print(threading.enumerate())
                print("Csound Cleaned Up")
            except:
                print("Unable to Cleanup Csound Instance")

ra = rataudioengine()


