import React, { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import { Button } from "@material-ui/core";
import axios from "axios";
import env from "react-dotenv";
import Spinner from "react-bootstrap/Spinner";
import { Redirect } from "react-router-dom";
import "./adminDashboard.css";
import Table from "react-bootstrap/Table";
import DownloadIcon from "@mui/icons-material/Download";
import AdminNavbar from "../../components/AdminNavbar/AdminNavbar";
import Alert from "@mui/material/Alert";
import IconButton from "@mui/material/IconButton";
import Collapse from "@mui/material/Collapse";
import CloseIcon from "@mui/icons-material/Close";
// import {BASE_URL} from './api'
import data from "./api";

function AdminLoginStatus() {
  function StaticTable(props) {
    return (
      <div className="container" style={{ width: "70%", margin: "auto" }}>
        <p style={{ textAlign: "center", fontWeight: "bolder" }}>
          {" "}
          Select the Prefered Slot and click the Fetch Batch Data Button
        </p>
      </div>
    );
  }

  function DynamicTable(batchData) {
    console.log(batchData);
    return (
      <div className="container" style={{ width: "70%", margin: "auto" }}>
        <Table striped bordered hover>
          <thead variant="dark">
            <tr>
              <td style={{ fontWeight: "bold", fontSize: "18px" }}>
                <center>Name</center>
              </td>
              <td style={{ fontWeight: "bold", fontSize: "18px" }}>
                <center>Roll Number</center>
              </td>
              <td style={{ fontWeight: "bold", fontSize: "18px" }}>
                <center>Test Password</center>
              </td>
              <td style={{ fontWeight: "bold", fontSize: "18px" }}>
                <center>Login Status</center>
              </td>
              <td style={{ fontWeight: "bold", fontSize: "18px" }}>
                <center>Bucket Creation Status</center>
              </td>
              <td style={{ fontWeight: "bold", fontSize: "18px" }}>
                <center>Merged File Status Status</center>
              </td>
            </tr>
          </thead>
          <tbody>
            {batchData.batchData.map((b, ind) => (
              <tr key={b.name + ind}>
                <td>
                  <center>{b.name}</center>
                </td>
                <td>
                  <center>{b.username}</center>
                </td>
                <td>
                  <center>{b.test_password}</center>
                </td>
                <td>
                  {b.start_time ? (
                    <center style={{ color: "green", fontWeight: "bold" }}>
                      Logged In
                    </center>
                  ) : (
                    <center style={{ color: "red", fontWeight: "bold" }}>
                      Not Logged In
                    </center>
                  )}
                </td>
                <td>
                  {b.submission_folder_id && b.submission_folder_id !== "" ? (
                    <center style={{ color: "green", fontWeight: "bold" }}>
                      Bucket created
                    </center>
                  ) : (
                    <center style={{ color: "red", fontWeight: "bold" }}>
                      Bucket not created
                    </center>
                  )}
                </td>
                <td>
                  {b.merged_file_id && b.merged_file_id !== "" ? (
                    <center style={{ color: "green", fontWeight: "bold" }}>
                      Merged File Received
                    </center>
                  ) : (
                    <center style={{ color: "red", fontWeight: "bold" }}>
                      Merged File not Received
                    </center>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
    );
  }

  function refreshPage() {
    window.location.reload(false);
  }

  let [batchData, setBatchData] = useState([]);
  const [batch, setBatch] = useState("");
  const [adminState, setAdminState] = useState({
    userName: "",
  });
  const [loginState, setLoginState] = useState("checking");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token") || "";
    axios
      .post(
        BASE_URL + "auth/authenticateAdmin",
        {},
        {
          headers: {
            token: token,
          },
        }
      )
      .then((result) => {
        if (result.data.status === "verified") {
          setLoginState("loggedIn");
          setAdminState({ ...adminState, userName: result.data.userName });
        } else setLoginState("notLoggedIn");
      })
      .catch((err) => {
        setLoginState("networkError");
      });
  }, []);

  // useEffect(async () =>{
  //     console.log(batchData)
  //     await axios.get(BASE_URL + `userData/get_batchwise_list/?batch=${batch}`).
  //         then((response) => {
  //             setBatchData(response.data)
  //         })
  // },[batch])

  const sortByFileMerged = () => {
    let sortedData = batchData;
    console.log(sortedData);
    sortedData.sort((a, b) => (b.merged_file_id && b.merged_file_id ? -1 : 1)); //sort by file merged
    setBatchData([...sortedData]);
    console.log(sortedData);
  };

  const sortByCreationStatus = () => {
    let sortedData = batchData;
    console.log(sortedData);
    sortedData.sort((a, b) =>
      b.submission_folder_id && b.submission_folder_id ? -1 : 1
    ); //sort by bucket creation
    setBatchData([...sortedData]);
    console.log(sortedData);
  };

  const sortByLoginStatus = async () => {
    // await setDataAsync(batchData);
    let sortedData = batchData;
    console.log(sortedData);
    sortedData.sort((a, b) => (b.start_time ? -1 : 1)); //sort by file login
    setBatchData([...sortedData]);
    console.log(sortedData);
  };

  const logoutMethod = () => {
    const token = localStorage.getItem("token") || "";
    axios
      .post(
        BASE_URL + "auth/logoutAdmin",
        {
          userName: adminState.userName,
          token: token,
        },
        {
          headers: {
            token: token,
          },
        }
      )
      .then((result) => {
        if (result.data.status === "logged out") {
          localStorage.removeItem("token");
          setAdminState({ ...adminState, userName: "" });
          setLoginState("notLoggedIn");
        } else {
        }
      })
      .catch((err) => {
        setLoginState("networkError");
      });
  };
  const BASE_URL = data.BASE_URL;
  // console.log(BASE_URL)
  const [openSuccessAlert, setOpenSuccessAlert] = React.useState(false);
  const [progressAlert, setProgressAlert] = React.useState(false);
  const [dataFetchedAlert, setDataFetchedAlert] = React.useState(false);
  const fetchBatchData = async () => {
    console.log(batch);
    setLoading(true);
    await axios
      .get(BASE_URL + `userData/get_slotWise_list_logincheck/?batch=${batch}`)
      .then((response) => {
        // response.sort((a,b) => a.test_password > b.test_password ?1:-1 )
        // const newSortedData = []
        // response.data.sort((a,b) => a.name > b.name ?1:-1 )
        // response.data.sort((a,b) =>(b.submission_folder_id && b.submission_folder_id) ?-1:1 ) //sort by bucket creation
        // response.data.sort((a,b) =>(b.merged_file_id && b.merged_file_id ) ?-1:1 ) //sort by file merged
        // response.data.sort((a,b) =>(b.start_time) ?-1:1 ) //sort by file merged
        setBatchData(response.data);
        console.log(response.data);
        setLoading(false);
      });
  };
  const downloadAllFiles = async () => {
    console.log(batchData.length);
    setProgressAlert(true);
    for (let i = 0; i < batchData.length; i++) {
      if (
        batchData[i][1] !== "" &&
        batchData[i][1] !== null &&
        typeof batchData[i][1] !== "undefined"
      ) {
        await axios
          .get(
            BASE_URL + `s3download/single_file/?username=${batchData[i][0]}`,
            {
              responseType: "blob",
            }
          )
          .then((response) => {
            const downloadUrl = window.URL.createObjectURL(
              new Blob([response.data])
            );

            const link = document.createElement("a");

            link.href = downloadUrl;

            link.setAttribute("download", batchData[i][0] + ".pdf"); //any other extension

            document.body.appendChild(link);

            link.click();

            link.remove();
          });
        console.log("Downloaded");
      }
    }
    setProgressAlert(false);
    setOpenSuccessAlert(true);
    setTimeout(refreshPage, 2000);
    console.log("For is completed");
  };

  const downloadSingleFile = async (username, fileId) => {
    console.log("The username from downloadSingleFile is", username);
    console.log("The fileId from downloadSingleFile is", fileId);
    setProgressAlert(true);
    if (fileId !== "" && fileId !== null && typeof fileId !== "undefined") {
      await axios
        .get(BASE_URL + `s3download/single_file/?username=${username}`, {
          responseType: "blob",
        })
        .then((response) => {
          const downloadUrl = window.URL.createObjectURL(
            new Blob([response.data])
          );

          const link = document.createElement("a");

          link.href = downloadUrl;

          link.setAttribute("download", username + ".pdf"); //any other extension

          document.body.appendChild(link);

          link.click();

          link.remove();
        });
      setProgressAlert(false);
      setOpenSuccessAlert(true);
      setTimeout(refreshPage, 2000);
      console.log("Downloaded");
    }
  };

  if (loginState === "checking") {
    return (
      <div style={{ textAlign: "center", width: "100%" }}>
        <br />
        <br />
        <Spinner animation="border" variant="primary" />
        <br />
        <br />
      </div>
    );
  } else if (loginState === "notLoggedIn") {
    return <Redirect to="/" />;
  } else if (loginState === "networkError") {
    return (
      <div style={{ textAlign: "center", width: "100%" }}>
        <br />
        <br />
        <h3>Network Error</h3>
        <br />
        <br />
      </div>
    );
  }

  return (
    <div>
      <AdminNavbar userName={adminState.userName} logoutMethod={logoutMethod} />
      <div className="container">
        <Collapse in={openSuccessAlert}>
          <Alert
            style={{
              position: "absolute",
              zIndex: "1",
              marginLeft: "750px",
              marginTop: "10px",
            }}
            severity="success"
            variant="filled"
            size="medium"
            action={
              <IconButton
                aria-label="close"
                style={{ color: "white" }}
                size="small"
                onClick={() => {
                  setOpenSuccessAlert(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
            sx={{ width: 500, float: "right", marginTop: "10px" }}
          >
            All Files Downloaded Successfully
          </Alert>
        </Collapse>
        <Collapse in={progressAlert}>
          <Alert
            style={{
              position: "absolute",
              zIndex: "1",
              marginLeft: "750px",
              marginTop: "10px",
            }}
            severity="warning"
            variant="filled"
            size="medium"
            action={
              <IconButton
                aria-label="close"
                style={{ color: "white" }}
                size="small"
                onClick={() => {
                  setProgressAlert(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
            sx={{ width: 500, float: "right", marginTop: "10px" }}
          >
            Download in Progress....
          </Alert>
        </Collapse>
        <div
          className="col-8  mt-5 mb-5 p-3 bg-light"
          style={{
            margin: "auto",
          }}
        >
          <h4 style={{ textAlign: "center", padding: "10px", color: "black" }}>
            Check Login Status Page
          </h4>
          <div
            className="timeSlot mb-5"
            style={{ width: "60%", marginLeft: "20px" }}
          >
            <h5 style={{ marginLeft: "10px" }}>
              STEP 1 : Please Select the Timeslot
            </h5>
            <select
              style={{
                width: "100%",
                border: "none",
                padding: "10px",
                borderRadius: "20px",
              }}
              name="Select Time Slot"
              onChange={(e) => setBatch(e.target.value)}
            >
              <option value="Slot 1">Select a Batch</option>
              <option value="Slot 1">Slot 1</option>
              <option value="Slot 2">Slot 2</option>
              <option value="Slot 3">Slot 3</option>
              <option value="Slot 4">Slot 4</option>
            </select>
          </div>
          <div
            className="timeSlot mb-5"
            style={{ width: "60%", marginLeft: "20px" }}
          >
            <h5 style={{ marginLeft: "10px", paddingBottom: "10px" }}>
              STEP 2 : Fetch Corresponding Batch Details
            </h5>
            <div className="col-md-6 col-12 " style={{ marginLeft: "20px" }}>
              <Button
                variant="contained"
                color="primary"
                onClick={fetchBatchData}
              >
                Fetch Batch Data
              </Button>
              {loading && <Spinner animation="border" variant="primary" />}
            </div>
          </div>
          <div
            className="timeSlot mb-5 pd-3"
            style={{ width: "100%", marginLeft: "20px" }}
          >
            <h5 style={{ marginLeft: "10px", paddingBottom: "10px" }}>
              STEP 3 : Click on the below button to download all submission
            </h5>
            <div className="col-md-6 col-12">
              <Button
                style={{ marginLeft: "20px" }}
                variant="contained"
                color="primary"
                endIcon={<DownloadIcon />}
                onClick={downloadAllFiles}
              >
                DownLoad All Submission
              </Button>
            </div>
          </div>
          <div style={{ display: "flex", justifyContent: "space-evenly" }}>
            <Button
              style={{ marginLeft: "20px" }}
              variant="contained"
              color="primary"
              onClick={sortByLoginStatus}
            >
              Sort by Login Status
            </Button>
            <Button
              style={{ marginLeft: "20px" }}
              variant="contained"
              color="primary"
              onClick={sortByCreationStatus}
            >
              Sort by Bucket Creation Status
            </Button>
            <Button
              style={{ marginLeft: "20px" }}
              variant="contained"
              color="primary"
              onClick={sortByFileMerged}
            >
              Sort by File Merged Status
            </Button>
          </div>
        </div>
        {batchData.length === 0 ? (
          <StaticTable />
        ) : (
          <DynamicTable batchData={batchData} />
        )}
      </div>
    </div>

    /* <div>
                        <h2 className="display-6 text-center my-3"><b>View Submissions</b></h2>
                        <div className="row m-5">
                            <div className="col-md-6 col-12">
                                <h5 style={{ marginLeft: '10px' }}>Please Select the Batch</h5>
                                <select style={{ width: '100%', border: 'none', padding: '10px', borderRadius: '20px' }} name="Select Batch"
                                    onChange={(e) => setBatch(e.target.value)}>
                                    <option value="Slot 1">Select a Batch</option>
                                    <option value="Slot 1">Slot 1 </option>
                                    <option value="Slot 2">Slot 2</option>
                                    <option value="Slot 3">Slot 3</option>
    
                                </select>
                            </div>
    
                            <div className="col-md-6 col-12">
                                <Button variant="contained" color="primary" endIcon={<DownloadIcon />} onClick={fetchBatchData}>Fetch Batch Data</Button>
                            </div>
                        </div>
                        <center> <div className="col-md-6 col-12">
                            <Button variant="contained" color="primary" endIcon={<DownloadIcon />} onClick={downloadAllFiles}>Download All Submission</Button>
                        </div></center>
                    </div> */

    /* {batchData.length>0 &&
                        <div>
                            <h1>Hi I am Tejas Tapas</h1>
                            <h2>I am Jjd</h2>
                            <Button>jndn</Button>
                        </div>
                    } */
  );
}

export default AdminLoginStatus;
