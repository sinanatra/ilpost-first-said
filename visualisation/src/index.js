import './main.css'
const d3 = require('d3')
const Matter = require('matter-js');

const date = new Date()
const options = { year: 'numeric', month: 'long', day: 'numeric' };
const parseDate = date.toISOString().split('T')[0];

const VIEW = {};
VIEW.SAFE_WIDTH = 20;
VIEW.SAFE_HEIGHT = 100;
VIEW.scale = Math.min(window.innerWidth / VIEW.SAFE_WIDTH, window.innerHeight / VIEW.SAFE_HEIGHT);
VIEW.width = window.innerWidth / VIEW.scale;
VIEW.height = window.innerHeight / VIEW.scale;
VIEW.centerX = VIEW.width / 2;
VIEW.centerY = VIEW.height / 2;
VIEW.offsetX = (VIEW.width - VIEW.SAFE_WIDTH) / 2 / VIEW.scale;
VIEW.offsetY = (VIEW.height - VIEW.SAFE_HEIGHT) / 2 / VIEW.scale;

const Engine = Matter.Engine,
    World = Matter.World,
    Bodies = Matter.Bodies;

const engine = Engine.create({
    positionIterations: 10,
    velocityIterations: 10,
    constraintIterations: 50
});

const ground = Bodies.rectangle(10, 350, 400, 500, {
    isStatic: true
});

World.add(engine.world, [ground]);
Engine.run(engine);

function loadData() {
    return d3.tsv('../../database/' + parseDate + '.tsv');
    //return d3.tsv('src/assets/database/'+parseDate+'.tsv');

}

(async () => {

    let dataset = await loadData();
    shuffle(dataset)

    let line, url, words, newtoken

    function parseLine(value) {
        line = dataset[value];
        url = line.page
        words = line.tokens.replace(/'/g, '').replace(/]/g, '').replace(/\[/g, '').split(",")
        newtoken = line.newtokens
        console.log(newtoken)
    }

    let linenum = 0
    parseLine(linenum)
    drawBoxes()



    function drawBoxes() {
        let info = d3.select('.info').append('div').attr('class', 'info-elem')

        info.append('a')
            .text(url)
            .attr("xlink:href", url)


        info.append('h1')
            .text(date.toLocaleDateString('it-IT', options))

        info.append('h2')
            .text('Articolo ' + (linenum + 1) + ' di ' + dataset.length)

        for (let i = 0; i < words.length; i++) {
            setTimeout(function () {

                let word = words[i];
                d3.selectAll('.word').remove();

                info.append('p')
                    .attr('class', 'word')
                    .text('Parola ' + (i + 1) + ' di ' + words.length)

                let element = d3.select('.canvas')
                    .append('div')
                    .attr('class', 'block')
                    .text(word);

                if (newtoken.includes(word.replace(' ', ''))) {
                    element.attr('id', 'highlight')
                }

                let randompos = Math.floor(Math.random() * VIEW.width) + 1
                renderEngine(element, randompos)

                if (i == words.length - 1 || i == 400) {

                    d3.select('.info-elem').remove()
                    d3.selectAll('.block').remove()

                    // reset world
                    World.clear(engine.world);
                    World.add(engine.world, [ground]);

                    linenum++;
                    parseLine(linenum)
                    drawBoxes()
                }

            }, i * 800);
        }
    }

})();


function renderEngine(element, pos) {
    element = element._groups[0][0]

    let body = Bodies.rectangle(
        pos,
        0,
        VIEW.width * element.offsetWidth / window.innerWidth,
        VIEW.height * element.offsetHeight / window.innerHeight, {
        friction: 1,
        frictionStatic: 1,
        density: 0.02,
        restitution: 0,
        torque: 0.0002
    }
    );


    World.add(engine.world, body);

    window.requestAnimationFrame(update);
    function update() {
        element.style.transform = ''
        element.style.transform = "translate( "
            + ((VIEW.offsetX + body.position.x) * VIEW.scale - element.offsetWidth / 2)
            + "px, "
            + (VIEW.offsetY * 2 + (body.position.y) * VIEW.scale - element.offsetHeight / 2)
            + "px )";
        element.style.transform += "rotate( " + body.angle + "rad )";
        window.requestAnimationFrame(update);
    }

}

function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }

    return array;
}