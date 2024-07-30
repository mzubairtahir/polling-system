
'use client'

const { createContext, useContext, useState, useEffect } = require("react");



const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState({ authenticated: false, user: null });

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        (async function () {
            const response = await fetch("/api/auth/session", {
                method: "GET",
            })
            if (response.status === 401) {
            }
            else {
                const data = await response.json()
                setUser({ authenticated: true, user: data.user })
            }
            setLoading(false)
        }());

    }, [])

    return <AuthContext.Provider value={{ user, setUser }}>

        {loading ? <>
            <div className="loading-overlay">
                <p className="font-bold">
                    Loading...
                </p>
            </div>
        </>
            :
            children
        }
    </AuthContext.Provider>

}