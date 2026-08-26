import styles from "./Home.module.css";
import { useAuth } from "../../context/AuthContext";

export default function Home() {
  const {
    usuario,
    carregando
  } = useAuth();


  if (carregando) {
    return <h1>Carregando...</h1>;
  }


  return (
    <>
      <h1>Home</h1>

      {usuario ? (
        <div>
          <p>
            Usuário: {usuario.nome}
          </p>

          <p>
            RA: {usuario.ra}
          </p>

          <p>
            Curso: {usuario.curso}
          </p>

          <p>
            Turno: {usuario.turno}
          </p>
        </div>
      ) : (
        <p>
          Nenhum usuário logado.
        </p>
      )}
    </>
  );
}