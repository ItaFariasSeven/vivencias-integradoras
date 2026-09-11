import styles from "./LoginAluno.module.css";
import Button from "../../../components/Button/Button";
import Input from "../../../components/Input/Input";
import inputStyles from "../../../components/Input/Input.module.css";

import { useContext, useEffect, useState } from "react";
import { ContextNav } from "../../../context/ContextNav";
import { useAuth } from "../../../context/AuthContext";
import { FaEyeSlash as EyesClose } from "react-icons/fa";
import { IoEyeSharp as EyesOpen} from "react-icons/io5";

import { Link, useLocation, useNavigate } from "react-router-dom";

export default function LoginAluno() {
  const { cor, setCor } = useContext(ContextNav);

  const { login, usuario, carregando } = useAuth();

  const navigate = useNavigate();
  const location = useLocation();

  const [ra, setRa] = useState("");
  const [senha, setSenha] = useState("");
  const [passwordVisible, setPasswordVisible] = useState(false);

  const [erro, setErro] = useState("");
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    setCor("branco");
  }, [setCor]);

  useEffect(() => {
    if (!carregando && usuario) {
      navigate("/sorteio");
    }
  }, [usuario, carregando, navigate]);

  async function handleSubmit(event) {
    event.preventDefault();

    setErro("");

    if (!ra.trim() || !senha) {
      setErro("Informe seu RA e sua senha.");

      return;
    }

    try {
      setEnviando(true);

      await login(ra.trim(), senha);
    } catch (erro) {
      console.error("Erro no login:", erro);

      if (erro.status === 400 || erro.status === 401) {
        setErro(erro.data?.erro || "RA ou senha inválidos.");
      } else {
        setErro("Não foi possível entrar. Tente novamente.");
      }
    } finally {
      setEnviando(false);
    }
  }

  function togglePasswordVisibility() {
    setPasswordVisible(!passwordVisible);
  }

  return (
    <main className={styles.login}>
      <section className={styles.containerLogin}>
        <form className={styles.cardLogin} onSubmit={handleSubmit}>
          {/* <div className={styles.cardLogin}> */}

          <span>
            Faça o seu <span className={styles.spanLogin}>login</span>
          </span>

          <div className={styles.camposInput}>
            {location.state?.mensagem && (
              <p className={styles.sucesso}>{location.state.mensagem}</p>
            )}

            <div className={styles.input}>
              <Input
                id="ra"
                name="ra"
                value={ra}
                onChange={(event) => setRa(event.target.value)}
                placeholder={"Ex: 12345"}
                autoComplete="username"
              >
                Digite seu <span className={styles.RA}>RA</span>:
              </Input>
            </div>

            <div className={styles.input}>
              <div
                className={`${inputStyles.containerInput} ${styles.inputContainer}`}
              >
                <label htmlFor="senha">
                  Digite sua <span className={styles.senha}>senha</span>:
                </label>
                <div className={styles.inputSenha}>
                  <input
                    style={{ width: "100%" }}
                    className={inputStyles.input}
                    id="senha"
                    name="senha"
                    type={passwordVisible ? "text" : "password"}
                    value={senha}
                    onChange={(event) => setSenha(event.target.value)}
                    placeholder={"•••••••••"}
                    autoComplete="current-password"
                  />{" "}
                 {passwordVisible ? <EyesOpen
                    className={styles.eyesIcon}
                    onClick={togglePasswordVisibility}
                  /> : <EyesClose
                    className={styles.eyesIcon}
                    onClick={togglePasswordVisibility}
                  />}
                </div>
              </div>
            </div>
          </div>

          {erro && <p className={styles.erro}>{erro}</p>}
          <Button type="submit" version="bckBlue" disabled={enviando}>
            {enviando ? "entrando..." : "Entre já"}
          </Button>

          <p className={styles.cadastro}>
            Ainda não possui uma conta?{" "}
            <Link to="/cadastro-aluno">Cadastre-se</Link>
          </p>
          {/* </div> */}
        </form>
      </section>
      <section className={styles.containerFoto}></section>
    </main>
  );
}
