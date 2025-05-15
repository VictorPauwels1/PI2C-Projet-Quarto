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
    return None

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
    return None

def choixpiececolonne(pieces2, piece) :
    
    for j in piece :  
            comp = []
            rempli = []
            for index in range(4) :
                colonne = pieces2[:, index]  
                compte = 0
                nbre = 0
                for element in colonne:
                    if element != None :
                        nbre += 1
                        if j in element:
                            compte += 1
                comp.append(compte)
                rempli.append(nbre)
                if 3 in comp : 
                    for recherche, m in enumerate(comp) : 
                        if m == 3 and rempli[recherche] == 4 :
                            return piece
                else : 
                    return piece
    return None

def choixpieceligne (pieces2, piece) : 
    for i in piece :
        for j in i :    
            comp = []
            rempli = []          
            for index, rangée in enumerate (pieces2) :
                compte = 0
                nbre = 0
                for l in rangée :
                    if l != None :  
                        nbre += 1
                        if j in l : 
                            compte += 1
                comp.append(compte)
                rempli.append(nbre)
                if 3 in comp : 
                    for recherche, m in enumerate(comp) : 
                        if m == 3 and rempli[recherche] == 4 :
                            fin = choixpiececolonne (pieces2, i) 
                            if fin != None : 
                                return fin 
                else :     
                    fin = choixpiececolonne (pieces2, i)
                    if fin != None :
                        return fin 
    return None

class client (): 
    def __init__ (self) : 
        matricule = "23203"
        pseudo = "The Lion Ping"
        self.host = '0.0.0.0'
        #print (self.host)
        self.portInscription = 5000
        s1 = socket.socket (type = socket.SOCK_STREAM)
        s1.bind ((self.host, self.portInscription))
        #s1.settimeout (0.5)
        self.s1 = s1
        self.IPserveur = input("Entrez l'adresse Ip du serveur : ")
        self.portServeur = 3000
        self.serveur = (self.IPserveur, self.portServeur)
        
        self.s1.connect (self.serveur)
        self.portJeu = 2000
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
                            #print (p)
                            plateau.append(set(p))

                    piecesrestantes = []
                    for i in self.pieces2 :
                        piecesrestantes.append(i)
                    #print(self.pieces2)
                    #print(piecesrestantes)

                    for i in plateau : 
                        if i in piecesrestantes :
                            piecesrestantes.remove(set(i))
                    #print(piecesrestantes)
                    
                    if piecesrestantes == [] :
                        choix = None
                    else :  
                        fin = choixpieceligne(matrice, piecesrestantes)
                        if fin != None :  
                            choix = ""
                            for y in fin :
                                choix += y
                        else : 
                            while True : 
                                piece = randint (0,15)
                                if self.pieces2[piece] not in plateau :
                                    break
                            choix = ""
                            for y in self.pieces2[piece] :
                                choix += y
                           


                    renvoi = {
                        "response" : "move",
                        "move" : {
                            "pos" : pos,
                            "piece" : choix
                        },
                        "message" : ""
                    }
                    
                    bidule = json.dumps (renvoi).encode()
                    #print (bidule)
                    self.client.sendall (bidule)
            except :
                pass

    def run(self) : 
        self.running = True
        threading.Thread(target=self.recept).start()
        
        try :    
            while True :
                pass  
        except KeyboardInterrupt:
            print("Arrêt du client.")
            self.s1.close()
            self.s2.close()
        
client().run()