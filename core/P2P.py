import sys
import socket
import json

class P2P:

    def __init__(self):
            self.msgListen = False

    def clientConfig(self,host, port):
            self.clientPort = port
            self.clientHost = host
            print(host, port)

    def serverConfig(self, host, port):
            self.serverPort = port
            self.serverHost = host
            print(host, port)            
        
    def listening(self):
        while True:
            ListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ListenerSocket.bind((self.serverHost, self.serverPort))

            message, address = ListenerSocket.recvfrom(1024)
            print(message, address)
            package = json.loads(message.decode('ascii'))
            msg = str(package.get("message"))
           
            data = json.dumps({"message": True})

            if msg:
                self.msgListen = True
            else :
                self.msgListen = False

            ListenerSocket.sendto(data.encode('ascii'), address)

    def reading(self):
        senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #ENVIO DA MENSAGEM
        data = json.dumps({"message": True})
        senderSocket.sendto(data.encode('ascii'), (self.clientHost, self.clientPort))
        
        #RECEBIMENTO DA RESPOSTA
        senderSocket.recv(1024)
        self.btVotar.setEnabled(False)
        self.lbAguardando.setText('Aguardando Liberação')
        self.txtVoto.clear()
        self.txtVoto.setEnabled(False)

        
