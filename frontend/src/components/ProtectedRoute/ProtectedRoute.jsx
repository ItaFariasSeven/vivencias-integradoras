import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { usuario, carregando } = useAuth();

  if (carregando) {
    return (
      <div>
        Carregando...
      </div>
    );
  }

  if (!usuario) {
    return (
      <Navigate
        to="/login-aluno"
        replace
      />
    );
  }

  return children;
}