import styles from "./LoginAluno.module.css";
import Button from "../../../components/Button/Button";
import Input from "../../../components/Input/Input";

import { useContext, useEffect } from "react";
import { ContextNav } from "../../../context/ContextNav";

export default function LoginAluno() {
  const { cor, setCor } = useContext(ContextNav);

  useEffect(() => {
    setCor("branco");
  }, []);

  return (
    <main className={styles.login}>
      <section className={styles.containerLogin}>
        <div className={styles.cardLogin}>
          <span>
            Faça o seu <span className={styles.spanLogin}>login</span>
          </span>
          <div className={styles.camposInput}>
            <Input placeholder={"Ex: 12345"}>
              Digite seu <span className={styles.RA}>RA</span>:
            </Input>
            <Input placeholder={"•••••••••"}>
              Digite sua <span className={styles.senha}>senha</span>:
            </Input>
          </div>
          <Button version="bckBlue">Entre Já!</Button>
        </div>
      </section>
      <section className={styles.containerFoto}></section>
    </main>
  );
}
