const process = require("process");
const flatten = require("@flatten-js/core");
const fs = require("fs");
const Ball = require("./ball.js");
const Plate = require("./plate.js");
const Wall = require("./wall.js");
const Laser = require("./laser.js");


// gameinfo, usrresult 는 인자값으로 들어올것이다.
if (process.argv.length < 5) {
    return;
}

const gameinfo = require(`${process.cwd()}/${process.argv[2]}`);
const usrresults = require(`${process.cwd()}/${process.argv[3]}`);
const lap = parseInt(process.argv[4] - 1);
const usrresult = usrresults[lap];

// usrresult 더미데이터
let balls = []
let plates = []
let walls = new Wall(gameinfo.info.canvas.width, gameinfo.info.canvas.height);
let ps = new flatten.Point(gameinfo.info.laser.x, gameinfo.info.laser.y);
let laser = new Laser(ps.x, ps.y, Laser.getvfromVector(new flatten.Vector(gameinfo.info.laser.vector.x, gameinfo.info.laser.vector.y)));

for (let i = 0; i < gameinfo.info.ball.num; i++) {
    balls[i] = new Ball(gameinfo.ball[i][0], gameinfo.ball[i][1], gameinfo.info.ball.radius);
}
for (let i = 0; i < usrresult.plate.length; i++) {
    plates[i] = new Plate(usrresult.plate[i].x, usrresult.plate[i].y, gameinfo.info.plate.width, gameinfo.info.plate.height, usrresult.plate[i].angle);
}

let result = {};
result.hit_point = [];

let cnt = 0;
let flag = true;
let wallhit;
let hitplate = -1;
while (flag) {
    flag = false;
    wallhit = walls.isCollide(laser);
    let collide = wallhit;
    for (let i = 0; i < plates.length; i++) {
        if (i == hitplate) continue;
        let tmp = plates[i].isCollide(laser);
        if (tmp[0] <= collide[0]) {
            flag = true;
            collide = tmp;
            hitplate = i;
        }
    }
    if (flag) {
        result.hit_point[cnt++] = { x: collide[1].x, y: collide[1].y };
        // let platevector = new flatten.Vector(collide[2].ps, collide[2].pe);
        // let v1 = new flatten.Vector(platevector.y, -platevector.x);
        // let v2 = new flatten.Vector(-platevector.y,platevector.x);
        // v1 = laser.point.distanceTo(collide[1].clone().translate(v1)) < laser.point.distanceTo(collide[1].clone().translate(v2)) ? v1.normalize() : v2.normalize();

        let v1 = collide[2].normalize();
        v1 = laser.getVector().add(v1.multiply(2 * laser.getVector().invert().dot(v1)));
        laser = new Laser(collide[1].x, collide[1].y, Laser.getvfromVector(v1));
    }
}
result.hit_point[cnt++] = { x: wallhit[1].x, y: wallhit[1].y };
// result.hit_ball = [];

let ballset = new Set();
let pe;
for (let p of result.hit_point) {
    pe = new flatten.Point(p.x, p.y);
    let segment = new flatten.Segment(ps, pe);
    for (let i = 0; i < balls.length; i++) {
        let tmp = balls[i].ball.intersect(segment);
        if (tmp.length > 0) {
            ballset.add(i);
        }
    }
    ps = pe;
}
result.hit_ball = [...ballset];



console.log(JSON.stringify(result));
