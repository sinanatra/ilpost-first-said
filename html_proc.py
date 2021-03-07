import os
import glob
import json
import time
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from pathlib import Path
import pymongo
import lxml.etree as ET    
from utils.tweet import updateStatus

# Connects to the Mongo instance
client = pymongo.MongoClient(os.environ['MONGO'])
db = client.ilpost
words = db.words

# Parses newspaper's feed
opener = urllib.request.build_opener()
tree = ET.parse(opener.open('https://www.ilpost.it/feed/'))

for link in tree.findall('channel/item/link'):
    print('href: ', link.text)
    try:
        innerHtml = urllib.request.urlopen(link.text).read()
        innerSoup = BeautifulSoup(innerHtml, features="lxml")
        # ignore all scripts and css
        for script in innerSoup(["script", "style"]):
            script.extract()
        #ignore iframes
        for div in innerSoup.find_all("blockquote", {'class':'twitter-tweet'}): 
            div.decompose()
        for div in innerSoup.find_all("blockquote", {'class':'instagram-media'}):
            div.decompose()
        #ignore tags
        for div in innerSoup.find_all("a", {'rel':'tag'}):
            div.decompose()

        #get title
        title = innerSoup.find("h1", {'class':'entry-title'}).get_text()
        # get  and cleans the text
        text = innerSoup.find('article').get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip()
                    for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        # get tokens - ignore punctuation and capital letters
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        # remove duplicates
        tokens = list(set(tokens))
        
        # Check if exists in db
        database_tokens = list(words.find({ "word": { "$in": tokens}} ))
        
        # Check differences with tokens
        cleaned_tokens = []

        for item in database_tokens:
            word = item['word'][0]
            cleaned_tokens.append(word)

        different_tokens = list(set(tokens) - set(cleaned_tokens))
        for token in different_tokens:
            if any(str.isdigit(c) or str.isupper(c) for c in token) is True:
                continue
            else:
                print('new token!', token)

                #Adds word to Mongo
                x = words.insert_one({ "word": token })

                #Defines text snippet
                range_snippet = 50
                start_index = text.find(token)
                end_index = start_index + len(token) 
                snippet = ''

                for i in range(start_index - range_snippet, end_index + range_snippet):
                    snippet += text[i]   
                finalsnippet = ' '.join(snippet.split()[1:-1])+ ' ...'
                
                # tweets word, snippet and link
                updateStatus(token, link.text, title, finalsnippet)
                time.sleep(5)
    except Exception as e:
        print(e)
