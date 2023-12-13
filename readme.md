![Screenshot 2023-12-13 at 11 12 17](https://github.com/sinanatra/ilpost-first-said/assets/20107875/85706397-c821-4705-bfae-cb4d8d882a18)

# [@ilPostDice](https://twitter.com/ilpostdice)

A script that tracks when the newspaper IlPost publishes a word for the first time.  
Running at: [@ilPostDice](https://t.me/nuoveparoledelpost). Largely inspired by the work of [Max Bittker](https://www.nytimes.com/2019/07/07/reader-center/nyt-first-said-words-twitter-bot.html).

## Scraper:
### Basic architecture
----------

Il Post first said is essentially a single script which runs every two hours as a cron job on Github.

`html_proc.py` parses an xml document. In this case `https://rss.draghetti.it/ilpost.xml` ( originally `https://www.ilpost.it/feed/`, but it appears to be sometimes unreliable).
It opens the url of each new article, retrieves the text of the article, tokenizes each word and can: tweet the new words using `utils/tweet.py` or add them to telegram via: `utils/telegramBot.py`.   
Each new word, its context, date and link are saved in a Mongo DB instance. For example:
```
{
  _id: 6579651f1a28f773943e8448
  word:"stsso"
  context
  "dei combustibili fossili, come ha detto lo stsso al Jaber. Al tempo stesso, però"
  date_added:"2023-12-13T06:00:04.000000+0000"
  url:"https://www.ilpost.it/2023/12/13/nuova-bozza-cop28/"
}
```


### Requisites
----------

Install PIP requirements with `pip install -r requirements.txt`.

### Start
-----

Run `html_proc.py` to launch the script.

# Visualization:


On the `visualization` branch a Sveltekit app visualizes the data over a timeline.

## Setup
Install dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version:

```bash
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.
