import sys
import socket
import json

class P2P:

    def __init__(self):
            self.msgListen = False

    def clientConfig(self,host, port):
            self.clientPort = port
            self.clientHost = host

    def serverConfig(self, host, port):
            self.serverPort = port
            self.serverHost = host
          
        
    def listening(self):
        while True:
            print(self.serverPort, self.serverHost)
            print(self.clientPort, self.clientHost)
            ListenerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ListenerSocket.bind((self.serverHost, self.serverPort))

            message, address = ListenerSocket.recvfrom(1024)
            package = json.loads(message.decode('ascii'))
            msg = str(package.get("message"))
           
            data = json.dumps({"message": True})
            print(data)
            if msg:
                self.msgListen = True


            ListenerSocket.sendto(data.encode('ascii'), address)

    def reading(self):
        try:
                senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                #ENVIO DA MENSAGEM
                data = json.dumps({"message": True})
                senderSocket.sendto(data.encode('ascii'), (self.clientHost, self.clientPort))
                senderSocket.settimeout(4)
                
                #RECEBIMENTO DA RESPOSTA
                senderSocket.recv(1024)
                return True
        except socket.timeout:
                return False


        
