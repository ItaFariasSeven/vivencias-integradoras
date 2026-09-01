import styles from "./CadastroAluno.module.css";

import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import Button from "../../../components/Button/Button";
import Input from "../../../components/Input/Input";

import { apiFetch } from "../../../services/api";
import { useAuth } from "../../../context/AuthContext";

export default function CadastroAluno() {

  const navigate = useNavigate();

  const {
    usuario,
    carregando,
  } = useAuth();


  const [formulario, setFormulario] = useState({
    nome: "",
    sobrenome: "",
    email: "",
    ra: "",
    data_nascimento: "",
    curso: "",
    turno: "NOTURNO",
    senha: "",
    confirmar_senha: "",
  });


  const [erro, setErro] = useState("");
  const [enviando, setEnviando] = useState(false);


  useEffect(() => {

    if (!carregando && usuario) {
      navigate("/sorteio");
    }

  }, [
    usuario,
    carregando,
    navigate,
  ]);


  function handleChange(event) {

    const {
      name,
      value,
    } = event.target;

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }));
  }


  async function handleSubmit(event) {

    event.preventDefault();

    if(enviando) {
      return;
    }

    setErro("");
    setEnviando(true);


    // if (
    //   !formulario.nome.trim() ||
    //   !formulario.sobrenome.trim() ||
    //   !formulario.email.trim() ||
    //   !formulario.ra.trim() ||
    //   !formulario.data_nascimento ||
    //   !formulario.curso ||
    //   !formulario.turno ||
    //   !formulario.senha ||
    //   !formulario.confirmar_senha
    // ) {
    //   setErro(
    //     "Preencha todos os campos."
    //   );

    //   return;
    // }


    // if (
    //   formulario.senha !==
    //   formulario.confirmar_senha
    // ) {
    //   setErro(
    //     "As senhas não coincidem."
    //   );

    //   return;
    // }


    try {

      await apiFetch(
        "/auth/cadastro/", {
          method: "POST",

          body: JSON.stringify(formulario),

          // body: JSON.stringify({
          //   // nome,
          //   // sobrenome,
          //   // email,
          //   // ra,
          //   // data_nascimento,
          //   // curso,
          //   // turno,
          //   // senha,
          //   // confirmar_senha,
          // }),
        }
      );


      navigate(
        "/login-aluno", {
          state: {
            mensagem:
              "Cadastro realizado com sucesso. Faça seu login.",
          },
        }
      );


    } catch (error) {

      console.error(
        "Erro no cadastro:",
        error
      );

      setErro(
        error.message || "Não foi possível realizar o cadastro"
      );

    } finally {
      setEnviando(false);
    }
  }

    //   if (
    //     erro.data &&
    //     typeof erro.data === "object"
    //   ) {

    //     const mensagens =
    //       Object.values(erro.data)
    //         .flat()
    //         .join(" ");

    //     setErro(
    //       mensagens ||
    //       "Não foi possível realizar o cadastro."
    //     );

    //   } else {

    //     setErro(
    //       "Não foi possível realizar o cadastro."
    //     );

    //   }

    // } finally {

    //   setEnviando(false);

    // }


  return (
    <main className={styles.cadastro}>

      <section
        className={styles.containerCadastro}
      >

        <form
          className={styles.cardCadastro}
          onSubmit={handleSubmit}
        >

          <div className={styles.titulo}>
            <h1>Crie sua conta</h1>

            <p>
              Cadastre seus dados para participar
              das Vivências Integradoras.
            </p>
          </div>


          {erro && (
            <p className={styles.erro}>
              {erro}
            </p>
          )}


          <div className={styles.campos}>

            <div className={styles.duasColunas}>

              <Input
                id="nome"
                name="nome"
                value={formulario.nome}
                onChange={handleChange}
                placeholder="Seu nome"
                autoComplete="given-name"
              >
                Nome
              </Input>


              <Input
                id="sobrenome"
                name="sobrenome"
                value={formulario.sobrenome}
                onChange={handleChange}
                placeholder="Seu sobrenome"
                autoComplete="family-name"
              >
                Sobrenome
              </Input>

            </div>


            <Input
              id="email"
              name="email"
              type="email"
              value={formulario.email}
              onChange={handleChange}
              placeholder="exemplo@email.com"
              autoComplete="email"
            >
              E-mail
            </Input>


            <div className={styles.duasColunas}>

              <Input
                id="ra"
                name="ra"
                value={formulario.ra}
                onChange={handleChange}
                placeholder="Ex: 12345"
              >
                RA
              </Input>


              <Input
                id="data_nascimento"
                name="data_nascimento"
                type="date"
                value={formulario.data_nascimento}
                onChange={handleChange}
              >
                Data de nascimento
              </Input>

            </div>


            <div className={styles.duasColunas}>

              <div className={styles.campoSelect}>

                <label htmlFor="curso">
                  Curso
                </label>

                <select
                  id="curso"
                  name="curso"
                  value={formulario.curso}
                  onChange={handleChange}
                  required
                >
                  <option value="">
                    Selecione
                  </option>

                  <option value="PEDAGOGIA">
                    Pedagogia
                  </option>

                  <option value="ENFERMAGEM">
                    Enfermagem
                  </option>

                  <option value="DIREITO">
                    Direito
                  </option>

                  <option value="ADS">
                    ADS
                  </option>

                  <option value="PSICOLOGIA">
                    Psicologia
                  </option>

                  <option value="PEDAGOGIA_EAD">
                    Pedagogia EAD
                  </option>
                </select>

              </div>


              <div className={styles.campoSelect}>

                <label htmlFor="turno">
                  Turno
                </label>

                <select
                  id="turno"
                  name="turno"
                  value={formulario.turno}
                  onChange={handleChange}
                  required
                >
                  <option value="NOTURNO">
                    Noturno
                  </option>

                  {/* <option value="MATUTINO">
                    Matutino
                  </option> */}
                </select>

              </div>

            </div>


            <div className={styles.duasColunas}>

              <Input
                id="senha"
                name="senha"
                type="password"
                value={formulario.senha}
                onChange={handleChange}
                placeholder="••••••••"
                autoComplete="new-password"
              >
                Senha
              </Input>


              <Input
                id="confirmar_senha"
                name="confirmar_senha"
                type="password"
                value={formulario.confirmar_senha}
                onChange={handleChange}
                placeholder="••••••••"
                autoComplete="new-password"
              >
                Confirmar senha
              </Input>

            </div>

          </div>


          <Button
            type="submit"
            version="bckBlue"
            disabled={enviando}
          >
            {enviando
              ? "Cadastrando..."
              : "Criar minha conta"}
          </Button>


          <p className={styles.login}>
            Já possui uma conta?{" "}

            <Link to="/login-aluno">
              Faça login
            </Link>
          </p>

        </form>

      </section>


      <section
        className={styles.containerFoto}
      />

    </main>
  );
}