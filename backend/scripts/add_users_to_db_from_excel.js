const User = require("../models/User");
const BatchData = require("../models/batchData");
const reader = require('xlsx')
const path = require('path')
const dotenv = require("dotenv")
const mongoose = require("mongoose")

dotenv.config();

mongoose
  .connect(process.env.MONGO_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true
  })
  .then(console.log("Connected to MongoDB\nFor adding users from excel"))
  .catch((err) => console.log(err));

const add_user_to_DB = async (user_data) => {
  try {
    let res = await User.findOne({ "username": user_data["username"] })
    if (res != null) return;
    const newUserData = new User(user_data)
    await newUserData.save()
    console.log(`${user_data["username"]} added to db`)
  }
  catch (err) {
    console.log(err)
  }
}

const add_batch_to_DB = async (batch_no, test_password) => {
  try {
    let res = await BatchData.findOne({ "test_password": test_password })
    if (res != null) return;
    const newBatchData = new BatchData({
      "test_password": test_password,
      "batch": "Slot " + batch_no.toString(),
    })
    await newBatchData.save()
    console.log(`${batch_no} added to db`)
  }
  catch (err) {
    console.log(err)
  }
}

// Reading our test file
let file_path = path.resolve(__dirname, 'student_data.xlsx')
const file = reader.readFile(file_path)

let data = []

const sheets = file.SheetNames

const load_data = async () => {
  for (let i = 0; i < sheets.length; i++) {
    let batch = (i + 1).toString()
    const temp = reader.utils.sheet_to_json(file.Sheets[file.SheetNames[i]])
    const test_password = `wcl24s${batch}`
    await add_batch_to_DB(batch,test_password)
    temp.forEach((res) => {
      let new_user_data = {
        "name": res["NAME"],
        "username": res["ROLL NO"].toString(),
        "user_password": "12345",
        "batch": `Slot ${batch}`,
        "test_password":test_password
      }
      data.push(new_user_data)
    })
  }
}

const main = async () => {
  await load_data()
  for (let i = 0; i < data.length; ++i) {
    // console.log(data[i])
    await add_user_to_DB(data[i])
  }
  console.log("All user data added to DB");
}
main()







