'use client'

import useFetch from "@/utils/useFetch";
import style from "../../../styles/auth.module.css"
import useInputErrorDisplay from '@/utils/useInputErrorsDisplay';
import { useMessage } from '@/context/MessageContext';
import { useRouter } from 'next/navigation';
import { useEffect, useRef } from "react";

export default function SignUp() {
    const { fetchData, loading, data, error } = useFetch();
    const displayErrors = useInputErrorDisplay();
    const { setMessage } = useMessage();
    const router = useRouter();

    const password = useRef(null);
    const confirmPassword = useRef(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (password.current.value != confirmPassword.current.value) {
            setMessage("Your password does not match with confirm password")
            return
        }
        const formData = new FormData(event.target);
        await fetchData({ url: "/api/auth/signup", type: "POST", req_data: formData })

    }

    useEffect(() => {
        if (data) {
            if (!data.success) {

                displayErrors(data.errors);
            }
            else {
                router.push("/auth/signin");

            }
            const messageToShow = data.message;
            setMessage(messageToShow);

        }
        if (error) {
            setMessage("Could not create account. Check Internet Connection");
        }


    }, [data, error, loading])

    return (
        <>
            <form onSubmit={handleSubmit} className="p-2 bg-secondary rounded">
                <div className="my-2">
                    <p className="text-center">Create Account</p>
                </div>
                <div>
                    <input required className={style.input} id="email" type="email" name="email" placeholder="Email"></input>
                    <small className="input-error"></small>
                </div>
                <div>
                    <input required className={style.input} id="first_name" name="first_name" placeholder="First Name"></input>
                </div>
                <div>
                    <input required className={style.input} id="last_name" name="last_name" placeholder="Last Name"></input>
                </div>
                <div>
                    <input required className={style.input} id="username" name="username" placeholder="Username"></input>
                    <small className="input-error"></small>

                </div>
                <div className="my-2">
                    <input required ref={password} className={style.input} id="password" type="password" name="password" placeholder="Enter password"></input>

                </div>
                <div className="my-2">
                    <input required ref={confirmPassword} className={style.input} id="confirmPassword" type="password" name="confirmPassword" placeholder="Confirm password"></input>
                </div>
                <div className="">
                    <button type="submit" className="p-1.5 w-full font-bold">
                        {loading ? "Creating account..." : "Sign Up"}
                    </button>
                </div>
                <p className="text-center">or</p>
                <div>
                    <a href="/auth/signup">
                        <button type='button' className='p-1 my-1 font-bold'>Sign In</button>
                    </a>
                </div>
            </form>


        </>
    )
}