import socket
import threading
import json

class client (): 
    def __init__ (self) : 
        self.host = '0.0.0.0'
        #print (self.host)
        self.portInscription = 2000
        s1 = socket.socket (type = socket.SOCK_STREAM)
        s1.bind ((self.host, self.portInscription))
        #s1.settimeout (0.5)
        self.s1 = s1
        self.IPserveur = input("Entrez l'adresse Ip du serveur : ")
        self.portServeur = int(input("Entrez le numéro de port du serveur : "))
        self.serveur = (self.IPserveur, self.portServeur)
        
        self.s1.connect (self.serveur)
        self.portJeu = 3500
        self.inscription = {
                                "request": "subscribe",
                                "port": self.portJeu,
                                "name": "The Lion Ping",
                                "matricules": ["23203"]
                            }
        self.reponse = json.dumps (self.inscription).encode()
        self.s1.sendall (self.reponse)
    

        
        s2 = socket.socket (type = socket.SOCK_STREAM)
        s2.bind((self.host, self.portJeu))
        self.s2 = s2
        #self.s2.connect (self.serveur)

    def recept (self) : 

        self.s2.listen()    
        self.client, self.addr = self.s2.accept ()
        data = self.client.recv(1024).decode()

        retour = json.loads(data)
        print (retour)

        if retour["request"] == "ping" :
            reponse = {"response" : "pong"}
            envoi = json.dumps (reponse).encode()
            self.client.sendall (envoi)

    def run(self) : 
        threading.Thread(target=self.recept).start()
        
        try :    
            while True :
                pass  # boucle infinie pour garder le programme en vie
        except KeyboardInterrupt:
            print("Arrêt du client.")
            self.s1.close()
            self.s2.close()
        
client().run()