import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "@material-ui/core/Button";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Container from "react-bootstrap/Container";
import AccountCircleIcon from "@material-ui/icons/AccountCircle";
// import Badge from "react-bootstrap/Badge";
import { Link } from "react-router-dom";
function AdminNavbar(props) {
  // console.log(props.username);
  return (
    <div>
      <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Container className="p-2">
          <Link style={{ textDecoration: "none" }} to="/adminDashboard">
            <Navbar.Brand>Admin Dashboard</Navbar.Brand>
          </Link>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="me-auto">
              <Link
                style={{
                  textDecoration: "none",
                  color: "white",
                  padding: "5px",
                }}
                to="/adminViewSubmission"
              >
                Download All Files
              </Link>
              <Link
                style={{
                  textDecoration: "none",
                  color: "white",
                  padding: "5px",
                }}
                to="/adminLoginStatus"
              >
                Check Login Status
              </Link>
              <Link
                style={{
                  textDecoration: "none",
                  color: "white",
                  padding: "5px",
                }}
                to="/increaseTime"
              >
                Increase Time
              </Link>
              <Link
                style={{
                  textDecoration: "none",
                  color: "white",
                  padding: "5px",
                }}
                to="/resetValues"
              >
                Reset Values
              </Link>
              <Link
                style={{
                  textDecoration: "none",
                  color: "white",
                  padding: "5px",
                }}
                to="/increaseBatchTime"
              >
                Increase Batch Time
              </Link>
              <Link
                style={{
                  textDecoration: "none",
                  color: "white",
                  padding: "5px",
                }}
                to="/adminWPMResults"
              >
                WPM Results
              </Link>
              <Link
                style={{
                  textDecoration: "none",
                  color: "white",
                  padding: "5px",
                }}
                to="/downloadRoll"
              >
                Download Rolls
              </Link>
            </Nav>
            <Nav>
              {/* <Link href="/contactus">Contact Us</Link> */}
              <span className="text-white">
                <AccountCircleIcon /> {props.userName}
              </span>
            </Nav>
            <Button
              style={{ marginLeft: "15px" }}
              variant="contained"
              onClick={props.logoutMethod}
              color="primary"
            >
              Logout
            </Button>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </div>
  );
}

export default AdminNavbar;
