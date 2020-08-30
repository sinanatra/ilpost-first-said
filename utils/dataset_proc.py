import os 
import glob
import json
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

dataset = "../scraped/"
dictionary = {}

for file in glob.iglob(dataset+'**/*.html', recursive=True):
    print(file)
    html = open(file, 'r', encoding="utf-8")
    soup = BeautifulSoup(html)

    # ignore all scripts and css
    for script in soup(["script", "style"]):
        script.extract()

    # get  and cleans the text
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # get article as tokepythonns - ignore punctuation and capital letters
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)

    for token in tokens:
        if token.istitle():
            continue
        else:
            dictionary[token] = token;

output = open("../dictionary.json", 'w')
json.dump(dictionary, output)
output.close()