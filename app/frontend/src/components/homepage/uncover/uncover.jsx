// Import React library and css style
import React from "react";
import "./uncover.css";

const Uncover = () => {
  return (
    // Create feature of section for homepage component 
    <section id='uncover'>
      <div className="uncover-s">
        <div className="un-container">
            <div className="uncover" id="uncover1">
              Uncover
          </div>
          <div className="uncover" id="uncover2">
              Uncover
          </div>
          <div className="uncover" id="uncover3">
              Uncover
          </div>
          <div className="uncover" id="uncover4">
              Uncover
          </div>
          <div className="unc-container">
            <div className="un-img">
              <img src="..\..\..\..\uncover.png" className="unc-image"/> {/* Import image from public folder to view on the page */}
            </div>
            <div className="unc-content">
                <h1>Uncover hidden emotions with our innovative technology that tracks your eye movements and analyzes your facial expressions as you view a series of curated images.
                <br/><br/></h1>
                <h1>Gain valuable insights into your emotional responses and achieve your goals, whether it's improving interpersonal skills or exploring your emotional reactions. 
                <br/><br/></h1>
                <h1><a href="/signup">Sign up now</a> and discover the emotions behind your gaze!
                </h1>
            </div>
          </div>
          
        </div>
      </div>
    </section>
  );
};

export default Uncover; // Export the Uncover component as the default export