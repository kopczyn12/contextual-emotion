// Importneeded components like footer, navbar and css style
import React from 'react';
import './infopage.css';
import Footer from '../homepage/footer/footer';
import Navbar from '../homepage/navbar/navbar';

function InfoPage() {
  return (
    <>
    {/* Render the Navbar component */}
    <Navbar/>
    {/* Create content with images about our site */}
    <div className="mainAbout">
      <div className="about-container">
        <div className="row">
          <div className="createdBy">
            Project developed by students from Gdańsk <br/> University of Technology
          </div>
        </div>
        <div className="row">
          <div className="technologyRects">
            <div className="technologyRect">
              <img src="..\..\..\..\react.png"/>  {/* Import image from public */}
              <h1>
                MERN <br/>
                <p>Mongo, Express, React, Node</p>
              </h1>
            </div>
            <div className="technologyRect" id="middleTechnologyRect">
              <img src="..\..\..\..\pytorch.png"/>  {/* Import image from public */}
              <h1>
              PyTorch <br/>
                <p>Deep Learning</p></h1>
            </div>  
            <div className="technologyRect">
              <img src="..\..\..\..\tensorflow.png"/>  {/* Import image from public */}
              <h1>TensorFlow<br/>
                <p>Machine Learning</p></h1>
            </div>
            
          </div>
        </div>
        <div className="row">
          <div className="technologyRects">
            <div className="technologyRect down" id="leftTechnologyRect">
              <img src="..\..\..\..\tobii.png"/>  {/* Import image from public */}
              <h1>Tobii<br/>
                <p>Eyetracking</p></h1>
            </div>  
            <div className="technologyRect down" id="rightTechnologyRect">
              <img src="..\..\..\..\aidmed.png"/>  {/* Import image from public */}
              <h1>Aidmed<br/>
                <p>Medical Device</p></h1>
            </div>
          </div>
        </div>
      </div>
    </div>
    {/* Render the Footer component */}
    <Footer/>
    </>
  );
};

export default InfoPage;