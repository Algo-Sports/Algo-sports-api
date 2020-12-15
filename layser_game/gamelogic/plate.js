const flatten = require("@flatten-js/core");
const collide = require("./collide.js");

class Plate extends collide{
    constructor(x,y,width,height,angle){
        super();
        this.point = new flatten.Point(x,y);
        let upleftpoint = new flatten.Point(x-width/2, y-height/2);
        let uprightpoint = new flatten.Point(x+width/2, y-height/2);
        let downrightpoint = new flatten.Point(x+width/2, y+height/2);
        let downleftpoint = new flatten.Point(x-width/2, y+height/2);
        this.points = [upleftpoint, uprightpoint,downrightpoint, downleftpoint];
        this.angle = (Math.PI*2)*angle/360;
        for(let i = 0;i<this.points.length;i++){
            this.points[i] = this.points[i].rotate(this.angle,this.point);
        }
        let upsegment = new flatten.Segment(this.points[0], this.points[1]);
        let downsegment = new flatten.Segment(this.points[3], this.points[2]);
        let leftsegment = new flatten.Segment(this.points[0], this.points[3]);
        let rightsegment = new flatten.Segment(this.points[1], this.points[2]);
        this.segments = [upsegment, downsegment, leftsegment, rightsegment];
        this.normalvectors = [new flatten.Vector(this.points[3],this.points[0])
            , new flatten.Vector(this.points[0],this.points[3])
            , new flatten.Vector(this.points[1],this.points[0])
            , new flatten.Vector(this.points[0],this.points[1])]
    }

}

module.exports = Plate;
