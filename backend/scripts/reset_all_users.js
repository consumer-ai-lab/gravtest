const User = require("../models/User");
const dotenv = require("dotenv")
const mongoose = require("mongoose")

dotenv.config();

mongoose
  .connect(process.env.MONGO_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
  .then(console.log("Connected to MongoDB"))
  .catch((err) => console.log(err));

const reset_all_users = async () => {
  try {
    const users = await User.updateMany({}, {
      $set: {
        submission_received: false,
        reading_submission_received: false,
        reading_elapsed_time: 0,
        elapsed_time: 0,
        wpm: null,
        wpm_normal: null,
        wpm_time: null,
      }
    })
    users
  }
  catch (err) {
    console.log("Error in reset_all_users")
    console.log(err)
  }
}

const main = async () => {
  await reset_all_users()
  console.log("All users were reset to default values.");
}
main()







