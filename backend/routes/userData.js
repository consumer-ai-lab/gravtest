// To handle all data of user incase of any network or electricity failure
const router = require("express").Router();
const User = require("../models/User");
const BatchData = require("../models/batchData");
const jwt = require("jsonwebtoken");
const fs = require("fs");
const csv = require("csv-parser");
const {
  applicationTokenVerifier,
  apiKeyVerifier,
  validRequestVerifier,
} = require("./tokenUtils");

router.post("/", async (req, res) => {
  try {
    console.log("\nUser login initiated :");
    console.log(req.body);
    const userData = await User.findOne({
      username: req.body.username,
      user_password: req.body.user_password,
    });
    console.log("This is user data");
    console.log(userData);

    if (userData === null) {
      console.log("Failed due to null user data");
      res.status(200).json({ result: "fail" });
      return;
    }

    const batch_data = await BatchData.findOne({
      test_password: req.body.test_password,
    });
    console.log("This is batch data");
    console.log(batch_data);

    if (batch_data === null) {
      console.log("Failed due to null batch data");
      res.status(200).json({ result: "fail" });
      return;
    }

    const token = await jwt.sign({ username: req.body.username }, "token", {
      expiresIn: "2d",
    });

    console.log("JWT token set");
    console.log(userData.batch, batch_data.batch);
    console.log(req.body.test_password, batch_data.test_password);

    if (
      req.body.test_password === batch_data.test_password &&
      userData.batch === batch_data.batch
    ) {
      let newUserData = userData.toObject();
      newUserData.token = token;
      newUserData.result = "success";
      userData.test_password = req.body.test_password;
      await userData.save();

      res.status(200).json(newUserData);
      console.log("Successfully logged in.\n");
    } else {
      console.log("Failed due to incorrect password");
      res.status(200).json({ result: "fail" });
    }
  } catch (err) {
    console.log(err);
    if (res.headersSent === false) {
      console.log("Failed due to network issue");
      res.status(400).json({});
    }
  }
});

