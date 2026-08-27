import { createContext, useContext, useEffect, useState } from "react";
import { apiFetch, prepararCsrf } from "../services/api";

const AuthContext = createContext(null);


export function AuthProvider({ children }) {

  const [usuario, setUsuario] = useState(null);

  const [carregando, setCarregando] = useState(true);


  async function verificarSessao() {
    try {

      const dados = await apiFetch(
        "/auth/me/"
      );

      setUsuario(dados);

    } catch (erro) {

      if (
        erro.status === 401 ||
        erro.status === 403
      ) {
        setUsuario(null);
        return;
      }

      console.error(
        "Erro ao verificar sessão:",
        erro
      );

      setUsuario(null);

    } finally {
      setCarregando(false);
    }
  }


  async function login(ra, senha) {

    const dados = await apiFetch(
      "/auth/login/",
      {
        method: "POST",

        body: JSON.stringify({
          ra,
          senha,
        }),
      }
    );

    setUsuario(dados.usuario);

    return dados;
  }


  async function logout() {

    await apiFetch(
      "/auth/logout/",
      {
        method: "POST",
      }
    );

    setUsuario(null);
  }


  useEffect(() => {

    async function iniciar() {

      try {
        await prepararCsrf();
      } catch (erro) {
        console.error(
          "Erro ao preparar CSRF:",
          erro
        );
      }

      await verificarSessao();
    }

    iniciar();

  }, []);


  return (
    <AuthContext.Provider
      value={{
        usuario,
        carregando,
        login,
        logout,
        verificarSessao,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {

  const contexto = useContext(
    AuthContext
  );

  if (!contexto) {
    throw new Error(
      "useAuth deve ser utilizado dentro de AuthProvider."
    );
  }

  return contexto;
}