const getRandomInt = (max = 500) => {
    return Math.floor(Math.random() * max);
}

let correct_usernames = [12721, 12722, 12737, 1245619, 1245614561, 1245961, 124561]
const generate_login = (requestParams, ctx, ee, next) => {
    ctx.vars["username"] = correct_usernames[getRandomInt(correct_usernames.length - 1)].toString()
    ctx.vars["test_password"] = "12345"
    ctx.vars["batch_password"] = "b1wcll1"

    return next();
}

module.exports = {
    generate_login,
};

