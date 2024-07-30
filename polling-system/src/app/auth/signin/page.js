"use client";

import { useEffect } from 'react';
import style from "../../../styles/auth.module.css"
import useFetch from '@/utils/useFetch';
import { useMessage } from '@/context/MessageContext';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';


export default function SignIn() {
    const { fetchData, loading, data, error } = useFetch();
    const { setMessage } = useMessage();
    const router = useRouter();
    const { user, setUser } = useAuth();

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        await fetchData({ url: "/api/auth/signin", type: "POST", req_data: formData })
    }

    useEffect(() => {
        if (data) {
            if (data.success) {
                setUser({ authenticated: true, user: data.data.user })
                router.push("/");
            }
            const messageToShow = data.message;
            setMessage(messageToShow);
        }
        if (error) {
            setMessage("Could not logging in. Check Internet Connection");
        }


    }, [data, error, loading])


    return (
        <>
            <form onSubmit={handleSubmit} className="p-2 bg-secondary rounded">
                <div className="my-2">
                    <p className="text-center">Login</p>
                </div>
                <div>
                    <input required className={style.input} id="email" name="email" type="email" placeholder="Enter email"></input>
                    <small className="input-error"></small>
                </div>
                <div className="my-2">
                    <input required className={style.input} id="password" name="password" type="password" placeholder="Enter password"></input>
                    <small className="input-error"></small>

                </div>
                <div>
                    <button type="submit" className="p-1.5 w-full font-bold">
                        {loading ? "Wait...." : "Login"}
                    </button>
                </div>
                <p className='text-center'>
                    or
                </p>
                <div>
                    <a href="/auth/signup">
                        <button type='button' className='p-1 my-1 font-bold'>Sign Up</button>
                    </a>
                </div>
            </form>


        </>
    )
}