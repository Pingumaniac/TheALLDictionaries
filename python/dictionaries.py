import json
import requests
from apiclient.discovery import build
from GoogleNews import GoogleNews
from PyDictionary import PyDictionary
from udpy import UrbanClient
import wikipediaapi
from wiktionaryparser import WiktionaryParser
from PyDictionary import PyDictionary
from youtubesearchpython import VideosSearch

def mwcDict(word):
    if word == "":
        return " is not found on Merriam Webster Dictionary."

    apiKey  = "c33d59f0-4576-4dfc-a389-918e5316421b"
    wordURL = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+ word + "?key=" + apiKey
    result = requests.get(wordURL)
    dictionaryResult = result.json()
    
    if dictionaryResult == {}:
        return word + " is not found on Merriam Webster Dictionary."
    else:
        stems = [] #lists all of the entry's headwords, variants, inflections, undefined entry words, and defined run-on phrases. Each stem string is a valid search term that should match this entry.
        shortDefinitionResults = []
        
        loopMax = 0
        if len(dictionaryResult) > 3:
            loopMax = 3
        else:
            loopMax = len(dictionaryResult)

        for i in range(loopMax):
            if 'meta' not in dictionaryResult[i]:
                return word + " is not found on Merriam Webster Dictionary."

            shortdefList = dictionaryResult[i].get('shortdef')
            for j in range(0, len(shortdefList)):
                shortDefinitionResults.append(shortdefList[j])
        return shortDefinitionResults

def mwlDict(word):
    if word == "":
        return " is not found on Merriam Webster Learner's Dictionary."

    apiKey  = "c0fe6dc9-3217-4825-b6ad-fac424c7d7b3"
    wordURL = "https://dictionaryapi.com/api/v3/references/learners/json/"+ word + "?key=" + apiKey
    result = requests.get(wordURL)
    dictionaryResult = result.json()
    
    if dictionaryResult == {}:
        return word + " is not found on Merriam Webster Learner's Dictionary."
    else:
        stems = [] #lists all of the entry's headwords, variants, inflections, undefined entry words, and defined run-on phrases. Each stem string is a valid search term that should match this entry.
        shortDefinitionResults = []
        
        loopMax = 0
        if len(dictionaryResult) > 3:
            loopMax = 3
        else:
            loopMax = len(dictionaryResult)

        for i in range(loopMax):
            if 'meta' not in dictionaryResult[i]:
                return word + " is not found on Merriam Webster Learner's Dictionary."
        
            shortdefList = dictionaryResult[i].get('shortdef')
            for j in range(0, len(shortdefList)):
                shortDefinitionResults.append(shortdefList[j])
        return shortDefinitionResults

def oxfordDict(word):
    if word == "":
        return " is not found in Oxford English Dictionary.", "No example found in Oxford English Dictionary.", "Not found", "Not found", "Not found"
    
    appID  = "501e439d"
    appKey  = "f7bd8a4c25db428d6b1f972d3acc85d7"
    endPoint = "entries"
    languageCode = "en-us"
    wordURL = "https://od-api.oxforddictionaries.com/api/v2/" + endPoint + "/" + languageCode + "/" + word.lower()
    result = requests.get(wordURL, headers = {"app_ID": appID, "app_Key": appKey})
    dictionaryResult = result.json()
    
    if dictionaryResult == {}:
        return word + " is not found in Oxford English Dictionary.", "No example found in Oxford English Dictionary.", "Not found", "Not found", "Not found"
    else:
        if "results" not in dictionaryResult:
            return word + " is not found in Oxford English Dictionary.", "No example found in Oxford English Dictionary.", "Not found", "Not found", "Not found"
        
        realResultList = dictionaryResult["results"]
        realResultDict = realResultList[0]
        resultInfoList = realResultDict["lexicalEntries"]
        resultInfoDict = resultInfoList[0]
        resultDataList = resultInfoDict["entries"]
        resultDataDict = resultDataList[0]
        
        partOfSpeech = "Not found"
        if "lexicalCategory" in resultInfoDict:
            wordCategoryList = resultInfoDict["lexicalCategory"]
            if len(wordCategoryList) != 0:
                partOfSpeech = wordCategoryList.get("text")

        wordPhoneticSpelling  = "Not found"
        audioFile = "Not found"
        if "pronunciations" in resultDataDict:
            wordPronunciationsList = resultDataDict["pronunciations"]
            if len(wordPronunciationsList) != 0:
                wordPronunciationsDict = wordPronunciationsList[0]
                wordPhoneticSpelling = wordPronunciationsDict.get("phoneticSpelling")
                if len(wordPronunciationsList) >= 1:
                    audioFile = wordPronunciationsList[1].get("audioFile")

        wordSensesList = resultDataDict["senses"]
        wordResult = {}
        for dict in wordSensesList:
            for list in dict:
                if list in wordResult:
                    wordResult[list] += (dict[list])
                else:
                    wordResult[list] = dict[list]

        outputDefinitions = []
        definitionList = wordResult.get("definitions")
        if definitionList == None:
            outputDefinitions.append(word + " is not found in Oxford English Dictionary.")
        else:
            for i in range(0, len(definitionList)):
                outputDefinitions.append(definitionList[i])

        outputExamples = []
        exampleList = wordResult.get("examples")
        if exampleList == None:
            outputExamples.append("No example found.")
        else:
            for i in range(0, len(exampleList)):
                outputExamples.append(exampleList[i].get("text"))

        return outputDefinitions, outputExamples, partOfSpeech, wordPhoneticSpelling, audioFile

