import { useCallback } from "react";

function setErrorMessage(name, message) {
    const inputElement = document.querySelector(`[name=${name}] ~ .input-error`);
    if (inputElement) {

        inputElement.textContent = message
    }
}

function removeAllMessages() {

    const allErrorElem = document.querySelectorAll(".input-error");
    for (const element of allErrorElem) {
        element.textContent = "";


    }

}

function useInputErrorDisplay() {


    return useCallback((errors) => {
        if (errors) {
            removeAllMessages();
            for (const key in errors) {
                setErrorMessage(key, errors[key][0])
            }
        }
        else {
            removeAllMessages();
        }


    })

}

export default useInputErrorDisplay;