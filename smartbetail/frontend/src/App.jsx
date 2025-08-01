import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import Predict from './components/Predict';
import Schedule from './components/Schedule';
import Animals from './components/Animals';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/schedule" element={<Schedule />} />
          <Route path="/animals" element={<Animals />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
