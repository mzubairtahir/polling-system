'use client'


const { useContext, createContext, useState } = require("react");


const MessageContext = createContext();

export const useMessage = () => useContext(MessageContext);

export const MessageProvider = ({ children }) => {

    const [message, setMessage] = useState('');
    return (
        <MessageContext.Provider value={{ message, setMessage }}>
            {children}
        </MessageContext.Provider>
    )

}