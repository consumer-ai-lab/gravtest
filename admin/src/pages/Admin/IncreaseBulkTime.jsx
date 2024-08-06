import { Container } from "@material-ui/core";
import AdminNavbar from "../../components/AdminNavbar/AdminNavbar";
import { useState } from "react";
import Constants from './api';
import axios from "axios";

// create similar page for bulk time update where it takes select menu batch options, batch 1, 2, 3
export default function IncreaseBulkTime() {

    const [batch, setBatch] = useState("");
    const [time, setTime] = useState("");

    const [msg, setMsg] = useState("");

    const handleIncreaseTime = async () => {
        setMsg("Updating Time, please sit back and relax");
        console.log("batch", batch);
        console.log("time", time);
        const res = await axios.post(`${Constants.BASE_URL}userdata/increase_batch_test_time`, {
            batch,
            time,
        });
        console.log(res);
        setMsg(res.statusText);
    }

    return (
        <div>
            <AdminNavbar />
            <Container>
                <div className="col-md-8 col-10  mt-5 mb-5 p-3 bg-light  d-flex  flex-column align-items-center  " style={{
                    margin: 'auto',
                }}>
                    <h1 className="mt-4">Increase Time</h1>
                    <div className="mt-5 col-md-8 col-12 ">
                        <select
                            className="form-select form-select-lg mb-3"
                            aria-label=".form-select-lg example"
                            style={{ borderRadius: "20px", border: "2px solid black" }}
                            onChange={(e) => {
                                setBatch(e.target.value);
                            }}
                        >
                            <option selected>Select Batch</option>
                            <option value="Slot 1">Slot 1</option>
                            <option value="Slot 2">Slot 2</option>
                            <option value="Slot 3">Slot 3</option>
                            <option value="Slot 4">Slot 4</option>
                        </select>
                        <input
                            type="number"
                            id="form1Example23"
                            xs={4}
                            className="form-control form-control-lg xs:12 md:6"
                            placeholder="Enter time to increase"
                            style={{ borderRadius: "20px", border: "2px solid black" }}
                            onChange={(e) => {
                                setTime(e.target.value);
                            }}
                        />
                        <button
                            className="btn btn-primary mt-3"
                            style={{ borderRadius: "20px" }}
                            onClick={handleIncreaseTime}
                        >
                            Increase Time
                        </button>
                        <p className="text-success mt-3">{msg}</p>
                    </div>
                </div>
            </Container>
        </div>
    )
}
