import { useCallback, useState } from "react";


function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}



function useFetch() {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const fetchData = useCallback(async ({ url, type = 'GET', req_data = null, json = true, headers = {} }) => {
        setLoading(true);
        setData(null);
        setError(null);

        try {
            const csrfToken = getCookie('csrftoken');


            const options = {
                method: type,
                headers: {
                    // 'Content-Type': json ? 'application/json' : 'text/plain',
                    'X-CSRFToken': csrfToken,
                    ...headers
                },
                body: req_data instanceof FormData ? req_data : (req_data ? JSON.stringify(req_data) : null)

            };

            const response = await fetch(url, options);
            if (response.status === 401) {
                window.location.href = "/auth/signin"
            }


            const result = json ? await response.json() : await response.text();
            setData(result);
            setError(null);
        } catch (err) {
            setError(err.message);
            setData(null);
        } finally {
            setLoading(false);
        }
    });

    return { fetchData, data, loading, error };

}

export default useFetch;