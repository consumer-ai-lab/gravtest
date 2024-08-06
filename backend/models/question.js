// Question Model to upload and fetch question
const mongoose = require("mongoose");

const questionSchema = new mongoose.Schema(
  {
    fileType:{
      type:String
    },
    timeSlot: {
      type: String,
    },
    testPassword:{
      type:String,
      required:true
    },
    driveId:{
      type:String
    },
  },
  { timestamps: true }
);
module.exports = mongoose.model("Question", questionSchema);
