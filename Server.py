import socket
import os
import string
import time
from threading import Lock
from _thread import *
cm=0
pin='0'
ServerSideSocket = socket.socket()
host = '192.168.0.168'
port = 8080
ThreadCount = 0

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket escuchando..')
ServerSideSocket.listen(5)

def measureDistance(cm):
    if (cm > 0 and cm <= 20):
        return '2'
    if (cm > 20 and cm <= 40):
        return '4'
    if (cm > 40 and cm <= 60):
        return '5'
    if (cm > 60 and cm <= 80):
        return '18'
    if (cm > 80 and cm <= 100):
        return '19'
    if (cm > 100):
        return '21'

def multi_threaded_client(connection,lock):
    global cm
    global pin
    lock.acquire()
    while True:

        data = connection.recv(2048)
        if not data:
            pin=measureDistance(int(cm))
            
            break
        else:
            print('distancia en cm: '+ data.decode('utf-8'))
            cm = data.decode('utf-8')
        
    lock.release()

    connection.close()
while True:
    lock=Lock()
    Client, address = ServerSideSocket.accept()
    print('Conectado a: ' + address[0] + ':' + str(address[1]))
    time.sleep(0.5)
    start_new_thread(multi_threaded_client, (Client, lock,))
    Client.send(str.encode(pin))
    ThreadCount += 1
    print('Thread : ' + str(ThreadCount))
""" """
