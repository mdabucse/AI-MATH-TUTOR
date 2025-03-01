import React, { useEffect, useState } from "react";
import "../styles/transcript.css";

const Transcript = () => {
  const [transcript, setTranscript] = useState("Loading...");

  useEffect(() => {
    const fetchTranscript = async () => {
      try {
        const response = await fetch("https://w4gw8kvg-5000.inc1.devtunnels.ms/load_transcribe");
        if (!response.ok) {
          throw new Error("Failed to fetch transcript");
        }
        const data = await response.text();
        formatTranscript(data);
      } catch (error) {
        setTranscript("Error loading transcript");
        console.error("Error fetching transcript:", error);
      }
    };

    fetchTranscript();
  }, []);

  // Function to format the transcript content
  const formatTranscript = (data) => {
    const formattedTranscript = data
      .split("\n")
      .map((line, index) => (
        <p key={index} className="transcript-line">
          {line}
        </p>
      ));
    setTranscript(formattedTranscript);
  };

  return <div className="transcript">{transcript}</div>;
};

export default Transcript;