def etymonlineDict(word):
    baseURL = "https://www.etymonline.com/"
    queryURL = "search?q=" + word.replace(" ", "+")
    wordURL = baseURL + queryURL
    return wordURL

def wordnetDict(word):
    dictionary = PyDictionary()
    output = []
    
    if word == "":
        output.append(["The word, , is not found on Wordnet", "The word, , is not found on Wordnet"])
        return output

    results = dictionary.meaning(word)
    partOfSpeechList = []
    definitionList = []

    if results == None:
        output.append(["The word," +  word + ", is not found on WordNet.", "The word, " +  word + ", is not found on WordNet."])
    else:
        for result in results:
            partOfSpeechList.append(result)
            definitionList.append(results.get(result)[0])
        for i in range(len(definitionList)):
            output.append([partOfSpeechList[i], definitionList[i]]) 
            
    return output

def synonymDict(word):
    syn_output = None
    ant_output = None
    
    thesaurus = PyDictionary()
    
    if word == "":
        syn_output = ["There is no synonym found at synonym.com"]
        ant_output = ["There is no antonym found at synonym.com"]
        return syn_output, ant_output

    synonyms = thesaurus.synonym(word)
    if synonyms == None:
        syn_output = ["There is no synonym found at synonym.com"]
    else:
        syn_output = synonyms

    antonyms = thesaurus.antonym(word)
    if antonyms == None:
        ant_output = ["There is no antonym found at synonym.com"]
    else:
        ant_output = antonyms
    
    return syn_output, ant_output

def thefreedictionaryDict(word):
    baseURL = "http://www.thefreedictionary.com/"
    queryURL = word.replace(" ", "+")
    wordURL = baseURL + queryURL

    return wordURL

def urbanDict(word):
    if word == "":
        return "There is no definition founded in Urban Dictionary.", "There is no example founded in Urban Dictionary", "https://www.urbandictionary.com/"
    
    outputDefinitions = []
    outputExamples = []
    client = UrbanClient()
    definitions = client.get_definition(word)

    if definitions == None:
        outputDefinitions.append("There is no definition founded in Urban Dictionary.")
        outputExamples.appned("There is no example founded in Urban Dictionary")
    else:
        loopMax = 0
        if len(definitions) > 3:
            loopMax = 3
        else:
            loopMax = len(definitions)
            
        for i in range(0, loopMax):
            outputDefinitions.append(definitions[i].definition)
            outputExamples.append(definitions[i].example)
            
    outputLink = "https://www.urbandictionary.com/define.php?term=" + word

    return outputDefinitions, outputExamples, outputLink

def wikiDict(word):
    if word == "":
        return None, None, None
    
    wikiResult = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)
    wikiPage = wikiResult.page(word)
    
    existence = wikiPage.exists()
    
    if existence == True:
        outputTitle = wikiPage.title
        outputSummary = wikiPage.summary
        outputURL =  wikiPage.fullurl 
        
        return outputTitle, outputSummary, outputURL
    else:
        return None, None, None

