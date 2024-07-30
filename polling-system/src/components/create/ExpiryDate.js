
export default function ExpiryDate() {
    return <div className="my-4">
        <h2>Expiry Date</h2>

        <input  required
            type="datetime-local"
            id="expiry_date"
            name="expiry-date"
            className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />


    </div>
}