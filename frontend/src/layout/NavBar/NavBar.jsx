import styles from "./NavBar.module.css";
import { Link } from "react-router-dom";
import { useContext } from "react";

import { ContextNav } from "../../context/ContextNav.jsx";

import Button from "../../components/Button/Button.jsx";

export default function NavBar() {

  const {cor, setCor} = useContext(ContextNav)

  return (
    <div className={styles.navBar}>
      <span style={{color: cor === 'branco' ? '#e2e7eb' : ''}}>IntegraGame</span>
      <nav>
        <ul>
          <li className={styles.menu}>
            <Link>Teste</Link>
          </li>
          <li className={styles.menu}>
            <Link>Teste</Link>
          </li>
          <li className={styles.menu}>
            <Link>Teste</Link>
          </li>
          <li>
            <Button style={{fontSize: '16px', paddingLeft: '20px', paddingRight: '20px'}} size="small" version="bckBlue" color="white">
              <Link to='/login-aluno'>Login</Link>
            </Button>
          </li>
        </ul>
      </nav>
    </div>
  );
}
