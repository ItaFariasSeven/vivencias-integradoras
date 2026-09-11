import styles from "./Sorteio.module.css";
import Input from "../../components/Input/Input.jsx";
import Button from "../../components/Button/Button.jsx";
import ViewSorteio from "../../components/ViewSorteio/ViewSorteio.jsx";
import { LuCircleUserRound as User} from "react-icons/lu";
import { PiGearSixLight as Gear} from "react-icons/pi";
import { MdVerifiedUser as Verified} from "react-icons/md";
import { useEffect, useState } from "react";
import { apiFetch } from "../../services/api.js";
import { useAuth } from "../../context/AuthContext.jsx";
import { useNavigate } from "react-router-dom";

export default function Sorteio() {
  const { usuario } = useAuth();

  const [eixos, setEixos] = useState([]);
  const [eixoSelecionado, setEixoSelecionado] = useState("");

  const [meuGrupo, setMeuGrupo] = useState(null);

  const [carregando, setCarregando] = useState(true);
  const [sorteando, setSorteando] = useState(false);

  const [erro, setErro] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    async function carregarDados() {
      try {
        setCarregando(true);
        setErro("");

        const [dadosEixos, dadosGrupo] = await Promise.all([
          apiFetch("/sorteio/eixos/"),
          apiFetch("/sorteio/meu-grupo/"),
        ]);

        setEixos(dadosEixos);
        console.log("Dados do grupo:", dadosEixos);
        if (dadosGrupo.grupo) {
          setMeuGrupo(dadosGrupo);
        }
      } catch (erro) {
        console.error("Erro ao carregar sorteio:", erro);
        setErro("Não foi possível carregar os dados do sorteio.");
      } finally {
        setCarregando(false);
      }
    }
    carregarDados();
  }, []);

  async function handleSortear() {
    if (!eixoSelecionado) {
      setErro("Selecione um eixo antes de sortear.");
      return;
    }

    try {
      setSorteando(true);
      setErro("");

      await apiFetch("/sorteio/sortear/", {
        method: "POST",
        body: JSON.stringify({
          eixo_id: Number(eixoSelecionado),
        }),
      });

      const dadosGrupo = await apiFetch("/sorteio/meu-grupo/");

      setMeuGrupo(dadosGrupo);
    } catch (erro) {
      console.error("Erro no sorteio:", erro);

      setErro(
        erro.data?.erro ||
          erro.message ||
          "Não foi possível realizar o sorteio.",
      );
    } finally {
      setSorteando(false);
    }
  }

  if (carregando) {
    return (
      <main className={styles.sorteio}>
        <div className={styles.loading}>Carregando sorteio...</div>
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

            {!meuGrupo ? (
              <>
                <h3>Escolha seu eixo</h3>

                <p>Selecione o eixo que deseja participar</p>

                <div className={styles.listaEixos}>
                  {eixos.map((eixo) => (
                    <Button
                      key={eixo.id}
                      type="button"
                      className={
                        Number(eixoSelecionado) === eixo.id
                          ? styles.eixoSelecionado
                          : styles.eixo
                      }
                      onClick={() => setEixoSelecionado(eixo.id)}
                    >
                      {" "}
                      <div className={styles.eixoDescricao}>
                        <Gear className={styles.gearIcon} />
                        <span>{eixo.nome_eixo}</span>
                        <p>{eixo.descricao}</p>
                      </div>
                      <div className={styles.eixoResponsavel}>
                       {eixo.professor_imagem ? <img src={eixo.professor_imagem}alt="Imagem do professor" /> : <User className={styles.userIcon} /> }
                        <div className={styles.cardResponsavel}>
                          <span className={styles.responsavel}>Responsável</span>
                          <span>
                            <strong>{eixo.professores_responsaveis}</strong> <Verified className={styles.verifiedIcon} />
                          </span>
                        </div>
                      </div>
                    </Button>
                  ))}
                </div>

                {erro && <p className={styles.erro}> {erro} </p>}

                <Button
                  size="large"
                  version="bckBlueWhite"
                  onClick={handleSortear}
                  disabled={sorteando || !eixoSelecionado}
                >
                  {sorteando ? "Sorteando..." : "Sortear meu grupo"}
                </Button>
              </>
            ) : (
              <div className={styles.resultado}>
                <span>Seu grupo foi definido</span>
                <h3>{meuGrupo.eixo.nome}</h3>

                <div className={styles.cardGrupo}>
                  <strong>{meuGrupo.grupo.nome}</strong>
                  <ul>
                    {meuGrupo.grupo.integrantes.map((integrante, index) => (
                      <li key={index}>
                        {integrante.nome}
                        <small>{integrante.curso}</small>
                      </li>
                    ))}
                  </ul>
                  <Button
                    version="bckBlue"
                    onClick={() => navigate(`/eixo/${meuGrupo.eixo.id}`)}
                  >
                    Ver Grupos do eixo
                  </Button>
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
