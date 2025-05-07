import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Primary from "./components/Primary";
import LatestNews from "./components/LatestNews";

const App = () => (
  <Router>
    <Routes>
      <Route path="/" element={<Primary />} />
      <Route path="/latest-news" element={<LatestNews />} />
    </Routes>
  </Router>
);

export default App;
