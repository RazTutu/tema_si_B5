# tema_si_B5
Nume: Țuțuianu Răzvan Constantin
Grupa: B5

Documentatie:
Limbajul de programare ales a fost Python.
Pentru a putea rula programul, este necesar sa aveti instalat python 3+ si biblioteca pycryptodome pe calculator.

Am pus un video pe youtube in care explic in mare ce am facut + fac un demo, in caz de nu doriti sa cititi textul acesta :)
Link: https://www.youtube.com/watch?v=7Zir5D_bFzs&feature=youtu.be

Pentru a instala pycrytodome:
	python -m pip install pycryptodome

De asemenea, proiectul trebuie rulat din Visual Studio Code + terminal. Cel putin mie nu imi merge si pe compilatorul PyCharm.

Intrati in folderul unde sunt cele 3 fisiere server.py, nodA.py, nodB.py.
Deschideti 3 terminale prin comanda CMD scrisa in search in windows, sau pe terminal normal in caz de e linux.
si scrieti pe rand, in fiecare terminal, cate o comanda(primul terminal are python server.py, al doilea terminal are python nodA.py etc):
python server.py
python nodA.py
python nodB.py


In nodA.py si nodB.py o sa va intrebe daca doriti criptare ECB sau OFB. Daca ambele noduri dau acelasi raspuns, key managerul(serverul) va incepe 
cripatrea in modul ales. Daca raspunsurile difera, alege el random un mod.
Mai departe se vor putea vedea pe terminalele de la nodA.py si nodB.py niste outputuri cu ce s-a trimis la server, ce s-a decriptat in nodB.py etc.

Chestii mai importante:

In legatura cu vectorul de initializare, si in cazul ECB si in cazul OFB, Key Managerul(serverul) va transmite o variabila
initialization_vector. Daca clientii au ales ECB, aceasta variabila va fi goala si nu va fi folosita la criptarea ECB. Daca clientii au ales
OFB, aceasta va fi una normala, de 16 bytes, si va fi folosita in criptarea OFB impreuna cu K2.

Cat despre OFB, nu am gasit o librarie anume pentru a cripta si sa pot scoate vectorii de initializare inainte de a face
xor, asa ca mi-am facut propria functie OFB. Ideea este ca voi cripta cheia K2 si vectorul de initializare pentru
a obtine "block cipher encryption" folosind un ECB simplu. Rezultatul, adica "block cipher encryption",
va fi folosit ca vector de initializare la urmatorul bloc si tot asa mai departe. Astfel pot sa il folosesc pentru
a face xor cu plaintextul si a obtine un criptotext. Totul functioneaza bine perfect :)
