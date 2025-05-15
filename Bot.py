import socket
import threading
import json
from random import randint

class client (): 
    def __init__ (self) : 
        matricule = 0
        pseudo = "The Lion Pong"
        self.host = '0.0.0.0'
        #print (self.host)
        self.portInscription = 5001
        s1 = socket.socket (type = socket.SOCK_STREAM)
        s1.bind ((self.host, self.portInscription))
        #s1.settimeout (0.5)
        self.s1 = s1
        self.IPserveur = input("Entrez l'adresse Ip du serveur : ")
        self.portServeur = 3000
        self.serveur = (self.IPserveur, self.portServeur)
        
        self.s1.connect (self.serveur)
        self.portJeu = 2001
        self.inscription = {
                                "request": "subscribe",
                                "port": self.portJeu,
                                "name": pseudo,
                                "matricules": [matricule]
                            }
        self.reponse = json.dumps (self.inscription).encode()
        self.s1.sendall (self.reponse)
    

        
        s2 = socket.socket (type = socket.SOCK_STREAM)
        s2.bind((self.host, self.portJeu))
        self.s2 = s2
        #self.s2.connect (self.serveur)

    def recept (self) : 
        self.caseocc = []
        self.piecesjouees = []
        self.pieces = ["BDEC","BDEP","BDFC","BDFP","BLEC","BLEP","BLFC","BLFP","SDEC","SDEP","SDFC","SDFP","SLEC","SLEP","SLFC","SLFP"]
        self.pieces2 = []
        for i in self.pieces : 
            self.pieces2.append (set(i))
        #print (self.pieces2)
        self.s2.listen()  

        while self.running == True : 
            try :
                  
                self.client, self.addr = self.s2.accept ()
                data = self.client.recv(1024)

                retour = json.loads(data.decode())
                print (retour)

                if retour["request"] == "ping" :
                    reponse = {"response" : "pong"}
                    envoi = json.dumps (reponse).encode()
                    self.client.sendall (envoi)

                if retour["request"] == "play" :
                    if retour["state"]["piece"] == None : 
                        pos = None
                    else :
                        while True : 
                            pos = randint(0,15)  
                            if retour["state"]["board"][pos] == None : 
                                break
                        
                    plateau = []
                    if retour["state"]["piece"] != None :
                        plateau.append(set(retour["state"]["piece"]))
                    for p in retour["state"]["board"]:
                        if p != None : 
                            plateau.append(set(p))
                    #print (plateau)
                    
                    while True : 
                        piece = randint (0,15)
                        #print (self.pieces2[piece])
                        if self.pieces2[piece] not in plateau :
                            break
                    #print(self.pieces2[piece])


                    self.pieces = ["BDEC","BDEP","BDFC","BDFP","BLEC","BLEP","BLFC","BLFP","SDEC","SDEP","SDFC","SDFP","SLEC","SLEP","SLFC","SLFP"]
                    self.pieces2 = []
                    for i in self.pieces : 
                        self.pieces2.append (set(i))
                    choix = ""
                    for y in self.pieces2[piece] :
                        choix += y
                    
                    #print (choix)


                    renvoi = {
                        "response" : "move",
                        "move" : {
                            "pos" : pos,
                            "piece" : choix
                        },
                        "message" : ""
                    }
                    
                    bidule = json.dumps (renvoi).encode()
                    print (bidule)
                    self.client.sendall (bidule)
            except :
                pass

    def run(self) : 
        self.running = True
        threading.Thread(target=self.recept).start()
        
        try :    
            while True :
                pass  # boucle infinie pour garder le programme en vie
        except KeyboardInterrupt:
            print("Arrêt du client.")
            self.s1.close()
            self.s2.close()
        
client().run()