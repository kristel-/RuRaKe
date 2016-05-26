'''
Author: Kristel Uiboaed
'''

import re
import os
import xml.etree.ElementTree as etree
import shutil

'''
Function that creates list of input xml files from directories within a working directory.
'''
def myInput():
    catalogues = os.listdir()
    inputFiles = []
    for cat in catalogues:
        if os.path.isdir(cat):
            os.chdir(cat)
            files = os.listdir()
            for file in files:
                    if file.endswith(".xml"):
                        if os.path.isfile(file):
                            inputFiles.append(os.path.join(cat, file))
            os.chdir('..')
    return inputFiles

'''
CSV file of errors in a form lemma;error;correction or
something similar (depending on the error type).
'''
def errors (errorFile):
    with open (errorFile, "r", encoding="utf-8") as inp:
        errorList = []
        for line in inp.readlines():
            correction = line.strip().split(";")
            errorList.append(correction)
    return errorList

'''
Create source dir for e.g. modified files files.
'''
def createSourceDir(destination, dirName):
    if not os.path.exists(destination + dirName):
        os.makedirs(os.path.join(destination + dirName))
        return os.path.join(destination + dirName)
    else:
        newDest = destination + dirName
        return newDest

'''
Move modified .temp-files from working dirs and change their extension back to xml.
'''
def moveFiles(destPath, dirName):
    newDest = createSourceDir(destPath, dirName)
    catalogues = os.listdir()
    for cat in catalogues:
        if os.path.isdir(cat):
            os.chdir(cat)
            files = os.listdir()
            for file in files:
                    if file.endswith(".temp"):
                        if os.path.isfile(file):
                            shutil.move(file, newDest)
            os.chdir('..')
    os.chdir(newDest)        
    for file in os.listdir(newDest):
        base = os.path.splitext(file)[0]
        os.rename(file, base + '.xml')
       
'''
Error correction function.
Correct the pos tag for a given lemma.
Writing tree, root from another function does not write the modifications in the new tree.
'''
def wrongPosForLemma(inputFile, errorFile):
    errorList = errors(errorFile)
    
    tree = etree.parse(inputFile)
    root = tree.getroot()
    lemmas = root.findall('./sisu/lause/sone[@liik]')
    fake_root = etree.Element(None) # Create 'fake' root node
    pi = etree.PI('xml-stylesheet', 'type="text/xsl" href="liivike_tekst.xsl"') # Add desired processing instructions.  Repeat as necessary.
    pi.tail = "\n"
    fake_root.append(pi)
    fake_root.append(root) # Add real root as last child of fake root
    tree = etree.ElementTree(fake_root)

    for error in errorList:
        for lemma in lemmas:
            if "lemma" in lemma.attrib and "liik" in lemma.attrib:
                if lemma.attrib["lemma"] == error[0] and lemma.attrib["liik"] == error[1]: # wrong pos for lemma error
                    print(lemma.attrib)
                    lemma.set("liik", error[2])
                    print(lemma.attrib)
                else:
                    continue
                tree.write((re.sub(".xml", "", inputFile) + ".temp"), xml_declaration=True, encoding="utf-8")

'''
Error correction function.
Modify the lemma with typo.
'''
def lemmaTypo(inputFile, errorFile):
    errorList = errors(errorFile)
    
    tree = etree.parse(inputFile)
    root = tree.getroot()
    lemmas = root.findall('./sisu/lause/sone[@liik]')
    fake_root = etree.Element(None) # Create 'fake' root node
    pi = etree.PI('xml-stylesheet', 'type="text/xsl" href="liivike_tekst.xsl"') # Add desired processing instructions.  Repeat as necessary.
    pi.tail = "\n"
    fake_root.append(pi)
    fake_root.append(root) # Add real root as last child of fake root
    tree = etree.ElementTree(fake_root)
    
    for error in errorList:
        for lemma in lemmas:
            if "lemma" in lemma.attrib and "liik" in lemma.attrib:
                if lemma.attrib["lemma"] == error[0] and lemma.attrib["liik"] == error[1]:
                    print(lemma.attrib)
                    lemma.set("lemma", error[2]) # set to the right lemma
                    print(lemma.attrib)
                    outputFile = (re.sub(".xml", "", inputFile) + ".temp")
                else:
                    continue
                tree.write((re.sub(".xml", "", inputFile) + ".temp"), xml_declaration=True, encoding="utf-8")


