const getRandomInt = (max = 500) => {
    return Math.floor(Math.random() * max);
}

const generate_record_ID = (requestParams, ctx, ee, next) => {
    ctx.vars["ID"] = getRandomInt()

    return next();
}

module.exports = {
    generate_record_ID,
};
