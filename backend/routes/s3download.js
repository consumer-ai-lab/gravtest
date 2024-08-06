// To handle all data of user incase of any network or electricity failure
const router = require("express").Router();
const User = require("../models/User");
const BatchData = require("../models/batchData");
const jwt = require('jsonwebtoken');
const fs = require('fs')
const csv = require('csv-parser')
const S3 = require('aws-sdk/clients/s3');
const multer = require('multer');
const Question = require("../models/question");
const path = require("path");
const mime = require("mime");
const dotenv = require("dotenv");

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, "Uploads/");
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname);
    },
});

const Upload = multer({ storage: storage });
dotenv.config();
const REGION = process.env.REGION;
const BUCKET_NAME = process.env.BUCKET_NAME;
const QUESTION_BUCKET_NAME = process.env.QUESTION_BUCKET_NAME
const IAM_USER_KEY = process.env.IAM_USER_KEY;
const IAM_USER_SECRET = process.env.IAM_USER_SECRET;
console.log("Region is",REGION)

let s3 = new S3({
    region: REGION,
    accessKeyId: IAM_USER_KEY,
    secretAccessKey: IAM_USER_SECRET,
    Bucket: BUCKET_NAME
});


let s3_question = new S3({
    region: REGION,
    accessKeyId: IAM_USER_KEY,
    secretAccessKey: IAM_USER_SECRET,
    Bucket: QUESTION_BUCKET_NAME
});

function uploadQuestion(key, path) {
    const fileStream = fs.createReadStream(path);
    const uploadParams = {
        Bucket: QUESTION_BUCKET_NAME,
        Body: fileStream,
        Key: key
    }
    return s3_question.upload(uploadParams).promise();
}

router.post('/fileUpload', Upload.single('file'), async (req, res) => {
    try {
        console.log('upload_file_s3');
        const { name, fileType, timeSlot, testPassword, key } = req.body;
        const s3key = 'questions/' + req.file.originalname;
        console.log("name: " + name);
        console.log("fileType: " + fileType);
        console.log("timeSlot: " + timeSlot)
        console.log("testPassword: " + testPassword);
        console.log("s3key: " + s3key);

        await uploadQuestion(s3key, req.file.path)
        const question = new Question({ fileType, testPassword, timeSlot, driveId:s3key })
        await question.save()

        fs.unlink(req.file.path, (e) => {
            if (e) {
                console.log(e);
            }
        })
        res.status(200).json({});
    }
    catch (err) {
        console.log(err)
        res.status(400).json({})
    }
})


router.get("/single_file", async (req, res) => {
    console.log("Inside Download File")
    try {
        const username = req.query.username;
        const userData = await User.findOne({ username: username })

        if (userData) {
            const fileLoc = path.join(__dirname, 'data', userData.username + ".pdf")
            var fileId = userData.merged_file_id;
            console.log("The File id is = ", fileId, "The roll no is", userData.username)

            if (fileId !== "" && fileId !== null && typeof (fileId) !== "undefined") {
                var fileName = userData.username + ".pdf"

                const params = {
                    Bucket: BUCKET_NAME,
                    Key: fileId
                }

                s3.getObject(params, function (err, data) {
                    if (err) {
                        throw err
                    }
                    else {
                        var filePath = path.join(__dirname, 'data', username + '.pdf');
                        var filename = path.basename(filePath);
                        var mimetype = mime.getType(filePath);
                        fs.writeFileSync(filePath, data.Body);
                        console.log('file downloaded successfully');

                        res.setHeader('Content-disposition', 'attachment; filename=' + filename);
                        res.setHeader('Content-type', mimetype);
                        res.download(filePath, (err) => {
                            try {
                                if (err) {
                                    console.log(err)
                                }
                                else {
                                    console.log("Download Done of a file")
                                    fs.unlink(filePath, (e) => {
                                        console.log(e)
                                    })
                                }
                            }
                            catch (e) {
                                console.log(e)
                            }

                        })
                    }

                })
            }
            else {
                res.status(200).json("File id not present")
            }
        }

    }
    catch (err) {
        console.log(err);
        res.status(500).json({});
    }
});


module.exports = router;