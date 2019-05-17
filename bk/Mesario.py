import sys
import socket
import json
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi
from threading import Thread

chat = True

class Mesario(QDialog):
    def __init__(self):
        super(Mesario, self).__init__()
        loadUi('Mesario.ui', self)
        self.setWindowTitle('Mesario')
        tread = Thread(target=self.listening)
        tread.start()
        self.lbAguardando.hide()
        self.btLiberar.clicked.connect(self.btLiberar_click)
    
    def btLiberar_click(self):
        self.reading()
    
    def listening(self):
        while True:
            host = '192.168.1.102'
            port = 9990

            ListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ListenerSocket.bind((host, port))

            message, address = ListenerSocket.recvfrom(1024)
            package = json.loads(message.decode('ascii'))
            msg = str(package.get("message"))

            print(message, address)
            data = json.dumps({"message": True})
            print(data)
            
            if msg:
                self.btLiberar.setEnabled(True)
                self.lbAguardando.hide()
            ListenerSocket.sendto(data.encode('ascii'), address)
    
    def reading(self):
        host = '192.168.1.102'
        port = 9991

        senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        data = json.dumps({"message": True})
        print(data)
        senderSocket.sendto(data.encode('ascii'), (host, port))

        senderSocket.recv(1024)
        self.btLiberar.setEnabled(False)
        self.lbAguardando.show()

app=QApplication(sys.argv)
widget = Mesario()
widget.show()
sys.exit(app.exec_())
