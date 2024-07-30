'use client'

import React, { useState, useEffect } from 'react';

const Loading = () => {
    const [dots, setDots] = useState('');

    useEffect(() => {
        const interval = setInterval(() => {
            setDots(prevDots => {
                if (prevDots.length < 3) {
                    return prevDots + '.';
                } else {
                    return '.';
                }
            });
        }, 500); // Change the interval as needed

        return () => clearInterval(interval);
    }, []);

    return <div>Loading{dots}</div>;
};

export default Loading;
