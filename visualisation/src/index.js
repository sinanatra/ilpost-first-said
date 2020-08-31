import './main.css'
const d3 = require('d3')
const forceGravity = require('d3-force-gravity')

function loadData() {
    return d3.tsv('src/assets/database/2020-08-31.tsv');
}


(async () => {
    let dataset = await loadData();

    for (let i in dataset) {
        let line = dataset[i];

        let url = line.page
        let words = line.tokens.replace(/'/g, '').replace(/]/g, '').replace(/\[/g, '').split(",")

        let newtoken = line.newtokens

        console.log(url);

        words.forEach(element => {
            d3.select('.canvas')
                .append('div')
                .text(element);
        });
  

        break
    }
})();