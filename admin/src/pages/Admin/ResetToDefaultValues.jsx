import React, { useState } from "react";
import Container from "react-bootstrap/Container";
import AdminNavbar from "../../components/AdminNavbar/AdminNavbar";
import data from "./api";
import Constants from './api';
import axios from "axios";

const ResetValues = () => {
  const BASE_URL = data.BASE_URL;
  const [rollNo, setRollNo] = useState(0);
  const [msg, setMsg] = useState(null);

  const handleSubmitResetValues = async () => {
    setMsg("Processing");
    // if (rollNo.length != 5) {
    //   setMsg("check roll no again!");
    //   return;
    // }
    await axios
      .post(BASE_URL + `userdata/set_default_user_value`, { rollNo })
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

  const resetBatch = async (batch) => {
    setMsg(`Reseting Time, please sit back and relax`);
    const res = await axios.get(`${Constants.BASE_URL}userdata/reset_batch_test_time?batch=${batch}`);
    console.log(res);
    setMsg(res.statusText);
  }

  const resetAll = async () => {
    if (confirm("Are you sure you want to reset all the batches?")) {
      if (confirm("Are you really sure?")) {
        alert("Resetting all batches");
        await resetBatch("Slot+1");
        await resetBatch("Slot+2");
        await resetBatch("Slot+3");
        await resetBatch("Slot+4");
      } else {
        alert("Reset cancelled");
      }
    } else {
      alert("Reset cancelled");
    }
  }

  return (
    <div>
      <AdminNavbar />
      <Container>
        <div className="col-md-8 col-10  mt-5 mb-5 p-3 bg-light d-flex  flex-column align-items-center " style={{
          margin: 'auto',
        }}>
          <h1 className="mt-4 ">Reset values to default</h1>
          <div style={{ minHeight: "50vh", }} className="col-md-8 col-12 ">
            <input
              type="number"
              id="form1Example23"
              className="form-control form-control-lg mt-5"
              placeholder="Enter roll no to reset values to default"
              onChange={(e) => setRollNo(e.target.value)}
              style={{ borderRadius: "20px", border: "2px solid black" }}
            />
            <button
              variant="contained"
              color="primary"
              type="submit"
              className="btn btn-primary btn-lg btn-block"
              onClick={handleSubmitResetValues}
              style={{ margin: "auto", marginTop: "2rem" }}
            >
              Set values to default
            </button>
            <button
              variant="contained"
              color="danger"
              type="submit"
              className="btn btn-danger btn-lg btn-block"
              onClick={resetAll}
              style={{ margin: "auto", marginTop: "2rem", marginLeft: "1rem" }}
            >
              Reset All
            </button>

            {msg &&
              <div style={{ fontSize: '1.5rem' }}>Status: {msg}</div>}
          </div>
        </div>
      </Container>
    </div>
  );
};

export default ResetValues;
