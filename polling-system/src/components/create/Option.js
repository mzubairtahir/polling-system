import styles from "../../styles/create.module.css"


export default function Option({ index }) {
    return <div className="my-2 poll-option">
        <h2>Option {index}</h2>
        <div className="py-4">

            <input required className={styles.plaininput} placeholder="Name" name={`name`} type="text" />
            <div className="input-bottom"></div>

        </div>
        <div>
            <input required
                className={` imageinput w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500`}
                type="file"
                name="photo"
                alt=""
            />

        </div>

    </div>
}