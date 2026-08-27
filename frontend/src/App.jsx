import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Home from "./pages/Home/Home.jsx";
import LoginAluno from "./pages/Login/Aluno/LoginAluno.jsx";
import Sorteio from "./pages/Sorteio/Sorteio.jsx";
import NavBar from "./layout/NavBar/NavBar.jsx";
import Footer from "./layout/Footer/Footer.jsx";
import CadastroAluno from "./pages/Cadastro/Aluno/CadastroAluno.jsx";
import EixoGrupos from "./pages/EixoGrupos/EixoGrupos.jsx";

import { ProviderNav } from "./context/ContextNav.jsx";

import { AuthProvider } from "./context/AuthContext.jsx";

import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute.jsx";
import NotFound from "./pages/NotFound/NotFound.jsx";

function App() {
  return (
    <Router>

      <ProviderNav>

        <AuthProvider>

          <NavBar />

          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login-aluno" element={<LoginAluno />} />
            <Route path="/cadastro-aluno" element={<ProtectedRoute> <CadastroAluno /> </ProtectedRoute>} />
            <Route path="/sorteio" element={<ProtectedRoute> <Sorteio /> </ProtectedRoute>} />
            <Route path="/eixo/:eixoId" element={<ProtectedRoute> <EixoGrupos /> </ProtectedRoute>} />
            <Route path="*" element={<NotFound />} />
          </Routes>

          <Footer />

        </AuthProvider>

      </ProviderNav>

    </Router>
  );
}

export default App;
