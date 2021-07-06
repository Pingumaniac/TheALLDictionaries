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
    apiKey  = "c33d59f0-4576-4dfc-a389-918e5316421b"
    wordURL = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+ word + "?key=" + apiKey
    result = requests.get(wordURL)
    dictionaryResult = result.json()
    return json.dumps(dictionaryResult)

def mwlDict(word):
    apiKey  = "c0fe6dc9-3217-4825-b6ad-fac424c7d7b3"
    wordURL = "https://dictionaryapi.com/api/v3/references/learners/json/"+ word + "?key=" + apiKey
    result = requests.get(wordURL)
    dictionaryResult = result.json()
    return json.dumps(dictionaryResult)

def oxfordDict(word):
    appID  = "501e439d"
    appKey  = "f7bd8a4c25db428d6b1f972d3acc85d7"
    endPoint = "entries"
    languageCode = "en-us"
    wordURL = "https://od-api.oxforddictionaries.com/api/v2/" + endPoint + "/" + languageCode + "/" + word.lower()
    result = requests.get(wordURL, headers = {"app_ID": appID, "app_Key": appKey})
    dictionaryResult = result.json()
    return json.dumps(dictionaryResult)

def urbanDict(word):
    client = UrbanClient()
    definitions = client.get_definition(word)
    dictOutput = []
    for definition in definitions:
        dictOutput.append(definition.__dict__)
    return json.dumps(dictOutput)

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
        syn_output = ["No synonym found at synonym.com"]
        ant_output = ["No antonym found at synonym.com"]
        return syn_output, ant_output

    synonyms = thesaurus.synonym(word)
    if synonyms == None:
        syn_output = ["No synonym found at synonym.com"]
    else:
        syn_output = synonyms

    antonyms = thesaurus.antonym(word)
    if antonyms == None:
        ant_output = ["No antonym found at synonym.com"]
    else:
        ant_output = antonyms
    
    return syn_output, ant_output

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