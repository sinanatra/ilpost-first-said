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
from utils.telegramBot import updateStatus
import asyncio
from datetime import datetime

# localhost
# from dotenv import load_dotenv
# load_dotenv()
# localhost

# Connects to the Mongo instance
client = pymongo.MongoClient(os.environ['MONGO'])

db = client.ilpost
words = db.words

# Parses newspaper's feed
opener = urllib.request.build_opener()
tree = ET.parse(opener.open('https://www.ilpost.it/feed')) # https://rss.draghetti.it/ilpost.xml alternative

for item in tree.findall('channel/item'):
    try:
        title = item.find('title')
        link = item.find('link')
        date = item.find('pubDate')
        pub_date = datetime.strptime(date.text, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%dT%H:%M:%S.%f%z')
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
        title = title.text
        # get  and cleans the text
        #text = innerSoup.find('div', {'class':'entry-container-main'}).get_text(separator=" ")
        text = innerSoup.find('article').get_text(separator=" ")
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip()
                    for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        # get tokens - ignore punctuation and capital letters
        tokenizer = RegexpTokenizer(r'(?<![@#])\b\w+\b')
        tokens = tokenizer.tokenize(text)
        # remove duplicates
        tokens = list(set(tokens))
        
        # Check if exists in db
        database_tokens = list(words.find({ "word": { "$in": tokens}} ))
        
        # Check differences with tokens
        cleaned_tokens = []

        for item in database_tokens:
            word = ''
            word = word.join(item['word'])
            cleaned_tokens.append(word)

        different_tokens = list(set(tokens) - set(cleaned_tokens))
        
        for token in different_tokens:
            if any(str.isdigit(c) or str.isupper(c) for c in token) or len(token) <= 3:
                continue
            else:
                print('new token!', token)
   
                #Defines text snippet
                range_snippet = 50
                start_index = text.find(token)
                end_index = start_index + len(token) 
                snippet = ''

                for i in range(start_index - range_snippet, end_index + range_snippet):
                    snippet += text[i]   
                finalsnippet = ' '.join(snippet.split()[1:-1])
                
                #Adds word to Mongo
                #x = words.insert_one({ "word": token })
                #x = words.update_one({'word': token},{'$set': {'word': token}}, upsert=True)

                x = words.update_one(
                    {'word': token},
                    {
                        '$set': {
                            'word': token,
                            'context': finalsnippet,
                            'url': link.text,
                             'date_added': pub_date #datetime.now() 
                        }
                    },
                    upsert=True
                )

                # tweets w
                loop = asyncio.get_event_loop()
                loop.run_until_complete(updateStatus(token, link.text, title, finalsnippet))
                time.sleep(5)
    except Exception as e:
        print(e)