def wiktionaryDict(word):
    if word == "":
        return " is not found in Wiktionary", " is not found in Wiktionary", " is not found in Wiktionary"
    
    jsonParser = WiktionaryParser()
    jsonResult = jsonParser.fetch(word)

    if jsonResult == []:
        return word + " is not found in Wiktionary", word + " is not found in Wiktionary", word + " is not found in Wiktionary"
    else:
        dictResult = jsonResult[0]
        definitionList = dictResult.get("definitions")
        if len(definitionList) == 0:
            return word + " is not found in Wiktionary", word + " is not found in Wiktionary", word + " is not found in Wiktionary"
        
        definitions = definitionList[0]
        textList = definitions.get("text")
        texts = textList[0]
        partOfSpeech = definitions.get("partOfSpeech")
        examples = definitions.get("examples")
        outputExamples = []
        
        loopMax = 0
        if len(examples) > 3:
            loopMax = 3
        else:
            loopMax = len(examples)
            
        for j in range(loopMax):
            outputExamples.append(examples[j])

        return texts, partOfSpeech, outputExamples

def googleNewsDict(word):
    output = []
    
    if word == "":
        return None

    googlenews = GoogleNews(lang='en')
    googlenews.get_news(word)
    result = googlenews.result()
    
    if result == None:
        return None
    
    loopMax = 0
    if len(result) > 10:
        loopMax = 10
    else:
        loopMax = len(result)
    
    for i in range(loopMax):
        res = result[i]
        link = "https://" + res['link']
        title = res['title']
        description = res['desc']
        image = res['img']
        siteName = res['site']
        if siteName == None:
            siteName = "Not applicable"
        output.append([title, link, description, image, siteName])

    return output

def googleImageDict(word):
    if word == "":
        return ["No such image found", "No such image found"]
    
    apiKey = "AIzaSyCB-M_Z2BlLfWgAMOuhLmNHHmoBoRCme50"
    searchEngineID = "4c4e5dd8e9cf81ff8"

    resource = build("customsearch", "v1", developerKey=apiKey).cse()
    results = resource.list(q=word, cx=searchEngineID, searchType='image').execute()

    resultURL = results.get('url').get('template')
    imageDataSet = results.get('items')
    
    if imageDataSet == None:
        return ["No such image found", "No such image found"]
    elif imageDataSet == []:
        return ["No such image found", "No such image found"]
    else:
        outputList = []
    
        loopMax = 0
        if len(imageDataSet) > 10:
            loopMax = 10
        else:
            loopMax = len(imageDataSet)

        for i in range(loopMax):
            image = imageDataSet[i].get('image')
            link = imageDataSet[i].get('link')
            title = imageDataSet[i].get('title')
            contextLink = image.get('contextLink')
            
            outputList.append([link, title, contextLink])
           
        return outputList

def youtubeDict(word):
    if word == "":
        return ["No results found in YouTube."]
    
    output = []
    videosSearch = VideosSearch(word)
    results = videosSearch.result()
    
    if results == None:
        return ["No results found in YouTube."]

    resultList = results['result']
    if resultList == None:
        return ["No results found in YouTube."]
    elif len(resultList) == 0:
        return ["No results found in YouTube."]

    titles = [sub['title'] for sub in resultList]
    links = [sub['link'] for sub in resultList]
    # embedLinks =["https://" + link.replace('watch?v=', 'embed/') for link in links]

    loopMax = 0
    if len(resultList) > 15:
        loopMax = 15
    else:
        loopMax = len(resultList)

    for i in range(loopMax):
        output.append([titles[i], links[i]])
    
    return output

def wordnik(word):
    if word != "":
        baseURL = "https://www.wordnik.com/words/"
        queryURL = word.replace(" ", "%20")
        wordURL = baseURL + queryURL
        return wordURL
    else:
        return "https://www.wordnik.com/"

def yourdictionary(word):
    if word != "":
        baseURL = "https://www.yourdictionary.com/search/"
        queryURL = word.replace(" ", "%20")
        wordURL = baseURL + queryURL
        return wordURL
    else:
        return "https://www.yourdictionary.com"
    
def visuwords(word):
    baseURL = "https://visuwords.com/"
    queryURL = word.replace(" ", "%20")
    wordURL = baseURL + queryURL
    return wordURL