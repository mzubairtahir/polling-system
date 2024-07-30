'use client'

import Link from "next/link";
import EditSvg from "@/components/EditSvg";



export default function CreatePollBtn() {



    return <>
        <Link href={"/create"} className="no-underline">
            <button className="p-1 flex items-center">

                <div className="mx-2">
                    <EditSvg />
                </div>
                Create Poll
            </button>
        </Link>
    </>


}