const User = require("../models/User");
const BatchData = require("../models/batchData");
const Question = require("../models/question");
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

const delete_docs_from_DB = async (model) => {
  try {
    await model.deleteMany({})
    console.log(`Deleted all docs of model ${model.modelName} from DB`);
  }
  catch (err) {
    console.log(err)
  }
}

const main = async () => {
  await delete_docs_from_DB(User)
  // await delete_docs_from_DB(Question)
  await delete_docs_from_DB(BatchData)
  console.log("All old docs deleted from DB");
}
main()







