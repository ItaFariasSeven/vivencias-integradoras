import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home/Home.jsx";
import LoginAluno from "./pages/Login/Aluno/LoginAluno.jsx";
import Sorteio from "./pages/Sorteio/Sorteio.jsx";
import NavBar from "./layout/NavBar/NavBar.jsx";
import Footer from "./layout/Footer/Footer.jsx";

import { ProviderNav } from "./context/ContextNav.jsx";

function App() {
  return (
    <Router>
      <ProviderNav>
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login-aluno" element={<LoginAluno />} />
          <Route path="/sorteio" element={<Sorteio />} />
        </Routes>
        <Footer />
      </ProviderNav>
    </Router>
  );
}

export default App;
