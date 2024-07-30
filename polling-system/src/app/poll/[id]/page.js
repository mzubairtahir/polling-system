'use client'

import CenterPage from "@/components/CenterPage"
import DeletePoll from "@/components/poll/DeletePoll";
import DetailAndVote from "@/components/poll/DetailAndVote";
import { useMessage } from "@/context/MessageContext";
import useFetch from "@/utils/useFetch";
import { useEffect, useState } from "react";



export default function PollDetailPage({ params }) {
    const { setMessage } = useMessage();
    const { fetchData, loading, data, error } = useFetch();
    const [pollData, setPollData] = useState(null);


    const copyUrlHandle = () => {
        navigator.clipboard.writeText(location.href).then(function () {
            setMessage("Url Copied!")
        }).catch(function (err) {
            console.error('Failed to copy text: ', err);
        });

    }


    useEffect(() => {
        (async function () {
            if (!data) {

                await fetchData({ url: `/api/poll/detail?poll_id=${params.id}` })
            }
        })();

        if (!loading && data) {
            if (data.success) {
                setPollData(data.data);
            }
        }




    }, [loading, data, error])

    return (
        <CenterPage>



            <h1 className="my-4 text-center font-bold">Poll Detail 📊</h1>
            {(!loading && pollData) ?
                <div className="mx-auto bg-white p-6 rounded-lg shadow-md flex flex-row flex-wrap">
                    <DetailAndVote poll_data={pollData}></DetailAndVote>
                    {/* <div>jhi</div> */}


                    <div className="p-7"></div>
                    <div>
                        <div className="pb-8 bg-gradient-to-r from-blue-50 to-blue-100 p-6 rounded-lg shadow-lg mt-6">
                            <h3 className="text-2xl font-bold text-blue-800 mb-4">Votes Summary</h3>
                            {pollData.options.map((option, index) => (
                                <div key={index} className="flex items-center justify-between border-b border-gray-300 py-2">
                                    <p className="text-lg font-medium text-gray-800">{option.name}</p>
                                    <p className="text-lg font-semibold text-blue-600 pl-4">{option.total_votes} votes</p>
                                </div>
                            ))}
                        </div>
                        <div className="my-4 flex justify-center">
                            <button onClick={copyUrlHandle} className="p-1.5">Copy Poll Link</button>
                        </div>
                    </div>


                </div>

                : ((data && !pollData) ? <p>Oops! We couldn't find the poll you're looking for</p> : (error ? "Could not load the poll" : "Loading..."))}
        </CenterPage>
    );
}
