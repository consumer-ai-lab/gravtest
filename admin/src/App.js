// Import Required dependecies
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

// Import required pages
import AdminLogin from "./pages/Admin/adminLogin";
import AdminDashboard from "./pages/Admin/adminDashboard";
import AdminViewSubmission from "./pages/Admin/adminViewSubmission";
import AdminLoginStatus from "./pages/Admin/adminLoginStatus";
import ResetValues from "./pages/Admin/ResetToDefaultValues";
import IncreaseTime from "./pages/Admin/IncreaseTime";
import AdminWPMResults from "./pages/Admin/AdminWPMResults";
import IncreaseBulkTime from "./pages/Admin/IncreaseBulkTime";
import DownloadRoll from "./pages/Admin/downloadRoll";
function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <AdminLogin />
        </Route>
        <Route exact path="/adminDashboard">
          <AdminDashboard />
        </Route>

        {/* Part Added - Yash */}

        <Route exact path="/adminViewSubmission">
          <AdminViewSubmission />
        </Route>

        <Route exact path="/adminLoginStatus">
          <AdminLoginStatus />
        </Route>
        <Route exact path="/increaseTime">
          <IncreaseTime />
        </Route>
        <Route exact path="/increaseBatchTime">
          <IncreaseBulkTime />
        </Route>
        <Route exact path="/resetValues">
          <ResetValues />
        </Route>
        <Route exact path="/adminWPMResults">
          <AdminWPMResults />
        </Route>
        <Route exact path="/downloadRoll">
          <DownloadRoll />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
