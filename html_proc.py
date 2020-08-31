import os
import glob
import json
import time
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from datetime import datetime
from utils.tweet import updateStatus

date = datetime.today().strftime('%Y-%m-%d')
#dateParser = datetime.today().strftime('%Y/%m/%d')

# this is the main dictionary
with open('./dictionary.json', 'r') as file:
    data = file.read()

dictionary = json.loads(data)

#  save array to be visualised later
database = open('./database/' + date + '.tsv', 'w')
database.write('page' + '\t' + 'tokens' + '\t' + 'newtokens' + '\n')

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

            # get  and cleans the text
            text = innerSoup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip()
                      for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            # get tokens - ignore punctuation and capital letters
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(text)
            # remove duplicates
            tokens = list(set(tokens))
            database.write(str(a_tag['href']) + '\t' + str(tokens))

            for token in tokens:
                if dictionary.get(token) is None:
                    if str(token).istitle() or str(token).isupper() or str(token).isdigit():
                        continue
                    else:
                        print('new token!', token)
                        database.write(str(token) + ', ')
                        dictionary[token] = token       

                        # tweets stuff
                        updateStatus(token, a_tag['href'])
                        time.sleep(1)
            
            database.write('\n')

        except Exception as e:
            print(e)

database.close()

output = open("./dictionary.json", 'w')
json.dump(dictionary, output)
output.close()
