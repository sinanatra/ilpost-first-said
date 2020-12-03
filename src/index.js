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
    return d3.json('https://spreadsheets.google.com/feeds/list/1TydqXkPrlhnETTwzsNeRLBTpi0rCCDxTFRuWcPMfwgU/od6/public/values?alt=json');
}

(async () => {
    let dataset = await loadData();
    dataset = dataset.feed.entry.reverse()

    let line;

    function parseLine(value) {
        line = dataset[value];
    }

    let linenum = 0
    parseLine(linenum)
    drawBoxes()



    function drawBoxes() {
        let info = d3.select('.info').append('div').attr('class', 'info-elem')

        for (let i = 0; i < dataset.length; i++) {

            setTimeout(function () {

                let word = dataset[i].gsx$words.$t;

                d3.selectAll('.word').remove();

                info.append('h2')
                    .attr('class', 'word')
                    .text('Parola ' + (i + 1) + ' di ' + dataset.length)

                let element = d3.select('.canvas')
                    .append('div')
                    .attr('class', 'block')
                    .text(word);

                let randompos = Math.floor(Math.random() * VIEW.width) + 1
                renderEngine(element, randompos)

                if (i == dataset.length - 1 ) {

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
