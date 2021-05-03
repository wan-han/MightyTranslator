from bs4 import BeautifulSoup # Library for HTML scraping
from urllib.request import urlopen
import googletrans # Google translate python library
from googletrans import Translator
from allLang import languages # Important python dictionary file of available languages
import PyPDF2 # Imports python library for working with PDF files
from PyPDF2 import PdfFileReader
import docx2txt 
from config import *
# Go to bottom of the code for library references to installment 

key_list = list(languages.keys()) # A variable of keys in the languages dictionary as a list
val_list = list(languages.values()) # A variable of values in the languages dictionary as a list
translator = Translator()

class transl: 
    def __init__(self, textIn, langInp, langOu): # This is for the googletrans variables
        self.textIn = textIn
        self.langInp = langInp
        self.langOu = langOu
        
    def actTransl(self):
        translation = translator.translate(self.textIn, src=self.langInp, dest=self.langOu) # Uses googletrans library to translate user's text
        print(translation)
        collection = save(self.textIn, translation)
        collection.fileSaver()

class file: # This class is for file manipulation for text, pdf files and word files for the translation library
    def __init__(self, fLoc, fType):
        self.fLoc = fLoc
        self.fType = fType

    def getFile(self): 
        if self.fType == "txt":
            file1 = open(self.fLoc,"r")
            fileRead = file1.read()
            trsl = transl(fileRead, keyIn, keyOut)
            trsl.actTransl()
            file1.close()
       
        elif self.fType == "pdf": # This section make use of the PyPDF2 library
            pdfFileObj = open(self.fLoc, "rb")
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            pageObj = pdfReader.getPage(0) 
            pdfText = pageObj.extractText()
            trsl = transl(pdfText, keyIn, keyOut)
            trsl.actTransl()
    
        elif self.fType == "word": # This section is for word documents
            docText = docx2txt.process(location)
            trsl = transl(docText, keyIn, keyOut)
            trsl.actTransl()
   
        else:
            print("No supported file format was entered. ")

class save:
    def __init__(self, textIn, textOut):
        self.textIn = textIn
        self.textOut = textOut
    
    def fileSaver(self):
        f = open(write_name+".txt", "w+", encoding="utf-8")
        f.write("Original text: \n")
        f.write(str(self.textIn))
        f.write("\nTranslated text: ")
        f.write(str(self.textOut))
        f.close

a = 1
while a == 1:

    b = 1
    while b == 1:
        langIn = str.lower(input("What language do you want to translate from? ")) # The user inputs a language to translate from
                                                                                   # Changes the user's input to lower case to make sure it's readable into the dictionary
        position = val_list.index(langIn) # Finds what number position the dictionary value that the user entered is
        keyIn = key_list[position] # Uses the number position of values to see the partnered key in the dictionary

        langOut = str.lower(input("What language do you want to translate to? ")) # The user inputs a language which they want to translate to

        position2 = val_list.index(langOut)
        keyOut = key_list[position2]
        b = 2

    which = str.lower(input("Do you want to translate specific text, a file or a website? text/file/web: "))
    if which == "text":
        print("Please type/ paste the text you'd like to translate here. We will separate each line with a '.' at the end of the previous line. (to end the submission press ctrl-z): ")
        contents = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            contents.append(line)

        str1 = '\n'.join(contents)
        str1 = str(str1)
        trsl = transl(str1, keyIn, keyOut)
        current = str.upper(input("Do you want to show the text in current language too? Y/N: ")) 
        # Asks the user if they want to have the text in current language or not
        # Converts user's input into uppercase

        if current == "Y": # If statement to check if user's input is viable
            print(str1)
        trsl.actTransl()
        again = str.upper(input("Do you want to translate something else? Y/N: "))
        if again == "Y":
            a = 1
        else:
            a = 2

    elif which == "file":
        location = str(input("What's the file location? "))
        tType = str.lower(input("What's the file format? i.e. txt, pdf, word "))
        datas = file(location, tType)
        datas.getFile() # Initiates the second function within the file class

    elif which == "web":
        url = str(input("Pleaase paste a link to the website you'd like to translate here: ")) 
        # User inputs the URL to the website they want to translate
        page = urlopen(url) # Opens the URL for access
        
        html = page.read().decode("utf-8") # Converts the HTML into UTF-8
        soup = BeautifulSoup(html, "html.parser") # Using BeautifulSoup to scan the page
        
        doc = soup.get_text() # Scrapes the HTML to leave just text and removes tags
        str(doc)
        trsl = transl(doc, keyIn, keyOut)
        trsl.actTransl()
#        word = translator.translate(doc, src=keyIn, dest=keyOut) # Translates the scraped HTML via BeautifulSoup by using the GoogleTrans library
                                                                 # src = Source language. Provided by Line 10-14
                                                                 # dest = Destination language. Provided by Line 16-19

        current = str.upper(input("Do you want to show the text in current language too? Y/N: ")) 
        # Asks the user if they want to have the document in current language or not
        # Converts user's input into uppercase

        if current == "Y": # If statement to check if user's input is viable
            trsl = transl(doc, keyIn, keyOut)
            trsl.actTransl()
            #print(soup.get_text()) # If viable as "Y", it will output the document in current language
            #print(word) # Will then continue to output in translated language
            again = str.upper(input("Do you want to translate something else? Y/N: "))
            if again == "Y":
                a = 1
            else:
                a = 2

        elif current == "N": # If viable as "N", it will output just the translated document
            print(word)
            again = str.upper(input("Do you want to translate something else? Y/N: "))
            if again == "Y":
                a = 1
            else:
                a = 2
       
        else:
            print("Input not recognised. Ending program... ") # If no viable input is detected, will output an error
            a = 2
input()

# Python Modules installed:
# beautifulsoup4:
#     pip install beautifulsoup4
# urllib3:
#     pip install urllib3
# googletrans:
#     pip install googletrans   
#     pip uninstall googletrans
#     pip update googletrans
# PyPDF2:
#     pip install PyPDF2
# Doc2text:
#     pip install docx2txt
