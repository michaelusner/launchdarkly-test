import React from "react";

import Synopsis from "./Synopsis.js"
import Title from "./Title.js"
import Rating from "./Rating.js"
import './App.css';
import { withLDProvider } from "launchdarkly-react-client-sdk";

function App() {
  return (
    <div className="App">
      <h1>Movie Info</h1>
      <Title />
      <Rating />
      <Synopsis />
    </div>
  );
}


export default withLDProvider({
  clientSideID: "620bd47d10601a14da99784b",  // should be in vault - environment specific
  reactOptions: {
    useCamelCaseFlagKeys: false
  }
})(App);
