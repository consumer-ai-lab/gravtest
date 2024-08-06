import AdminNavbar from "../../components/AdminNavbar/AdminNavbar";
import { useEffect, useState } from 'react';
import constants from './api';
import Table from 'react-bootstrap/Table'

export default function AdminWPMResults() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(constants.BASE_URL + 'userData/get_slotWise_list_logincheck?batch=Slot+3')
            .then(response => response.json())
            .then(data => {
                data = data.filter(r => r.wpm);
                setData(data);
                console.log(data);
                setLoading(false);
            });
    }, []);

    return (
        <div>
            <AdminNavbar />
            <h1 style={{
                padding: "1rem"
            }}>WPM Results</h1>
            <p
                style={{
                    textAlign: "center",
                    fontSize: "1.5rem",
                    fontWeight: "bold"
                }}
            >
                Pass Count: {loading ? "Loading" : data.filter(r => Number(r.wpm).toFixed(2) >= 30).length}
                <br />
                Fail Count: {loading ? "Loading" : data.filter(r => Number(r.wpm).toFixed(2) < 30).length}
                <br />
                Potentially Pass Count: {loading ? "Loading" : data.filter(r => Number(r.wpm_normal).toFixed(2) >= 30).length}
                <br />
                Total Count: {loading ? "Loading" : data.length}
            </p>
            <div style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }}>
                <Table striped bordered hover style={{
                    width: "60%",
                    borderColor: "black"
                }}>
                    <thead>
                        <tr>
                            <th>Sr. No</th>
                            <th>Roll No.</th>
                            <th>Name</th>
                            <th>WPM</th>
                            <th>RAW</th>
                            {/* <th>Submitted</th> */}
                        </tr>
                    </thead>
                    <tbody>
                        {loading ? <tr><td colSpan="6">Loading...</td></tr> : data.map((r, i) => {
                            // const date = new Date(r.updatedAt);
                            return (<tr key={i} style={{
                                backgroundColor: Number(r.wpm).toFixed(2) > 30 ? "lightgreen" : Number(r.wpm_normal).toFixed(2) > 30 ? "lightyellow" : ""
                            }}>
                                <td>{i + 1}</td>
                                <td>{r.username}</td>
                                <td>{r.name}</td>
                                <td>{Number(r.wpm).toFixed(2)}</td>
                                <td style={{ color: "grey" }}>{Number(r.wpm_normal).toFixed(2)}</td>
                                {/* <td>{formatTimeAgo(date)}</td> */}
                            </tr>)
                        }
                        )}
                    </tbody>
                </Table>
            </div>
        </div>
    );
}

const formatter = new Intl.RelativeTimeFormat(undefined, {
    numeric: "auto",
});

const DIVISIONS = [
    { amount: 60, name: "seconds" },
    { amount: 60, name: "minutes" },
    { amount: 24, name: "hours" },
    { amount: 7, name: "days" },
    { amount: 4.34524, name: "weeks" },
    { amount: 12, name: "months" },
    { amount: Number.POSITIVE_INFINITY, name: "years" },
];

function formatTimeAgo(date) {
    let duration = (date.getTime() - new Date().getTime()) / 1000;

    for (let i = 0; i < DIVISIONS.length; i++) {
        const division = DIVISIONS[i];
        if (Math.abs(duration) < division.amount) {
            return formatter.format(Math.round(duration), division.name);
        }
        duration /= division.amount;
    }
}