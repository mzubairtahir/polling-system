// components/NavBar.js
'use client'

import Link from 'next/link';

export default function NavBar() {
    return (
        <nav className="bg-blue-600 p-4">
            <div className="container mx-auto flex justify-between items-center">
                <div className="text-white text-2xl font-bold">
                    <Link className='text-white' href="/">
                        e-Poll
                    </Link>
                </div>
                <div className="flex flex-wrap space-x-4 text-white">
                    <Link className="text-white  hover:bg-blue-500 px-3 py-2 rounded" href="/create">
                        Create Poll
                    </Link>
                    <Link className="text-white hover:bg-blue-500 px-3 py-2 rounded" href="/profile">
                        Profile
                    </Link>
                    <Link className="text-white hover:bg-blue-500 px-3 py-2 rounded" href="/auth/signin">
                        Login
                    </Link>
                </div>
            </div>
        </nav>
    );
}
