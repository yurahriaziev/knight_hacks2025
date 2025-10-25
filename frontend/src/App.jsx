import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from "./pages/LandingPage"
import Simulate from './pages/Simulate';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path='/simulate' element={<Simulate />} />
      </Routes>
    </Router>
  )
}

export default App
