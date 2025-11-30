import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Welcome } from './pages/Welcome';
import { Interview } from './pages/Interview';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/interview/:sessionId" element={<Interview />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;