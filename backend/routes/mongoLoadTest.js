const router = require("express").Router();
const dotenv = require("dotenv")
const { MongoClient } = require("mongodb");
dotenv.config()

const TABLE_NAME = "load-test-table"
const client = new MongoClient(process.env.MONGO_URL);

// Connecting with Mongoose Database
client.connect()
    .then(console.log("Connected to MongoDB in load test"))
    .catch((err) => console.log(err))

// database and collection code goes here
const db = client.db("myFirstDatabase")
const collection_var = db.collection(TABLE_NAME)

// data format
// {
//     "_id": number as Id,
//     "msg":"some text message"
// }


router.post("/", async (req, res) => {
    try {

        let doc_ID = req.body.ID

        // read data
        const data = await collection_var.findOne({ _id: doc_ID })

        // write data
        const filter = { _id: doc_ID }
        const options = { upsert: true }
        const updateDoc = {
            $set: {
                msg: `Load test says hello, ID: ${doc_ID}`
            },
        }

        await collection_var.updateOne(filter, updateDoc, options)
            .then((result) => {
                console.log(`${doc_ID}: message updated`);
            })
            .catch((error) => {
                console.log("Error while updating data");
                console.log(error);
            })


        res.status(200).json({
            "msg": data.msg
        });
    }
    catch (err) {
        console.log("error", err);
        res.status(500).json(err);
    }
});


module.exports = router;