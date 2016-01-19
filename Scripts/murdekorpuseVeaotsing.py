import os
import re
import xml.etree.ElementTree as etree


'''
Funktsioon, mis koostab sisendfailide listi
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
etteantud list vigastest kohtadest
otsitakse faile, kus see viga esineb
tagastatakse viga + fail eraldi failis
'''

def viganeFailVeaga (sisendfailideList, veadListina, valjundfailiNimi):
    vigadegaFailid = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            failYheStringina = sisend.read().replace('\n', '')
            for viga in veadListina:
                if viga in failYheStringina:
                    vigadegaFailid.append(viga + ";" + fail)
    with open (valjundfailiNimi, "w", encoding="utf-8") as valjund:
        for i in vigadegaFailid:
            valjund.write(i + "\n")


def viganeFailVigaseSonega (sisendfailideList, veadListina, valjundfailiNimi):
    vigadegaFailid = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            tree = etree.parse(sisend)
            root = tree.getroot()
            soned = root.findall('./sisu/lause/sone[@vorm]')
            for sone in soned:
                if sone.attrib['vorm'] in veadListina:
                    vigadegaFailid.append(sone.text + ";" + sone.attrib['vorm'] + ";" + fail)                                   
    with open (valjundfailiNimi, "w", encoding="utf-8") as valjund:
        for i in vigadegaFailid:
            valjund.write(i + "\n")


'''
konkreetse vea otsing
siin otsitakse sõnaliigita märgendeid (liik = "")
'''

def sonaLiigita (sisendfailideList, valjundfailiNimi):
    tulemused = []
    for fail in sisendfailideList:
        with open (fail, "r", encoding="utf-8") as sisend:
            failYheStringina = sisend.read().replace('\n', '')
            yhedVead = re.findall(r'<[^>]*liik=""[^>]*>', failYheStringina)
            for i in yhedVead:
                tulemused.append(i)
    with open (valjundfailiNimi, "w", encoding="utf-8") as valjund:
        for i in tulemused:
            valjund.write(i + "\n")


#olla = ['(<sone id="[^"]*" lemma=")palk(" vorm="[^"]*" liik="V">)']
vead = ['lk=""']

viganeFailVeaga(sisend(), vead, "test.csv")




#viganeFailVigaseSonega(sisend(), vead, "vigasedFailid.csv")

#olla = re.compile('(<sone id="[^"]*" lemma=")palk(" vorm="[^"]*" liik="V">)')


#lemma="olema" vorm="pers.ind.pr.sg.3." liik="V">
#for fail in sisend():
#    with open (fail, "r", encoding="utf-8") as sisend:
#        for rida in sisend:
#            if re.search(olla, rida):
#                print(fail)
#                uusRida = re.sub(olla, '\1palkama\2', rida)
#                with open("fail.txt", "w", encoding="utf-8") as valjund:
#                    valjund.write(uusRida + "\n")


#for fail in sisendfailid:
#    with open (fail, "r", encoding="utf-8") as sisend:
#        valjund = open((re.sub(".kym", "", fail) + ".sag"), "w", encoding="utf-8")
#        for rida in sisend:
#            rida2 = re.sub("    .*", "", rida)
#            rida3 = html.parser.HTMLParser().unescape(rida2.strip())
#            rida4 = re.sub("<.*>", "", rida3)
#            if len(rida4) > 0:
#                valjund.write(rida4 + "\n")
#        valjund.close()

