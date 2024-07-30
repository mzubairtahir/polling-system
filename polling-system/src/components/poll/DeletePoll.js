import { useAuth } from "@/context/AuthContext"
import { useMessage } from "@/context/MessageContext";
import useFetch from "@/utils/useFetch";
import { useRouter } from "next/navigation";
import { useEffect } from "react";



export default function DeletePoll({ poll_user_id, poll_id }) {
    const { fetchData, loading, data, error } = useFetch();
    const { user, setUser } = useAuth();
    const { setMessage } = useMessage();
    const router = useRouter();



    const deltePollHandle = async () => {
        await fetchData({ url: "/api/poll/delete", type: "POST", req_data: { id: +poll_id }, headers: { 'Content-Type': 'application/json' } })
    }

    useEffect(() => {
        if (!loading && data) {
            if (data.success) {
                setMessage("Poll Deleted!")

                router.push("/")
            }
            else {
                setMessage("Could not delete poll")
            }
        }
        if (error) {
            setMessage("Could not delete poll")
        }

    }, [loading, data, error])


    if (user.authenticated && user.user === poll_user_id) {
        return <>
            <button onClick={deltePollHandle} className="p-1 bg-red-600">
                {loading ? "Deleting poll..." : "Delete Poll"}
            </button>
        </>
    }
    return

}