'''
Error correction function.
Modify the incorrect lemma, pos, and form.
Error input file format:
incorrect lemma;incorrect pos;correct lemma;correct pos;correct form
'''
def lemmaPosMissingForm(inputFile, errorFile):
    errorList = errors(errorFile)
    
    tree = etree.parse(inputFile)
    root = tree.getroot()
    lemmas = root.findall('./sisu/lause/sone[@liik]')
    fake_root = etree.Element(None) # Create 'fake' root node
    pi = etree.PI('xml-stylesheet', 'type="text/xsl" href="liivike_tekst.xsl"') # Add desired processing instructions.  Repeat as necessary.
    pi.tail = "\n"
    fake_root.append(pi)
    fake_root.append(root) # Add real root as last child of fake root
    tree = etree.ElementTree(fake_root)
    
    for error in errorList:
        for lemma in lemmas:
            if "lemma" in lemma.attrib and "liik" in lemma.attrib and "vorm" not in lemma.attrib:
                if lemma.attrib["lemma"] == error[0] and lemma.attrib["liik"] == error[1]:
                    print(lemma.attrib)
                    lemma.set("lemma", error[2]) # set to the right lemma
                    lemma.set("liik", error[3]) # set to the right pos
                    lemma.attrib["vorm"] = error[4] # add morph attribute
                    print(lemma.attrib)
                    outputFile = (re.sub(".xml", "", inputFile) + ".temp")
                else:
                    continue
                tree.write((re.sub(".xml", "", inputFile) + ".temp"), xml_declaration=True, encoding="utf-8")



'''
Error correction function.
Modify the incorrect lemma, pos, and form.
Error input file format:
incorrect lemma;incorrect pos;correct lemma;correct pos;correct form
'''
def posFormMistakes(inputFile, errorFile):
    errorList = errors(errorFile)
    
    tree = etree.parse(inputFile)
    root = tree.getroot()
    lemmas = root.findall('./sisu/lause/sone[@liik]')
    fake_root = etree.Element(None) # Create 'fake' root node
    pi = etree.PI('xml-stylesheet', 'type="text/xsl" href="liivike_tekst.xsl"') # Add desired processing instructions.  Repeat as necessary.
    pi.tail = "\n"
    fake_root.append(pi)
    fake_root.append(root) # Add real root as last child of fake root
    tree = etree.ElementTree(fake_root)
    
    for error in errorList:
        for lemma in lemmas:
            if "lemma" in lemma.attrib and "liik" in lemma.attrib and "vorm" not in lemma.attrib:
                if lemma.attrib["lemma"] == error[0] and lemma.attrib["liik"] == error[1]:
                    lemma.set("lemma", error[2]) # set to the right lemma
                    lemma.set("liik", error[3]) # set to the right pos
                    lemma.attrib["vorm"] = error[4] # add morph attribute
                    outputFile = (re.sub(".xml", "", inputFile) + ".temp")
                else:
                    continue
                tree.write((re.sub(".xml", "", inputFile) + ".temp"), xml_declaration=True, encoding="utf-8")



'''
Error correction function.
Modify the incorrect lemma with correct pos.
Error input file format: pos;incorrect lemma;correct lemma
'''

def correctLemmaWithRightPos(inputFile, errorFile):
    errorList = errors(errorFile)
    
    tree = etree.parse(inputFile)
    root = tree.getroot()
    lemmas = root.findall('./sisu/lause/sone[@liik]')
    fake_root = etree.Element(None) # Create 'fake' root node
    pi = etree.PI('xml-stylesheet', 'type="text/xsl" href="liivike_tekst.xsl"') # Add desired processing instructions.  Repeat as necessary.
    pi.tail = "\n"
    fake_root.append(pi)
    fake_root.append(root) # Add real root as last child of fake root
    tree = etree.ElementTree(fake_root)
    
    for error in errorList:
        for lemma in lemmas:
            if "lemma" in lemma.attrib and "liik" in lemma.attrib:
                if lemma.attrib["lemma"] == error[1] and lemma.attrib["liik"] == error[0]:
                    print(lemma.attrib)
                    lemma.set("lemma", error[2]) # set to the right lemma
                    print(lemma.attrib)
                    outputFile = (re.sub(".xml", "", inputFile) + ".temp")
                else:
                    continue
                tree.write((re.sub(".xml", "", inputFile) + ".temp"), xml_declaration=True, encoding="utf-8")

'''
for f in myInput():    
    print(f)
    #wrongPosForLemma(f, "pos-mistakes.csv")
    lemmaFormMistakes(f, "lemma-pos-form-mistakes.csv")
moveFiles('destinationPath', 'destinationFolder')
'''











