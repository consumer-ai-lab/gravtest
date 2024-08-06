// Admin Model to register and login new admin
const mongoose = require("mongoose");

const AdminSchema = new mongoose.Schema(
    {
        userName: {
            type: String,
            required: true
        },
        password: {
            type: String,
            required: true,
        },
        token: {
            type: Array,
        },
    },
    { timestamps: true },
    { collection: 'Admin' }
);

module.exports = mongoose.model("Admin", AdminSchema);
