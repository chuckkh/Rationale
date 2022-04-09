import threading
import subprocess
import socket
import queue
import time
import sys
import chardet

cbport = 5899
active = 1
magicNumber = b'\x2c\x9e\xb4\xf2'

def waitforconnect(sock, q):
    print("waiting...")
    conn = sock.accept()
    print("Wow!")
    q.put(conn)

def delegatecallbacks(sock):
    active = 1
    cbtext = ""
    end = "END"
    endIndex = 0
    print("delegating...")
    while active == 1:
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
                        active = 0
                        break

   #             bb.append(msg)
#                sock.send(msg)
#                enc = chardet.detect(msg)["encoding"]
#                if enc != "ascii":
                    
#                print("enc ", enc)
#                if msg:
#                dec = msg.decode()
   #             while bb.startswith(magicNumber):
   #                 bb = bb[32:]
   #             msg = msg[32:]
#                    hx = [hex(i) for i in list(msg)]
#                    print(hx)
   #             continue
   #             if enc == "ascii":
   #                 cbtext += msg.decode(enc)
   #                 print(enc, hx, cbtext)
   #                 if cbtext == "E" or cbtext == "N" or cbtext == "D":
   #                     print("Oh bajesus!", endIndex)
   #                 if cbtext == "D" and endIndex == 2:
   #                     active = 0
   #                     print("Almost done delegating!")
   #                 if cbtext == "END":
   #                     active = 0
   #                     print("Almost done delegating!")
   #                 elif cbtext == end[endIndex]:
   #                     endIndex += 1
   #                 else:
   #                     endIndex = 0
   #             else:
   #                 print(enc, hx)
#            while cbtext.count('CB'):
#                cb, cbtext = cbtext.split('CB', 1)

        except:
                print("Callback Socket Unavailable:", sys.exc_info()[0])
#                print sock
                active = 0
                pass
    print("Done delegating!")


def launch(dbg):
    cbport = 5899
    #create socket to receive callbacks to move the time cursor
    cbwait = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    cbwait.settimeout(4.0)
    count = 0
    while count < 30000:
        try:
            cbwait.bind(("127.0.0.1", cbport))
            print('Callback Port: %s' % str(cbport))
            break
        except:
            cbport += 1
            count += 1
            if count == 30000:
                print("NO PORTS AVAILABLE FOR CALLBACK")
                active = 0

    cbwait.listen(2)

        #thread to wait for ratengine to connect
    q = queue.Queue()
    wait = threading.Thread(target=waitforconnect, args=(cbwait, q)) # 
    wait.start()

    count = 0

    if dbg:
        print("With debug...")
        launchWithDebug()
    else:
        print("Without debug...")
        launchWithoutDebug()
        
    wait.join()
    print("joined")
    cbsock = q.get()[0]
    cbThread = threading.Thread(target=delegatecallbacks, args=(cbsock,)).start()
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
    active = 0
#    rau.communicate()
#    try:
#        cbsock.sendall('HelloRATENDMESSAGE')
#    except:
#        print("Unable to start")

def launchWithDebug():
    try:
        rau = subprocess.Popen((r'C:\Users\Home\Documents\Coding\rationale-2020\RatEngine\Builds\VisualStudio2019\x64\Debug\ConsoleApp\RatEngine.exe', str(cbport)))
    except:
        print("Engine stolen")
        active = 0

def launchWithoutDebug():
    try:
        rau = subprocess.Popen((r'C:\Users\Home\Documents\Coding\rationale-2020\RatEngine\Builds\VisualStudio2019\x64\Release\ConsoleApp\RatEngine.exe', str(cbport)))
    except:
        print("Engine stolen")
        active = 0
#print(sys.argv[1])
launch(int(sys.argv[1]))
