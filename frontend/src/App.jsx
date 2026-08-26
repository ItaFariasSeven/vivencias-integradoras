import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home/Home.jsx";
import LoginAluno from "./pages/Login/Aluno/LoginAluno.jsx";
import Sorteio from "./pages/Sorteio/Sorteio.jsx";
import NavBar from "./layout/NavBar/NavBar.jsx";
import Footer from "./layout/Footer/Footer.jsx";
import CadastroAluno from "./pages/Cadastro/Aluno/CadastroAluno.jsx";

import { ProviderNav } from "./context/ContextNav.jsx";

import { AuthProvider } from "./context/AuthContext.jsx";

function App() {
  return (
    <Router>

      <ProviderNav>

        <AuthProvider>

          <NavBar />

          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login-aluno" element={<LoginAluno />} />
            <Route path="/cadastro-aluno" element={<CadastroAluno />} />
            <Route path="/sorteio" element={<Sorteio />} />
          </Routes>

          <Footer />

        </AuthProvider>

      </ProviderNav>

    </Router>
  );
}

export default App;
