import { useFlags } from "launchdarkly-react-client-sdk"
import React, { useState, useEffect } from "react";
import "./App.css";

function Synopsis() {
    const { SHOW_SYNOPSIS } = useFlags();
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
    }, [SHOW_SYNOPSIS]);

    return SHOW_SYNOPSIS ? <div>Synopsis: {synopsis}</div> : null;
}

export default Synopsis