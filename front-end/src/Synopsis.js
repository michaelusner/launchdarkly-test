import { useFlags } from "launchdarkly-react-client-sdk"
import React, { useState, useEffect } from "react";
import "./App.css";

function Synopsis() {
    const { T_20220217_1234_SHOW_MOVIE_SYNOPSIS } = useFlags();
    const [synopsis, setSynopsis] = useState([])
    const fetchSynopsis = async () => {
        setSynopsis("loading...")
        const synopsisResponse = await fetch(
            "http://localhost:8080/movie/0092086/synopsis"
        );
        if (synopsisResponse.status === 200)
            setSynopsis(await synopsisResponse.text());
        else
            setSynopsis(null);
    };

    useEffect(() => {
        fetchSynopsis();
    }, [T_20220217_1234_SHOW_MOVIE_SYNOPSIS]);

    return T_20220217_1234_SHOW_MOVIE_SYNOPSIS ? <div>Synopsis: {synopsis}</div> : null;
}

export default Synopsis