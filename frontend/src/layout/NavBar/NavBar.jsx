import styles from "./NavBar.module.css";
import { Link } from "react-router-dom";
import { useContext } from "react";

import { ContextNav } from "../../context/ContextNav.jsx";

import Button from "../../components/Button/Button.jsx";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext.jsx";

import { HiBars4 as Bars} from "react-icons/hi2";

export default function NavBar() {

  const { usuario, logout } = useAuth();
  const navigate = useNavigate();

  async function handleLogout() {
  try {
    await logout();
    navigate("/login-aluno");
  } catch (erro) {
    console.error("Erro ao sair:", erro);
    }
  }

  const {cor, setCor} = useContext(ContextNav)

  return (
    <div className={styles.navBar}>
      <span style={{color: cor === 'branco' ? '#e2e7eb' : ''}}>IntegraGame</span>
      <nav>
        <Bars className={styles.bars}/>
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
            {usuario? 
            (<Button style={{fontSize: '16px', paddingLeft: '20px', paddingRight: '20px'}} size="small" version="bckBlue" color="white" onClick={handleLogout}>
              Sair
            </Button> ) : (
            <Button style ={{fontSize: '16px', paddingLeft: '20px', paddingRight: '20px'}} size="small" version="bckBlue" color="white">
              <Link to='/login-aluno'>Login</Link>
            </Button>
            )} 
          </li>
        </ul>
      </nav>
    </div>
  );
}
