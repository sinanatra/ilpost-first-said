
Requisites
----------

Install PIP requirements with `pip install -r requirements.txt`.


Start
-----

To start from scratch, download ilPost (or another newspaper website) with wget: `wget --limit-rate=200k --follow-tags=a --no-clobber --convert-links --random-wait -r -E -e robots=off -U "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36" -A html --domain=www.ilpost.it/ https://www.ilpost.it/` into the scraped directory, then lauch `dataset_proc.py` to create the dictonary. 

Run `html_proc.py` to launch the script.
