import React, { useState, useEffect } from "react";
import "./App.css";

function Rating() {
    const [rating, setRating] = useState([])
    const fetchInfo = async () => {
        setRating("loading...")
        const response = await fetch(
            "http://localhost:8080/movie/0092086/rating"
        );
        if (response.status === 200)
            setRating(await response.text());
        else
            setRating(null);
    };

    useEffect(() => {
        fetchInfo();
    }, []);


    return <div>Rating: {rating}</div>
}

export default Rating