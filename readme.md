# [@ilPostDice](https://twitter.com/ilpostdice)

A twitter bot to track when the newspaper IlPost publishes a word for the first time in history. running at: [@ilPostDice](https://twitter.com/ilpostdice). Largely inspired by the work of Max Bittker.

It also replies to each tweet with a few words of source-text context, and a link to the original article.

Basic architecture
----------

Il Post first said is essentially a single script which runs every two hour as a cron job on Github.

`html_proc.py` parses the xml provided by the newspaper `https://www.ilpost.it/feed/`. It opens every new article url, retrieves the article text, tokenize every word and tweets new words using `utils/tweet.py`. It also append every new word to a Mongo DB instance.


Requisites
----------

Install PIP requirements with `pip install -r requirements.txt`.

Start
-----

Run `html_proc.py` to launch the script.
