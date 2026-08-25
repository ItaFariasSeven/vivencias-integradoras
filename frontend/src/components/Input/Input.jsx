import styles from './Input.module.css'

export default function Input({children, styleLabel, styleInput, size, placeholder}){
    return (
        <div className={styles.containerInput}>
        <label className={styles.label} style={styleLabel} htmlFor="input">{children}</label>
        <input className={styles.input} style={styleInput} placeholder={placeholder} id='input' type="text" />
        </div>
    )
}