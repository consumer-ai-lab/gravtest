import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import AdminNavbar from "../../components/AdminNavbar/AdminNavbar";
import data from "./api";
import axios from "axios";

const IncreaseTime = () => {
  const BASE_URL = data.BASE_URL;
  const [rollNo, setRollNo] = useState(0);
  const [time, setTime] = useState(0);
  const [msg, setMsg] = useState(null);

  const handleIncreaseTime = async () => {
    setMsg("Processing");
    // if (rollNo.length != 5) {
    //   setMsg("check roll no again!");
    //   return;
    // }
    if (time === 0 || time < 0 || time > 30) {
      setMsg("enter correct value of time!");
      return;
    }
    console.log(rollNo);
    console.log(time);

    const timeData = { rollNo, time };
    await axios
      .post(BASE_URL + `userdata/increase_user_test_time`, { timeData })
      .then((response) => {
        console.log(response.data);
        console.log("successfully done");
        setMsg("successfully done");
      })
      .catch((err) => {
        console.log(err);
        setMsg(err.msg);
      });
  };

  return (
    <div>
      <AdminNavbar />
      <Container>
        <div
          className="col-md-8 col-10  mt-5 mb-5 p-3 bg-light  d-flex  flex-column align-items-center  "
          style={{
            margin: "auto",
          }}
        >
          <h1 className="mt-4">Increase Time</h1>
          <div className="mt-5 col-md-8 col-12 ">
            <input
              type="number"
              id="form1Example23"
              xs={4}
              className="form-control form-control-lg xs:12 md:6"
              // maxLength="5"
              // minLength={5}
              placeholder="Enter roll no to increase time"
              style={{ borderRadius: "20px", border: "2px solid black" }}
              onChange={(e) => {
                setRollNo(e.target.value);
              }}
            />
            <input
              type="number"
              id="form1Example23"
              className="form-control form-control-lg"
              placeholder="Enter minutes"
              onChange={(e) => setTime(e.target.value)}
              style={{
                borderRadius: "20px",
                border: "2px solid black",
                marginTop: "10px",
              }}
            />

            <button
              variant="contained"
              color="primary"
              type="submit"
              className="btn btn-primary btn-lg btn-block"
              onClick={handleIncreaseTime}
              style={{ marginTop: "2rem" }}
            >
              Click to increase time
            </button>
            <br />

            {msg && <div style={{ fontSize: "1.5rem" }}>Status: {msg}</div>}
          </div>
        </div>
      </Container>
    </div>
  );
};

export default IncreaseTime;
