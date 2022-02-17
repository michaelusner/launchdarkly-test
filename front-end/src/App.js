import React, { useState, useEffect } from "react";

import Synopsis from "./Synopsis.js"
import './App.css';
import { withLDProvider } from "launchdarkly-react-client-sdk";

function App() {
  const [title, setTitle] = useState([])
  const [rating, setRating] = useState([])

  const fetchTitle = async () => {
    setTitle("loading...");
    const titleResponse = await fetch(
      "http://localhost:8080/movie/0092086/title"
    );
    setTitle(await titleResponse.json());
  };

  const fetchRating = async () => {
    setRating("loading...");
    const infoResponse = await fetch(
      "http://localhost:8080/movie/0092086/rating"
    );
    setRating(await infoResponse.json());
  };

  useEffect(() => {
    fetchTitle();
    fetchRating();
  }, []);

  return (
    <div className="App">
      <h1>Movie Info</h1>
      <div>
        Title: {title}<br />
        Rating: {rating}
      </div>
      <Synopsis />
    </div>
  );
}


export default withLDProvider({
  clientSideID: "620bd47d10601a14da99784b",  // should be in vault - environment specific
})(App);
