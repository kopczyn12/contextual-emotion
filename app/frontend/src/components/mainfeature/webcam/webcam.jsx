import React, { useRef, useEffect } from 'react';
import './face.css';
import * as faceapi from '@vladmandic/face-api';
import ImageSlider from '../ImageSlider/ImageSlider';

function App() {
  const videoRef = useRef();

  useEffect(() => {
    startVideo();
  }, []);

  const startVideo = () => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((currentStream) => {
        videoRef.current.srcObject = currentStream;
      })
      .catch((err) => {
        console.log(err);
      });
  };


  return (
    <>
      <video crossOrigin="anonymous" className="webcam" ref={videoRef} autoPlay></video>
      <ImageSlider videoRef={videoRef}/>
    </>
  );
}

export default App;
