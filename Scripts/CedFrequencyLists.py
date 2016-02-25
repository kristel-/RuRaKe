'''
Author: Kristel Uiboaed
'''

import os
import re
from operator import itemgetter
from collections import Counter
import xml.etree.ElementTree as etree

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

class Ced:

    def __init__(self, inputFile='NULL'):
        self.inputFile = inputFile


    '''
    Function that returns transcription characters in input files
    '''
    
    def transcrCharList(self, inputFile):
        transcrChars = []
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            char = root.findall("./sisu/lause/sone[@meta='vahemärk']")
            for i in char:
                transcrChars.append(i.text)
        return transcrChars

    '''
    Function that returns informant codes in input files
    '''

    def informantList(self, inputFile):
        informants = []
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            fileInformants = root.findall("./sisu/lause[@koneleja]")
            for i in fileInformants:
                informants.append(i.attrib['koneleja'])
        return informants

    '''
    Function that returns a list of meta character attribute values in input files
    '''

    def metaChars (self, inputFile):
        metaCharAttributes = []
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            metaChars = root.findall("./sisu/lause/sone[@meta]")
            for i in metaChars:
                metaCharAttributes.append(i.attrib['meta'])
        return metaCharAttributes


    '''
    Function that returns tags for morphological/grammatical categories
    '''

    def grammaticalCategories (self, inputFile):
        grammCats = []
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            gramm = root.findall("./sisu/lause/sone[@vorm]")
            for i in gramm:
                grammCats.append(i.attrib['vorm'])
        return grammCats

    '''
    Function that returns part of speech tags
    '''

    def partOfSpeech (self, inputFile):
        posTags = []
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            pos = root.findall("./sisu/lause/sone[@liik]")
            for i in pos:
                posTags.append(i.attrib['liik'])
        return posTags


    '''
    Function that returns comment attribute values.
    '''

    def comments (self, inputFile):
        commentList = []
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            comment = root.findall("./sisu/lause/sone[@kommentaar]")
            for i in comment:
                commentList.append(i.attrib['kommentaar'])
        return commentList


    '''
    Function that returns list of lemmas with given pos-tag (see CED pos tags in README).
    Noun lemmas are returned default, if some other lemmas are desireble change the pos value
    '''

    def lemmas (self, inputFile, pos="S"):
        lemmaList = []
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            lemma = root.findall('./sisu/lause/sone[@liik]')
            for i in lemma:
                posAttributes = i.attrib
                if posAttributes['liik'] == pos:
                    lemmaList.append(posAttributes.get('lemma', 'missing lemma'))
        return lemmaList



    '''
    Retrieve file metadata from header.
    Output as a string, values separated with ;
    Missing values marked with NA
    '''

    def fileHeaderInfo(self, inputFile):
        with open (inputFile, "r", encoding="utf-8") as myInput:
            fileName = re.sub(r".*\\", "", inputFile)
            tree = etree.parse(myInput)
            root = tree.getroot()
            parish = root.find("./info/kihelkond").text
            dialect = root.find("./info/murre").text
            village = root.find("./info/kyla").text
            long = root.find("./info/kyla[@longituud]").attrib['longituud']
            lat = root.find("./info/kyla[@latituud]").attrib['latituud']

            '''
            Some files have several informants.
            Retrieve metainfo for every single informant separately.
            There are missing values, mark with NA.
            '''

            headerInfoString = fileName + ";" + parish + ";" + dialect + ";" + village + ";" + long + ";" + lat

        return headerInfoString

    '''
    Retrieve informant information from file.
    Return list of lists, every element is a separate informant.
    '''
    
    def informantInfo(self, inputFile):
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()
            fileInformants = root.findall("./info/keelejuht")

            informants = []
            
            '''
            Some files have several informants.
            Retrieve metainfo for every single informant separately.
            Mark missing values with NA.
            '''

            for s in range(len(fileInformants)):
                singleList = []
                singleList.append(fileInformants[s].attrib['id'])
                singleList.append(fileInformants[s].attrib['vanus'])
                singleList.append(fileInformants[s].attrib['synniaasta'])
                informants.append(singleList)

            for j, k in enumerate(informants):
                for l, m in enumerate(k):
                    if m == '':
                        informants[j][l] = 'NA'
                        
        return informants

    '''
    Function that returns a list of pos, lemma and file info strings, e.g.
    V;tulema;KJ1;FileName.xml;Plt;Kesk;Leisu;26.16556;58.64694;KJ1;82;1887
    '''

    def posLemmaListWithFileInfo(self, inputFile):
        posLemmaHeaderList = []
        header = self.fileHeaderInfo(inputFile)
        informants = self.informantInfo(inputFile)
        with open (inputFile, "r", encoding="utf-8") as myInput:
            tree = etree.parse(myInput)
            root = tree.getroot()

            turns = root.findall("./sisu/lause/[@koneleja]")

            for turn in turns:
                if 'KJ' in turn.attrib['koneleja']: # only turns of informants
                    for word in turn:
                        if ('liik' in word.attrib.keys() and 'lemma' in word.attrib.keys()) and word.attrib['liik'] != '' and word.attrib['lemma'] != '': # only words with these attributes and without missing values
                            pos = word.attrib['liik']
                            lemma = word.attrib['lemma']
                            informant = turn.attrib['koneleja']

                            for inf in range(len(informants)):
                                if informants[inf][0] == informant:
                                    infString = ";".join(informants[inf])
                            
                            wholeEntry = pos + ";" + lemma + ";" + informant + ";" + header + ";" + infString
                            posLemmaHeaderList.append(wholeEntry)
            return posLemmaHeaderList

    '''
    Return frequency list of input list items.
    The output is in dictionary format containing of tuples (word, freq).
    '''

    @staticmethod
    def frequencyList(inputList):
        freqs = dict(Counter(inputList))
        sortedFreqs = sorted(freqs.items(), key=itemgetter(1), reverse=True)
        return sortedFreqs


    '''
    Output the frequency dictionary to file.
    The input should be in dictionary format containing of tuples (word, freq).
    '''

    @staticmethod
    def freqDictToFile(inputFreqDict, outputFileName):
        with open(outputFileName, "w", encoding="utf-8") as outputFile:
            for i in inputFreqDict:
                outputFile.write(i[0] + ";" + str(i[1]) + "\n") #i[0] is a string(word), i[1] is frequency, will be separated by ; in the file

    '''
    Output the given list into file.
    Every element as a separate line.
    '''

    @staticmethod
    def longFormatToFile(inputList, outputFileName):
        with open(outputFileName, "w", encoding="utf-8") as outputFile:
            for i in inputList:
                outputFile.write(i + "\n")

        
    '''
    Function that returns a singl list of e.g. lemmas from input file list.
    The first argument is the list of files.
    The second argument should be function from the class ced e.g lemmas, comments etc.
    '''

    @staticmethod
    def meltList(inputFileList, func):
        meltedList = []
        for file in inputFileList:
            for item in func(file):
                meltedList.append(item)
        return meltedList
            


