// BatchData Model 
const mongoose = require("mongoose");

const BatchDataSchema = new mongoose.Schema(
    {
        test_password: {
            type: String,
        },
        batch: {
            type: String,
        },
    },
    { timestamps: true },
    { collection: 'BatchDataSchema' }
);

module.exports = mongoose.model("BatchData", BatchDataSchema);
