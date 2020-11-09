import os
import glob
import json
import time
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from datetime import datetime
from pathlib import Path
from utils.tweet import updateStatus

import gspread
from google.oauth2.service_account import Credentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(os.environ['SHEET_JSON'], scopes=scope)

gc = gspread.authorize(credentials)
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1TydqXkPrlhnETTwzsNeRLBTpi0rCCDxTFRuWcPMfwgU/edit?usp=sharing')
worksheet_list = sh.worksheets()
sheet = worksheet_list[0]
sheetValues = sheet.get_all_values()

dictionary = {}

for i in sheetValues:
    dictionary[i[0]] = i[0]
    
date = datetime.today().strftime('%Y-%m-%d')
dateParser = datetime.today().strftime('%Y/%m/%d')


#  save array to be visualised later
file = Path('./database/' + date + '.tsv')
if file.is_file():
    database = open('./database/' + date + '.tsv', 'a')
else:
    database = open('./database/' + date + '.tsv', 'w')
    database.write('page' + '\t' + 'tokens' + '\t' + 'newtokens' + '\n')

checkLinks = open('./database/' + date + '.tsv').read()

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0'}

req = urllib.request.Request("https://www.ilpost.it", None, headers)
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, features="lxml")
previousUrl = ''

for a_tag in soup.find_all('a', href=True):
    if(str(a_tag['href']) not in previousUrl and 'www.ilpost.it' in a_tag['href']):
        print('href: ', a_tag['href'])
        previousUrl = str(a_tag['href'])
        try:
            innerHtml = urllib.request.urlopen(a_tag['href']).read()
            innerSoup = BeautifulSoup(innerHtml, features="lxml")

            # ignore all scripts and css
            for script in innerSoup(["script", "style"]):
                script.extract()
            
            #ignore iframes
            for div in innerSoup.find_all("blockquote", {'class':'twitter-tweet'}): 
                div.decompose()

            for div in innerSoup.find_all("blockquote", {'class':'instagram-media'}):
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
            
            if str(dateParser) in a_tag['href'] and str(a_tag['href']) not in checkLinks:
                database.write(str(a_tag['href']) + '\t' + str(tokens) + '\t' )
    
            
            for token in tokens:
                if dictionary.get(token) is None:
                    if any(str.isdigit(c) or str.isupper(c) for c in token) is True:
                        continue
                    else:
                        print('new token!', token)
                        if str(dateParser) in a_tag['href'] and str(a_tag['href']) not in checkLinks:
                            database.write(str(token) + ', ')
                            
                        # appends the data to the temporary dictionary and to the spreadsheet
                        dictionary[token] = token
                        sheet.append_row([token])

                        # tweets stuff
                        updateStatus(token, a_tag['href'],title)
                        time.sleep(5)
                        
            if str(dateParser) in a_tag['href'] and str(a_tag['href']) not in checkLinks:
                database.write('\n')

        except Exception as e:
            print(e)

database.close()
