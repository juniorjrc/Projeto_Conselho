import sys
import socket
import json
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog, QMessageBox
from PyQt5.uic import loadUi
from threading import Thread
from core.P2P import P2P

class M(QDialog):
    def __init__(self):
        super(M, self).__init__()

        '''
            Classe Peer to Peer com os metodos
            ClientConfig, ServerConfig, Listening, Reading
            O ip client deve ser o ip config da outra ponta
            e o ip server dessa ponta deve ser o ip client da outra
        '''
        
        self.p2p = P2P()
        self.p2p.clientConfig('192.168.1.35',9000)
        self.p2p.serverConfig('192.168.1.40',9001)


        '''
            Para boas praticas, a UI está separada em uma pasta
        '''
        loadUi('ui/M.ui', self)
        self.setWindowTitle('mesario')

        '''
            O sistema comporta-se de duas threads,
            1° é para ficar ouvindo o socket
            2° para verificar se pode ou não habilitar os botoes
            tem uma variavel no P2P que é responsavel por essa função
        '''
        self.tread = Thread(target=self.p2p.listening)
        self.tread.start()
        self.treadV = Thread(target=self.verify)
        self.treadV.start()



        self.lbAguardando.hide()      
        self.btLiberar.clicked.connect(self.btLiberar_click)


            
    def btLiberar_click(self):
        reader = self.p2p.reading()

        while reader is not True:
            alert = QMessageBox.warning(self, 'Aviso', "A conexão foi perdida, clique em 'Retry' para tentar re-estabelecer! ou em 'Cancel' para fechar o programa", QMessageBox.Retry | QMessageBox.Cancel, QMessageBox.Retry)
            if alert == QMessageBox.Cancel:
                sys.exit(QApplication(sys.argv).exec_())
            else:
                reader = self.p2p.reading()
        
        self.btLiberar.setEnabled(False)
        self.lbAguardando.show()
        
    def verify(self):
        while True:
            if self.p2p.msgListen:
                self.btLiberar.setEnabled(True)
                self.lbAguardando.hide()
                self.p2p.msgListen = False
        
app=QApplication(sys.argv)
widget = M()
widget.show()
sys.exit(app.exec_())
