const flatten = require("@flatten-js/core")

class Ball {
    constructor(x, y, radius) {
        this.ball = new flatten.Arc(new flatten.Point(x, y), radius, 0, Math.PI*2,true);
    }
}

module.exports = Ball
