const flatten = require("@flatten-js/core")
const collide = require("./collide.js");

class Wall extends collide{
    constructor(cwidth,cheight){
        super();
        this.segments = [new flatten.Segment(new flatten.Point(), new flatten.Point(0,cheight))
            , new flatten.Segment(new flatten.Point(),new flatten.Point(cwidth,0))
            , new flatten.Segment(new flatten.Point(0,cheight), new flatten.Point(cwidth,cheight))
            , new flatten.Segment(new flatten.Point(cwidth,0), new flatten.Point(cwidth,cheight))]
    }
}

module.exports = Wall;
