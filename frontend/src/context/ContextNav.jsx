import { createContext, useContext, useState } from "react";

export const ContextNav = createContext();

export const ProviderNav = ({ children }) => {
  const [cor, setCor] = useState("azulEscuro");

  return (
    <ContextNav.Provider value={{ cor, setCor }}>
      {children}
    </ContextNav.Provider>
  );
};
