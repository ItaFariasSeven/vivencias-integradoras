import styles from "./Input.module.css";

export default function Input({
  children,
  styleLabel,
  styleInput,
  size,
  placeholder,
  id,
  name,
  type = "text",
  value,
  onChange,
  ...props
}) {
  const inputId = id || name;

  return (
    <div className={styles.containerInput}>
      <label className={styles.label} style={styleLabel} htmlFor={inputId}>
        {children}
      </label>
      <input
        className={styles.input}
        style={styleInput}
        placeholder={placeholder}
        id={inputId}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        {...props}
      />
    </div>
  );
}
