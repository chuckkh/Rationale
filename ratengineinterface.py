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

import threading
import subprocess
import socket
import queue
import time
import sys
#import chardet
import pathlib
import os
sys.path.insert(0, "./RatEngine/Builds")
if sys.platform.count("win32"):
    import execPathRelease
    import execPathDebug
else:
    import execPath as execPathRelease
    import execPath as execPathDebug

class RatEngineInterface:
    def __init__(self, parent):
        self.parent = parent
        self.cbport = 5899
        self.active = 1
        self.magicNumber = b'\x2c\x9e\xb4\xf2'
        self.rau = None
        self.sock = None

    def findEnginePath(self):
        fileDirectory = pathlib.Path(__file__).parent.absolute()
        print(fileDirectory)

    def waitforconnect(self, sock, q):
        print("waiting...")
        conn = sock.accept()
        print("Wow!")
        q.put(conn)

    def delegatecallbacks(self, sock):
        self.active = 1
        cbtext = ""
        end = "END"
        endIndex = 0
        print("delegating...")
        print("self.active =", self.active)
        print("self.parent.engineActive =", self.parent.engineActive)
        while self.active == 1:
            #bb = bytearray()
            time.sleep(0.2)
            try:
#            print("cbtext: ", cbtext)
#            print(sock.recv(1))
                msg = sock.recv(16)
#            sock.send(msg)
#            time.sleep(0.1)
                if msg:
#                    print("Msg ", msg)
#                enc = chardet.detect(msg)["encoding"]
#                print(enc)
                    wtf = msg.decode()
#                print("wtf ", wtf)
                    cbtext += wtf
#                print("text ", cbtext)
#                cbtext += wtf
                    while cbtext.count("CB"):
                        cmd, cbtext = cbtext.split("CB", 1)
#                        print("Engine to Rationale:", cmd)
                        if cmd == "END" or cbtext == "ENDCB":
                            print("Ennnnnndaaa: ratengineinterface.py line 77")
                            self.parent.engineActive = 0
                            self.active = 0
                            break
                        elif cmd.startswith("TICK:"):
                            position = float(cmd[5:])
#                            print("Rat tick", position, file=sys.stderr)
                            self.parent.cursor.scrollabs(position)
                        else:
                            self.parent.bufferFromEngine.append(cmd)

            except:
                pass
#                print("Callback Socket Unavailable:", sys.exc_info()[0])
#                print sock
#                self.parent.engineActive = 0
#                self.active = 0
            if self.parent.engineActive == 0:
                try:
                    sock.send(b'\x2c\x9e\xb4\xf2')
                    sock.send(b'\x05\x00\x00\x00')
                    sock.send(b'\x45\x4e\x44\x43\x42')
                except:
                    print("Unable to send END.")

                self.active = 0
        self.parent.engineActive = -1
        print("Done delegating!")


    def launch(self, dbg):
        self.cbport = 5899
    #create socket to receive callbacks to move the time cursor
        cbwait = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #cbwait.setblocking(0)
#    cbwait.settimeout(4.0)
        count = 0
        while count < 30000:
            try:
                cbwait.bind(("127.0.0.1", self.cbport))
                print('Callback Port: %s' % str(self.cbport))
                break
            except:
                self.cbport += 1
                count += 1
                if count == 30000:
                    print("NO PORTS AVAILABLE FOR CALLBACK")
                    active = 0

        cbwait.listen(2)

        #thread to wait for ratengine to connect
        q = queue.Queue()
        wait = threading.Thread(target=self.waitforconnect, args=(cbwait, q)) # 
        wait.start()

        count = 0

        if dbg:
            print("With debug...")
            self.launchWithDebug()
        else:
            print("Without debug...")
            self.launchWithoutDebug()
        
        wait.join()
        print("wait joined")
        cbsock = q.get()[0]
        cbsock.setblocking(0)
        self.sock = cbsock
        cbThread = threading.Thread(target=self.delegatecallbacks, args=(cbsock,))
        cbThread.start()
        time.sleep(4)
        #self.sendToEngine("GetMidiIn")
#        cbsock.send(b'\x2c\x9e\xb4\xf2')
#        cbsock.send(b'\x0a\x00\x00\x00')
#        cbsock.send(b'\x47\x65\x74\x4d\x69\x64\x69\x4f\x75\x74')

    def sendToEngine(self, outMessage):
        ln = len(outMessage)
        ln0 = ln%256
        ln1 = (ln//256)%256
        ln2 = (ln//256//256)%256
        ln3 = (ln//256//256//256)%256
        header2 = bytes([ln0,ln1,ln2,ln3])

#        header2 = bytes(str(ln0) + str(ln1) + str(ln2) + str(ln3), 'ascii')
        messageBytes = bytes(outMessage, 'ascii')
        self.sock.send(self.magicNumber)
        self.sock.send(header2)
        self.sock.send(messageBytes)


    def launchWithDebug(self):
        try:
            enginePath = execPathDebug.exec_path
#            if sys.platform.count("win32"):
#                enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
#                enginePath = execPathDebug.exec_path
#            elif sys.platform.count("linux"):
#                enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "ConsoleApp" + os.sep + "RatEngine"
#                enginePath = execPath.exec_path
#            enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "VisualStudio2019" + os.sep + "x64" + os.sep + "Debug" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
        #rau = subprocess.Popen((r'C:\Users\Home\Documents\Coding\rationale-2020\RatEngine\Builds\VisualStudio2019\x64\Debug\ConsoleApp\RatEngine.exe', str(cbport)))
            self.rau = subprocess.Popen((enginePath, str(self.cbport)))

        except:
            print("Engine stolen")
            self.active = 0

    def launchWithoutDebug(self):
        try:
            enginePath = execPathRelease.exec_path
#            if sys.platform.count("win32"):
#                enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
#                enginePath = execPathRelease.exec_path
#            elif sys.platform.count("linux"):
#                enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "ConsoleApp" + os.sep + "RatEngine"
#                enginePath = execPath.exec_path

#            enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "VisualStudio2019" + os.sep + "x64" + os.sep + "Release" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
            print("path ", enginePath)
            #rau = subprocess.Popen((r'C:\Users\Home\Documents\Coding\rationale-2020\RatEngine\Builds\VisualStudio2019\x64\Release\ConsoleApp\RatEngine.exe', str(cbport)))
            self.rau = subprocess.Popen((enginePath, str(self.cbport)))
        except:
            print("Engine stolen")
            self.active = 0

    def interruptEngine(self):
        self.active = 0

#print(sys.argv[1])

#findEnginePath()
#launch(int(sys.argv[1]))
#launch(0)
#enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "VisualStudio2019" + os.sep + "x64" + os.sep + "Release" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
