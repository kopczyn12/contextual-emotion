// Import React library and css style
import React from "react";
import "./approach.css";

const Approach = () => {
  return (
    // Create feature of section for homepage component 
    <section id='approach'>
      <div className="approach">
        <div className="app-container">
          <div className="texts">
            <div className="title">Our Innovative Approach</div>
            <div className="subtitle">Carefully designed tools that enhance your emotional exploration</div>
          </div>  
          <div className="app-content">
            <div className="rect" id="left">
              <img src="..\..\..\..\emotion.png" className="approach-image"/> {/* Import image from public folder to view on the page */}
              <div className="approach-img-desc">Real-time emotion detection</div>
            </div>
            <div className="rect" id="mid">
              <img src="..\..\..\..\target.png" className="approach-image"/> {/* Import image from public folder to view on the page */}
              <div class="approach-img-desc">Eye tracking technology</div>
            </div>
            <div className="rect" id="side">
              <img src="..\..\..\..\brainstorm.png" className="approach-image"/> {/* Import image from public folder to view on the page */}
              <div className="approach-img-desc">Dozens of hand-prepared images</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Approach; // Export the Approach component as the default export