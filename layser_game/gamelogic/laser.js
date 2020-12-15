const flatten = require("@flatten-js/core");

class Laser{
    constructor(x,y,v){
        this.point = new flatten.Point(x,y);
        this.v = v.normalize(); // ray's vector is orthogonal
        this.ray = new flatten.Ray(this.point, this.v);
        this.vector = new flatten.Vector(this.v.y, -this.v.x); // ray goes this.vector
    }

    getVector(){
        return this.vector;
    }

    static getvfromVector(Vector){
        return new flatten.Vector(-Vector.y,Vector.x);
    }
}

module.exports = Laser;
