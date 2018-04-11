# Lifesaver

NOTE:pentru a rula aplicatia trebuie rulat scriptul python index.py si de asemenea conexiunea la o baza de date Mysql 
Eu am folosit anaconda pentru instalarea librariilor



Lifesaver este un site menit sa ii ajute pe cei care au probleme cardiace.

Cum ii va ajuta?


Oamenii care au probleme vor purta bratari care le va lua pulsul si pozitia ,in momentul in care se observa o "anomalie" in valorile pulsului bolnavului .(sau acesta simte ca este ceva in neregula si apeleaza serviciile de pe aplicatie) Aplicatia client-side va trimite latitudinea si loncitudinea catre serverul Apache unde vor fi stocate intr.o baza de date  Mysql si va fi trimis un mesaj atat celor care au numarul acestuia de telefon (la prieteni ,familie )cat si celor din jurul sau pe distanta de 1 km care au aplicatia si sunt simpli utilizatori.(dar si la 112).

Cei care dispun de aplicatie:
- le va arata directia catre bolnav (asta daca sunt de acord sa ajute) folosind Google Maps Directions API
-vor trimite medicamentele de care acesta ar avea nevoie.(poate printe utilizatori sunt oameni care ar avea ceea ce i.ar trebui lui in materie de medicamente)

Aplicatia client-side dispune de un bot care va incepe automat sa.i dea indicatii bolnavului din momentul trimiterii semnalului  si care ii poate raspunde la diferite intrebari cum ar fi : timpul estimativ in care va sosi ambulanta sau cati oameni au fost de acord sa.l ajute .

De asemenea aplicatia poate sa functioneze fara internet folosindu-se de semnalul telefonului mobil.
  
Site.ul pe langa acest ajutor care il acorda bolnavilor dispune de mai multe facilitati.
Cum ar fi:
-cei care au cont pot sa citeasca diferite postari legate despre biologie,medicina

- pot scrie diferite postari cu informatii care vor fi votate de alti utilizatori si in cazul in care acestea nu aduc un content folositor cititorilor vor fi banate
-pot scrie carti pe site pe diferite teme care de asemenea si acestea la randul lor vor fi votate.
-pot da upload sau embed la diferite modele 3d  care acestea pot fi vizualizate in AR.
si multe alte facilitati






Proiectul inca nu este terminat decat in proportie de 80% deci vor mai fi adaugate diferite facilitati sau sterse cele existente .De asemenea vor fi rezolvate elementele de securitate a site.ului.

Pt Server-side am folosit python.
Jos voi enumera cateva librarii pe care le.am folosit
-flask 
-pentru conectarea la baza de am folosit pymysql
-flask-socketio pentru elemente de real time
-scikit-learn 
-gtts
-pygal
-flask-googlemaps

Pt client-side:
-html
-css 
-boostrap
-javascript
-jquery


 
 
