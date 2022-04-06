import threading
import subprocess
import socket
import queue
import time
import sys
import chardet
import pathlib
import os

class RatEngineInterface:
    def __init__(self, parent):
        self.parent = parent
        self.cbport = 5899
        self.active = 1
        self.magicNumber = b'\x2c\x9e\xb4\xf2'

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
        while self.active == 1:
            bb = bytearray()
            time.sleep(0.2)
            try:
#            print("cbtext: ", cbtext)
#            print(sock.recv(1))
                msg = sock.recv(16)
#            sock.send(msg)
#            time.sleep(0.1)
                if msg:
#                print("Msg ", msg)
#                enc = chardet.detect(msg)["encoding"]
#                print(enc)
                    wtf = msg.decode()
#                print("wtf ", wtf)
                    cbtext += wtf
#                print("text ", cbtext)
#                cbtext += wtf
                    while cbtext.count("CB"):
                        cmd, cbtext = cbtext.split("CB", 1)
                        print("Command: ", cmd)
                        if cmd == "END" or cbtext == "ENDCB":
                            self.active = 0
                            break

            except:
                print("Callback Socket Unavailable:", sys.exc_info()[0])
#                print sock
                self.active = 0
                pass
        print("Done delegating!")


    def launch(self, dbg):
        self.cbport = 5899
    #create socket to receive callbacks to move the time cursor
        cbwait = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        print("joined")
        cbsock = q.get()[0]
        cbThread = threading.Thread(target=self.delegatecallbacks, args=(cbsock,)).start()
        time.sleep(2)
        try:
            cbsock.send(b'\x2c\x9e\xb4\xf2')
            cbsock.send(b'\x0a\x00\x00\x00')
            cbsock.send(b'\x47\x65\x74\x4d\x69\x64\x69\x4f\x75\x74')


            cbsock.send(b'\x2c\x9e\xb4\xf2')
            cbsock.send(b'\x01\x00\x00\x00')
            cbsock.send(b'\x65')
            time.sleep(8)

            cbsock.send(b'\x2c\x9e\xb4\xf2')
            cbsock.send(b'\x05\x00\x00\x00')
            cbsock.send(b'\x45\x4e\x44\x43\x42')
        except:
            print("Not sent")
#    cbThread.join()
        time.sleep(10)
        self.active = 0
#    rau.communicate()
#    try:
#        cbsock.sendall('HelloRATENDMESSAGE')
#    except:
#        print("Unable to start")

    def launchWithDebug(self):
        try:
            enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "VisualStudio2019" + os.sep + "x64" + os.sep + "Debug" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
        #rau = subprocess.Popen((r'C:\Users\Home\Documents\Coding\rationale-2020\RatEngine\Builds\VisualStudio2019\x64\Debug\ConsoleApp\RatEngine.exe', str(cbport)))
            self.rau = subprocess.Popen((enginePath, str(self.cbport)))

        except:
            print("Engine stolen")
            self.active = 0

    def launchWithoutDebug(self):
        try:
            enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "VisualStudio2019" + os.sep + "x64" + os.sep + "Release" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
        #rau = subprocess.Popen((r'C:\Users\Home\Documents\Coding\rationale-2020\RatEngine\Builds\VisualStudio2019\x64\Release\ConsoleApp\RatEngine.exe', str(cbport)))
            print(enginePath)
            self.rau = subprocess.Popen((enginePath, str(self.cbport)))
        except:
            print("Engine stolen")
            self.active = 0
#print(sys.argv[1])

#findEnginePath()
#launch(int(sys.argv[1]))
#launch(0)
#enginePath = pathlib.Path(__file__).parent.absolute().__str__() + os.sep + "RatEngine" + os.sep + "Builds" + os.sep + "VisualStudio2019" + os.sep + "x64" + os.sep + "Release" + os.sep + "ConsoleApp" + os.sep + "RatEngine.exe"
