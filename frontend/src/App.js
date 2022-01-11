import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Index from './pages/Index';
import './styles/global.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route exact path='/' element={ <Index /> }/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
