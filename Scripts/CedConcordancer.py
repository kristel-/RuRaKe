'''
Concordancer for Corpus of Estonian Dialects
Author: Kristel Uiboaed
Functions getrightcontext, getleftcontext and concordance (modified here) originally from
https://github.com/fbkarsdorp/python-course/blob/master/pyhum/concordance.py
'''

import os
import re
import xml.etree.ElementTree as etree
import time
import sys

start = time.time()

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


class CedConcordancer:

        def __init__ (self, inputFile='NULL', queryWord=0, queryWordUnit=0, contextSize=0, contextWordUnit=0, contextWord=0):
            self.queryWord = queryWord
            self.contextSize = contextSize
            self.queryWordUnit = queryWordUnit
            self.inputFile = inputFile
            self.contextWordUnit = contextWordUnit
            self.contextWord = contextWord

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
                Mark missing values with NA.
                '''

                headerInfoString = fileName + ";" + parish + ";" + dialect + ";" + village + ";" + long + ";" + lat

            return headerInfoString

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
                '''
                Every informant as a separate string with informant metainfo.
                '''

            return informants

        def getleftcontext(self, tokens, i, contextSize):
            begin = i - contextSize
            if begin < 0:
                begin = 0 #begin musn't be negative (because that is special syntax for specifying an index from the right)
            return tokens[begin:i]

        def getrightcontext(self, tokens, i, contextSize):
            return tokens[i+1:i+1+contextSize] #no problem if i+1+contextsize exceeds the len(tokens), but there will simply not be more to slice off

        '''
        Searchable unit can be
        "liik" - pos, "vorm" - morphological category / form, "lemma" - some lemma
        '''

        def concordance(self, tokens, queryWord, contextSize, queryWordUnit):
            conc = []
            for i, token in enumerate(tokens):
                if token[queryWordUnit] == queryWord:
                    leftcontext = self.getleftcontext(tokens,i,contextSize)
                    rightcontext = self.getrightcontext(tokens,i,contextSize)
                    myConc = (leftcontext, token, rightcontext)
                    conc.append(myConc)
            return conc

        def cedconcordances(self, inputFile, queryWord, contextSize, queryWordUnit, contextWordUnit="0", contextWord="0"):
            header = self.fileHeaderInfo(inputFile)
            informants = self.informantInfo(inputFile)
            fileConcordances = []                                                   # concordances of the input file
            with open (inputFile, "r", encoding="utf-8") as myInput:
                tree = etree.parse(myInput)
                root = tree.getroot()
                turns = root.findall("./sisu/lause")

                for t in turns:                                                     # following steps only for one turn
                    oneTurn = []
                    if "koneleja" in t.attrib and "KJ" in t.attrib['koneleja']:     # if it is an informant's turn
                        words = t.findall("./sone")                                 # extract all annotated tokens
                        whoseTurn = t.attrib['koneleja']                            # informant code for identifying the utterance
                        for word in words:
                            word.attrib['kj'] = whoseTurn
                            if "meta" not in word.attrib:                           # exclude all tokens with word attribute, but are not actual content words
                                word.attrib['sone'] = word.text                     # add also the text word into token attributes (to simplify further processing)
                                if "liik" not in word.attrib:
                                    word.attrib['liik'] = "NA"                      # unannotated and interruptions don't have pos value, just add the attribute to avoid           xml-error
                                if "vorm" not in word.attrib:
                                    word.attrib['vorm'] = "NA"
                                if "sone" not in word.attrib:
                                    word.attrib['sone'] = "NA"
                                if "lemma" not in word.attrib:
                                    word.attrib['lemma'] = "NA"
                                oneTurn.append(word.attrib)

                    '''
                    Concordance the turn, the resulting data structure:
                    [([{}, {}, ..], {}, [{}, {}, ..]), ([{}, {}, ..], {}, [{}, {}, ..]), ([{}, {}, ..], {}, [{}, {}, ..]), ...]
                    List that contains all the concordances of one turn
                    One concordadance is a tuple of three members:
                    0 - list of left context words, every "word" is the dictionary with its attributes
                    1 - keyword as a dictionary
                    2 - list of left context words, every "word" is the dictionary with its attributes
                    '''

                    concordances = self.concordance(oneTurn, queryWord, contextSize, queryWordUnit)

                    if len(concordances) > 0:           # if there were any matches in the turn

                        if contextWordUnit == "0" and contextWord == "0":                        # simple search with no context conditions
                            for conc in concordances:
                                rightContext = ""
                                leftContext = ""
                                keyword = ";" + conc[1]["sone"] + ";"
                                for w in conc[0]:
                                    leftContext = leftContext + w["sone"] + " "
                                for w in conc[2]:
                                    rightContext = rightContext + w["sone"] + " "
                                for inf in range(len(informants)):                      # go through informants (the file can have several informants)
                                    if informants[inf][0] == conc[1]["kj"]:             # match the informant code with the concordance
                                        infString = ";".join(informants[inf])

                                wholeEntry = leftContext.strip() + keyword + rightContext.strip() + ";" + header + ";" + infString # paste the concordance, append file metainfo and the informant info
                                fileConcordances.append(wholeEntry)

                        else: # continue with context analysis

                            '''
                            Loop through concordances and collect left and right context words with attributes into one list.
                            Only items that have searched key valu pair in left or right context will be selected.
                            '''

                            withContext = []
                            for conc in concordances:
                                concItems = []
                                for lw in conc[0]:
                                    for k, v in lw.items():
                                        concItems.append((k, v))

                                for rw in conc[2]:
                                    for k, v in rw.items():
                                        concItems.append((k, v))

                                if (contextWordUnit, contextWord) in concItems:
                                    withContext.append(conc)

                            for conc in withContext:
                                rightContext = ""
                                leftContext = ""
                                keyword = ";" + conc[1]["sone"] + ";"
                                for w in conc[0]:
                                    leftContext = leftContext + w["sone"] + " "
                                for w in conc[2]:
                                    rightContext = rightContext + w["sone"] + " "
                                for inf in range(len(informants)):                      # go through informants (the file can have several informants)
                                    if informants[inf][0] == conc[1]["kj"]:             # match the informant code with the concordance
                                        infString = ";".join(informants[inf])

                                wholeEntry = leftContext.strip() + keyword + rightContext.strip() + ";" + header + ";" + infString # paste the concordance, append file metainfo and the informant info
                                fileConcordances.append(wholeEntry)

            return fileConcordances
            
def main():
    CorpConc = CedConcordancer()
    searchType = input("Enter the search type: 1 (simple) or 2 (contextual)\n").strip()
    queryWordUnit = input("Enter the keyword category to be searched (\"lemma\", \"vorm\" (for form), \"liik\" (for pos))\n").strip()
    queryWord = input("Enter the keyword term (lemma, form or pos tag)\n").strip()
    contextSize = int(input("Enter the context window size in numbers\n").strip())

    if searchType == "1":
        contextWordUnit = "0"
        contextWord = "0"
    elif searchType == "2":
        contextWordUnit = input("Enter the context category to be searched (\"lemma\", \"vorm\" (for form), \"liik\" (for pos))\n").strip()
        contextWord = input("Enter the keyword term (lemma, form or pos tag)\n").strip()

    outputFileName = input("Enter the output file name.\n").strip()

    with open (outputFileName, "a", encoding="utf-8") as outputFile:
        for file in myInput():
            for item in CorpConc.cedconcordances(file, queryWord, contextSize, queryWordUnit, contextWordUnit, contextWord):
                outputFile.write(item + "\n")

if __name__ == '__main__':
    main()

print("Done.\nThe task took %.2f seconds." % (time.time() - start))
