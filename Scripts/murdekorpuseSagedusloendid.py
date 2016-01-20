import os
import re
from operator import itemgetter
from collections import Counter
import xml.etree.ElementTree as etree

'''
Function that creates list of input files within a working directory.
'''

def sisend():
    kataloogid = os.listdir()
    sisendfailid = []
    for kat in kataloogid:
        if os.path.isdir(kat):
            os.chdir(kat)
            failid = os.listdir()
            for fail in failid:
                    if fail.endswith(".xml"):
                        if os.path.isfile(fail):
                            sisendfailid.append(os.path.join(kat, fail))
            os.chdir('..')
    return sisendfailid

'''
vahemärkide list
'''

def vahemarkideList (sisendfailideList):
    vahemargid = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            vahemark = root.findall("./sisu/lause/sone[@meta='vahemärk']")
            for i in vahemark:
                vahemargid.append(i.text)
    return vahemargid

'''
informantide koodide list
'''

def konelejateList (sisendfailideList):
    konelejad = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            kj = root.findall("./sisu/lause[@koneleja]")
            for i in kj:
                konelejad.append(i.attrib['koneleja'])
    return konelejad

'''
metamärgendite list
'''

def metaMargendid (sisendfailideList):
    metad = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            metamark = root.findall("./sisu/lause/sone[@meta]")
            for i in metamark:
                metad.append(i.attrib['meta'])
    return metad

'''
grammatiliste kategooriate list
'''

def grammKat (sisendfailideList):
    grammatilised = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            gramm = root.findall("./sisu/lause/sone[@vorm]")
            for i in gramm:
                grammatilised.append(i.attrib['vorm'])
    return grammatilised

'''
sõnaliikide list
'''

def sonaLiik (sisendfailideList):
    sonaliigid = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            sonaliik = root.findall("./sisu/lause/sone[@liik]")
            for i in sonaliik:
                sonaliigid.append(i.attrib['liik'])
    return sonaliigid

'''
kommentaaride list
'''

def kommentaar (sisendfailideList):
    kommentaarid = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            komm = root.findall("./sisu/lause/sone[@kommentaar]")
            for i in komm:
                kommentaarid.append(i.attrib['kommentaar'])
    return kommentaarid

'''
funktsioon, mis koostab etteantud listist sagedusloendi
väljundfaili nimi defineerida sõnena
'''

def sagedusloendiFail (sisendList, valjundfail):
    sagedused = dict(Counter(sisendList))
    sorteeritudSagedused = sorted(sagedused.items(), key=itemgetter(1), reverse=True)
    valjund = open(valjundfail, "w", encoding="utf-8")
    for i in sorteeritudSagedused:
        valjund.write(i[0] + ";" + str(i[1]) + "\n")
    valjund.close()

'''
funktsioon, mis tagastab sagedusloendi etteantud sõnaliigi märgindiga lemmadest
(nt verbide sagedusloend, adjektiivide sagedusloend jne)
POS ette anda sõnena
'''

def lemmaSagedus (sisendfailideList, pos):
    lemmad = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            lemma = root.findall('./sisu/lause/sone[@liik]')
            for i in lemma:
                atribuudid = i.attrib
                if atribuudid['liik'] == pos:
                    lemmad.append(atribuudid.get('lemma', 'lemma puudub'))
    return lemmad

'''
Kogu võimalik päise info.
Väljund stringina, info eraldatud semikooloniga.
Puuduvad atribuudi väärtused on asendatud NA-ga.
Funtksioon tagastab päiseinfo stringina, kus eri infot eraldab ;
'''

