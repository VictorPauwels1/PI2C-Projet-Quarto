# PI2C-Projet-Quarto

## Stratégie : 

La stratégie est simple, si la pièce donnée par mon adversaire peut me faire gagner, elle sera placée à l'endroit ou je gagne.  Ensuite, pour le choix de la pièce, je choisis, si c'est possible, une pièce qui ne peut pas faire gagner l'adversaire.  

## Bibliothèques : 

J'utilise les bibliothèques socket, threading, json, random, numpy. 

Socket : Je crée 2 socket, l'un qui s'inscrit au serveur et le deuxième qui communique avec le serveur pour jouer contre les autres IA's. 
Threading : J'utilise threading pour écouter et parler en même temps sur le socket
Json : Json est indispensable car les message échangés avec les serveur doivent être au format json. 
Random : J'utilise random dans les cas où je ne peux pas gagner, la pièce est placée de manière aléatoire sur le plateau.  Pareil pour le choix de la pièce, si aucune pièce permet d'être sûre de ne pas perdre, il prend une pièce aléatoire grâce à random. 
numpy : J'utilise numpy pour transformer le board en matrice et pouvoir parcourir facilement les lignes et les colonnes 
