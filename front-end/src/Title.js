import React, { useState, useEffect } from "react";
import "./App.css";

function Title() {
    const [title, setTitle] = useState([])
    const fetchInfo = async () => {
        setTitle("loading...")
        const response = await fetch(
            "http://localhost:8080/movie/0092086/title"
        );
        if (response.status === 200)
            setTitle(await response.text());
        else
            setTitle(null);
    };

    useEffect(() => {
        fetchInfo();
    }, []);


    return <div>Title: {title}</div>
}

export default Title