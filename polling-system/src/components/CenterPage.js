

export default function CenterPage({ children }) {
    return <>
        <div className="flex justify-center w-full">
            <div className="centerpage px-2">

            {children}
            </div>
        </div>
    </>

}