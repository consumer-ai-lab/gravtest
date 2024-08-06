// User Model to register new user(candiate)
const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema(
  {
    name: {
      type: String,
    },
    username: {
      type: String,
      required: true,
    },
    user_password: {
      type: String,
      required: true,
    },
    start_time: {
      type: String,
    },
    elapsed_time: {
      type: Number,
    },
    submission_received: {
      type: Boolean,
    },
    reading_elapsed_time: {
      type: Number,
    },
    reading_submission_received: {
      type: Boolean,
    },
    batch: {
      type: String,
    },
    submission_folder_id: {
      type: String,
    },
    merged_file_id: {
      type: String,
    },
    test_password: {
      type: String,
    },
    wpm_time: {
      type: Number,
    },
    wpm: {
      type: Number,
    },
    wpm_normal: {
      type: Number,
    },
    resultDownloaded: {
      type: Boolean,
    },
  },
  { timestamps: true },
  { collection: "user" }
);

module.exports = mongoose.model("User", UserSchema);