import styles from "./Home.module.css";
import { useAuth } from "../../context/AuthContext";

export default function Home() {

  const { usuario } = useAuth();

  {usuario && (
    <p>
      Bem-vindo, {usuario.nome}!
    </p>
  )}

  // return (
  
  // )
}