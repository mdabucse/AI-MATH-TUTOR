import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

const App = () => {
  const [videoUrl, setVideoUrl] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Function to validate YouTube URL
  const isValidYouTubeUrl = (url) => {
    const pattern =
      /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]+$/;
    return pattern.test(url);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("https://w4gw8kvg-5000.inc1.devtunnels.ms/transcript", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ video_ids: videoUrl }), // Sending video URL
      });

      if (!response.ok) {
        throw new Error("Failed to fetch transcript");
      }

      const data = await response.json();
      console.log("Transcript Response:", data); // Debugging purposes

      // Navigate to Home page with videoUrl and transcript data
      navigate("/home", { state: { videoUrl, transcript: data } });

    } catch (error) {
      console.error("Error fetching transcript:", error);
      setError("Failed to fetch transcript. Please try again.");
    }
  };

  return (
    <div className="container1">
      <h1 className="title">AI Math Tutor</h1>
      <p className="subtitle">to make your learning easy</p>
      <div className="input-container">
        <label htmlFor="videoUrl" className="label">
          Paste the URL
        </label>
        <input
          type="text"
          id="videoUrl"
          className="input-box"
          placeholder="Enter video URL..."
          value={videoUrl}
          onChange={(e) => {
            setVideoUrl(e.target.value);
            setError(""); // Clear error on change
          }}
        />
        <button onClick={handleSubmit} className="submit-btn">
          Proceed
        </button>
        {error && <p className="error">{error}</p>}
      </div>
    </div>
  );
};

export default App;
