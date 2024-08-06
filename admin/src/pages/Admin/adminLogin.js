import React, { useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import { TextField, Button } from '@material-ui/core';
import Spinner from 'react-bootstrap/Spinner';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Logo from "./images/WCL_LOGO.png"
import Profile from './images/profile.png'
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Alert from '@mui/material/Alert';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';
import data from './api'

function AdminLogin() {

    const BASE_URL = data.BASE_URL
    const [open, setOpen] = React.useState(false);

    const [openSuccessAlert, setOpenSuccessAlert] = React.useState(false);

    const [openErrorAlert, setOpenErrorAlert] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };


    const [passwordData, setPasswordData] = useState({
        userName: "",
        password: "",
        newPassword: ""
    })

    const [formState, setFormState] = useState({
        userName: '',
        password: ''
    });

    const [loginInfo, setLoginInfo] = useState('');

    const [loginState, setLoginState] = useState('checking');

    const [loadingState, setLoadingState] = useState(false);

    const inputHandler = (event) => {
        setFormState({ ...formState, [event.target.name]: event.target.value });
    }
    function refreshPage() {
        window.location.reload(false);
      }

    const handleChangePassword = async () => {
        try {
            await axios.patch(BASE_URL+"password/", passwordData).
                then((response) => {
                    console.log(response)
                })
                setOpen(false);
                setOpenSuccessAlert(true)
                setTimeout(refreshPage, 3000);
        } catch (err) {
            setOpen(false);
            setOpenErrorAlert(true)
            setTimeout(refreshPage, 4000);
        }
    }


    useEffect(() => {
        const token = localStorage.getItem("token") || '';
        axios.post(BASE_URL+"auth/authenticateAdmin", {}, {
            headers: {
                'token': token
            }
        })
            .then(result => {
                console.log("result: ", result)
                if (result.data.status === 'verified') {
                    setLoginState('loggedIn');
                }
                else
                    setLoginState('notLoggedIn');
            }).catch((err) => {
                console.log(err);
            })
    }, []);

    const handleFormSubmission = () => {
        setLoadingState(true);
        setLoginInfo('');
        console.log(formState)
        const res = axios.post(BASE_URL+'auth/loginAdmin',
            formState)
            .then((response) => {
                console.log("response", response);
                if (response.data['status'] === 'verified') {
                    console.log("logged in");
                    localStorage.setItem('token', response.data['token'])
                    setLoginState('loggedIn');
                }
                else {
                    console.log("incorrect credentials");
                    setLoginInfo('Incorrect Credentials');
                }
                setLoadingState(false);
            }).catch((err) => {
                console.log("err", err);
                setLoginInfo('Error: Check your network connection and try again');
                setLoadingState(false);
            });
    }


    if (loginState === 'loggedIn')
        return <Redirect to="/adminDashboard" />
    else if (loginState === 'checking') {
        return (
            <div style={{ textAlign: "center", width: "100%" }}>
                <br /><br />
                <Spinner animation="border" variant="primary" />
                <br /><br />
            </div>
        );
    }

    return (
        <div className="container-fluid">
            <Collapse in={openSuccessAlert}>
                <Alert
                   style={{position:'absolute',zIndex:'1',marginLeft:'850px',marginTop:'20px'}}
                    severity="success"
                    variant="filled"
                    size="medium"
                    action={
                        <IconButton
                            aria-label="close"
                            style={{color:'white'}}
                            size="small"
                            onClick={() => {
                                setOpenSuccessAlert(false);
                            }}
                        >
                            <CloseIcon fontSize="inherit" />
                        </IconButton>
                    }
                    sx={{ width: 500,float:'right',marginTop:'10px' }}
                >
                    Password Changed Successfully
                </Alert>
            </Collapse>
            <Collapse in={openErrorAlert}>
                <Alert
                    style={{position:'absolute',zIndex:'1',marginLeft:'850px',marginTop:'20px'}}
                    severity="error"
                    variant="filled"
                    size="medium"
                    action={
                        <IconButton
                            aria-label="close"
                            style={{color:'white'}}
                            size="small"
                            onClick={() => {
                                setOpenErrorAlert(false);
                            }}
                        >
                            <CloseIcon fontSize="inherit" />
                        </IconButton>
                    }
                    sx={{ width: 500,float:'right',marginTop:'10px' }}
                >
                    Username or Current Password Incorrect
                </Alert>
            </Collapse>
            <Dialog open={open} onClose={handleClose}>
                <DialogTitle>Change Password</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Add Your username, your current password and new password so as to change the password.
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Username"
                        type="text"
                        fullWidth
                        variant="standard"
                        onChange={(e) => setPasswordData({ ...passwordData, userName: e.target.value })}
                    />
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="Current Password"
                        type="password"
                        fullWidth
                        variant="standard"
                        onChange={(e) => setPasswordData({ ...passwordData, password: e.target.value })}
                    />
                    <TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="New Password"
                        type="password"
                        fullWidth
                        variant="standard"
                        onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose}>Cancel</Button>
                    <Button onClick={handleChangePassword}>Change Password</Button>
                </DialogActions>
            </Dialog>
            <div className="row">

                {/* WCL Display Window */}
                <div className="col-12 col-sm-7" style={{ height: "100vh", background: "linear-gradient(60deg, #66bb6a, #43a047)", boxShadow: "0 4px 20px 0 rgb(0 0 0 / 14%), 0 7px 10px -5px rgb(76 175 80 / 40%)" }} >
                    <div className="row">
                        <img className="img-fluid" src={Logo} style={{ borderRadius: "50%", padding: "8px", width: "200px", margin: "auto", marginTop: "30px" }} />
                        <p className="display-3" style={{ color: "white", fontWeight: "bold", marginLeft: "30px", marginTop: "30px" }}>
                            Western Coalfields Limited(WCL)
                        </p>

                        <p className="display-6 " style={{ color: "white", fontWeight: "bold", marginLeft: "30px", marginTop: "30px" }}>
                            Recruitment Test
                        </p>


                    </div>

                </div>

                {/* Login Window */}

                <div className="col-12 col-sm-5">

                    <div className="" style={{
                        alignItems: 'center', justifyContent: 'center', marginTop: '40px'
                    }}>
                        <center><img src={Profile} style={{ width: '250px', height: '250px' }} className="img-fluid"></img></center>
                    </div>
                    <form>
                        {/* <!-- Email input --> */}

                        <div className="form-outline mb-4 mt-4" style={{ width: '70%', margin: 'auto' }}>
                            <label className="form-label" for="form1Example13">UserName</label>
                            <center><input type="text" id="form1Example13" className="form-control form-control-lg" defaultValue={formState.userName} onChange={(e) => setFormState({ ...formState, userName: e.target.value })} placeholder="Enter Username" /></center>
                        </div>

                        {/* <!-- Password input --> */}
                        <div className="form-outline mb-4" style={{ width: '70%', margin: 'auto' }}>
                            <label className="form-label" for="form1Example23">Password</label>
                            <input type="password" id="form1Example23" onChange={(e) => setFormState({ ...formState, password: e.target.value })} className="form-control form-control-lg" placeholder="Enter Password" />
                        </div>

                        <div className={loadingState ? "d-block" : "d-none"} style={{ textAlign: "center", width: "100%" }}>
                            <Spinner animation="border" variant="primary" /> <br />
                        </div>

                        <div>
                            {loginInfo}
                        </div>

                        <Button onClick={handleClickOpen} style={{ marginLeft: '85px' }}>
                            Change Password
                        </Button>

                        <div className="mt-4" style={{ width: '70%', margin: 'auto' }}>
                            <button disabled={loadingState} variant="contained" onClick={handleFormSubmission} color="primary"  type="submit" className="btn btn-primary btn-lg btn-block" style={{ width: '100%', margin: 'auto' }}>Sign in</button>
                        </div>
                    </form>

                </div>
            </div>
        </div>
    )
}

export default AdminLogin