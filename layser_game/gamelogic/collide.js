const flatten = require("@flatten-js/core");

class Collide{
    constructor(){
        this.segments = [];
        this.normalvectors = [];
    }

    isCollide(laser){
        let collide = new flatten.Point();
        let dist = Number.MAX_SAFE_INTEGER;
        // let segment = new flatten.Segment();
        let normalvector;
        for(let i = 0;i<this.segments.length;i++){
            let tmp = laser.ray.intersect(this.segments[i]);
            for(let c of tmp){
                let [d, shortest_segment] = laser.point.distanceTo(c);
                if(d < dist && d > 0.0000000000090000001){   // 충돌 threshold 0.000000000000000001.
                                                                // 0.000000000000000001미만의 거리는 충돌취급 X
                    dist = d;
                    collide = c;
                    // segment = this.segments[i];
                    normalvector = this.normalvectors[i];
                }
            }
        }
        // return [dist, collide, segment];
        return [dist, collide, normalvector];
    }
}

module.exports = Collide;
