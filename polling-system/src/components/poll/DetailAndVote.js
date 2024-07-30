'use client'

import { useMessage } from "@/context/MessageContext";
import useFetch from "@/utils/useFetch";
import { useEffect, useState } from "react";
import RemoveVote from "./RemoveVote";
import DeletePoll from "./DeletePoll";


export default function DetailAndVote({ poll_data }) {
    const [voted, setVoted] = useState(false);
    const { fetchData, loading, data, error } = useFetch();
    const [votedOptionId, setVotedOptionId] = useState(null);
    const { setMessage } = useMessage();


    const onChangeRadio = (event) => {
        setVotedOptionId(event.target.value);

    }


    const handleVoteSubmit = async (event) => {
        event.preventDefault();

        const dataToSend = {
            poll_id: poll_data.id,
            option_id: +votedOptionId
        }

        await fetchData({ url: "/api/poll/vote/add", req_data: dataToSend, type: "POST", headers: { 'Content-Type': 'application/json' } })
    }


    const removeVote = () => {
        setVoted(false);
    }

    useEffect(() => {
        if (poll_data) {
            setVoted(poll_data.voted)
        }

        if (data) {
            if (data.success) {
                setVoted(true);
            }
            setMessage(data.message);
        }

    }, [poll_data, loading, data, error])

    return poll_data ? <>
        <div>
            <div className="flex flex-wrap">
                <h2 className="text-2xl font-bold mr-4">{poll_data.title}</h2>
                <DeletePoll poll_user_id={poll_data.user.id} poll_id={poll_data.id} />

            </div>
            <p className="text-xs text-gray-700 mb-6">Poll created by {poll_data.user.username}</p>

            <div className="flex justify-around">
                {poll_data.options.map((option, index) => (
                    <div key={index} className="text-center">
                        <img
                            src={option.picture}
                            alt={option.name}
                            className="object-cover w-32 h-32 rounded-full mx-auto mb-2"
                        />
                        <p className="text-lg pr-4 font-semibold">{option.name}</p>
                        {
                            voted ? null :
                                <input onChange={onChangeRadio} type="radio" name="vote" value={option.id} />
                        }
                    </div>
                ))}
            </div>
            <div className="flex justify-center my-4">
                {
                    voted ? (
                        <>
                            <div>

                                <div className="text-green-900 font-bold">You've already voted!</div>
                                <RemoveVote poll_id={poll_data.id} removeVote={removeVote} />
                            </div>
                        </>
                    ) :
                        <button disabled={votedOptionId === null} onClick={handleVoteSubmit} className="p-1.5">
                            {loading ? "Casting your vote" : "Vote"}
                        </button>
                }
            </div>
        </div>
    </> : "Loading..."
}