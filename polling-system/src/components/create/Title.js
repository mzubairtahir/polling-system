import styles from "../../styles/create.module.css"

export default function Title() {
    return <div className="my-4">
        <input required className={styles.plaininput} placeholder="Give a Title" id="title" name="title" type="text" />
        <div className="input-bottom"></div>

    </div>
}