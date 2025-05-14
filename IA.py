import socket
import threading
import json
from random import randint
import numpy as np

def ligne (pieces2, piece) : 
    for j in piece :              
        for index, rangée in enumerate (pieces2) :
            compte = 0
            for l in rangée :
                if l != None :  
                    if j in l : 
                        compte += 1
            if compte == 3 :
                n = 0
                for indice, colonne in  enumerate (rangée):
                    n += 1
                    if colonne == None : 
                        pos = index * 4 + indice
                        return pos
    pos = None
    return pos

def colonne(pieces2, piece) :
    for j in piece :  
        for index in range(4) :
            colonne = pieces2[:, index]  
            compte = 0
            for element in colonne:
                if element is not None and j in element:
                    compte += 1
            if compte == 3:
                for indice, elements in enumerate(colonne):
                    if elements is None:
                        pos = indice * 4 + index
                        return pos
    pos = None
    return pos

class client (): 
    def __init__ (self) : 
        matricule = input("Entrez votre matricule : ")
        pseudo = input("Entrez votre pseudo : ")
        self.host = '0.0.0.0'
        #print (self.host)
        self.portInscription = int(input("Entrez le port d'inscription : "))
        s1 = socket.socket (type = socket.SOCK_STREAM)
        s1.bind ((self.host, self.portInscription))
        #s1.settimeout (0.5)
        self.s1 = s1
        self.IPserveur = input("Entrez l'adresse Ip du serveur : ")
        self.portServeur = int(input("Entrez le numéro de port du serveur : "))
        self.serveur = (self.IPserveur, self.portServeur)
        
        self.s1.connect (self.serveur)
        self.portJeu = int(input("Entrez le port de jeu : "))
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

                    matrice = np.array([[]])

                    for i in retour["state"]["board"] :
                        matrice = np.append(matrice, i)
                    matrice = np.reshape(matrice, (4,4))

                    if retour["state"]["piece"] == None : 
                        pos = None
                    else : 
                        pos = ligne(matrice, retour["state"]["piece"])
                        if pos == None : 
                            pos = colonne(matrice, retour["state"]["piece"])
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