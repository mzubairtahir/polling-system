'use client'

import { useMessage } from "@/context/MessageContext"
import { useEffect, useRef } from "react"


export default function Message() {

    const { message, setMessage } = useMessage();
    const messageElem = useRef();



    const closeMessage = () => {
        setMessage("")
    }

    useEffect(() => {
        if (message !== null && message !== undefined && message !== '') {
            const timer = setTimeout(() => {
                closeMessage();
            }, 3000);

            // Cleanup function to clear the timeout if the message changes or component unmounts
            return () => clearTimeout(timer);
        }
    }, [message]);


    if (message === null || message === undefined || message === '') {
        return;
    }

    return <>

        <div ref={messageElem} id="message" className="bg-secondary p-4 rounded-lg shadow-lg max-w-sm w-full">

            <div className="flex items-center justify-between">
                <p className="text-gray-700 mt-4">
                    {/* This is an alert message. Please pay attention to this important information. */}
                    {message}
                </p>
                <button className="" onClick={closeMessage}>
                    <svg className="w-6 h-6" fill="white" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>

            </div>
        </div>
    </>

}

