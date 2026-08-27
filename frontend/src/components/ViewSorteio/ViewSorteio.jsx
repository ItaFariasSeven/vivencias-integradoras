import styles from './ViewSorteio.module.css'

export default function ViewSorteio({grupo}){
    return (
        <div className={styles.container}>
            <span className={styles.grupo}>{grupo[0].titulo}</span>
            <ul>
                {grupo[0].nome.map((nome, index) => {
                    return (
                        <li key={index}>{nome}</li>
                    )
                })}
            </ul>
        </div>
    )
}