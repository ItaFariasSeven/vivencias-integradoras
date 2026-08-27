import styles from "./EixoGrupos.module.css";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Button from "../../components/Button/Button";
import { apiFetch } from "../../services/api";

export default function EixoGrupos() {

  const { eixoId } = useParams();

  const navigate = useNavigate();

  const [dados, setDados] = useState(null);

  const [carregando, setCarregando] =
    useState(true);

  const [erro, setErro] =
    useState("");


  useEffect(() => {

    async function carregarGrupos() {

      try {

        setCarregando(true);
        setErro("");

        const resposta =
          await apiFetch(
            `/sorteio/eixos/${eixoId}/grupos/`
          );

        setDados(resposta);

      } catch (erro) {

        console.error(
          "Erro ao carregar grupos:",
          erro
        );

        setErro(
          erro.data?.detail ||
          erro.data?.erro ||
          "Não foi possível carregar os grupos."
        );

      } finally {

        setCarregando(false);

      }
    }

    carregarGrupos();

  }, [eixoId]);


  if (carregando) {

    return (
      <main className={styles.pagina}>
        <p>Carregando grupos...</p>
      </main>
    );
  }


  if (erro) {

    return (
      <main className={styles.pagina}>

        <p className={styles.erro}>
          {erro}
        </p>

        <Button
          onClick={() =>
            navigate("/sorteio")
          }
        >
          Voltar
        </Button>

      </main>
    );
  }

return (
    <main className={styles.pagina}>

      <div className={styles.header}>

        <div>
          <h1>
            {dados.eixo.nome}
          </h1>

          <p>
            Confira os grupos deste eixo.
          </p>
        </div>


        <Button onClick={() => navigate("/sorteio")} >
          Meu grupo
        </Button>

      </div>

      <section className={styles.grupos}>

        {dados.grupos.map((grupo) => (

          <article
            key={grupo.id}
            className={styles.cardGrupo}
          >

            <h2>
              {grupo.nome}
            </h2>


            <span className={styles.quantidade}>
              {grupo.integrantes.length} / 10
            </span>


            {grupo.integrantes.length === 0 ? (

              <p className={styles.vazio}>
                Nenhum integrante ainda.
              </p>

            ) : (

              <ul>

                {grupo.integrantes.map(
                  (integrante, index) => (

                    <li key={index}>

                      <span>
                        {integrante.nome}
                      </span>

                      <small>
                        {integrante.curso}
                      </small>

                    </li>

                  )
                )}

              </ul>

            )}

          </article>

        ))}

      </section>

    </main>
  );
}