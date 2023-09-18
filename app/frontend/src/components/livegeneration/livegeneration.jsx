// Importing needed components like footer, navbar and css style
import React from 'react';
import { useState } from "react";
import './livegeneration.css';
import Footer from '../homepage/footer/footer';
import Navbar from '../homepage/navbar/navbar';

function LiveGen() {
  const [promptText, setPromptText] = useState(''); // State for storing the prompt text
  const [generatedImage, setGeneratedImage] = useState(''); // State for storing the generated image URL

  const handlePromptChange = (event) => {
    setPromptText(event.target.value); // Updating the prompt text state when the input value changes
  };

  const handleGenerateImage = async () => {
    // Function to handle image generation
    const emotion = document.querySelector('input[name="emotion"]:checked').value;
    const emotionPrefix = `${emotion}CxE, `;
    const modifiedPromptText = emotionPrefix + promptText;
  
    try {
      const response = await fetch(`${process.env.REACT_APP_SERVER}stable/generate-image`, {
        // Sending a POST request to the server to generate the image
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ promptText: modifiedPromptText, emotionPrefix }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate image');
      }
      
      const data = await response.json();
      const imageURL = data.imageURL; // Extracting the image URL from the response data

  
      setGeneratedImage(imageURL); // Updating the generated image URL state
      console.log(imageURL);
    } catch (error) {
      console.error('Error with generating image:', error);
    }
  };  

  return (
    <>
    {/* Render the Navbar component */}
    <Navbar />
     {/* Create feature of the live generation page */}
    <div id='livegen'>
      <div className='gen-con'>
        <div className='live-containere'>
          <div className='radio-buttons'>
            <label>
              <p>
                Style of generation:
              </p>
            </label>
            <label>
              <input type="radio" name="emotion" value="angry" /> Angry
            </label>
            <label>
              <input type="radio" name="emotion" value="happy" /> Happy
            </label>
            <label>
              <input type="radio" name="emotion" value="surprise" /> Surprised
            </label>
            <label>
              <input type="radio" name="emotion" value="disgust" /> Disgusted
            </label>
            <label>
              <input type="radio" name="emotion" value="sad" /> Sad
            </label>
          </div>
          <div className='input-label'>
            <input
              type="text"
              id="promptInput"
              placeholder="Enter your prompt"
              value={promptText}
              onChange={handlePromptChange}
            />
            <button className='button-generate' onClick={handleGenerateImage}>Generate image</button>  {/* Button to generate the image */}
          </div>
          <div className='image-place'>
            {generatedImage && <img src={generatedImage} alt="Generated image" />} {/* Render the generated image if available */}
          </div>
        </div>
      </div>
    </div>
    {/* Render the Footer component */}
    <Footer />
  </>
);
};


export default LiveGen;
