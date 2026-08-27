import styles from "./Button.module.css";
import clsx from "clsx";

export default function Button({
  size = "medium",
  version = "bckBlue",
  color = "white",
  border = false,
  style,
  children,
  ...props
}) {
  const button = clsx(
    styles.button,
    styles[size],
    styles[color],
    styles[version],
    border ? styles.border : '',
  );

  return <button style={style} className={button} {...props}>{children}</button>;
}
