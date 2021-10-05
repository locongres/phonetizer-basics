import sys
import re
import pickle


dico={}

fichierexc=open('exceptions.csv')
for ligne in fichierexc:
	ligne=ligne.rstrip('\n')
	ligne=ligne.split('§')
	
	mot=ligne[1]
	pron=ligne[3]
	loc=ligne[4]
	active=ligne[5]
	
	if active=="1":
			
		if mot not in dico:
			dico[mot]={}
		
		dico[mot][loc]=pron


with open("exceptions", 'wb') as fichier:
	mon_pickler = pickle.Pickler(fichier)
	mon_pickler.dump(dico)
		
