import { Link } from "react-router-dom";


export default function NotFound() {
  return (
    <main>
      <h1>404</h1>

      <h2>
        Página não encontrada
      </h2>

      <p>
        O endereço informado não existe.
      </p>

      <Link to="/">
        Voltar para o início
      </Link>
    </main>
  );
}