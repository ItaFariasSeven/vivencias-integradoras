// NavBar.jsx
import styles from "./NavBar.module.css";
import { Link } from "react-router-dom";
import { useContext, useState } from "react";
import { ContextNav } from "../../context/ContextNav.jsx";
import Button from "../../components/Button/Button.jsx";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext.jsx";
import { HiBars4 as Bars } from "react-icons/hi2";
import { IoIosArrowForward as ArrowRigth } from "react-icons/io";


export default function NavBar() {
  const [bars, setBars] = useState(false);
  const [mobileNavMounted, setMobileNavMounted] = useState(false);
  const { usuario, logout } = useAuth();
  const navigate = useNavigate();

  function toggleMobileNav() {
    if (bars) {
      setBars(false);
      return;
    }

    setMobileNavMounted(true);
    setBars(true);
  }

  async function handleLogout() {
    try {
      await logout();
      navigate("/login-aluno");
    } catch (erro) {
      console.error("Erro ao sair:", erro);
    }
  }

  const { cor, setCor } = useContext(ContextNav);

  return (
    <>
      <div className={styles.navBar}>
        <span style={{ color: cor === "branco" ? "#e2e7eb" : "" }}>
          IntegraGame
        </span>
        
        <Bars
          onClick={toggleMobileNav}
          className={styles.bars}
        />

        {/* Nav original do desktop (fica intacto) */}
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
              {usuario ? (
                <Button
                  style={{ fontSize: "16px", paddingLeft: "20px", paddingRight: "20px" }}
                  size="small"
                  version="bckBlue"
                  color="white"
                  onClick={handleLogout}
                >
                  Sair
                </Button>
              ) : (
                <Button
                  style={{ fontSize: "16px", paddingLeft: "20px", paddingRight: "20px" }}
                  size="small"
                  version="bckBlue"
                  color="white"
                >
                  <Link to="/login-aluno">Login</Link>
                </Button>
              )}
            </li>
          </ul>
        </nav>
      </div>

      {/* Novo Nav exclusivo para Mobile que ativa com position relative e blur */}
      {mobileNavMounted && (
        <>
          <div
            className={`${styles.mobileOverlay} ${!bars ? styles.mobileOverlayClosing : ""}`}
            onClick={() => setBars(false)}
            aria-hidden="true"
          />
          <div
            className={`${styles.mobileNav} ${!bars ? styles.mobileNavClosing : ""}`}
            onAnimationEnd={() => {
              if (!bars) {
                setMobileNavMounted(false);
              }
            }}
          >
            <button
              type="button"
              className={styles.closeMobileNav}
              onClick={() => setBars(false)}
              aria-label="Fechar menu"
            >
              <ArrowRigth />
            </button>
            <ul>
              <li className={styles.menu}>
                <Link to="#">Teste</Link>
              </li>
              <li className={styles.menu}>
                <Link to="#">Teste</Link>
              </li>
              <li className={styles.menu}>
                <Link to="#">Teste</Link>
              </li>
              <li>
                {usuario ? (
                  <Button
                    size="small"
                    version="bckBlue"
                    color="white"
                    onClick={handleLogout}
                  >
                    Sair
                  </Button>
                ) : (
                  <Button
                    size="small"
                    version="bckBlue"
                    color="white"
                  >
                    <Link to="/login-aluno">Login</Link>
                  </Button>
                )}
              </li>
            </ul>
          </div>
        </>
      )}
    </>
  );
}