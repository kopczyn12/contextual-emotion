// Import React library and css style
import React from "react";
import "./stable.css";

const Stable = () => {
  return ( 
    // Create feature of section for homepage component 
    <section id="image-generator">
      <div className="image-generator-container">
        <div className="image-generator-content">
          <h1>Experience the power of AI image generation on our website.</h1>
          <h1>Unlock the potential of artificial intelligence to create stunning and realistic images at your fingertips.</h1>
          <h1>Explore the endless possibilities of AI-generated images!</h1>
        </div>
        <div className="image-generator-img">
          <img src="..\..\..\..\stablediffusion.png" className="image-generator-image" alt="AI Image Generation" />
        </div>
      </div>
    </section>
  );
};

export default Stable; // Export the Stable component as the default export
