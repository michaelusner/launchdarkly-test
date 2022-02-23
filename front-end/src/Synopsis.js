import { useFlags } from "launchdarkly-react-client-sdk"
import React, { useState, useEffect } from "react";
import "./App.css";

function Synopsis() {
    const { TEST_FEATURE_FLAG } = useFlags();
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
    }, [TEST_FEATURE_FLAG]);

    return TEST_FEATURE_FLAG ? <div>Synopsis: {synopsis}</div> : null;
}

export default Synopsis