'''
Set of functions to look for errors in CED files.
Author: Kristel Uiboaed
v. 01.02.2016
'''

import os
import re
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

'''
Write input list items to file on separate lines.
'''

def listToFile(inputList, outputFileName):
    with open (outputFileName, "w", encoding="utf-8") as outputFile:
        for item in inputList:
            outputFile.write(item + "\n")

'''
Create a list that consists of searchable units.
Look for file that contains these items.
Return search word + file name pairs in a separate file.
'''

def fileWithError (inputFileList, errorList, outputFileName):
    filesWithErrors = []
    for file in inputFileList:
        with open (file, "r", encoding="utf-8") as inp:
            fileAsString = inp.read().replace('\n', '')
            for error in errorList:
                if error in fileAsString:
                    filesWithErrors.append(error + ";" + file)
    listToFile(filesWithErrors, outputFileName)

'''
Look for grammatical category error.
Input list is the list of errors.
Output into file (category error, token with that category and file name)
'''

def fileWithTokenError (inputFileList, errorList, outputFileName):
    filesWithErrors = []
    for file in inputFileList:
        with open (file, "r", encoding="utf-8") as inp:
            tree = etree.parse(inp)
            root = tree.getroot()
            tokens = root.findall('./sisu/lause/sone[@vorm]')
            for token in tokens:
                if token.attrib['vorm'] in errorList:
                    filesWithErrors.append(token.text + ";" + token.attrib['vorm'] + ";" + file)                                   
    listToFile(filesWithErrors, outputFileName)
 
'''
Search files with regular expressions, e.g.
regexSearch(myInput(), '<[^>]*liik=""[^>]*>', "myOutputFile.csv")
'''

def regexSearch(inputFileList, pattern, outputFileName):
    filesWithErrors = []
    for file in inputFileList:
        with open (file, "r", encoding="utf-8") as inp:
            fileAsString = inp.read().replace('\n', '')
            errors = re.findall(r''+pattern, fileAsString)
            for error in errors:
                filesWithErrors.append(error)
    listToFile(filesWithErrors, outputFileName)




























