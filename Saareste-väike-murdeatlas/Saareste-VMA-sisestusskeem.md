*v. 29-2-16*

Lisatud Exceli failis (*Atlase-geoinfo-29-2-16*) on viis töölehte:

- VMA. Sisaldab Saareste VMA kogumispunktide loetelu.  
- Eesti kihelkonnad. Sisaldab Eesti kihelkondade lühendeid ja nimesid. 
- Asustusyksused. Sisaldab Maa-ameti asustusüksuste kaardi atribuuttabelit. 
- Ühendatud tabel. Sisaldab VMA, Eesti kihelkondade ja Maa-ameti andmete ühendatud atribuuttabelit, mis koosneb järgnevatest veergudest:

	- ANIMI: Asustusüksuse nimi
	- AKOOD: Asustusüksuse kood Eesti haldus- ja asustusjaotuse klassifikaatori (EHAK) järgi
	- TYYP	Asustusüksuse tüüp EHAK-i asula tüüpide tunnuste järgi
	- ONIMI: Omavalitsuse nimi
	- OKOOD: Omavalitsuse kood EHAK-i järgi
	- MNIMI: Maakonna nimi
	- MKOOD: Maakonna kood EHAK-i järgi
	- SaKhkLyh: Saareste VMA kihelkonna lühend
	- SaKhk: Saareste VMA kihelkonna nimi
	- SaKylaNr: Saareste VMA kogumispunkti number vastavas kihelkonnas
	- SaKyla: Saareste VMA küla nimi kogumispunktis vaadeldavas kihelkonnas
	- SaKJEes: Saareste VMA keelejuhi eesnimi, kui see on olemas. Kui on mitu, eraldada semikooloniga.
	- SaKJPrk: Saareste VMA keelejuhi perekonnanimi, kui see on olemas. Kui on mitu, eraldada semikooloniga.
	- SaKJSynd: Saareste VMA keelejuhi sünniaasta, kui see on olemas. Kui on mitu, eraldada semikooloniga.
	- Keelend: Keelend murdekaardilt. Kui ühe punkti alla saab märkida mitu keelendit, eraldada semikooloniga. 
	- SaKommentaar: Saareste muu tekstiline kommentaar, mida pole võimalik olemasolevatesse lahtritesse lisada 
	- KhkLyh: Kihelkondade lühendid
	- KhkNimi: Kihelkondade nimed 

- Dok: info täidetavate lahtrite kohta. 


Iga küla kohta on tehtud tabelis eraldi rida. Keelejuhtide ees- ja perenimede jaoks eraldi veerud, mitme korral on need eraldatud samas lahtris semikooloniga. Samamoodi on tehtud sünniaastatega. Kui VMA-s nimetatud küla/asulat enam ei ole, on nende asemel märgitud praegune lähiküla (koos vastavate EHAK-i tunnustega). Kui osadel VMA kogumispunktidel puuduvad EHAK-i andmed, siis neid külasid/asulaid samuti tänapäeval enam pole. Nendele küladele ei leitud andmebaasidest lähikülasid, ent need on siiski punktidena aluskaardil (kogumispuntkid_utf8_97.shp) olemas ning sestap ka VMA atribuuttabelis esindatud. 


Algallikate info

Kihelkondade kaardi info on pärit kihelkondade Shapefile'i atribuuttabelist. Kuna Shapefile'is ID-d puuduvad, siis seda veergu praegu seal pole.
Maa-ameti asustusüksuste kaart, mis VMA andmetega ühendatati, on seisuga 01.04.2015.
