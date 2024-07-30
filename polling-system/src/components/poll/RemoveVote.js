import useFetch from "@/utils/useFetch";
import { useEffect } from "react";


export default function RemoveVote({ poll_id, removeVote }) {
    const { fetchData, loading, data, error } = useFetch();

    const removeVoteHandle = async (event) => {
        await fetchData({ url: "/api/poll/vote/remove", type: "POST", req_data: { "poll_id": +poll_id }, headers: { "Content-Type": "application/json" } })


    }

    useEffect(() => {
        if (data && data.success) {
            removeVote();
        }



    }, [loading, data, error])



    return (
        <div className="py-2 flex justify-center">
            <button onClick={removeVoteHandle} className="p-1">
                {loading ? "Removing Vote..." : "Remove Vote"}

            </button>
        </div>
    )
}