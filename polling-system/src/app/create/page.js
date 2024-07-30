'use client'

import CenterPage from "@/components/CenterPage";
import Title from "@/components/create/Title";
import Option from "@/components/create/Option";
import ExpiryDate from "@/components/create/ExpiryDate";
import useInputErrorDisplay from '@/utils/useInputErrorsDisplay';
import { useMessage } from '@/context/MessageContext';
import useFetch from "@/utils/useFetch";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

const prepareData = async () => {
    const data = {
        title: '',
        expiry_date: '',
        options: []
    };

    // Extract the title and expiry date from input fields
    const titleElement = document.getElementById('title');
    const expiryDateElement = document.getElementById('expiry_date');

    if (titleElement) {
        data.title = titleElement.value;
    }

    if (expiryDateElement) {
        data.expiry_date = expiryDateElement.value;
    }

    // Extract options from a list of option elements
    const optionElements = document.querySelectorAll('.poll-option');

    const readFilesPromises = Array.from(optionElements).map(optionElement => {
        const nameElement = optionElement.querySelector("input[name='name']");
        const pictureElement = optionElement.querySelector("input[name='photo']");

        const name = nameElement ? nameElement.value : '';
        let picture = '';

        if (pictureElement && pictureElement.files[0]) {
            const file = pictureElement.files[0];
            const reader = new FileReader();

            return new Promise((resolve) => {
                reader.onloadend = () => {
                    picture = reader.result;
                    data.options.push({
                        name,
                        picture
                    });
                    resolve();
                };
                reader.readAsDataURL(file);
            });
        } else {
            data.options.push({
                name,
                picture
            });
            return Promise.resolve();
        }
    });

    await Promise.all(readFilesPromises);

    return data;
};

export default function CreatePage() {
    const { fetchData, data, loading, error } = useFetch();
    const displayErrors = useInputErrorDisplay();
    const { setMessage } = useMessage();
    const router = useRouter();

    async function handleSubmit(event) {

        event.preventDefault();
        const post_data = await prepareData();

        await fetchData({ url: "/api/poll/new", type: "POST", req_data: post_data, headers: { 'Content-Type': 'application/json' } });
    }

    useEffect(() => {
        if (data) {
            if (data.success) {
                router.push(`/poll/${data.data.id}`)
            }
            const messageToShow = data.message;
            setMessage(messageToShow);
        }
        if (error) {
            setMessage("Could not logging in. Check Internet Connection");
        }
    }, [data, error, loading]);

    return (
        <CenterPage>
            <div>
                <form onSubmit={handleSubmit}>
                    <h1 className="text-center my-2">
                        Create Poll
                    </h1>
                    <Title />
                    <Option index={1} />
                    <Option index={2} />
                    <ExpiryDate />
                    <div className="my-8 flex justify-center">
                        <button disabled={loading} type="submit" className="p-1.5">
                            {loading ? "Uploading Poll..." : "Post"}
                        </button>
                    </div>
                </form>
            </div>
        </CenterPage>
    );
}
