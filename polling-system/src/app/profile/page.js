'use client'
import CenterPage from "@/components/CenterPage";
import CreatePollBtn from "@/components/CreatePollBtn";
import { useAuth } from "@/context/AuthContext";
import useFetch from "@/utils/useFetch";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";


function LogOut() {
    const { fetchData, loading, data, error } = useFetch();
    const router = useRouter();
    const { user, setUser } = useAuth();

    const logOutHandle = async () => {
        await fetchData({ url: "/api/auth/logout", type: "POST" })

    }

    useEffect(() => {
        if (data && data.success) {
            setUser({ authenticated: false, user: null })
            router.push("/auth/signin")
        }

    }, [loading, data])


    return <>
        <button onClick={logOutHandle} className="px-4 py-2 bg-[var(--accent-color)] text-white rounded-md hover:bg-[var(--hover-color)]">
            {loading ? "Logging Out..." : "Logout"}
        </button>
    </>

}

export default function ProfilePage() {

    const { fetchData, loading, data, error } = useFetch();
    const [userData, setUserData] = useState();

    useEffect(() => {
        if (!loading && !data && !error) {

            (async function () {
                await fetchData({ url: "/api/auth/profile" })
            })();
        }


        if (data && data.success && !userData) {
            setUserData(data.data)
        }


    }, [loading, data])


    return (
        <CenterPage>
            {!data ? "Loading..." : (
                (((data && !userData) || error) ?
                    "Could not load your profile" :
                    <div className="max-w-4xl mx-auto p-6 bg-gray-100">
                        <div className="flex justify-between items-center mb-8">
                            <h1 className="text-4xl font-extrabold text-gray-900">Your Profile</h1>
                            <LogOut />
                        </div>
                        <div className="flex flex-col lg:flex-row gap-6">
                            {/* User Info Section */}
                            <div className="bg-white shadow-lg rounded-lg p-6 flex-1">
                                <h2 className="text-2xl font-semibold text-gray-800 mb-4">User Information</h2>
                                <div className="space-y-4">
                                    <div>
                                        <h3 className="text-lg font-medium text-gray-600">Username</h3>
                                        <p className="text-gray-800">{userData.username}</p>
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-medium text-gray-600">Email</h3>
                                        <p className="text-gray-800">{userData.email}</p>
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-medium text-gray-600">First Name</h3>
                                        <p className="text-gray-800">{userData.first_name}</p>
                                    </div>
                                    <div>
                                        <h3 className="text-lg font-medium text-gray-600">Last Name</h3>
                                        <p className="text-gray-800">{userData.last_name}</p>
                                    </div>
                                </div>
                            </div>
                            {/* User Polls Section */}
                            <div className="bg-white shadow-lg rounded-lg p-6 flex-1">
                                <h2 className="text-2xl font-semibold text-gray-800 mb-4">Your Polls</h2>
                                {userData.polls.length === 0 ? (
                                    <div className="text-center">
                                        <p className="text-gray-600 mb-4">You have not created any polls yet.</p>
                                        <CreatePollBtn />
                                    </div>
                                ) : (
                                    <ul className="list-disc pl-5 space-y-2">
                                        {userData.polls.map((poll, index) => (
                                            <li key={index}>
                                                <Link href={`/poll/${poll.id}`} className="text-blue-500 hover:text-blue-700 hover:underline">
                                                    {poll.title}
                                                </Link>
                                            </li>
                                        ))}
                                    </ul>
                                )}
                            </div>
                        </div>
                    </div>
                )
            )}
        </CenterPage>

    );
}
