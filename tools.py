# pip install requests
import requests
import json
import string
# pip install nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import operator


class NoResults(Exception):
    def __init__(self, query, message = "No results found with "):
        self.query = query
        self.message = message + query
        super().__init__(self.message)


class queryJSON:

    def __init__(self, url=None, file=None, query=None):
        self.url = url
        self.file = file
        self.query = query

    def saveData(self, url):
        validURL = False
        try:
            r = requests.get(url)
            data = r.content
            with open('data.json', 'wb') as f:
                f.write(data)
            self.file = 'data.json'
            validURL = True
            return validURL
        except Exception as e:
            data = {"data": [], "error": e}
            print(data)
            return validURL

    def index(self, file):
        try:
            f = open(file)
            data = json.load(f)
            data["error"] = []
            return data
            f.close()
        except Exception as e:
            data = {"data": [], "error": e}
            return data

    def search(self, file, query):

        try:
            # CONVERT JSON OBJ. TO DICTIONARY OF SENTENCES SPLIT BY WORD

            rawJSON = self.index(file)
            values = rawJSON.values()

            # Populate splitDict with Key/Value Pair of Sentence Index and Sentence
            count = 0
            splitDict = {}

            for value in values:
                for sentence in value:
                    splitSentence = sentence.split()
                    splitDict[count] = splitSentence
                    count += 1

            # COUNT OCCURRENCE OF QUERY IN EACH SENTENCE

            # Create Dictionary Key/Value Pair for Each Sentence to Count Occurrence of Query
            wordCount = {n: 0 for n in splitDict}

            # Stem Each Word and Query for Fuzzy Search
            stemmer = PorterStemmer()

            # Iterate through Each Word in Each Sentence
            for sentence in splitDict:
                for word in splitDict[sentence]:

                    # Stem and Lowercase Query and Word Ex: Sentences => sentence
                    # Remove Punctuation from Each word Ex: learning! => learning
                    formatWord = stemmer.stem((word.lower()).translate(
                        str.maketrans('', '', string.punctuation)))
                    formatQuery = stemmer.stem(query.lower())

                    # If Match => Increment Value of the Sentence in the Dictionary
                    if formatQuery == formatWord:
                        wordCount[sentence] += 1

            # RETURN RESULTS DICT. OF SENTENCES AT INDEXES OF QUERY OCCURRENCE IN DESCENDING ORDER

            sortedDict = dict(
                sorted(wordCount.items(), key=operator.itemgetter(1), reverse=True))

   
            resultIndexes = []

            # Identify Indexes to Return with in Descending Order
            for i in sortedDict:
                if sortedDict[i] > 0:
                    resultIndexes.append(i)

            if resultIndexes == []:
                raise NoResults(query)

            resultList = []

            #Format Values Variable
            valueIterator = iter(values)
            value = next(valueIterator)

            for i in resultIndexes:
                resultList.append(value[i])

            errorMessage = ""
            resultDict = {
                "results": resultList,
                "error": errorMessage
            }
            returnJSON = json.dumps(resultDict, ensure_ascii=False)
            return returnJSON
            
        except Exception as e:
            data = {"results": value, "error": e}
            return data
