# Murdekorpuse vigade parandamine (uued XML-id)
*Versioon 08-03-16*
  
On olemas Pythoni skriptid erinevate sagedusloendite tegemiseks. Olemas on ka eraldi veaotsingu skript, mis võimaldab mitmeid vigu listina korraga otsida. Väljastatakse fail, kus on semikooloniga eraldatud otsitav viga ja faili nimi. Selle põhjal saab tagasi minna vastavatesse failidesse ja seal vead käsitsi parandada.  
Samuti on tehtud skriptid vigade automaatseks parandamiseks, seda eeskätt sõnaliikide ja lemmade paranduste jaoks. Skripti sisendiks on *csv*-fail, milles on lemma, sõnaliigi ja paranduse väljad. Skripti väljundiks on sama fail uue laiendiga, mille saab omakorda tõsta automaatselt uude kausta, kus laiendi saab muuta uuesti *xml*-iks.  

Skriptid: *CedFrequencyLists.py*, *CedErrorSearch.py*, *CedCorrectMistakes.py*  


## I Vigased grammatilised märgendid  

Murdekorpuse failides on hulk vigaseid märgendeid, mis on reeglina lihtsalt näpuvead või tekkinud ühest formaadist teise teisendamise käigus. Märgendite sagedusloendite põhjal on kontrollitud kõik sellised kategooriad ja kategooriate kombinatsioonid, mis esinevad ainult mõne korra; parandatud on ka süsteemsemaid vigu ja ühtlustatud ebajärjepidevust. 
Paranduste failis on eraldi tulpa märgitud vigased kategooriad, samuti on parandusi kommenteeritud. Parandatud on enamasti morfoloogilist infot, ent samuti mõnel juhul sõnaliiki ja lemmat. Kõige viimases tulbas on semikooloniga eraldatud failid, milles viga esineb. Vigade leidmiseks failidest kasutati skripti *CedErrorSearch.py*. Enamik grammatiliste kategooriate vigu tuleb failides parandada käsitsi; üleliigseid punkte, tühikuid jms saab parandada automaatselt.  

Failid: *I_grammkatideSagedused.csv*, *I_grammkatideParandamine.xlsx*  

## II Vahemärgid  

Vahemärkide sagedusloendi põhjal on ära märgitud vigased vahemärgid. Põhiliselt on seal lindi pealt halvasti välja kuuldud sõned, mis on märgitud sulgude sisse, ent mis peaksid olema sulgudest eraldatud eraldi sõnedena. Eraldi tulpades on parandamist vajavate failide loendid, paranduste liigid ja kommentaarid. Vigaste failide leidmiseks kasutati jällegi skripti *CedErrorSearch.py*.  

Failid: *II_vahemarkideSagedused.csv*, *II_vahemarkideParandamine.xlsx*  

## III Sõnaliigi märgendita üksused (liik = "")  

Failis *III_puuduvad-sonaliigid.csv* on sõnaliigita üksuste loend ja failinimed. Paranduste failis on lisaks puuduva sõnaliigiga üksus (enamasti poolikud sõnad), vead, parandused ja kommentaarid. Vead parandatakse käsitsi.  

Failid: *III_puuduvad-sonaliigid.csv*, *III_puuduvad-sonaliigidParandamine.xlsx*  

## IV Keelejuhtide ja küsitlejate koodid  

Fail *IV_konelejateSagedused.csv* sisaldab keelejuhtide ja küsitlejate koode ja nende esinemise sagedusi. Failis on suuresti küsitlejate voorud, mis ei ole küll morfoloogiliselt märgendatud, ent on saanud sellegipoolest kõneleja info. Tühi kõneleja info (KJ="") on tekkinud vahemärkuste märgendamisel. Paranduste failis on lisaks märgitud veakohad, parandused, vigadega failid ja kommentaarid.

Failid: *IV_konelejateSagedused.csv*, *IV_konelejateParandamine.xlsx*

## V Kommentaarid  

Fail *kommentaarideSagedused.csv* sisaldab kommentaariks märgitud fraase ja nende sagedusi. Paranduste failis on lisaks märgitud vead, parandused, vigadega failid ja kommentaarid. Kommentaar "import:viga" on failide teisendamisel tekkinud kategooria nende sõnade kohta, mida ei ole osatud märgendada. Hilisemaks failide täiendamiseks tuleb see teisendada kommentaariks "märgendamata". Ära tuleb kustutada tühjad kommentaarid. Ülejäänud kommentaaridega on põhiliselt märgitud fraase (nt ühend- ja väljendverbid).

Failid: *V_kommentaarideSagedused.csv*, *V_kommentaarideParandamine.xlsx*

## VI Metamärkide korrastamine  

Fail *metamarkideSagedused.csv* sisaldab metamärkide märgendeid ja nende sagedusi korpuses. Paranduste failis on lisaks märgitud veakohad, parandused, vigadega failid ja kommentaarid.  

Failid: *VI_metamarkideSagedused.csv*, *VI_metamarkideParandamine.xlsx*

## VII Päised  

Murdekorpuse failide päised on korrastatud (sh lisatud nt külade koordinaadid, keelejuhtide vanused ja sood, kui selline info oli kättesaadav, jm).

## VIII Külade, kihelkondade ja failide nimede ühtlustamine  

Ühtlustatud on külade, kihelkondade ja failide nimed.

## IX Lemmade parandamine  

Kontrollitud on, et lemma oleks õiges vormis (*ma*-infinitiiv, ainsuse nimetav jne). Lemma võib olla ka kirjaveaga või vale sõnaliigiga (näiteks on verb märgitud substantiiviks vmt). Kõik vigased kohad on üksikute sõnaliikide failide veatulbas märkitud "v"-tähega. Kontrollitud on senini pärisnimed, afiksaaladverbid, küsisõnad, sidesõnad, järgarvud, põhiarvud, pronumeraalid, nimisõnad ja verbid.  
Lisaks üksikute failide läbikäimisele on loodud koondfail *vigased-lemmad-kokkuvote.xlsx*, mis koondab kõikide kontrollitud sõnaliikide vigaseid lemmasid, vea liike, parandusi ja kommentaare. Koondfaili põhjal tehtud *csv*-failid (sama infoga, mis koondfaili eraldi töölehtedel) on sisendiks automaatsele vigade parandamisele skriptiga *CedCorrectMistakes.py*.  
Vigadest, mida automaatselt parandada ei saa, on loodud list, mille põhjal otsitakse välja need failid, mida on vaja parandada käsitsi.  

Failid: *Adva.xlsx*, *H.xlsx*, *Intr.xlsx*, *Konj.xlsx*, *Numj.xlsx*, *Nump.xlsx*, *ProNum.xlsx*, *S.xlsx*, *V.xlsx*, *vigased-lemmad-kokkuvote.xlsx*  
