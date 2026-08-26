import styles from "./Sorteio.module.css";
import Input from "../../components/Input/Input.jsx";
import Button from "../../components/Button/Button.jsx";
import ViewSorteio from "../../components/ViewSorteio/ViewSorteio.jsx";
import { useEffect, useState } from "react";
import { apiFetch } from "../../services/api.js";
import { useAuth } from "../../context/AuthContext.jsx";

export default function Sorteio() {
  const { usuario } = useAuth();

  const [eixos, setEixos] = useState([]);
  const [eixoSelecionado, setEixoSelecionado] = useState("");

  const [meuGrupo, setMeuGrupo] = useState(null);

  const [carregando, setCarregando] = useState(true);
  const [sorteando, setSorteando] = useState(false);

  const [erro, setErro] = useState("");

  useEffect(() => {
    async function carregarDados() {

      try {
        setCarregando(true);
        setErro("");

        const [
          dadosEixos,
          dadosGrupo
        ] = await Promise.all([
          apiFetch("/sorteio/eixos/"),
          apiFetch("/sorteio/meu-grupo/")
        ]);

        setEixos(dadosEixos);
        if (dadosGrupo.grupo) {
          setMeuGrupo(dadosGrupo);
        }

        } catch (erro) {
          console.error(
            "Erro ao carregar sorteio:",
            erro
          );
          setErro(
            "Não foi possível carregar os dados do sorteio."
          );
        } finally {
          setCarregando(false);
        }
      }
      carregarDados();
    }, []);

async function handleSortear() {
    if (!eixoSelecionado) {
      setErro(
        "Selecione um eixo antes de sortear."
      );
      return;
    }

    try {
      setSorteando(true);
      setErro("");

      await apiFetch(
        "/sorteio/sortear/",
        {
          method: "POST",
          body: JSON.stringify({
            eixo_id:
              Number(eixoSelecionado)
          })
        }
      );

      const dadosGrupo =
        await apiFetch(
          "/sorteio/meu-grupo/"
        );

      setMeuGrupo(dadosGrupo);

    } catch (erro) {
      console.error(
        "Erro no sorteio:",
        erro
      );

      setErro(
        erro.data?.erro ||
        erro.message ||
        "Não foi possível realizar o sorteio."
      );

    } finally {
      setSorteando(false);
    }
  }

  if (carregando) {
    return (
      <main className={styles.sorteio}>
        <div className={styles.loading}>
          Carregando sorteio...
        </div>
      </main>
    );
  }


  return (
    <main className={styles.sorteio}>
      <div className={styles.header}>
        <h2>Tela de Sorteio</h2>
      </div>

      <div className={styles.boxSorteio}>
        <div className={styles.containerSorteio}>
          <div className={styles.cardSorteio}>

            <span>Olá, {usuario?.nome}</span>

            {!meuGrupo? (
              <>
                <h3>
                  Escolha seu eixo
                </h3>

                <p>
                  Selecione o eixo que deseja participar
                </p>

                <div className={styles.listaEixos}>
                  {eixos.map((eixo) =>(
                    <Button key={eixo.id} type='button' className={Number(eixoSelecionado) === eixo.id ? styles.eixoSelecionado : styles.eixo}
                    onClick={() => setEixoSelecionado(eixo.id)}> {eixo.nome_eixo} </Button>
                  ))}
                </div>

                {erro && (
                  <p className={styles.erro}> {erro} </p>
                )}

                <Button size='large' version="bckBlueWhite" onClick={handleSortear} disabled={sorteando || !eixoSelecionado}>
                  {sorteando ? 'Sorteando...' : "Sortear meu grupo"}
                </Button>
              </>
            ) : (
              <div className={styles.resultado}>
                <span>
                  Seu grupo foi definido
                </span>
                <h3>
                  {meuGrupo.eixo.nome}
                </h3>

                <div className={styles.cardGrupo}>
                  <strong>
                    {meuGrupo.grupo.nome}
                  </strong>
                  <ul>
                    {meuGrupo.grupo.integrantes.map(
                      (
                        integrante, index
                      ) => (
                        <li key={index}>
                          {integrante.nome}
                            <small>
                              {integrante.curso}
                            </small>
                        </li>
                      )
                    )}
              </ul>
            </div>
          </div>
        )}
       </div>
      </div>
    </div>
  </main>
);
}      
    //         <Input
    //           styleInput={{ border: "2px solid #1f72e6" }}
    //           placeholder="Digite seu nome"
    //         ></Input>
    //         <Button size="large" version="bckBlueWhite">
    //           Sorteie Aqui
    //         </Button>
    //       </div>
    //       <div className={styles.cardGrupo}>
    //         <span>Seu grupo foi definido</span>
    //         <ViewSorteio grupo={grupo}> </ViewSorteio>
    //       </div>
    //     </div>
    //   </div>
    // </div>
//   );
// }
