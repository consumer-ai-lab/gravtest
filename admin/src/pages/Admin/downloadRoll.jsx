import { useState } from "react";
import AdminNavbar from "../../components/AdminNavbar/AdminNavbar";
import axios from "axios";
import Constants from './api';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

export default function DownloadRoll() {
    const [from, setFrom] = useState(0);
    const [to, setTo] = useState(0);
    const [rollData, setRollData] = useState([]);

    async function getRolls() {
        await axios.get(Constants.BASE_URL + `userData/get_batchwise_list_roll?from=${from}&to=${to}`).then((response) => {
            setRollData(response.data);
            console.log(response.data);
        }).catch((err) => {
            console.log(err);
        }).then(() => {
            alert("Rolls fetched successfully");
        });
    }

    async function download(f = false) {
        await downloadAndZipFiles(rollData, f).then(zip => {
            if (zip) {
                zip.generateAsync({ type: "blob" })
                    .then(function (content) {
                        saveAs(content, "results.zip");
                    });
            }
        }).then(async () => {
            await axios.get(Constants.BASE_URL + `userData/set_result_downloaded?from=${from}&to=${to}&resultDownloaded=true`).then((response) => {
                console.log(response.data);
            })
        });

    }

    async function downloadAndZipFiles(rollData, f) {
        console.log(f);
        return new Promise((resolve, reject) => {
            const zip = new JSZip();
            let data = rollData.filter(data => {
                if (f && data[4] === true) {
                    return true;
                } else {
                    const downloaded = data[3];
                    const submitted = data[4];
                    return !downloaded && submitted;
                }
            });
            console.log(data);

            if (data.length === 0) {
                alert("No files to download");
                reject(null);
            }
            const promises = data.map(data => downloadFile(data[0]));

            Promise.all(promises)
                .then(results => {
                    results.forEach((d, i) => {
                        if (d) {
                            zip.file(`${data[i][0]}.pdf`, d);
                        }
                        if (i === results.length - 1) {
                            resolve(zip);
                        }
                    });
                })
                .catch(error => {
                    console.error(error);
                    reject(null);
                });
        });
    }

    async function reset() {
        await axios.get(Constants.BASE_URL + `userData/set_result_downloaded?from=${from}&to=${to}&resultDownloaded=false`).then((response) => {
            console.log(response.data);
        }).then(() => {
            alert(`Reset Successfull!`)
        })
    }

    async function downloadFile(user) {
        return axios.get(Constants.BASE_URL + `s3download/single_file/?username=${user}`, {
            responseType: 'blob'
        })
            .then((response) => {
                return response.data;
            }).catch((err) => {
                console.log(err);
                return null;
            })
    }

    return <div>
        <AdminNavbar />
        <div className="col-md-8 col-10  mt-5 mb-5 p-3 bg-light d-flex  flex-column align-items-center " style={{
            margin: 'auto',
        }}>
            <h1 className="mt-4 ">Download Rolls</h1>
            <div style={{ minHeight: "50vh", }} className="col-md-8 col-12 ">
                <input
                    type="number"
                    id="form1Example23"
                    className="form-control form-control-lg mt-5"
                    placeholder="Enter starting roll no"
                    onChange={(e) => setFrom(e.target.value)}
                    style={{ borderRadius: "20px", border: "2px solid black" }}
                />
                <input
                    type="number"
                    id="form1Example23"
                    className="form-control form-control-lg mt-5"
                    placeholder="Enter ending roll no"
                    onChange={(e) => setTo(e.target.value)}
                    style={{ borderRadius: "20px", border: "2px solid black" }}
                />
                <button
                    variant="contained"
                    color="primary"
                    type="submit"
                    className="btn btn-primary btn-lg btn-block"
                    onClick={getRolls}
                    style={{ margin: "auto", marginTop: "2rem", marginInlineEnd: "1rem" }}
                >
                    Fetch
                </button>
                <button
                    variant="contained"
                    color="primary"
                    type="submit"
                    className="btn btn-primary btn-lg btn-block"
                    onClick={() => download(false)}
                    style={{ margin: "auto", marginTop: "2rem", marginInlineEnd: "1rem" }}
                >
                    Download
                </button>
                <button
                    variant="contained"
                    color="primary"
                    type="submit"
                    className="btn btn-primary btn-lg btn-block"
                    onClick={() => download(true)}
                    style={{ margin: "auto", marginTop: "2rem", marginInlineEnd: "1rem" }}
                >
                    Force Download
                </button>
                <button
                    variant="contained"
                    color="primary"
                    type="submit"
                    className="btn btn-primary btn-lg btn-block"
                    onClick={reset}
                    style={{ margin: "auto", marginTop: "2rem" }}
                >
                    Reset
                </button>
            </div>
        </div>
    </div>
}