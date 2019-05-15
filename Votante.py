import sys
import socket
import json
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi
from threading import Thread

chat = True

class Votante(QDialog):
    def __init__(self):
        super(Votante, self).__init__()
        loadUi('Votante.ui', self)
        self.setWindowTitle('Votante')
        tread = Thread(target=self.listening)
        tread.start()
        self.btVotar.clicked.connect(self.btVotar_click)

    def btVotar_click(self):
        self.reading()
    
    def listening(self):
        while True:
            host = '192.168.1.40'
            port = 9991

            ListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ListenerSocket.bind((host, port))

            message, address = ListenerSocket.recvfrom(1024)
            package = json.loads(message.decode('ascii'))
            msg = str(package.get("Mensagem"))
            
            answer = "\nYour Message has been sent!!"
            data = json.dumps({"Answer": answer})

            if msg == "Liberou a votação":
                self.btVotar.setEnabled(True)
                self.lbAguardando.setText('Votação Liberada')
                self.txtVoto.setEnabled(True)

            ListenerSocket.sendto(data.encode('ascii'), address)

    def reading(self):
        #IP E PORTA CONFIGURÁVEL
        host = '192.168.1.40'
        port = 9990

        senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #ENVIO DA MENSAGEM
        message = "Votou"
        data = json.dumps({"Mensagem": message})

        senderSocket.sendto(data.encode('ascii'), (host, port))

        #RECEBIMENTO DA RESPOSTA
        senderSocket.recv(1024)
        self.btVotar.setEnabled(False)
        self.lbAguardando.setText('Aguardando Liberação')
        self.txtVoto.clear()
        self.txtVoto.setEnabled(False)

app=QApplication(sys.argv)
widget = Votante()
widget.show()
sys.exit(app.exec_())