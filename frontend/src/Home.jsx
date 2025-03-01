import React from "react";
import { useLocation } from "react-router-dom";
import VideoPlayer from "./components/VideoPlayer";
import Transcript from "./components/Transcript";
import ChatBot from "./components/ChatBot";
import Canvas from "./components/Canvas";
import "./styles/homepage.css";

const Home = () => {
  const location = useLocation();
  const videoUrl = location.state?.videoUrl || "";
  const transcriptData = location.state?.transcript || "";

  return (
    <div>
      <div className="heading">AI MATH TUTOR</div>
      <div className="container">
        <div className="left-panel">
          <ChatBot />
        </div>
        <div className="right-panel">
          <div className="video-transcript">
            <VideoPlayer videoUrl={videoUrl} />
            <Transcript transcriptData={transcriptData} />
          </div>
          <div className="canvas-tool">
            <Canvas />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
