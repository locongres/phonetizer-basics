""" functions.py contains functions and classes to phonetize and expand text :

- expandTxt(text) : to expand un texte
- phonTxt(texte, locutor="speaker", exceptions=True, link=False) : to phonetize a text. You can specify a speaker who has specific pronunciations. You can choose to use or not the exception database, and to make the liaisons between word.

---------------------------------------

Detail of classes and functions called by phonTxt() and expandTxt():

- motmin(string) : pass a string to uppercase considering diacritical signs
- romanToArabic(string) : convert roman numbers to arabic numbers
- assemble(list) : assemble a list of phonetized words doing liaisons and adapting finals letters

Class Texte(content):
- tractMails() : makes mails and url explicits for oral
- tractDates() : makes dates explicits for oral
- tractHours() : makes hours explicits for oral
- tractMesures() : makes measurments and symbols explicits for oral
- tractRomanNumbers() : converts roman numbers to arabic numbers and tract symbols and measurment which follow
- tractNumbers() : pass numbers to letters
- tractSigles() : spel acronyms
- minuscules() : pass a string to uppercase considering diacritical signs
- pretrait() : corrects some specific words to anticipate their pronunciation
- charSpe() : deals with special characters
- tractAbbrev() : treats abbreviations
- supDblEsp() : deletes double whitespaces
- listeMots() : tokenizes
- tractSelf() : applies all treatments and returns the word list

Class Mot(content, pos="grammatical category", locuteur="speaker"):
- sFinal(following_letter) : deals with final -s pronunciation according to the first letter of the following word
- minuscules() : pass to uppercase considering diacritical signs
- phonetize(lettre_suivante) : transcribes the word in API
- syllabize() : splits a phonetized word in syllables
- accent() : puts the word stress in a syllabized word
- correct() : corrects pronunciation according to syllabization and word stress
- tract(following_letter, exceptions=True, link=False) : applies all the treatments considering the first letter of the following word

"""


import re
import pickle

#punctuations patterns
ponctuations='\.\?\!;;:,???\[\]\(\)\{\}"????/\\^_`\*??????????????\$\#\%???\&\+<>=\`\|\~\*\????????????????????????????????????????????????'
ponctuationsweb='\.\?\!;;:,???\[\]\(\)\{\}"????\\^_`\*??????????????\$\#\%???\&\+<>=\`\|\~\*\????????????????????????????????????????????????'

#numbers ----> to complete
chiffresvar={
		'0':'z??ro',
		'1':'un',
		'2':'dos',
		'3':'tres',
		'4':'quatre',
		'5':'cinc',
		'6':'seis',
		'7':'sete',
		'8':'ueit',
		'9':'n??u',
		'10':'detz',
		'11':'??nze',
		'12':'dotze', 
		'13':'tretze',
		'14':'cat??rze',
		'15':'quinze',
		'16':'setze',
		'17':'detz-e-sete',
		'18':'detz-e-ueit',
		'19':'detz-e-n??u',
		'20':'vint',
		'30':'trenta',
		'40':'quaranta',
		'50':'cinquanta',
		'60':'seissanta',
		'70':'setanta',
		'80':'ueitanta',
		'90':'novanta',
		'100sing':'cent',
		'100plur':'cents',
		'1000':'mila',
		'millionsing':'milion',
		'millionplur':'milions',
		'milliardsing':'miliard',
		'milliardplur':'miliards',
		'billionsing':'bilion',
		'billionplur':'bilions',
		'premier':'prim??ir',
		'second':'segond',
		'moins':'mens',
		'fois':'c??ps',
		'divise':'devesit per',

};


#comma name ----> to complete
virgule='virgula'


def motmin(texte):
		
		
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.replace('??', '??')
	texte=texte.lower()
	
	return texte



def romanToArabic(chaine):
	romans = {
		'M' : 1000,
		'CM' : 900,
		'D' : 500,
		'CD' : 400,
		'C' : 100,
		'XC' : 90,
		'L' : 50,
		'XL' : 40,
		'X' : 10,
		'IX' : 9,
		'V' : 5,
		'IV' : 4,
		'I' : 1,
	}

	result = 0

	for key, value in romans.items():
		
		while chaine.find(key)==0:
		    result += value;
		    chaine = chaine[len(key):len(chaine)];
		
	return result





