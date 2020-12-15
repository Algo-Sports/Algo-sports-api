const fs = require("fs");
const process = require("process")
const jsonGenerator = require("./jsonGenerator.js");

let gamesetting = {};

gamesetting = JSON.parse(fs.readFileSync(`${process.cwd()}/layser_game/gamesetting.json`));
let gameinfo = jsonGenerator.gameinfo(gamesetting.canvas, gamesetting.ball, gamesetting.laser, gamesetting.plate, gamesetting.wave, gamesetting.maxlap);

console.log(JSON.stringify(gameinfo));
