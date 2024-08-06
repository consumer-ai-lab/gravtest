const router = require("express").Router();
const Admin = require("../models/admin");
var bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { tokenVerifier } = require('./tokenUtils');

router.post("/registerAdmin", async (req, res) => {
    try {
        const newOperator = new Admin(req.body);
        const hashedPassword = await bcrypt.hash(newOperator.password, 12);
        newOperator.password = hashedPassword;
        const operator = await newOperator.save();
        res.status(200).json(newOperator);
    } catch (err) {
        console.log("error", err);
        res.status(500).json(err);
    }
});


router.post("/loginAdmin", async (req, res) => {
    try {
        console.log("HI")
        console.log(req.body)
        const { userName, password } = req.body;
        console.log(userName)
        try {
            const user = await Admin.findOne({ userName });
            const comparePass = await bcrypt.compare(password, user.password);
            if (comparePass === true) {

                const token = await jwt.sign(
                    { userName: userName }
                    , 'token',
                    {
                        expiresIn: "2d",
                    }
                );
                //process.env.TOKEN_KEY            
                user.token.push(token);
                await user.save();
                res.status(200).json({ 'status': 'verified', 'token': token });
            }
            else {
                res.status(200).json({ 'status': 'not_verified' });
            }
        }
        catch (err) {
            res.status(500).json({})
        }


    } catch (err) {
        console.log("error", err);
        res.status(500).json(err);
    }
});


router.post("/logoutAdmin", async (req, res) => {
    try {
        console.log("/logoutAdmin", req.body);
        const { userName, token } = req.body;
        const user = await Admin.findOne({ userName });
        console.log(user);

        if (user) {
            user.token = user.token.filter(e => e !== token);
            user.save();
            res.status(200).json({ 'status': 'logged out', 'token': token });
        }
        else {
            res.status(200).json({ 'status': 'not logged out' });
        }

    } catch (err) {
        console.log("error", err);
        res.status(500).json(err);
    }
});

router.post("/authenticateAdmin", async (req, res) => {
    try {
        console.log("token: ", req.headers.token)
        const decoded = await tokenVerifier(req.headers.token);
        console.log("decoded: ", decoded)
        if (decoded)
            res.status(200).json({ 'status': 'verified', 'userName': decoded.userName });
        else
            res.status(200).json({ 'status': 'not verified' });
    } catch (err) {
        console.log("error", err);
        res.status(500).json(err);
    }
});

module.exports = router;