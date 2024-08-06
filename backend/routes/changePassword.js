const router = require("express").Router();
const Admin = require("../models/admin");
var bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const {tokenVerifier} = require('./tokenUtils');

router.patch("/", async (req, res) => {
    try {
        console.log(req.body)
        const data = await Admin.findOne({userName:req.body.userName})
        const comparePass = await bcrypt.compare(req.body.password,data.password);
        console.log(comparePass)
        if(comparePass === true){
            try{
                const hashedPassword = await bcrypt.hash(req.body.newPassword, 12);
                console.log(hashedPassword)
                data.password = hashedPassword;
                const response = await data.save()
                res.status(200).json("Password Reset Successfully")
            }
            catch(err){
                res.status(500).json(err)
            } 
        }
        else{
            res.status(500).json("error")
        }
    }
    catch (err) {
        console.log("error", err);
        res.status(500).json(err);
    }
});


module.exports = router;