const randomInt = (limit) => {
    return Math.floor(Math.random() * limit);
}


module.exports.ball = (color, radius, strokecolor, strokesize) => {
    return {
        color: color,
        radius: radius,
        strokecolor: strokecolor,
        strokesize: strokesize
    }
}

module.exports.laser = (x,y,vectorx,vectory,color) => {
    return {
        x : x,
        y : y,
        vector : {x : vectorx, y : vectory},
        color: color
    }
}

module.exports.plate = (color, width, height) => {
    return {
        color: color,
        width: width,
        height: height
    }
}

module.exports.wave = (color, speed, nums, startpoint, pinspeed) => {
    return {
        color: color,
        speed: speed,
        nums: nums,
        startpoint: startpoint,
        pinspeed: pinspeed
    }
}

module.exports.gameinfo = (canvas, ball, laser, plate, wave, lapnum) => {
    let ret = {};
    let balloons = [];
    for (let i = 0; i < ball.num; i++) {
        balloons.push([randomInt(canvas.width), randomInt(canvas.height)]);
    }

    ret.info = {};
    ret.info.canvas = canvas;
    ret.info.ball = ball;
    ret.info.laser = laser;
    ret.info.plate = plate;
    ret.info.wave = wave;
    ret.info.maxlap = lapnum;
    ret.ball = balloons;

    return ret;
}
