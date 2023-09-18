// Import React library and css style
import React from "react";
import "./footer.css";

const Footer = () => {
  return (
    // Create feature of footer component 
    <footer id='footer'>
      <div className="container mx-auto">
        <div className="flex">
          <div className="w-full md:w-1/3 px-4 mb-8 md:mb-0 flex flex-col items-center">
            <h3>Contact Us</h3>
            <ul>
              <li><a href="#">E-mail</a></li>
            </ul>
          </div>
          <div className="w-full md:w-1/3 px-4 mb-8 md:mb-0 flex flex-col items-center">
            <h3>Info</h3>
            <ul>
              <li><a href="#about">About Us</a></li>
              <li><a href="#">Terms of Service</a></li>
            </ul>
          </div>
          <div className="w-full md:w-1/3 mb-8 md:mb-0 flex flex-col items-center">
            <h3>Social media</h3>
            <ul className="flex justify-between">
              <li><a href="#"><i className="fab fa-facebook-f"></i></a></li>
              <li><a href="#"><i className="fab fa-twitter"></i></a></li>
              <li><a href="#"><i className="fab fa-instagram"></i></a></li>
            </ul>
          </div>
        </div>
      </div>
      <div className="container mx-auto text-center">
        <p className="text-xs">&copy; 2023 CxE</p>
      </div>
    </footer>
  );
};

export default Footer; // Export the Footer component as the default export