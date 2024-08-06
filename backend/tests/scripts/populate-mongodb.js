const dotenv = require("dotenv")
const { MongoClient } = require("mongodb");
dotenv.config()

const TABLE_NAME = "load-test-table"
const client = new MongoClient(process.env.MONGO_URL);

// insert 500 records
const RECORD_COUNT = 500


console.log(process.env.MONGO_URL);

// Connecting with Mongoose Database
client.connect()
    .then(console.log("Connected to MongoDB"))
    .catch((err) => console.log(err))

// database and collection code goes here
const db = client.db("myFirstDatabase")
const collection_var = db.collection(TABLE_NAME)

// data format
// {
//     "_id": number as Id,
//     "msg":"some text message"
// }

let data_list = []
for (let i = 0; i < RECORD_COUNT; ++i) {
    let data = {
        "_id": i,
        "msg": `This is record: ${i}`
    }
    data_list.push(data)
}
console.log(data_list.length)


// insert all data
collection_var.insertMany(data_list)
    .then((result) => {
        // display the results of your operation
        console.log(`${RECORD_COUNT} data inserted in table: ${TABLE_NAME}`);
        console.log(result.insertedIds);
    })
    .catch((error) => {
        console.log("Error while populating data");
        console.log(error);
    })

// close client
client.close()