'''
Enter the input type from command line.
A word "list" will create the file list from directories within a working directory.
By entering the file or the path to file only this file will be analyzed.
'''

def main():
    Corpus = Ced()
    typeOfInput = input("Enter input as a word \"list\" (input file list will be created from directories in working directory) or path to the file (e.g. C:\\MyDocs\\Files\\filename).\nIf the file is in the working directory only the file name is sufficient:\n").strip()

    if typeOfInput == "list":
        typeOfInput = myInput()
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.meltList(typeOfInput, Corpus.transcrCharList)), "transcriptionCharsInFiles.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.meltList(typeOfInput, Corpus.informantList)), "informantsInFiles.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.meltList(typeOfInput, Corpus.metaChars)), "metaCharsInFiles.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.meltList(typeOfInput, Corpus.grammaticalCategories)), "grammCatsInFiles.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.meltList(typeOfInput, Corpus.comments)), "commentsInFiles.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.meltList(typeOfInput, Corpus.partOfSpeech)), "partOfSpeechInFiles.csv")
        Corpus.longFormatToFile(Corpus.meltList(typeOfInput, Corpus.posLemmaListWithFileInfo), "posLemmaInFiles.csv")

    elif os.path.isfile(typeOfInput) == True:
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.transcrCharList(typeOfInput)), "transcriptionCharsInFile.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.informantList(typeOfInput)), "informantsInFile.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.metaChars(typeOfInput)), "metaCharsInFile.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.grammaticalCategories(typeOfInput)), "grammCatsInFile.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.comments(typeOfInput)), "commentsInFile.csv")
        Corpus.longFormatToFile(Corpus.posLemmaListWithFileInfo(typeOfInput), "posLemmaFiles.csv")
        Corpus.freqDictToFile(Corpus.frequencyList(Corpus.partOfSpeech(typeOfInput)), "partOfSpeechInFile.csv")


if __name__ == '__main__':
    main()