class Texte:
	def __init__(self, content):
		content=content.strip(" ")
		content=" "+content+" "
		content=re.sub('([\s]{1,})', ' ', content)
		
		self.content=content
		self.prononciation=''
		
		

	
	
	#Processing
	
	#Tags deletion
	def tractTags(self):
		texte=self.content
		
		texte=texte.replace('\\', '??')
		
		while re.search('="([^"]*?)??"', texte):
			texte=re.sub('="([^"]*?)??"', '="\g<1>', texte)
		
		while re.search("='([^']*?)??'", texte):
			texte=re.sub("='([^']*?)??'", "='\g<1>???", texte)
			
		
		texte=re.sub('<([^ >]*?)>', '', texte)
		#texte=re.sub('<( ([^> ]+)=("([^"]*?)"|\'([^\']*?)\'))+>', '', texte)
		texte=re.sub('<([^ >]+)( ([^> ]+)=("([^"]*?)"|\'([^\']*?)\'))+>', '', texte)
		
		
		texte=texte.replace('??', '\\')
		
		self.content = texte
	
	
	#Mails and URL processing
	def tractMails(self):
		texte=self.content
		
		#URL signs ----> to complete
		signesvar={
				'point':'punt',
				'arobase':'ar??ba',
				'tiret':'tiret',
				'soulign??':'solinhat',
				'slash':'slach',
				'http:':'acha te te pe dos punts',
				'https:':'acha te te pe ??ssa dos punts',
				'www':'tres ve dobles'
		}
		
		
		# Change punctuations to keep
		texte=texte.replace('-', 'tttttt6ttttt')
		texte=texte.replace('_', 'tttttt8ttttt')

		# Email pattern
		motif='(([\W])([^'+ponctuationsweb+'\s]*?)([\.]?)([^'+ponctuationsweb+'\s]*?)@([^'+ponctuationsweb+'\s]*?)\.([^'+ponctuationsweb+'\s]*?)([\W]))'


		# For each 
		for resulta in re.findall(motif, texte):
			resulta=resulta[0]
			resulta=resulta[1:-1]
			resorig=resulta
			# Expand punctuations
			resulta=resulta.replace('.',' '+signesvar['point']+' ')
			resulta=resulta.replace('@',' '+signesvar['arobase']+' ')
			resulta=resulta.replace('tttttt6ttttt',' '+signesvar['tiret']+' ')
			resulta=resulta.replace('tttttt8ttttt',' '+signesvar['soulign??']+' ')
			# Replace original text
			texte=texte.replace(resorig,resulta)
	
		
		
		
		




		# ------- Process websites url ------- */


		# Change punctuations to keep
		texte=texte.replace('/', 'ttttttsttttt')
		texte=re.sub('\.([^ ])','ttttttpttttt\g<1>',texte)



		# Website pattern beginning with http:// */
		motif='(([\W])https?:ttttttstttttttttttsttttt([\w]*?)([\W]))'



		for resulta in re.findall(motif, texte):
			resulta=resulta[0]
			resulta=resulta[1:-1]
			resorig=resulta
	
			# Keep final point
			resulta=re.sub('ttttttpttttt$','.',resulta)
	
			# Expand punctuations
			resulta=resulta.replace('ttttttpttttt',' '+signesvar['point']+' ')
			resulta=resulta.replace('ttttttsttttt',' '+signesvar['slash']+' ')
			resulta=resulta.replace('http:',' '+signesvar['http:']+' ')
			resulta=resulta.replace('https:',' '+signesvar['https:']+' ')
			resulta=resulta.replace('tttttt6ttttt',' '+signesvar['tiret']+' ')
			resulta=resulta.replace('tttttt8ttttt',' '+signesvar['soulign??']+' ')
	
			# Replace original text
			texte=texte.replace(resorig,resulta)


		# Website pattern beginning with www. */
		motif='(([\W])wwwttttttpttttt([\w]*?)([\.]?)([\w]*?)([\W]))';


		for resulta in re.findall(motif, texte):
			resulta=resulta[0]
			resulta=resulta[1:-1]
			resorig=resulta
	
			# Keep final point
			resulta=re.sub('ttttttpttttt$','.',resulta)

			# Expand punctuations
			resulta=resulta.replace('ttttttpttttt',' '+signesvar['point']+' ')
			resulta=resulta.replace('ttttttsttttt',' '+signesvar['slash']+' ')
			resulta=resulta.replace('www',' '+signesvar['www']+' ')
			resulta=resulta.replace('tttttt6ttttt',' '+signesvar['tiret']+' ')
			resulta=resulta.replace('tttttt8ttttt',' '+signesvar['soulign??']+' ')
	
			# Replace original text
			texte=texte.replace(resorig,resulta)
	

		


		# Other website pattern */
		motif='(([\W])([\w]*?)ttttttpttttt(org|com|fr|net|eu|it|bzh|cat|tv)ttttttsttttt([\w]*?)([\W]))'


		for resulta in re.findall(motif, texte):
			resulta=resulta[0]
			resulta=resulta[1:-1]
			resorig=resulta
	
			# Keep final point
			resulta=re.sub('ttttttpttttt$','.',resulta)

			# Expand punctuations
			resulta=resulta.replace('ttttttpttttt',' '+signesvar['point']+' ')
			resulta=resulta.replace('ttttttsttttt',' '+signesvar['slash']+' ')
			resulta=resulta.replace('www',' '+signesvar['www']+' ')
			resulta=resulta.replace('tttttt6ttttt',' '+signesvar['tiret']+' ')
			resulta=resulta.replace('tttttt8ttttt',' '+signesvar['soulign??']+' ')
	
			# Replace original text
			texte=texte.replace(resorig,resulta)
	


		# Other website pattern */
		motif='(([\W])([\w]*?)ttttttpttttt(org|com|fr|net|eu|it|bzh|cat|tv)([\W]))'


		for resulta in re.findall(motif, texte):
			resulta=resulta[0]
			resulta=resulta[1:-1]
			resorig=resulta
	
			# Keep final point
			resulta=re.sub('ttttttpttttt$','.',resulta)

			# Passer les ponctuations en lettre */
			resulta=resulta.replace('ttttttpttttt',' '+signesvar['point']+' ')
			resulta=resulta.replace('ttttttsttttt',' '+signesvar['slash']+' ')
			resulta=resulta.replace('www',' '+signesvar['www']+' ')
			resulta=resulta.replace('tttttt6ttttt',' '+signesvar['tiret']+' ')
			resulta=resulta.replace('tttttt8ttttt',' '+signesvar['soulign??']+' ')
	
			# Replace original text
			texte=texte.replace(resorig,resulta)
		





		# Reset punctuations
		texte=texte.replace('ttttttsttttt', '/')
		texte=texte.replace('ttttttpttttt', '.')
	
		texte=texte.replace('tttttt6ttttt', '-')
		texte=texte.replace('tttttt8ttttt', '_')
		

		
		self.content = texte
	
	
	
	#Dates processing
	def tractDates(self):
	
		texte=self.content
	
		#Months ----> to complete
		moisvar={
				'01':'genier',
				'02':'febrier',
				'03':'mar??',
				'04':'abriu',
				'05':'mai',
				'06':'junh',
				'07':'julhet',
				'08':'avost',
				'09':'setembre',
				'10':'oct??bre',
				'11':'novembre',
				'12':'decembre', 
		}
		
		
		#Searching date patterns
		#JJ/MM/AAAA and J/M/AAAA
		texte=re.sub('(^|[\W])([0-9]{1,2})(\/|\-|\.)([0-9]{1,2})(\/|\-|\.)([0-9]{4})', '\g<1>????j\g<2>j????m\g<4>m????a\g<6>a????',  texte)
		#JJ/MM/AA and J/M/AA
		texte=re.sub('(^|[\W])([0-2])?([0-9])(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([0-9]{2})', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????a\g<8>a????',  texte)
		texte=re.sub('(^|[\W])([0-2])?([0-9])(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([0-9]{2})', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????a\g<8>a????',  texte)
		texte=re.sub('(^|[\W])([3])?([0-1])(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([0-9]{2})', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????a\g<8>a????',  texte)
		texte=re.sub('(^|[\W])([3])?([0-1])(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([0-9]{2})', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????a\g<8>a????',  texte)
		#AAAA/JJ/MM and AAAA/J/M
		texte=re.sub('(^|[\W])([0-9]{4})(\/)([0-9]{1,2})(\/|\-|\.)([0-9]{1,2})', '\g<1>????j\g<6>j????m\g<4>m????a\g<2>a????',  texte)
		#AA/JJ/MM and AA/J/M
		texte=re.sub('(^|[\W])([0-9]{2})(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([0-2])?([0-9])', '\g<1>????j\g<7>\g<8>j????m\g<4>\g<5>m????a\g<2>a????',  texte)
		texte=re.sub('(^|[\W])([0-9]{2})(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([0-2])?([0-9])', '\g<1>????j\g<7>\g<8>j????m\g<4>\g<5>m????a\g<2>a????',  texte)
		texte=re.sub('(^|[\W])([0-9]{2})(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([3])?([0-1])', '\g<1>????j\g<7>\g<8>j????m\g<4>\g<5>m????a\g<2>a????',  texte)
		texte=re.sub('(^|[\W])([0-9]{2})(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([3])?([0-1])', '\g<1>????j\g<7>\g<8>j????m\g<4>\g<5>m????a\g<6>a????',  texte)
		#JJ/MM
		texte=re.sub('(^|[\W])([0-2])?([0-9])(\/)([0])?([1-9])([\W]|$)', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????\g<7>',  texte)
		texte=re.sub('(^|[\W])([0-2])?([0-9])(\/)([1])?([0-2])([\W]|$)', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????\g<7>',  texte)
		texte=re.sub('(^|[\W])([3])?([0-1])(\/)([0])?([1-9])([\W]|$)', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????\g<7>',  texte)
		texte=re.sub('(^|[\W])([3])?([0-1])(\/)([1])?([0-2])([\W]|$)', '\g<1>????j\g<2>\g<3>j????m\g<5>\g<6>m????\g<7>',  texte)
		#MM/AAAA
		texte=re.sub('(^|[\W])([0])([1-9])(\/|\-)([0-9]{4})', '\g<1>????m\g<2>\g<3>m????a\g<5>a????',  texte)
		texte=re.sub('(^|[\W])([1])([0-2])(\/|\-)([0-9]{4})', '\g<1>????m\g<2>\g<3>m????a\g<5>a????',  texte)
		#MM/AA
		texte=re.sub('(^|[\W])([0])([1-9])(\/)([0-9])([0-9])([\W]|$)', '\g<1>????m\g<2>\g<3>m????a\g<5>\g<6>a????\g<7>',  texte)
		texte=re.sub('(^|[\W])([1])([0-2])(\/)([0-9])([0-9])([\W]|$)', '\g<1>????m\g<2>\g<3>m????a\g<5>\g<6>a????\g<7>',  texte)
		
		motif1='(??(??([^??]*?)??)??)'
		
		for resulta1 in re.findall(motif1, texte):
			resulta1=resulta1[1]
		
			matches=re.search('??j([^??]*?)j??', resulta1)
			if matches:	
				jour=matches.group(1)
			else:
				jour=""
			
			
			matches=re.search('??m([^??]*?)m??', resulta1)
			if matches:		
				mois=matches.group(1)
			else:
				mois=""
			
			
			matches=re.search('??a([^??]*?)a??', resulta1)
			if matches:		
				an=matches.group(1)
			else:
				an=""
			
			
			jour=re.sub('^0', '',  jour)
			
			#Changing "one" in "first" ----> to complete
			if jour=="1":
					jour="1??r"
			
			if re.search('^([1-9])$', mois):
				mois="0"+mois
			
			if mois in moisvar:
				mois=moisvar[mois]
				if jour!="":
					if re.search('^([aeiou??????????????????????????????????????])', mois):
						mois="d'"+mois
					else:
						mois="de "+mois
				
			
			#Adding "de" before year ----> to complete (delete if it doesn't apply to your language)
			if mois!="" and an!="":
				an="de "+an
			
			nvdate=jour
			if nvdate!="" and mois!="":
				nvdate=nvdate+" "+mois
			elif mois!="":
				nvdate=mois
			
			if nvdate!="" and an!="":
				nvdate=nvdate+" "+an

			texte=re.sub('??'+resulta1+'??',nvdate, texte)
		
		
		
		texte=re.sub('??', '',  texte)
	
		self.content = texte
	
	
	
	
	#Traitement des heures
	def tractHours(self):
	
		texte=self.content
	
		#Durations names ----> to complete
		heuresvar={
				'heure_sing':'ora',
				'heure_plur':'oras',
				'minute_sing':'minuta',
				'minute_plur':'minutas',
				'seconde_sing':'segonda',
				'seconde_plur':'segondas',
				'centieme_sing':'centen',
				'centieme_plur':'centens',
				
		}
		
		#Hours symbols ----> to complete
		heuressymbol=['h', 'o', '??']
		
		
		motifs={
			#01h01 01 h 01 01o01 01??01 1h1...
			'(^|[\W])(([0-1])?([0-9])|([2])?([0-4])) ?('+'|'.join(heuressymbol)+') ?(([0-5])?([0-9]))([\W]|$)':'\g<1>????h\g<2>h????m\g<8>m????\g<11>',
			#01h 01 h 01o 01??...
			'(^|[\W])(([0-1])?([0-9])|([2])?([0-4])) ?('+'|'.join(heuressymbol)+')([\W]|$)':'\g<1>????h\g<2>h????\g<8>',
			#01:01 1:01
			'(^|[\W])(([0-1])?([0-9])|([2])?([0-4])):(([0-5])?([0-9]))([\W]|$)':'\g<1>????h\g<2>h????m\g<7>m????\g<10>',
			
			
			#01'01"01 1'1"01
			'(^|[\W])(([0-5])?([0-9]))\'(([0-5])?([0-9]))(\'\'|")([0-9]{1,2})([\W]|$)':'\g<1>????m\g<2>m????s\g<5>s????c\g<9>c????\g<10>',
			
			#01'01 1'01
			'(^|[\W])(([0-5])?([0-9]))\'(([0-5])?([0-9]))([\W]|$)':'\g<1>????m\g<2>m????s\g<5>s????\g<8>',
			
			#01"01 1"01
			'(^|[\W])(([0-5])?([0-9]))(\'\'|")([0-9]{1,2})([\W]|$)':'\g<1>????s\g<2>s????c6c????\g<7>',
		}
		
		#On recherche les diff??rents formats de date
		for motif, rempl in motifs.items():
			while re.search(motif, texte):
				texte=re.sub(motif, rempl,  texte)
		
		
		
		
		motif1='(??(??([^??]*?)??)??)';
		
		for resulta1 in re.findall(motif1, texte):
			resulta1=resulta1[1]
		
			matches=re.search('??h([^??]*?)h??', resulta1)
			if matches:		
				heure=matches.group(1)
			else:
				heure=""
			
			matches=re.search('??m([^??]*?)m??', resulta1)
			if matches:		
				minu=matches.group(1)
			else:
				minu=""
			
			matches=re.search('??s([^??]*?)s??', resulta1)
			if matches:		
				sec=matches.group(1)
			else:
				sec=""
			
			matches=re.search('??c([^??]*?)c??', resulta1)
			if matches:		
				cent=matches.group(1)
			else:
				cent=""
			
			nvdate="";
			
			if heure!="":
				if heure=="00":
					heure="0"
				nvdate=nvdate+heure
				try:
					heure=int(heure)
					if heure<2:
						nvdate=nvdate+" "+heuresvar['heure_sing']
					else:
						nvdate=nvdate+" "+heuresvar['heure_plur']
				except:
					nvdate=nvdate+" "+heuresvar['heure_plur']
				
				nvdate=nvdate+' '
			
			
			if minu!="" and minu!="0" and minu!="00":
				minu=re.sub('^0', '',  minu)
				nvdate=nvdate+minu
				try:
					minu=int(minu)
					if minu<2:
						nvdate=nvdate+" "+heuresvar['minute_sing']
					else:
						nvdate=nvdate+" "+heuresvar['minute_plur']
				except:
					nvdate=nvdate+" "+heuresvar['minute_plur']
		
				nvdate=nvdate+' '
			
			
			if sec!="" and sec!="0" and sec!="00":
				sec=re.sub('^0', '',  sec)
				nvdate=nvdate+sec
				try:
					sec=int(sec)
					if sec<2:
						nvdate=nvdate+" "+heuresvar['seconde_sing']
					else:
						nvdate=nvdate+" "+heuresvar['seconde_plur']
				except:
					nvdate=nvdate+" "+heuresvar['seconde_plur']
										
				nvdate=nvdate+' '
			
			
			if cent!="" and cent!="0" and cent!="00":
				cent=re.sub('^0', '',  cent)
				nvdate=nvdate+cent
				try:
					cent=int(cent)
					if cent<2:
						nvdate=nvdate+" "+heuresvar['centieme_sing']
					else:
						nvdate=nvdate+" "+heuresvar['centieme_plur']
				except:
					nvdate=nvdate+" "+heuresvar['centieme_plur']
								
				nvdate=nvdate+' '
			
			
			nvdate=re.sub('([ ]{2,})', ' ',  nvdate)
			nvdate=nvdate.strip(' ')
			
		
		
			texte=re.sub('??'+resulta1+'??',nvdate, texte)
		
		
	
		self.content = texte
	
	
	
	#measurments processing
	def tractMesures(self):
	
		texte=self.content
		
		#measurments names ----> to complete (singular and plural)
		mesuresvar={
				'nm':('nanom??tre', 'nanom??tres'),
				'??m':('microm??tre', 'microm??tres'),
				'mm':('millim??tre', 'millim??tres'),
				'cm':('centim??tre', 'centim??tres'),
				'dm':('d??cim??tre', 'd??cim??tres'),
				'hm??':('ectom??tre', 'ectom??tres'),
				'km':('quilom??tre', 'quilom??tres'),
				'??s':('miliseconde', 'milisecondes'),
				'mn':('minuta', 'minutas'),
				'min':('minuta', 'minutas'),
				'nL':('nanolitre', 'nanolitres'),
				'??l':('microlitre', 'microlitres'),
				'??L':('microlitre', 'microlitres'),
				'ml':('millilitre', 'millilitres'),
				'cl':('centilitre', 'centilitres'),
				'cL':('centilitre', 'centilitres'),
				'dl':('d??cilitre', 'd??cilitres'),
				'dL':('d??cilitre', 'd??cilitres'),
				'daL':('d??calitre', 'd??calitres'),
				'hl':('ectolitre', 'ectolitres'),
				'hL':('ectolitre', 'ectolitres'),
				'kl':('quilolitre', 'quilolitres'),
				'kL':('quilolitre', 'quilolitres'),
				'ng':('nanograma', 'nanogramas'),
				'??g':('micrograma', 'microgramas'),
				'mg':('milligrama', 'milligramas'),
				'cg':('centigrama', 'centigramas'),
				'dg':('decigrama', 'decigramas'),
				'dag':('decagrama', 'decagramas'),
				'hg':('ectograma', 'ectogramas'),
				'kg':('quilograma', 'quilogramas'),
				'Mt':('megatona', 'megatonas'),
				'mA':('milliamp??re', 'milliamp??res'),
				'Amp':('amp??re', 'amp??res'),
				'amp':('amp??re', 'amp??res'),
				'mHz':('millihertz', 'millihertz'),
				'Hz':('Hertz', 'Hertz'),
				'kHz':('quilohertz', 'quilohertz'),
				'MHz':('megahertz', 'megahertz'),
				'hPa':('ectopascal', 'ectopascals'),
				'MPa':('megapascal', 'megapascals'),
				'GPa':('gigapascal', 'gigapascals'),
				'TPa':('terapascal', 'terapascals'),
				'GV':('gigav??lt', 'gigav??lts'),
				'MV':('megav??lt', 'megav??lts'),
				'kV':('quilov??lt', 'quilov??lts'),
				'hV':('ectov??lt', 'ectov??lts'),
				'daV':('decav??lt', 'decav??lts'),
				'dV':('deciv??lt', 'deciv??lts'),
				'cV':('centiv??lt', 'centiv??lts'),
				'mV':('milliv??lt', 'milliv??lts'),
				'??V':('microv??lt', 'microv??lts'),
				'nV':('nanov??lt', 'nanov??lts'),
				'Wb':('Weber', 'Webers'),
				'lm':('lumen', 'lumens'),
				'sr':('Radian', 'Radians'),
				'lx':('Lux', 'Luxs'),
				'Bq':('Becquerel', 'Becquerels'),
				'Gy':('Gray', 'Grays'),
				'kat':('Katal', 'Katals'),
				'Ko':('quil??octet', 'quil??octets'),
				'Kb':('quil??octet', 'quil??octets'),
				'Mb':('megaoctet', 'megaoctets'),
				'Gb':('gigaoctet', 'gigaoctets'),
		}
		
		#measurments unities names ----> to complete (singular and plural)
		unitesvar={
				'm':('m??tre', 'm??tres'),
				's':('segonda', 'segondas'),
				'A':('amp??re', 'amp??res'),
				'm2':('m??tre cairat', 'm??tres cairats'),
				'm3':('m??tre cubic', 'm??tres cubics'),
				'm??':('m??tre cairat', 'm??tres cairats'),
				'm??':('m??tre cubic', 'm??tres cubics'),
				'm\/s':('m??tre per segonda', 'm??tres per segonda'),
				'm\/s2':('m??tre per segonda cairada', 'm??tres per segonda cairada'),
				'km\/h':('quilom??tre per ora', 'quilom??tre per ora'),
				'Hz':('h??rtz', 'h??rtzes'),
				'Pa':('pascal', 'pascals'),
				'V':('v??lt', 'v??lts'),
				'carre':'au cairat',
				'cube':'au cube',
				'puiss':'a la pot??ncia',
		}
		
		#singular determiners ----> to complete
		singDeterminers=['lo', 'la', 'un', 'una', 'zero', 'z??ro', 'z??ro', 'zer??']
		
		
		texte=re.sub('([a-z??????????????????????????????????????????A-Z??????????????????????????????????????????])??([^????????????????????????])', '\g<1> '+unitesvar['carre']+'\g<2>', texte)
		texte=re.sub('([a-z??????????????????????????????????????????A-Z??????????????????????????????????????????])??([^????????????????????????])', '\g<1> '+unitesvar['cube']+'\g<2>', texte)
		texte=re.sub('([a-z??????????????????????????????????????????A-Z??????????????????????????????????????????0-9 ])([????????????????????????])', '\g<1> '+unitesvar['puiss']+' \g<2>', texte)
		texte=texte.replace("??","1")
		texte=texte.replace("??","2")
		texte=texte.replace("??","3")
		texte=texte.replace("???","4")
		texte=texte.replace("???","5")
		texte=texte.replace("???","6")
		texte=texte.replace("???","7")
		texte=texte.replace("???","8")
		texte=texte.replace("???","9")
		
		
		for mesure, nom in mesuresvar.items():
			#Putting singular name after 1 or 0
			texte=re.sub('([^0-9 ]|[^0-9] )([0-1])(,([0-9]+))? ?'+mesure+'([\W]????????????????????????|$)','\g<1>\g<2>\g<3> '+nom[0]+'\g<5>',texte)
			#Putting singular name after singular determiners
			texte=re.sub('('+'|'.join(singDeterminers)+') '+mesure+'([\W]????????????????????????|$)','\g<1> '+nom[0]+'\g<2>',texte)
			
			#Otherwise putting plural names
			texte=re.sub('([^a-z??????????????????????????????????????????A-Z??????????????????????????????????????????])'+mesure+'([\W????????????????????????]|$)','\g<1> '+nom[1]+'\g<2>',texte)
			#On v??rifie les carr??s
			texte=re.sub(nom[1]+' (carrat|cubic)([^s])', nom[1]+' \g<1>s\g<2>' ,texte)
		
		
		
		for unite, nom in unitesvar.items():
			#On met le nom au singulier apr??s 1 ou 0
			texte=re.sub('([^0-9 ]|[^0-9] )([0-1])(,([0-9]+))? ?'+unite+'([\W]|$)','\g<1>\g<2>\g<3> '+nom[0]+'\g<5>',texte)
			#On met le nom au pluriel apr??s un autre chiffre	
			texte=re.sub('([0-9]) ?'+unite+'([\W]|$)','\g<1> '+nom[1]+'\g<2>', texte)
		
		
		texte=re.sub(unitesvar['m'][0]+' '+unitesvar['carre'], unitesvar['m2'][0], texte)
		texte=re.sub(unitesvar['m'][1]+' '+unitesvar['carre'], unitesvar['m2'][1], texte)
		texte=re.sub(unitesvar['m'][0]+' '+unitesvar['cube'], unitesvar['m3'][0], texte)
		texte=re.sub(unitesvar['m'][1]+' '+unitesvar['cube'], unitesvar['m3'][1], texte)
		
		
		#Atomes
		
		#atomes names ----> to complete
		atomes={
				'CO2':'c?? o dos',
				'O2':'o dos',
				'H2O':'at??a dos o',
		}
		
		for code, nom in atomes.items():
			texte=re.sub('(^|[\W])'+code+'([\W]|$)','\g<1>'+nom+'\g<2>',texte)
		
		
		
		
	
		self.content = texte
	
	
	#Processing roman numbers
	def tractRomanNumbers(self):
		
		#ordinal numbers abbreviations ending ----> to complete
		terminaisonsord=['e', 'au', 'en', 'n', 'e', 'er', 'era', '??r', '??ra', 'nd', 'nda', 'd', 'da', 'ra', 'me', 'ma', 'esme', 'sme', 'esma', 'sma']
		
		#words for "century" ----> to complete
		siecle=['s.', 's??gle', 'si??cle', 'secle', 'siecle']
		siecleespap=[]
		siecleespav=[]
		for s in siecle:
			s=s.replace('.', '\.')
			s=s+' '
			siecleespap.append(s+' ')
			siecleespav.append(' '+s)
	
		texte=self.content
		
		#Replacing CD width "c??d??" ----> to complete (change "c??d??" with the pronunciation of this word in your language)
		texte=re.sub('([\W]|^)CD([\W]|$)', '\g<1>c??d??\g<2>', texte)
		
		#Searching for patterns
		texte=re.sub('([\W]|^)([IVXLCDM]{2,})([\W]|$)', '\g<1>#\g<2>#\g<3>', texte)
		texte=re.sub('([\W]|^)([IVXLCDM]{2,})('+'|'.join(terminaisonsord)+')([\W]|$)', '\g<1>#\g<2>#\g<3>\g<4>', texte)
		texte=re.sub('([\W]|^)([X])(au|en)([\W]|$)', '\g<1>#\g<2>#\g<3>\g<4>', texte)
		texte=re.sub('([\W]|^)('+'|'.join(siecleespap)+')([IVXLCDM])([\W]|$)', '\g<1>\g<2>#\g<3>#\g<4>', texte)
		texte=re.sub('([\W]|^)([IVXLCDM])('+'|'.join(siecleespav)+')', '\g<1>#\g<2>#\g<3>', texte)
		
		motif1='(#([IVXLCDM]+)#)'
		


		for resulta1 in re.findall(motif1, texte):
			resulta1=resulta1[1]
			chiffres=romanToArabic(resulta1)
			texte=re.sub('\#'+resulta1+'\#',str(chiffres), texte)
		
	
		
	
		self.content = texte;
	
	
	
	#Numbers processing
	def tractNumbers(self):
	
		texte=self.content
		
		# Checking for phone numbers
		texte=re.sub('(^|[^0-9 ])( ?)0([1-9])([\.\- ])([0-9]{2})\4([0-9]{2})\4([0-9]{2})\4([0-9]{2})( ?)([^0-9 ]|$)', '\g<1> '+chiffresvar['0']+' #??\g<3>??# #??\g<5>??# #??\g<6>??# #??\g<7>??# #??\g<8>??#\g<9>\g<10>', texte)
		
		
		texte=re.sub('(^|[^0-9 ])( ?)\+([1-9]{2}) ?([0-9]) ([0-9 ]+)([0-9])( ?)([^0-9 ]|$)', '\g<1>\g<2>+#??\g<3>??# #??\g<4>??# /___tel___\g<5>\g<6>___tel___/\g<7>\g<8>', texte)
		
		while re.search('/___tel___([^_]*?)([^\#]) ', texte):
			texte=re.sub(')/___tel___([^_]*?)([^\#]) ', '/___tel___\g<1>\g<2>??# #??', texte)
		
		
		texte=texte.replace('/___tel___', '#??')
		texte=texte.replace('___tel___/', '??#')

		# Checking for operations
		texte=re.sub('([0-9]+) ?- ?([0-9]+)', '\g<1> '+chiffresvar['moins']+' \g<2>', texte)
		texte=re.sub('([0-9]+) ?(x|\*) ?([0-9]+)', '\g<1> '+chiffresvar['fois']+' \g<3>', texte)
		
		# Number pattern
		motif='(^|[^0-9\??# ])( ?)([0-9| |]+)((,|\.)([0-9]+)([0-9| |]*?))?( ?)([^0-9\??# ]|$)'

		# Surrounding numbers with #?? ??# */
		for i in range(0,10):
			texte=re.sub(motif,'\g<1>\g<2>#??\g<3>\g<4>??#\g<8>\g<9>',texte)
		
		texte=re.sub('#?? *???#', ' ', texte)
		
		texte=re.sub('#?? ', ' #??', texte)
		texte=re.sub(' ??#', '??# ', texte)
		
		while re.search('#??([^??]*?) ',texte):
			texte=re.sub('#??([^??]*?) ', '#??\g<1>', texte)
		
		
		
		
		# Processing zeros */
		
		#Telling it if it's before a comma
		texte=re.sub('#?? ?(0*?)0 ???# ?,', '#??\g<1>??# '+chiffresvar['0']+' ,', texte)
		#Telling it if it's before another zero
		while re.search('#?? ?(0*?)0 ???# ?'+chiffresvar['0']+'', texte):
			texte=re.sub('#?? ?(0*?)0 ???# ?'+chiffresvar['0']+'', '#??\g<1>??#'+chiffresvar['0']+' '+chiffresvar['0']+'', texte)
		
		#Telling it if it's after a comma
		texte=re.sub(', ?#?? ?0',' '+virgule+' '+chiffresvar['0']+' #??',texte)
	
		#Telling it if it's at the beginning of a number
		texte=re.sub('#?? ?0', ' '+chiffresvar['0']+' #??', texte)
		
		#Telling it if it's after a zero
		while re.search(''+chiffresvar['0']+' #?? ?0', texte):
			texte=re.sub(''+chiffresvar['0']+' #?? ?0', ''+chiffresvar['0']+' '+chiffresvar['0']+' #??\g<1>', texte)
		
		
		texte=re.sub(' ??#', '??# ', texte)
		texte=re.sub('#?? ', ' #??', texte)
		texte=re.sub('#??([12])??#', '#??\g<1>??#??', texte)

		motif1='(#??([0-9,\. ]+)??#)'
			
		

		for resulta1 in re.findall(motif1, texte):
			resulta1=resulta1[0]
			
			#Sorting the result and splitting with commas
			resulta1=re.sub('^( *?)#(.*?)#( *?)$', '\g<2>', resulta1)
			resulta1=resulta1.strip(" ")
			resulta1=resulta1.replace('??', '')
	
			resulta_expl=resulta1.replace('.', ',')
			resultas=resulta_expl.split(',')
			
			# Memorize the initial number
			chifra=resulta1
			
			# Initialize final number
			resfin="";
	
			# For every side of the comma
			for resulta in resultas:
				

				resulta=resulta.replace(' ', '')
	
	
				# ------- If there are thousands, millions, billions... ------- */
	
				#Millions of millions*/
				resulta=re.sub('(.)(...............)$', '\g<1>??\g<2>', resulta)
	
				#Thousand billions*/
				resulta=re.sub('(.)(............)$', '\g<1>#\g<2>', resulta)
	
				#Billions
				resulta=re.sub('(.)(.........)$', '\g<1>??\g<2>', resulta)
	
				#Millions
				resulta=re.sub('(.)(......)$', '\g<1>??\g<2>', resulta)
	
				#Thousands
				resulta=re.sub('(.)(...)$', '\g<1>#\g<2>', resulta)
	
				# ------- Putting into letters the last numeral ------- */	
	
				# Tens */
				resulta=re.sub('10([??|??|,|#|??]|$)',chiffresvar['10']+' \g<1>',resulta)
				resulta=re.sub('11([??|??|,|#|??]|$)',chiffresvar['11']+' \g<1>',resulta)
				resulta=re.sub('12([??|??|,|#|??]|$)',chiffresvar['12']+' \g<1>',resulta)
				resulta=re.sub('13([??|??|,|#|??]|$)',chiffresvar['13']+' \g<1>',resulta)
				resulta=re.sub('14([??|??|,|#|??]|$)',chiffresvar['14']+' \g<1>',resulta)
				resulta=re.sub('15([??|??|,|#|??]|$)',chiffresvar['15']+' \g<1>',resulta)
				resulta=re.sub('16([??|??|,|#|??]|$)',chiffresvar['16']+' \g<1>',resulta)
				resulta=re.sub('17([??|??|,|#|??]|$)',chiffresvar['17']+' \g<1>',resulta)
				resulta=re.sub('18([??|??|,|#|??]|$)',chiffresvar['18']+' \g<1>',resulta)
				resulta=re.sub('19([??|??|,|#|??]|$)',chiffresvar['19']+' \g<1>',resulta)
	
				# Twenties */
				resulta=re.sub('20([??|??|,|#|??]|$)',chiffresvar['20']+' \g<1>',resulta)
				resulta=re.sub('21([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['1']+' \g<1>',resulta)
				resulta=re.sub('22([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['2']+' \g<1>',resulta)
				resulta=re.sub('23([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['3']+' \g<1>',resulta)
				resulta=re.sub('24([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['4']+' \g<1>',resulta)
				resulta=re.sub('25([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['5']+' ',resulta)
				resulta=re.sub('26([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['6']+' \g<1>',resulta)
				resulta=re.sub('27([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['7']+' \g<1>',resulta)
				resulta=re.sub('28([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['8']+' \g<1>',resulta)
				resulta=re.sub('29([??|??|,|#|??]|$)',chiffresvar['20']+'-e-'+chiffresvar['9']+' \g<1>',resulta)
	
				# Units */
				resulta=re.sub('1([??|??|,|#|??]|$)',chiffresvar['1']+'\g<1>',resulta)
				resulta=re.sub('2([??|??|,|#|??]|$)',chiffresvar['2']+'\g<1>',resulta)
				resulta=re.sub('3([??|??|,|#|??]|$)',chiffresvar['3']+'\g<1>',resulta)
				resulta=re.sub('4([??|??|,|#|??]|$)',chiffresvar['4']+'\g<1>',resulta)
				resulta=re.sub('5([??|??|,|#|??]|$)',chiffresvar['5']+'\g<1>',resulta)
				resulta=re.sub('6([??|??|,|#|??]|$)',chiffresvar['6']+'\g<1>',resulta)
				resulta=re.sub('7([??|??|,|#|??]|$)',chiffresvar['7']+'\g<1>',resulta)
				resulta=re.sub('8([??|??|,|#|??]|$)',chiffresvar['8']+'\g<1>',resulta)
				resulta=re.sub('9([??|??|,|#|??]|$)',chiffresvar['9']+'\g<1>',resulta)
				resulta=re.sub('0([??|??|,|#|??]|$)',chiffresvar['0']+'\g<1>',resulta)
	
			
	
				# ------- Putting into letters the second-to-last numeral ------- */	
	
				resulta=re.sub('3([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)',chiffresvar['30']+' \g<1>\g<2>',resulta)
	
				resulta=re.sub('4([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)',chiffresvar['40']+' \g<1>\g<2>',resulta)
	
				resulta=re.sub('5([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)',chiffresvar['50']+' \g<1>\g<2>',resulta)
	
				resulta=re.sub('6([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)',chiffresvar['60']+' \g<1>\g<2>',resulta)
	
				resulta=re.sub('7([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)',chiffresvar['70']+' \g<1>\g<2>',resulta)
	
				resulta=re.sub('8([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)',chiffresvar['80']+' \g<1>\g<2>',resulta)
	
				resulta=re.sub('9([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)',chiffresvar['90']+' \g<1>\g<2>',resulta)
	
				resulta=re.sub('0([a-z|??|??|??|??|??|??|??|??]+)([??|??|,|#|??]|$)', ' \g<1>\g<2>', resulta)
	
	
	
	
				# ------- Putting into letters the hundreds ------- */	
	
				resulta=re.sub('1([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('2([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['2']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('3([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['3']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('4([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['4']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('5([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['5']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('6([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['6']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('7([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['7']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('8([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['8']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('9([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)',chiffresvar['9']+'_'+chiffresvar['100sing']+' \g<1> \g<2>\g<3>',resulta)
	
				resulta=re.sub('0([^ ]*?) ([^ ]*?)([??|??|,|#|??]|$)', ' \g<1> \g<2>\g<3>', resulta)
	
	
				# Adding a "s" to "hundred" if there is nothing after ----> to complete (delete if it doesn't apply to your language)
				resulta=re.sub('_'+chiffresvar['100sing']+'$','_'+chiffresvar['100plur'],resulta)
				resulta=re.sub('_'+chiffresvar['100sing']+'  '+chiffresvar['0']+'$','_'+chiffresvar['100plur'],resulta)
				resulta=re.sub('_'+chiffresvar['100sing']+' ,$', '_'+chiffresvar['100plur']+' ,', resulta)
	
	
	
	
	
				# ------- Removing zeros, writting thousand, million... ------- */	
		
				resulta=resulta.replace(chiffresvar['0'], ' ')
	
				resulta=re.sub('??([ ]{1,})#', '??', resulta)
				resulta=resulta.replace('#',' '+chiffresvar['1000']+' ')
				resulta=resulta.replace('un '+chiffresvar['1000']+'',''+chiffresvar['1000']+'')
				resulta=re.sub('??([ ]{1,})??', '??', resulta)
				resulta=resulta.replace('??',' '+chiffresvar['millionsing']+' ')
				resulta=re.sub('( un|[^u]n|[^n]) '+chiffresvar['millionsing']+'', '\g<1> '+chiffresvar['millionplur']+'',  resulta)
				
				
				resulta=resulta.replace('??',' '+chiffresvar['milliardsing']+' ')
				resulta=re.sub('( un|[^u]n|[^n]) '+chiffresvar['milliardsing']+'', '\g<1> '+chiffresvar['milliardplur']+'',  resulta)
				resulta=resulta.replace('??',' '+chiffresvar['billionsing']+' ')
				resulta=re.sub('( un|[^u]n|[^n]) '+chiffresvar['billionsing']+'', '\g<1> '+chiffresvar['billionplur']+'',  resulta)
				resulta=resulta.replace('_', ' ')
				resulta=resulta.replace('??', '')
				resulta=resulta.replace('  ', ' ')
				resulta=resulta.replace('  ', ' ')
				resulta=resulta.strip(' ')

				# ------- Adding the result to the final text ------- */
				resfin=resfin+','+resulta
		
			
			
	
	
			# ------- Removing the first comma and replacing the second ------- */
			resfin=resfin[1:]
			resfin=resfin.replace(',', ' '+virgule+' ')
			
			texte=re.sub('([\s]){2,}', ' ', texte)
			# ------- Replacing the number with the final text ------- */
			
			
			texte=re.sub('#??( ?)'+chifra+'( ?)??#', '\g<1>'+resfin+'\g<2>??', texte)
			texte=re.sub(' ??', '??', texte)
		
		#Correcting ordinal endings
		texte=re.sub('un?????([??e]r)(a?)([\W]|$)',chiffresvar['premier']+"\g<2>\g<3>",texte)
		texte=re.sub('un????a([\W]|$)',chiffresvar['premier']+"a\g<1>",texte)
		texte=re.sub('d[ou]s???(n?d)(a?)([\W]|$)',chiffresvar['second']+"\g<2>\g<3>",texte)
		texte=re.sub('un?????ra([\W]|$)',chiffresvar['premier']+"a\g<1>",texte)
		texte=re.sub('d[ou]s?????da([\W]|$)',chiffresvar['second']+"a\g<1>",texte)
		texte=re.sub('??', '', texte)
		texte=re.sub('??n(a?)([\W]|$)', '??en\g<1>\g<2>', texte)
		texte=re.sub('??a([\W]|$)', '??ena\g<1>', texte)
		texte=re.sub('??e([\W]|$)', '??en\g<1>', texte)
		texte=re.sub('??e?s?m(e|a)([\W]|$)', '??esm\g<1>\g<2>', texte)
		texte=re.sub('(c)??(ena?|au|esm[ea])([\W]|$)', 'qu??\g<2>\g<3>', texte)
		texte=re.sub('(g)??(ena?|au|esm[ea])([\W]|$)', 'gu??\g<2>\g<3>', texte)
		texte=re.sub('([ea])??(ena?|au|esm[ea])([\W]|$)', '\g<2>\g<3>', texte)

		#Removing hashes
		texte=re.sub('??', '', texte)
		



		
		texte=re.sub('#??', '', texte)
		texte=re.sub('??#', '', texte)

		self.content = texte
	
	
	
	#Acronyms processing
	def tractSigles(self):
		texte=self.content
		texte=texte.replace("???", "'")
		
		# acronyms ----> to complete
		
		acronymes={
			'ADEME':'ademe',
			'ASSEDIC':'assedic',
			'CD-ROM':'CD r??m',
			'CEDEX':'cedex',
			'CNED':'cned',
			'CNIL':'cnil',
			'COGEMA':'cogem??',
			'DOM-TOM':'d??m-t??m',
			'DOS':'d??s',
			'ENA':'en??',
			'ESPE':'esp??',
			'EUROPOL':'europ??l',
			'EUROSTAT':'eurostat',
			'FEDER':'fed??r',
			'FIFA':'fifa',
			'FRONTEX':'frontex',
			'GAEC':'ga??c',
			'GAFA':'gaf??',
			'GAFAM':'gafam',
			'GRETA':'gret??',
			'HADOPI':'adop??',
			'IBAN':'ib??n',
			'INRA':'inr??',
			'INSA':'ins??',
			'ISO':'is??',
			'LED':'l??d',
			'MAC':'mac',
			'MIDI':'mid??',
			'MOOC':'m??c',
			'ONU':'onu',
			'OTAN':'otan',
			'OVNI':'ovni',
			'PAC':'pac',
			'RAM':'ram',
			'RASED':'raz??d',
			'RIB':'rib',
			'SAMU':'sam??',
			'SEGPA':'secp??',
			'SEPA':'sep??',
			'SICAV':'sicav',
			'SIDA':'sid??',
			'SIREN':'sir??n',
			'SIRET':'sir??t',
			'SMIC':'esmic',
			'STAPS':'staps',
			'UNEDIC':'unedic',
			'UNESCO':'un??sco',
			'URSSAF':'ursaf',
			'ZAD':'zad',
			'ZEP':'zep',
			'ZUP':'zup',
			'ERASMUS':'erasmus',
			'OPLO':'oplo',
			'??PLO':'??plo',
			'INOC':'in??c',
			'IN??C':'in??c',
			'CFPOC':'CFP ??c',
			'CFP??C':'CFP ??c',
			'CIRDOC':'cird??c',
			'CIRD??C':'cird??c',
			'CAPOC':'cap??c',
			'CAP??C':'cap??c',
			'OC TELE':'??c tele',
			'??C TELE':'??c tele',
			'CLAB':'clab',
			'OCBI':'??cb??',
			'??CBI':'??cb??',
			'OC-BI':'??cb??',
			'??C-BI':'??cb??',
			'FIMOC':'fim??c',
			'FIM??C':'fim??c',
			'CIAPA':'ciap??',
			'CREO':'cre??',
			'CR??O':'cre??',
			'BIOCOOP':'bioc??p',
			'IDELIS':'idel??s',
			'SACEM':'sac??m',
			'DASEN':'dasen',
			'AMAP':'amap',
			'TAFTA':'tafta',
			'DRAC':'drac',
			'EHPAD':'epad',
			'INSEE':'ins??',
			'INSERM':'ins??rm',
			'MEDEF':'med??f',
			'WIFI':'wifi',
			'WI-FI':'wifi',

		
		}
		
		for acron, nom in acronymes.items():
			texte=re.sub("(^|'|[\W])"+acron+"([\W]|$)",'\g<1>'+nom+'\g<2>',texte)
		
		
		
		# Remplace the points with characters
		texte=texte.replace('.', 'TTTTTPTTTTT')

		# Acronym pattern
		motif="((^|'|[\W])([A-Z????????????????????]{2,})([\W]|$))";

		# Surrounding acronyms with #
		texte=re.sub(motif,'\g<2>#\g<3>#\g<4>',texte)
		

		for res in re.findall(motif, texte):
			resulta=res[0]

			resulta=resulta[1:-1]
			resorig=resulta
			resulta=resulta.replace('TTTTTPTTTTT', '.')
	
			# Replacing letters with their names ----> to complete (change the name of each letter !!! keep the ending whitespace)
			resulta=resulta.replace('A', ' a ')
			resulta=resulta.replace('??', ' a ')
			resulta=resulta.replace('??', ' a ')
			resulta=resulta.replace('B', ' be ')
			resulta=resulta.replace('C', ' ce ')
			resulta=resulta.replace('D', ' de ')
			resulta=resulta.replace('E', ' e ')
			resulta=resulta.replace('??', ' e ')
			resulta=resulta.replace('??', ' ?? ')
			resulta=resulta.replace('F', ' ??fa ')
			resulta=resulta.replace('G', ' ge ')
			resulta=resulta.replace('H', ' acha ')
			resulta=resulta.replace('I', ' i ')
			resulta=resulta.replace('??', ' i ')
			resulta=resulta.replace('??', ' i ')
			resulta=resulta.replace('J', ' ji ')
			resulta=resulta.replace('K', ' ka ')
			resulta=resulta.replace('L', ' ??la ')
			resulta=resulta.replace('M', ' ??ma ')
			resulta=resulta.replace('N', ' ??na ')
			resulta=resulta.replace('O', ' o ')
			resulta=resulta.replace('??', ' o ')
			resulta=resulta.replace('??', ' ?? ')
			resulta=resulta.replace('P', ' pe ')
			resulta=resulta.replace('Q', ' ku ')
			resulta=resulta.replace('R', ' ??ra ')
			resulta=resulta.replace('S', ' ??ssa ')
			resulta=resulta.replace('T', ' te ')
			resulta=resulta.replace('U', ' u ')
			resulta=resulta.replace('??', ' u ')
			resulta=resulta.replace('??', ' u ')
			resulta=resulta.replace('V', ' ve ')
			resulta=resulta.replace('W', ' ve dobla ')
			resulta=resulta.replace('X', ' icsa ')
			resulta=resulta.replace('Y', ' i gr??ga ')
			resulta=resulta.replace('Z', ' iz??da ')
	
			# Looking if there is a point at the end */
			if re.search('\.$',resulta):
				if re.search('\.(.+)$',resulta):
					pf="n"
				else:
					pf="o"
			else:
				pf="n"
			
	
			# Removing points and spaces */
			resulta=resulta.replace('.', '')
			resulta=resulta.strip(' ')
	
			# Adding a point if the acronym ends with a point and is followed by an uppercase or the end of the text
			if re.search('#'+resorig+'#( ?)([A-Z????????????????????]|$)',texte) and pf=="o":
				resulta=resulta+'.'
			

			# Replacing the sigle with its name
			texte=texte.replace('#'+resorig+'#',resulta)
			
	

		# Putting points again
		texte=texte.replace('TTTTTPTTTTT', '.')
		
		
		self.content = texte

	
	
	#Uppercase
	def minuscules(self):
		texte=self.content
		texte=motmin(texte)
		
		self.content = texte

	


	
	
	#Pre-processing some specific words
	def pretrait(self):
	
		texte=self.content
		
		#Insert here, if needed, processing for words whose pronunciation is more complex than a single exception
		
		self.content = texte
		
		
	
	#Special characters processing
	def charSpe(self, etendue="all"):
	
		texte=self.content
		
		#Symbols names ----> to complete
		signesvar={
				'$':'d??lar',
				'??':'liura',
				'???':'colon',
				'???':'shek??l',
				'???':'won',
				'??':'ien',
				'???':'eur??',
				'???':'tugrik',
				'???':'peso',
				'z??':'zl??ti',
				'???':'bat',
				'@':'ar??ba',
				'+':'plus',
				'#':'diesi',
				'&':'e',
				'/':'eslash',
				'%':'per cent',
				'<':'inferior a',
				'>':'superior a',
				'=':'egala',
				'???':'soma',
				'??':'devesit per',
				'???':'infinit',
				'???':'perpendicular a',
				'???':'integrala',
				'???':'diferent de',
				'???':'environ',
				'???':'inferior o egau a',
				'???':'superior o egau a',
				'??':'pi',
				'???':'d??lta',
				'&':'e',
				'??C':'grad',
				'??F':'grad Fahrenheit',
				'n??':'num??ro',
				'N??':'num??ro',
				'??':'grad',
				'??':'paragrafe',
				'??':'alf??',
				'??':'bet??',
				'??':'gamm??',
				'??':'fi',
				'??':'psi',
				'??':'omeg??',
				'*':'asterisc',
				'??':'micr??',
				'??':'??hm',
		}
		
		#Symbols plural names ----> to complete
		signesplurvar={
				'$':'d??lars',
				'??':'liuras',
				'???':'colons',
				'???':'shek??ls',
				'???':'wons',
				'??':'iens',
				'???':'eur??s',
				'???':'tugriks',
				'???':'pesos',
				'z??':'zl??tis',
				'???':'bats',
				'??C':'grads',
				'??F':'grads Fahrenheit',
				'??':'grads',
				'??':'??hms',
		}
		
		
		
		
		texte=texte.replace('...', '??? ')
		texte=texte.replace("???","-")
		texte=texte.replace("???","'")
		texte=texte.replace("' ","'")
		texte=texte.replace("!"," !")
		texte=texte.replace("?"," ?",)
		texte=re.sub("[ ]{2,}"," ",texte)
		
		#Deleting multiple punctuations
		texte=re.sub("([^\!\?])(( \? \!)+)( ([^\!\?])| ?$)","\g<1> ?\g<4>",texte)
		texte=re.sub("([^\!\?])(( \! \?)+)( ([^\!\?])| ?$)","\g<1> ?\g<4>",texte)
		texte=re.sub("(([\!]|( \!)){2,})"," ! ",texte)
		texte=re.sub("(([\?]|( \?)){2,})"," ? ",texte)
		
		
		
		if etendue!="light":
			texte=texte.replace('-', ' ')
		
		
		#regexp for plural numbers
		regexplur="("
		for chiffre, nom in chiffresvar.items():
			if re.search("([1-9][01]|[2-9])",chiffre):
				regexplur=regexplur+nom+"|"
			
		
		regexplur=re.sub("\|$",")",regexplur)
		
		#Replacing symbols with their names
		for signe, nom in signesvar.items():
			
			#Replacing plurals first
			if signe in signesplurvar:
				if not re.search('^[a-z????????????????????????????????????????????????A-Z????????????????????????????????????????????????0-9]', signe):
					signerg="\\"+signe
				else:
					signerg=signe
				#Replacing if the text ends with a plural number
				texte=re.sub(""+regexplur+"( *?)"+signerg,"\g<1> "+signesplurvar[signe],texte)
				#Replacing if the text ends with a plural number then 1
				texte=re.sub(regexplur+"( e | ?- ?| "+virgule+" | )"+chiffresvar["1"]+"( *?)"+signerg,"\g<1>\g<2>"+chiffresvar["1"]+" "+signesplurvar[signe],texte)
			
			
		
			texte=texte.replace(signe," "+nom+" ")
		
		
		
		
		texte=texte.replace("???", "?? ")
		texte=texte.replace("???", " ??")
		texte=re.sub("([ ]{2,})"," ",texte)
		
		
		if etendue!="light":
			texte=re.sub("(['???])n"," n",texte)
			texte=re.sub("qu[???'???]","k'",texte)
			texte=re.sub("gu[???'???]([a????????o????????u????????])","g'\g<1>",texte)
		
		texte=texte.replace("???","'")
		texte=texte.replace('???',"'")
		
		
		if etendue!="light":
			texte=re.sub("([^a-z????????????????????????????????????????????????A-Z????????????????????????????????????????????????0-9 \W???????'])"," ",texte)
		
		
		
		
		texte=re.sub('([\s]){2,}', ' ', texte)
		
		
		self.content = texte

	
	
	#Abbreviations processing
	def tractAbbrev(self):
	
		texte=self.content
		
		#Abbreviations names ----> to complete
		signesvar={
				'CDs':'ced??s',
				'adj':'liura',
				'adj':'adjectiu',
				'etc':'et cetera',
				'eca':'et cetera',
				'expr':'expression',
				'masc??=':'masculin',
				'rdv':'rendetz-vos',
				'R\.\-V.':'rendetz-vos',
				'RV':'rendetz-vos',
				'RDV??':'rendetz-vos',
				'R\.D\.V':'rendetz-vos',
				'apt':'apartament',
				'APT':'apartament',
				'bd':'baloard',
				'bld':'baloard',
				'Cie':'companhi??',
				'Cia':'companhi??',
				'Dr':'doctor',
				'ex':'exemple',
				'HS':'f??ra servici',
				'H\.S\.':'f??ra servici',
				'hs':'f??ra servici',
				'h\.s\.':'f??ra servici',
				'HT':'f??ra taxa',
				'H\.T\.':'f??ra taxa',
				'ht':'f??ra taxa',
				'h\.t\.':'f??ra taxa',
				'TTC':'totas taxas compresas',
				'T\.T\.C\.':'totas taxas compresas',
				'ttc':'totas taxas compresas',
				't\.t\.c\.':'totas taxas compresas',
				'Mme':'D??na',
				'Na':'D??na',
				'Da':'D??na',
				'Sr':'S??nher',
				'Mr':'S??nher',
				'pb':'probl??ma',
				'PJ':'p????a joncha',
				'P\.J\.':'p????a joncha',
				'pj':'p????a joncha',
				'p\.j\.':'p????a joncha',
				'PM':'de l???apr??s-miegjorn',
				'P\.M\.':'de l???apr??s-miegjorn',
				'pm':'de l???apr??s-miegjorn',
				'p\.m\.':'de l???apr??s-miegjorn',
				'AM':'dau matin',
				'A\.M\.':'dau matin',
				'am':'dau matin',
				'a\.m\.':'dau matin',
				'pt':'ponch',
				'St':'sant',
				'ST':'sant',
				'Sta':'santa',
				'STA':'santa',
				'Ste':'santa',
				'STE':'santa',
				'STP':'si te plai',
				'S\.T\.P\.':'si te plai',
				'stp':'si te plai',
				's\.t\.p\.':'si te plai',
				'SVP':'si vos plai',
				'S\.V\.P\.':'sie vos plai',
				'svp':'si vos plai',
				's\.v\.p\.':'si vos plai',
				'rte':'rota',
				'rta':'rota',
				'NB':'nota bene',
		}
		

		for signe, nom in signesvar.items():
			texte=re.sub('(^|[\W])'+signe+'([\W]|$)', '\g<1>'+nom+'\g<2>', texte)
		
		
		
		self.content = texte

	
	
	#Deleting double spaces
	def supDblEsp(self):
	
		texte=self.content
		texte=re.sub('([\s]){2,}', ' ', texte)
		self.content = texte

	
	
	#Splitting text in words
	def listeMots(self):
		texte=self.content
		mots=texte.split(' ')
		
		nvmots=[]
		for i in range(0,len(mots)):
			if  mots[i]!='':
				if re.search('([\w???????])([\W???????]+)$', mots[i]):
					mot1=re.sub('([\w???????])([\W???????]+)$', '\g<1>', mots[i])
					
					if re.search('^([\W???????]+)([\w???????])', mot1):
						mot1a=re.sub('^([\W???????]+)([\w???????])(.*?)$', '\g<1>', mot1)
						nvmots.append(mot1a)
						mot2a=re.sub('^([\W???????]+)([\w???????])(.*?)$', '\g<2>\g<3>', mot1)
						nvmots.append(mot2a)
					
					else:
						nvmots.append(mot1)
					
					
					mot2=re.sub('^(.*?)([\w???????])([\W???????]+)$', '\g<3>', mots[i])
					nvmots.append(mot2)
				elif re.search('^([\W???????]+)([\w???????])', mots[i]):
					mot1a=re.sub('^([\W???????]+)([\w???????])(.*?)$', '\g<1>', mots[i])
					nvmots.append(mot1a)
					mot2a=re.sub('^([\W???????]+)([\w???????])(.*?)$', '\g<2>\g<3>', mots[i])
					nvmots.append(mot2a)
					
				else:
				
					nvmots.append(mots[i])
				
			
		
		return nvmots
	
	#Expand text
	def expandSelf(self):
		self.tractTags()
		self.tractMails()
		self.tractDates()
		self.tractHours()
		self.tractMesures()
		self.tractRomanNumbers()
		self.tractNumbers()
		self.tractSigles()
		self.pretrait()
		self.charSpe()
		self.tractAbbrev()
		self.supDblEsp()
		
	
	#Expand text and split it into words
	def tractSelf(self):
		self.expandSelf()
		
		mots=self.listeMots()
		
		return mots

	



class Mot :
	def __init__(self, content, pos="", locutor="_all"):
		
		self.content=content
		self.prononciation=''
		self.pos=pos
		self.locutor=locutor
	
	
	
	#Checking final s 
	def sFinal(self, letrap):
	
		monmot=self.content
		mapron=self.prononciation
		
		#choosing if final s is said "s" or "z" ----> to complete (delete if it doesn't apply to your language)
		voyelles='a|??|??|??|e|??|??|??|i|??|??|??|o|??|??|??|u|??|??|??|??|w|??|??|y'

		if re.search('s$', monmot) and re.search('('+voyelles+')s$', mapron) and re.search(')^('+voyelles+')$', letrap):
			mapron=re.sub('s$', 'z', mapron)
			self.prononciation=mapron
		
	
	
	#Lowercase
	def minuscules(self):
		texte=self.content
		texte=motmin(texte)
		self.content = texte

	
		
	#Phonetize
	def phonetize(self, letrap):
	
		macat=self.pos
		
		
		monmot=self.content
		monmot=monmot.replace("'","")
		monmot=monmot.replace("???","")
		
		
		locutor=self.locutor
	
		monmot=monmot.replace('temps', 'tems')
		monmot=monmot.replace('??', 'e')
		monmot=monmot.replace('??', 'e')
		monmot=monmot.replace('??', 'e')
		monmot=monmot.replace('??', 'e')
		monmot=monmot.replace('??', '??')
		monmot=monmot.replace('??', '??')
		monmot=monmot.replace('???', '??')
		
		
		voyelles='a|??|??|??|e|??|??|??|i|??|??|??|o|??|??|??|u|??|??|??|??|w|??|??|y'
		voydoux='e|??|??|??|i|??|??|??|??'
		consonnes='b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|x|z|??|??|??|??|??|??|??|??|??|??'
		
		#You have to put here all rules to phonetize your language ----> to complete
		
		
		
		
	
		self.prononciation = monmot
	
	
	#Syllabize ----> to complete (check if the following syllabization rules all apply to your language)
	def syllabize(self):
	
		monmot=self.prononciation
		
		
		voyelles='a|??|??|??|e|??|??|??|i|??|??|??|o|??|??|??|u|??|??|??|??|w|j|??|??|y'
		consonnes='b|c|d|f|g|h|k|l|m|n|p|q|r|s|t|v|x|z|??|??|??|??|??|??|???|??|??|??|??'
		
		#------------------ Treating double vocals ----------------------*/

		# Double vocals which split syllables */
		monmot=re.sub('(a|??|??|??|e|??|??|??|??|i|??|o|??|??|??|??|u|??|??|??|y)(a|??|??|??|e|??|??|??|??|i|??|o|??|??|??|??|u|??|??|??|y)', '\g<1>??\g<2>', monmot)
		monmot=monmot.replace('uu', 'u??u')
		monmot=monmot.replace('ua', 'u??a')
		monmot=monmot.replace('u??', 'u????')
		monmot=monmot.replace('u??', 'u????')
		monmot=monmot.replace('ii', 'i??i')
		
		monmot=re.sub('(['+voyelles+'])j??(['+voyelles+'])', '\g<1>j????\g<2>', monmot)
		
		
		monmot=re.sub('(a|??|??|??|e|??|??|??|??|i|??|o|??|??|??|??|u|??|??|??|y)([jw])(j?)(a|??|??|??|e|??|??|??|??|i|??|o|??|??|??|??|??|u|??|??|??|y)', '\g<1>??\g<2>\g<3>\g<4>', monmot)
		


		#--------------------------- Other syllables -------------------------------
		
		for i in range(0,10):

			

			# --- A consonant between two vocals introduces a new syllable --- 

			#(C)(C)(C)V(V)(V)CV*/
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+'])(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>??\g<8>\g<9>';
			
			monmot=re.sub(motif,replacement,monmot)

			# --- If there are two consonants between two vocals, the first belongs to the previous syllable, the second to the following syllable. However, bl, cl, fl, gl, pl, br, cr, dr, fr, gr, pr, tr, vr, groups can't be separated (and in occitan dj tg) --- 

			#(C)(C)(C)V(V)(V)CCV
	
			#bl, cl, fl, gl, pl
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)([b|c|f|g|p|k])l(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>??\g<8>l\g<9>';
			monmot=re.sub(motif,replacement,monmot)
	
			#br, cr, dr, fr, gr, pr, tr, vr
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)([b|c|d|f|g|p|t|v|k])(r|??)(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>??\g<8>\g<9>\g<10>';
			monmot=re.sub(motif,replacement,monmot)
	
			#sbr, scr, sdr, sfr, sgr, spr, str, svr
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+']?)s([b|c|d|f|g|p|t|v|k])(r|??)(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>\g<8>??s\g<9>\g<10>\g<11>';
			monmot=re.sub(motif,replacement,monmot)

			#dj, tg
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)([d|t])([??|??])(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>??\g<8>\g<9>\g<10>';
			monmot=re.sub(motif,replacement,monmot)

			# Autres consonnes 
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+'])(['+consonnes+'])(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>\g<8>??\g<9>\g<10>';
			monmot=re.sub(motif,replacement,monmot)

			# --- When there are three following consonants in a word, usually the two firsts ends a syllable, the third begin a new syllable. But the groups bl, cl, fl, etc. (mentioned upper) usually begin a syllable

			#(C)(C)(C)V(V)(V)CCCV*/
	
			#bl, cl, fl, gl, pl*/
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+'])([b|c|f|g|p|k])l(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>\g<8>??\g<9>l\g<10>';
			monmot=re.sub(motif,replacement,monmot)

			#br, cr, dr, fr, gr, pr, tr, vr*/
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+'])([b|c|d|f|g|p|t|v|k])(r|??)(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>\g<8>??\g<9>\g<10>\g<11>';
			monmot=re.sub(motif,replacement,monmot)

			#dj, tg*/
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+'])([d|t])([??|??])(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>\g<8>??\g<9>\g<10>\g<11>';
			monmot=re.sub(motif,replacement,monmot)

			# Others consonants */
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+'])(['+consonnes+'])(['+consonnes+'])(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>\g<8>\g<9>??\g<10>\g<11>';
			monmot=re.sub(motif,replacement,monmot)
			
			
			
			#4 consonants*/
			motif='([??]|^)(['+consonnes+']?)(['+consonnes+']?)(['+consonnes+']?)(['+voyelles+'])(['+voyelles+']?)(['+voyelles+']?)(['+consonnes+'])(['+consonnes+'])(['+consonnes+'])(['+consonnes+'])(['+voyelles+'])'
			replacement='\g<1>\g<2>\g<3>\g<4>\g<5>\g<6>\g<7>\g<8>\g<9>??\g<10>\g<11>\g<12>';
			monmot=re.sub(motif,replacement,monmot)

		
		
		
	
		self.prononciation = monmot
	
	
	#Accentuating ----> to complete (check if the following syllabization rules all apply to your language)
	def accent(self):
	
		monmot=self.prononciation
		if not re.search('??',monmot):
			# If the word has only one syllable, accentuate it
			monmot='??%'+monmot+''
		else:


			# By default, accentuate the last syllable
			ac='d'


			# Accentuate the penultimate if the words is ended by a non accented vocal
			if re.search('([aeiou??])$', monmot):
				ac='ad'
			
			# Accentuate the penultimate if the words is ended by a non accented vocal followed by s or ?? */
			if re.search('([aeiou??])([???s??])$', monmot):
				ac='ad'
			

			# Accentuate elsewhere if there is an accent
			motif='([??]|^)([^??]*?)([????????????????????])([^??]*?)([??]|$)'
			if re.search(motif,monmot):
				ac='autres'
			
	
			# Place the tonic accent at the right place
			longmot=len(monmot)
			longmot=longmot-2;
			deb=monmot[0:longmot]
			fin=monmot[longmot:2]
	
			# Last syllable
			if ac=='d':
				monmot=re.sub('??([^??]*?)$', '??%\g<1>', monmot)
	
			# Penultimate syllable
			elif ac=='ad':
				monmot=re.sub('([??]|^)([^??]*?)??([^??]*?)$', '\g<1>%\g<2>??\g<3>', monmot)
	
			# Words with an accent
			else:
				monmot=re.sub('([??]|^)([^??]*?)([????????????????????])([^??]*?)([??]|$)', '\g<1>%\g<2>\g<3>\g<4>\g<5>', monmot)
	
			
			#If there are two accents in the two last syllables
			monmot=re.sub('??%([^??]*?)??%([^??]*?)$', '??%\g<1>??\g<2>', monmot)
	
	
		
		monmot=re.sub('^??%([^\??]*?)$',"??'\g<1>",monmot)
		
		
		
	
		self.prononciation = monmot
	
	
	#Correcting the pronunciation according to the accentuation ----> to complete (check if the following syllabization rules all apply to your language)
	def correct(self):
	
		voyelles='a|??|??|??|e|??|??|??|i|??|??|??|o|??|??|??|u|??|??|??|??|??|??|y'
	
		monmot=self.prononciation
		
		
		
		
		monmot=re.sub("^(???)('?)([^??]*?)??([^??]*?)$",'\g<1>\g<2>\g<3>a\g<4>',monmot)
		
		
		
		monmot=re.sub('??', 's', monmot)
		monmot=re.sub('??', '??', monmot)
		monmot=re.sub('??', '??', monmot)
		monmot=re.sub('??', 'a', monmot)
		monmot=re.sub('??', 'e', monmot)
		monmot=re.sub('???', 'z', monmot)
		monmot=re.sub('[????]', 'i', monmot)
		monmot=re.sub('[??o]', 'u', monmot)
		monmot=re.sub('[????]', 'y', monmot)
		monmot=monmot.replace('??', 'a')
		monmot=monmot.replace('??', 'e')
		monmot=monmot.replace('??', 'i')
		monmot=monmot.replace('??', 'u')
		monmot=monmot.replace('??', 'y')
		
		
		#Replacing the signs with these for human reading
		monmot=re.sub('??', '/', monmot)
		monmot=re.sub('%',"'",monmot)
		
	
		self.prononciation = monmot
	
	
	#Doing all the processings
	def tract(self, letrap):
		self.minuscules()
		self.sFinal(letrap)
		self.phonetize(letrap)
		self.syllabize()
		self.accent()
		self.correct()



def assemble(mots):
	voyelles='a|??|??|??|e|??|??|??|i|??|??|??|o|??|??|??|u|??|??|??|??|??|??|y'
	consonnes='b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|x|z|??|??|??|??|??|??|??|??|??'
	for i in range(0,len(mots)):
		mot=mots[i]
		mot=mot.strip(' ')
		
		if i<len(mots)-1:
			motsuiv=mots[i+1];
		else:
			motsuiv=''
		
		
		if i>0:
			motprec=mots[i-1]
		else:
			motprec=''
		
		
		#Liaison rules ----> to complete (check if the following syllabization rules all apply to your language)
		
		
		#Doing the liaison if necessary with ??
		if re.search("(.+)/([^/']*?)[????]$", mot) and re.search("^(/?)('?)("+voyelles+")", motsuiv):
			dernsyl=re.sub("^(.+)/([^/']*?)[????]$", "\g<2>", mot)
			motsuiv=re.sub("^(/?)('?)("+voyelles+")", "\g<1>\g<2>"+dernsyl+"\g<3>", motsuiv)
			mots[i+1]=motsuiv
			mot=re.sub("^(.+)/([^/']*?)[????]$", "\g<1>", mot)
		
		#Processing a potential final S
		if re.search('([^ptk])s$', mot) and re.search('^('+voyelles+')', motsuiv) and mot!="/'s":
			mot=re.sub('s$', 'z', mot)
		
		
		
		#If the word ends with a consonant and the other begins with a vocal, do liaison
		if re.search("("+consonnes+")$", mot) and re.search("^(/?)('?)("+voyelles+")", motsuiv):
			dernsyl=re.sub("^(.+)("+consonnes+")$", "\g<2>", mot)
			motsuiv=re.sub("^(/?)('?)("+voyelles+")", "\g<1>\g<2>"+dernsyl+"\g<3>", motsuiv)
			mots[i+1]=motsuiv
			mot=re.sub("^(.+)("+consonnes+")$", "\g<1>", mot)
		
		
		
		
		#If the word is a consonant and the previous one ends with a vocal, we glue them
		if re.search("^(/?)('?)("+consonnes+")$", mot) and re.search("("+voyelles+")$", motprec):
			dernsyl=re.sub("^(/?)('?)("+consonnes+")$", "\g<3>", mot)
			motprec=motprec+dernsyl
			mots[i-1]=motprec
			mot=''
		
		
		#Adding whitespaces before and after punctuations
		if re.search("^([\W])$", mot):
			mot=re.sub("^([\W])$", " \g<1> ", mot)
		else:
			mot=re.sub("^([^/])", "/\g<1>", mot)
		
		
		
		if re.search("^([/]?)([']?)$", mot):
			mot=''
		
		
		mots[i]=mot
		
		texte=''.join(mots)
	
	texte=re.sub('/{2,}', '/', texte)
	
	return texte


#Correcting pronunciation according to the accentuation for exceptions ----> to complete (check if the following syllabization rules all apply to your language)
def correctException(monmot, letrap):

	voyelles='a|??|??|??|e|??|??|??|i|??|??|??|o|??|??|??|u|??|??|??|??|??|??|y'

	if re.search('^('+voyelles+')$', letrap):
		monmot=re.sub('???', 'z', monmot)
	else:
		monmot=re.sub('???', 's', monmot)
	
	monmot=re.sub('??', 's', monmot)
	monmot=re.sub('??', '??', monmot)
	monmot=re.sub('??', '??', monmot)
	monmot=re.sub('??', 'a', monmot)
	monmot=re.sub('??', 'e', monmot)
	monmot=re.sub('[????]', 'i', monmot)
	monmot=re.sub('[??]', 'u', monmot)
	monmot=re.sub('[????]', 'y', monmot)
	monmot=monmot.replace('??', 'a')
	monmot=monmot.replace('??', 'e')
	monmot=monmot.replace('??', 'i')
	monmot=monmot.replace('??', 'u')
	monmot=monmot.replace('??', 'y')

	return monmot

	
	

def expandTxt(chaine):
	txt=Texte(chaine)
	
	txt.expandSelf()
	
	return txt.content
		


def phonTxt(chaine, locutor="_all", exceptions=True, link=False, repex="exceptions"):
	if exceptions==True:
		with open('exceptions', 'rb') as fichier:
			mon_depickler = pickle.Unpickler(fichier)
			exceptions = mon_depickler.load()
	
	#Initialize text
	txt=Texte(chaine)
	#Treating text
	mots=txt.tractSelf()
	#Treating word by word
	aas=[]
	for i in range(0,len(mots)):
		#getting the first letter of the following word
		if i<len(mots)-1:
			motap=mots[i+1]
			letrap=motap[0]
		else:
			letrap=""
		m=mots[i]
		
		#If the word is a punctuation, write it
		if re.search('^([^a-z????????????????????????????????????????????????A-Z????????????????????????????????????????????????]+)$', m):
			aas.append(m)
		
		#Else, if the word is in the exceptions, getting its pronunciation
		elif m in exceptions and (locutor in exceptions[m] or "_all" in exceptions[m]):
			prons=exceptions[m]
			if locutor in prons:
				pronmot=prons[locutor]
			elif "_all" in prons:
				pronmot=prons["_all"]
			
			#Correcting according to the following word
			pronmot=correctException(pronmot, letrap)
			aas.append(pronmot)

		#Else, if there is an apostrophe
		elif "'" in m:
			#Splitting by word
			mm=m.split("'")
			#Initializing pronunciations list
			pp=[]
			#For every word
			for i in range(0,len(mm)):
				m=mm[i]
				if i<len(mm)-1:
					letrapap=mm[i+1][0]
				else:
					letrapap=letrap

				m=motmin(m)
				#If it's in the exceptions lists, getting its pronunciations
				if m in exceptions and (locutor in exceptions[m] or "_all" in exceptions[m]):
					prons=exceptions[m]
					if locutor in prons:
						p=prons[locutor]
					elif "_all" in prons:
						p=prons["_all"]
					#Correcting according to the following word
					p=correctException(p, letrapap)
				#Else, phonetize
				else:
					#Initiate the word
					mot=Mot(m, locutor=locutor)
					#Treating the word
					mot.tract(letrapap)
					#Adding to the list
					p=mot.prononciation
				#Adding pronunciation to the list
				pp.append(p)
			#Merging pronunciations
			pron=assemble(pp)
			aas.append(pron)
					
					
				
		
		#Else, if the uppercase word is in the exceptions, getting its pronunciations
		elif motmin(m) in exceptions and (locutor in exceptions[motmin(m)] or "_all" in exceptions[motmin(m)]):
			prons=exceptions[motmin(m)]
			if locutor in prons:
				pronmot=prons[locutor]
			elif "_all" in prons:
				pronmot=prons["_all"]
			#Correcting according to the following word
			pronmot=correctException(pronmot, letrap)
			aas.append(pronmot)
				
		#Else, phonetize
		else:
			#Initiate the word
			mot=Mot(m, locutor=locutor)
			#Treating the word
			mot.tract(letrap)
			#Adding to the list
			aas.append(mot.prononciation)
	
	#Merging words
	if link==True:
		txtfinal=assemble(aas)
	else:
		txtfinal=" ".join(aas)
		
	return txtfinal






