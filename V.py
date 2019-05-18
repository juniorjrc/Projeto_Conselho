import sys
import socket
import json
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QMessageBox
from PyQt5.uic import loadUi
from threading import Thread
from core.P2P import P2P
from core.Logger import Logger

class V(QDialog):
    def __init__(self):
        super(V, self).__init__()
        self.p2p = P2P()
        self.p2p.clientConfig('192.168.1.102',9001)
        self.p2p.serverConfig('192.168.1.102',9000)

        #Interface
        loadUi('ui/V.ui', self)
        self.setWindowTitle('Votante')

        #threads
        self.tread = Thread(target=self.p2p.listening)
        self.tread.start()
        self.treadV = Thread(target=self.verify)
        self.treadV.start()

        #Logger
        self.logger = Logger('data/votos.txt','data/eleitores.txt') 
        if self.logger.compare() is not True :
           self.logger.repair()
        
        self.btVotar.clicked.connect(self.btVotar_click)


        if self.p2p.msgListen:
            self.btVotar.setEnabled(True)
            self.lbAguardando.setText('Votação Liberada')
            self.txtVoto.setEnabled(True)
            
    def btVotar_click(self):

        self.btVotar.setEnabled(False)
        self.lbAguardando.setText('Aguardando Liberação')
        self.logger.write(self.txtVoto.text())
        self.txtVoto.clear()
        self.txtVoto.setEnabled(False)

        if self.logger.compare() is not True :
            self.logger.repair()

        reader = self.p2p.reading()

        while reader is not True:
            alert = QMessageBox.warning(self, 'Aviso', "A conexão foi perdida, clique em 'Retry' para tentar re-estabelecer! ou em 'Cancel' para fechar o programa", QMessageBox.Retry | QMessageBox.Cancel, QMessageBox.Retry)
            if alert == QMessageBox.Cancel:
                sys.exit(QApplication(sys.argv).exec_())
            else:
                reader = self.p2p.reading()



    def verify(self):
        while True:
            if self.p2p.msgListen:
                self.btVotar.setEnabled(True)
                self.lbAguardando.setText('Votação Liberada')
                self.txtVoto.setEnabled(True)
                self.p2p.msgListen = False                
            
app=QApplication(sys.argv)
widget = V()
widget.show()
sys.exit(app.exec_())