router.post("/create_batch_data", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const batchData = new BatchData(req.body);
    const data = await batchData.save();
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.post("/update_start_time", async (req, res) => {
  try {
    console.log("/update_start_time");
    console.log("headers: ", req.headers);
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    console.log("c2: update start time");

    const userData = await User.findOne({ username: req.body.username });
    console.log("c3: update start time", userData);
    userData.start_time = req.body.start_time;
    console.log("c4: update start time", userData);
    userData.elapsed_time = 0;
    await userData.save();
    console.log("c5: update start time", userData);
    res.status(200).json(userData);
  } catch (err) {
    console.log("update start time", err);
    res.status(500).json(err);
  }
});

router.post("/update_reading_submission_received", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const userData = await User.findOne({ username: req.body.username });
    userData.reading_submission_received = true;
    await userData.save();
    console.log("update_read_sub_time", userData);
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.post("/update_submission_received", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const userData = await User.findOne({ username: req.body.username });
    userData.submission_received = true;
    await userData.save();
    console.log("sub_rec", userData);
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.post("/update_elapsed_time", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const userData = await User.findOne({
      username: req.body.username,
    });
    userData.elapsed_time = req.body.elapsed_time;
    await userData.save();
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.get("/get_elapsed_time", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const userData = await User.findOne({ username: req.query.username });
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.post("/update_reading_elapsed_time", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const userData = await User.findOne({
      username: req.body.username,
    });
    userData.reading_elapsed_time = req.body.reading_elapsed_time;
    await userData.save();
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.get("/get_reading_elapsed_time", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const userData = await User.findOne({ username: req.query.username });
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.post("/update_submission_folder_id", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const userData = await User.findOne({ username: req.body.username });
    userData.submission_folder_id = req.body.submission_folder_id;
    userData.merged_file_id = req.body.merged_file_id;
    await userData.save();
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.post("/wpm", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }
    const userData = await User.findOne({ username: req.body.username });
    userData.wpm = req.body.wpm;
    userData.wpm_time = req.body.wpm_time;
    userData.wpm_normal = req.body.wpm_normal;
    await userData.save();
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.get("/get_batchwise_list", async (req, res) => {
  try {
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    if (valid_request === false) {
      res
        .status(200)
        .json({ fail_reason: "invalid request: token or apikey is invalid" });
      return;
    }

    const batch = req.query.batch;
    const userData = await User.find({ batch: batch });
    let opArr = [];
    for (let i = 0; i < userData.length; i++) {
      opArr.push([
        userData[i].username,
        userData[i].merged_file_id,
        userData[i].submission_folder_id,
      ]);
    }
    res.status(200).json(opArr);
  } catch (err) {
    res.status(500).json(err);
  }
});

// define a route for getting batch data from x roll to y
router.get("/get_batchwise_list_roll", async (req, res) => {
  try {
    const from = req.query.from;
    const to = req.query.to;
    let userData = await User.find();
    userData = userData.filter((r) => +r.username >= from && +r.username <= to);
    let opArr = [];
    for (let i = 0; i < userData.length; i++) {
      opArr.push([
        userData[i].username,
        userData[i].merged_file_id,
        userData[i].submission_folder_id,
        userData[i].resultDownloaded,
        userData[i].submission_received,
      ]);
    }
    res.status(200).json(opArr);
  } catch (err) {
    res.status(500).json(err);
  }
});

// define a post route for getting batch data from x roll to y, now set resultDownloaded to true/false
router.get("/set_result_downloaded", async (req, res) => {
  try {
    const from = req.query.from;
    const to = req.query.to;
    const resultDownloaded = req.query.resultDownloaded === "true";
    console.log(resultDownloaded);
    let userData = await User.find();
    userData = userData.filter((r) => +r.username >= from && +r.username <= to);
    for (let i = 0; i < userData.length; i++) {
      if (userData[i].submission_received === false) continue;
      userData[i].resultDownloaded = resultDownloaded;
      await userData[i].save();
    }
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.get("/get_slotWise_list_frontend", async (req, res) => {
  try {
    const batch = req.query.batch;
    console.log(batch);
    const userData = await User.find({ batch: batch });
    console.log("User Data is correct");
    // userData.sort({test_password:1})
    // console.log("UserData is cooooorect")
    let opArr = [];
    for (let i = 0; i < userData.length; i++) {
      if (
        userData[i].start_time !== " " &&
        userData[i].start_time !== null &&
        typeof userData[i].start_time !== "undefined"
      ) {
        opArr.push([
          userData[i].username,
          userData[i].merged_file_id,
          "Present",
          userData[i].submission_folder_id,
        ]);
      } else {
        opArr.push([
          userData[i].username,
          userData[i].merged_file_id,
          "Absent",
          userData[i].submission_folder_id,
        ]);
      }
    }
    res.status(200).json(opArr);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.get("/get_slotWise_list_logincheck", async (req, res) => {
  try {
    const batch = req.query.batch;
    console.log(batch);
    const userData = await User.find({ batch: batch });

    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.get("/registerAllUser", async (req, res) => {
  try {
    fs.createReadStream("./studentData.csv")
      .pipe(csv())
      .on("data", async function (row) {
        console.log(row.roll_no);
        let batch = row.slot_allocated.trim();
        batch = batch[batch.length - 1];
        batch = "Slot " + batch;
        console.log(batch);
        const user = {
          name: row.name,
          username: row.roll_no,
          user_password: "12345",
          batch: batch,
        };
        const newUserData = new User(user);
        await newUserData.save();
        res.status(200).json("Data Sent");
      })
      .on("end", function () {});
  } catch (err) {
    console.log(err);
  }
});

router.get("/token_test", async (req, res) => {
  try {
    console.log("/token_test");
    const token = req.headers.token;
    const valid_request = await validRequestVerifier(
      req.headers.token,
      req.headers.apikey
    );
    console.log(valid_request);

    res.status(200).json({});
  } catch (err) {
    console.log(err);
    res.status(500).json(err);
  }
});

router.post("/increase_user_test_time", async (req, res) => {
  try {
    const data = req.body;
    const username = data.timeData.rollNo;
    const timeToIncrease = data.timeData.time; //time in minutes
    console.log(data);
    const userDataArr = await User.find({ username: username });
    let userData = userDataArr[0];
    const prevTimeElapsedOfUser = userData.elapsed_time;
    console.log(userData);
    userData.elapsed_time = prevTimeElapsedOfUser - 60 * timeToIncrease;
    if (userData.elapsed_time > 1797) userData.elapsed_time = 1797;
    if (userData.elapsed_time < 0) userData.elapsed_time = 0;
    await userData.save();
    console.log(userData);
    res.status(200).json(userData);
  } catch (err) {
    res.status(500).json(err);
  }
});

// create a route for increasing time for whole batch
router.post("/increase_batch_test_time", async (req, res) => {
  try {
    const data = req.body;
    const batch = data.batch;
    const timeToIncrease = data.time; //time in minutes
    const userDataArr = await User.find({ batch: batch });

    for (let i = 0; i < userDataArr.length; i++) {
      let userData = userDataArr[i];
      const prevTimeElapsedOfUser = userData.elapsed_time;
      if (!prevTimeElapsedOfUser) continue;
      userData.elapsed_time = prevTimeElapsedOfUser - 60 * timeToIncrease;
      if (userData.elapsed_time > 1797) userData.elapsed_time = 1797;
      if (userData.elapsed_time < 0) userData.elapsed_time = 0;
      await userData.save().catch((err) => {
        console.log(err);
        return null;
      });
    }
    res.status(200).json(userDataArr);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.get("/reset_batch_test_time", async (req, res) => {
  try {
    const batch = req.query.batch;
    const userDataArr = await User.find({ batch: batch });

    for (let i = 0; i < userDataArr.length; i++) {
      let userData = userDataArr[i];
      if (!userData.reading_submission_received) continue;
      if (!userData.submission_received) continue;
      userData.reading_submission_received = false;
      userData.submission_received = false;
      userData.reading_elapsed_time = 0;
      userData.elapsed_time = 0;
      await userData.save().catch((err) => {
        console.log(err);
        return null;
      });
      console.log(`reset_batch_test_time: ${userData.name}`);
    }
    res.status(200).json(userDataArr);
    console.log(`reset_batch_test_time: ${batch}`);
  } catch (err) {
    res.status(500).json(err);
  }
});

router.post("/set_default_user_value", async (req, res) => {
  try {
    const data = req.body;
    const username = data.rollNo;
    const userDataArr = await User.find({ username: username });
    let userData = userDataArr[0];

    //updating values
    userData.submission_received = false;
    userData.reading_submission_received = false;
    userData.reading_elapsed_time = 0;
    userData.elapsed_time = 0;

    await userData.save();
    console.log(userData);
    res.status(200).json(userData);
  } catch (err) {
    console.log(err);
    res.status(500).json(err);
  }
});

module.exports = router;
