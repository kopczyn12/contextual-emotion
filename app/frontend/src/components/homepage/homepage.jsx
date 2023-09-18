// Importing needed components like footer, navbar, approach, uncover, stable and css style
import React from 'react';
import './homepage.css';
import Footer from './footer/footer';
import Approach from './approach/approach';
import Navbar from './navbar/navbar';
import Uncover from './uncover/uncover';
import Stable from './stable/stable'; 


function HomePage() {
  function handleModel() {
    window.location.href = '/feature' // Redirect to the feature page when the "Get started" button is clicked
  }

  function handleSignup() {
    window.location.href = '/signup' // Redirect to the signup page when the "Sign up" button is clicked
  }
  
  return (
    <>
    {/* Rendering navbar component */}
    <Navbar/>
    {/* Creating homepage blue banner with buttons redirecting to feature and sign up pages */}
    <div className="homepage-main">
      <div className="banner">
        <h1>See beyond the smile</h1>
        <p>Experience cutting-edge technology that tracks your eye movements and detects your emotions as you view a series of captivating images</p>
        <button className="ban-button" id="button-get-started" onClick={handleModel}>Get started</button>
        <button className="ban-button" id="button-sign-up" onClick={handleSignup}>Sign up</button>
        <div className="image">
          <img src="..\..\..\..\laptop.png" className="laptop-image"/>
        </div>
      </div>
      </div>
    {/* Rendering the rest of components */}
    <Approach/>
    <Stable/>
    <Uncover/>
    <Footer/>
    </>
  );
}

export default HomePage // Export the HomePage component as the default export
