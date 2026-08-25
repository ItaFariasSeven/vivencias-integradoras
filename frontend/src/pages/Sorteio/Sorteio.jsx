import styles from "./Sorteio.module.css";
import Input from "../../components/Input/Input.jsx";
import Button from "../../components/Button/Button.jsx";
import ViewSorteio from "../../components/ViewSorteio/ViewSorteio.jsx";

export default function Sorteio() {
  const grupo = [
    { titulo: "Grupo 4", nome: ["Joao", "Maria", "Claudia", "Oi", "Ai"] },
  ];

  return (
    <div className={styles.sorteio}>
      <div className={styles.header}>
        <h2>Tela de Sorteio</h2>
      </div>
      <div className={styles.boxSorteio}>
        <div className={styles.containerSorteio}>
          <div className={styles.cardSorteio}>
            <span>Entre em seu grupo</span>
            <Input
              styleInput={{ border: "2px solid #1f72e6" }}
              placeholder="Digite seu nome"
            ></Input>
            <Button size="large" version="bckBlueWhite">
              Sorteie Aqui
            </Button>
          </div>
          <div className={styles.cardGrupo}>
            <span>Seu grupo foi definido</span>
            <ViewSorteio grupo={grupo}> </ViewSorteio>
          </div>
        </div>
      </div>
    </div>
  );
}
