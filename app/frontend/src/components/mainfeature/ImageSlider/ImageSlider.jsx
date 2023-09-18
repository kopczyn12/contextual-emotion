import React, { useRef, useState, useEffect } from 'react';
import axios from 'axios';
import * as faceapi from '@vladmandic/face-api';

import Footer from '../../homepage/footer/footer';
import Navbar from '../../homepage/navbar/navbar';

const ImageSlider = ({videoRef}) => {
  const [user, setUserId] = useState(null);
  const canvasRef = useRef();
 // Retrieve user from local storage on component mount
  useEffect(() => {
    const userFromLocalStorage = localStorage.getItem('user');
    if (userFromLocalStorage) {
      const parsedUser = JSON.parse(userFromLocalStorage);
      const email = parsedUser.email;
      setUserId(email);

    }
  }, []);
  
useEffect(() => {
  loadModels();
}, []);
  // Load face-api models on component mount
const loadModels = async () => {
  await Promise.all([
    faceapi.nets.tinyFaceDetector.loadFromUri("/models"),
    faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
    faceapi.nets.faceRecognitionNet.loadFromUri("/models"),
    faceapi.nets.faceExpressionNet.loadFromUri("/models")
  ]);

};


  const [currentImageIndex, setCurrentImageIndex] = useState(0);
  const [sliderActive, setSliderActive] = useState(false);
  const [showUI, setShowUI] = useState(true);
  const images = [
    'surprise1.jpg',
    'surprise2.jpg', 
    'surprise3.jpg', 
    'surpise4.jpg', 
    'surpise5.jpg', 
    'surprise6.jpg', 
    'surprise7.jpg',  
    'happy1.jpg',
    'happy2.jpg',
    'happy3.jpg',
    'happy4.jpg',
    'happy5.jpg',
    'happy6.jpg',
    'happy7.jpg',
    'sad1.jpg',
    'sad2.jpg',
    'sad3.jpg',
    'sad4.jpg',
    'sad5.jpg',
    'sad7.jpg',
    'sad8.jpg',
    'disgust1.jpg',
    'disgust2.jpg',
    'disgust3.jpg',
    'disgust4.jpg',
    'disgust5.jpg',
    'disgust6.jpg',
    'disgust7.jpg',
    'angry1.jpg',
    'angry2.jpg',
    'angry3.jpg',
    'angry4.jpg',
    'angry5.jpg',
    'angry6.jpg',
    'angry7.jpg'
];
   // Function to handle slider activity 
useEffect(() => {
  let requestIntervalId = null;
  let changeIndexIntervalId = null;

  if (sliderActive) {
    let emotionsList = [];

    requestIntervalId = setInterval(async () => {


        const detections = await faceapi.detectAllFaces(videoRef.current,
        new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
    
        const displaySize = {
          width: videoRef.current.videoWidth,
          height: videoRef.current.videoHeight
        };
        faceapi.matchDimensions(canvasRef.current, displaySize);
    
        const resizedDetections = faceapi.resizeResults(detections, displaySize);
    
        canvasRef.current.getContext('2d').clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
        faceapi.draw.drawDetections(canvasRef.current, resizedDetections);
        faceapi.draw.drawFaceLandmarks(canvasRef.current, resizedDetections);
        faceapi.draw.drawFaceExpressions(canvasRef.current, resizedDetections);
    
        // Pobranie wycinka z twarzą jako Base64
        if (resizedDetections && resizedDetections.length > 0) {
          const currentTimestamp = new Date().toLocaleString('pl-PL', {
            timeZone: 'Europe/Warsaw',
            hour12: false,
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            fractionalSecondDigits: 3
          });
          const faceBox = resizedDetections[0].detection.box;
          const faceImage = await faceapi.extractFaces(videoRef.current, [faceBox]);
          
        // Prepare canvas for drawing detections
          const canvas = document.createElement('canvas');
          canvas.width = faceImage[0].width;
          canvas.height = faceImage[0].height;
          canvas.getContext('2d').drawImage(faceImage[0], 0, 0);
          const base64Data = canvas.toDataURL('image/jpeg');
          const imageSrc = base64Data;
          // Send face image to the server for emotion detection
          axios.post(`${process.env.REACT_APP_SERVER}model/detect-emotion`, { image: imageSrc })
          .then(response => {
            const emotion = response.data.emotion2;
            emotionsList.push({ emotion, timestamp: currentTimestamp });
          })
          .catch(error => {
            console.log(error);
          });
        }
    }, 500);

      // Interval function to change the image index
    changeIndexIntervalId = setInterval(() => {
      setCurrentImageIndex(currentImageIndex => {
        const newIndex = (currentImageIndex + 1) % images.length;

        // Display emotions list before resetting
        console.log(`Emotions for Image ${images[currentImageIndex]}:`, emotionsList);
        axios.post(`${process.env.REACT_APP_SERVER}emotions/add-image`, {
          user: user,
          image: images[currentImageIndex].toString(),
          emotions: emotionsList
        });

        // Reset emotions list
        emotionsList = [];
        if (newIndex === 0) {
          handleRedirect(); // Redirect to "/end_test" page
        }

        return newIndex;
      });
    }, 5000);


    return () => {
      clearInterval(requestIntervalId);
      clearInterval(changeIndexIntervalId);
    };
  }
}, [sliderActive]);


  // Function to toggle the slider
const toggleSlider = async () => {
  setSliderActive(!sliderActive);
  setShowUI(!showUI);
};

function enterFullscreen() {
  const element = document.documentElement; // Element, który ma być wyświetlany na całym ekranie
  // Function to enter fullscreen mode
  if (element.requestFullscreen) {
    element.requestFullscreen();
  } else if (element.mozRequestFullScreen) { // Obsługa dla starszych wersji Firefoksa
    element.mozRequestFullScreen();
  } else if (element.webkitRequestFullscreen) { // Obsługa dla starszych wersji Chrome, Safari, Opera
    element.webkitRequestFullscreen();
  } else if (element.msRequestFullscreen) { // Obsługa dla starszych wersji Internet Explorer
    element.msRequestFullscreen();
  }
};
  // Function to exit fullscreen mode
function exitFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) { // Obsługa dla starszych wersji Firefoksa
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) { // Obsługa dla starszych wersji Chrome, Safari, Opera
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { // Obsługa dla starszych wersji Internet Explorer
    document.msExitFullscreen();
  }
};
  // Function to handle the start button click
function handleButtonClickStart() {
  toggleSlider();
  enterFullscreen();
  setTimeout(handleRedirect, 200000);
};
  // Function to handle the redirect
const handleRedirect = () => {
  window.location.href = '/end_test';
};

function handleButtonClickStop() {
  toggleSlider();
  exitFullscreen();
};

return (
  <>
  {showUI ? (<Navbar/>) : null}
  <div id='content'>
    <div className="flex column-2">
      <div id='imgtheme'>
        {showUI ? (
          <>
            <h1 className='testtext'>
              <p>Detect</p>
              <p>Your</p>
              <p>emotions</p>
            </h1>
            <i className='fa fa-angle-down'></i>
          </>
        ) : (
        <div className='pictures'>
        <img
          src={`images/${images[currentImageIndex]}`}
          alt="slider"
          className="w-full h-screen img"
          style={{ display: sliderActive ? 'block' : 'none' }}
        />
        <canvas ref={canvasRef} className="appcanvas" />
        </div>
        )}
      </div>
        
      {!sliderActive && (
        <button onClick={handleButtonClickStart} className='buttonsliderstart'>
        Start
      </button>
      )}
    </div>
  </div>
  {showUI ? (<Footer/>) : null}
  </>
);
};

export default ImageSlider;
