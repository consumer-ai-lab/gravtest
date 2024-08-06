// Utility File for creating the tokens for login and logout
const Admin = require("../models/admin");
const User = require("../models/User");
const jwt = require('jsonwebtoken');
const dotenv = require("dotenv");
dotenv.config();

const tokenVerifier = async (token) => {
    const tokenKey = 'token';
    try{
        const decoded = jwt.verify(token, tokenKey);
        const operator = await Admin.findOne({userName: decoded.userName});
        if(operator && operator.token.includes(token)){
            return(decoded);
        }
        return(null);
    }
    catch{
        return(null);
    }
}

const applicationTokenVerifier = async (token) => {
    const tokenKey = 'token';
    try{
        const decoded = jwt.verify(token, tokenKey);
        //console.log('decoded -> ', decoded)
        const user = await User.findOne({username: decoded.username});
        if(user){
            return(decoded);
        }
        return(null);
    }
    catch(err){
        //console.log(err);
        return(null);
    }
}

const apiKeyVerifier = async (apikey) => {
    try{
        const backend_api_secret = process.env.BACKEND_API_SECRET;
        console.log("apikey = ", apikey);
        console.log("api_sec = ", backend_api_secret)
        if(apikey === backend_api_secret)
            return(true);
        else
            return(false);
    }
    catch(err){
        return(false);
    }    
}

const validRequestVerifier = async(token, apikey) => {
    try{
        console.log("validRequestVerifier: called");
        //return(true);
        const decoded = await applicationTokenVerifier(token);
        console.log("validRequestVerifier: decoded: ", decoded);
        const apiKeyResult = await apiKeyVerifier(apikey);
        console.log("validRequestVerifier: apiKeyResult", apiKeyResult);
        if(decoded && apiKeyResult)
            return(true);
        return(false);
    }    
    catch(err){
        console.log("validRequestVerifier: ", err);
        return(false);
    }
}

module.exports = {
    tokenVerifier: tokenVerifier,
    applicationTokenVerifier: applicationTokenVerifier,
    apiKeyVerifier: apiKeyVerifier,
    validRequestVerifier: validRequestVerifier
};