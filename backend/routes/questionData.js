// Routes to handle upload and fetch of question data

// importing all the required libraries
const router = require("express").Router();
const Question = require("../models/question");
const multer = require("multer");
const fs = require('fs');
const path = require('path');
const { google } = require('googleapis')
const dotenv = require("dotenv");
dotenv.config();

// A Get Api to fetch all data based on the password of a particular batch
router.get('/', async (req, res) => {
  const { pass, key } = req.query
  // const pass= req.query.pass
  try {
    if (key === process.env.BACKEND_API_SECRET) {
      const data = await Question.find({ testPassword: pass })
      res.status(200).json(data)
    }
    else {
      res.status(500).json({})
    }

  }
  catch (error) {
    res.status(500).json(error)
  }
})


module.exports = router;