def paiseInfo (sisendfailiNimi):
    with open (sisendfailiNimi, "r", encoding="utf-8") as sisend:
        failinimi = re.sub(r".*\\", "", sisendfailiNimi)
        tree = etree.parse(sisend)
        root = tree.getroot()
        khk = root.find("./info/kihelkond").text
        murre = root.find("./info/murre").text
        kyla = root.find("./info/kyla").text
        long = root.find("./info/kyla[@longituud]").attrib['longituud']
        lat = root.find("./info/kyla[@latituud]").attrib['latituud']
        kjlist = root.findall("./info/keelejuht")

        paiseKJ = []

        for s in range(len(kjlist)):
            yksiklist = []
            yksiklist.append(kjlist[s].attrib['id'])
            yksiklist.append(kjlist[s].attrib['vanus'])
            yksiklist.append(kjlist[s].attrib['synniaasta'])
            paiseKJ.append(yksiklist)
        
        for j, k in enumerate(paiseKJ):
            for l, m in enumerate(k):
                if m == '':
                    paiseKJ[j][l] = 'NA'

        paiseInfoStringina = failinimi + ";" + khk + ";" + murre + ";" + kyla + ";" + long + ";" + lat
        
#        paiseInfoListina = [paiseInfoStringina] + paiseKJ
#        print(paiseInfoStringina, paiseKJ)
        
    return paiseInfoStringina, paiseKJ


def sonaliigiLoend (sisendfailideList, valjundfail):
    sonaliigidFailiInfoga = []
    for fail in sisendfailideList:
        pais = paiseInfo(fail)
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()

            konevoorud = root.findall("./sisu/lause/[@koneleja]")

            for kv in konevoorud:
                if 'KJ' in kv.attrib['koneleja']:
                    for sone in kv:
                        if ('liik' in sone.attrib.keys() and 'lemma' in sone.attrib.keys()) and sone.attrib['liik'] != '' and sone.attrib['lemma'] != '':
                            sonaliik = sone.attrib['liik']
                            lemmasona = sone.attrib['lemma']
                            keelejuht = kv.attrib['koneleja']

                            for kj in range(len(pais[1])):
                                if keelejuht == pais[1][kj][0]:
                                    yheKJinfo = pais[1][kj]
                            
                            koguInfoStringina = sonaliik + ";" + lemmasona + ";" + keelejuht + ";" + pais[0] + ";" + ";".join(yheKJinfo)
                            sonaliigidFailiInfoga.append(koguInfoStringina)

    with open (valjundfail, "w", encoding="utf-8") as valjund:
        for i in sonaliigidFailiInfoga:
            valjund.write(i + "\n")

                            
#sonaliigiLoend(sisend(), "testinFunktsiooni.csv")

with open ("testest.csv", "w") as valjund:
    for i in sisend():
        for j in range(len(paiseInfo(i)[1])):
            valjundString = paiseInfo(i)[0] + ";" + ";".join((paiseInfo(i)[1][j]))
            valjund.write(valjundString + "\n")


#        keelejuhid = sum(paiseInfo(i)[1], [])
#        kjString = ";".join(keelejuhid)
#        valjundString = paiseInfo(i)[0] + ";" + kjString
#        valjund.write(valjundString + "\n")


'''
NÄITEID

Kõigepealt tuleb koostada sisendfailide list kas eraldi või teise funktsiooni sees.
Praegu töötab sisendfailide sisselugemise funktsioon nii, et skript tuleb käivitada kaustas,
kus on sisendi jaoks vajalikud alamkaustad.

Nii koostatakse verbide sagedusloend:

sagedusloendiFail(lemmaSagedus(sisend(), "V"), "Verbide-sagedusloend.csv")

grammatiliste kategooriate sagedusloend:

sagedusloendiFail(grammKat(sisend()), "Grammatiliste-kategooriate-sagdusloend.csv")

sõnaliikide sagedusloend
sagedusloendiFail(sonaLiik(sisend()), "Sonaliikide-sagedusloend.csv")

jne.

Sisendfailide listi võib eelnevalt eraldi defineerida ja seejärel kasutada vastavat muutujat teiste funktsioonide argumendina:
'''







