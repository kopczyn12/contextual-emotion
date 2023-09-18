
// Importing the React library, Link component from react-router-dom, AiOutlineMenu and AiOutlineClose icons from react-icons/ai
// Importing useState hook from React, useLogout hook, useAuthContext hook

import { Link } from 'react-router-dom';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import { useState } from 'react';
import { useLogout } from '../../../hooks/useLogout';
import { useAuthContext } from '../../../hooks/useAuthContext';

const NavBar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false); // Using the useState hook to manage mobile menu state
  const { logout } = useLogout(); // Using the useLogout hook to get the logout function
  const { user } = useAuthContext(); // Using the useAuthContext hook to get the user object

  const handleMobileMenuToggle = () => {
  setIsMobileMenuOpen(!isMobileMenuOpen); // Toggling the mobile menu state
  };

  const handleClick = () => {
    console.log('clicked');
    logout();  // Logging out the user
  };

return (
// Create the Navbar feature and Links to pages
<nav className="bg-white">
  <div className="max-w-full mx-auto px-2 sm:px-6 lg:px-8">
    <div className="relative flex items-center justify-between h-16">
      <div className="absolute inset-y-0 left-0 flex items-center sm:hidden">
        <button
          onClick={handleMobileMenuToggle}
          className="inline-flex items-center justify-center p-2 rounded-md hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
        >
        <span className="sr-only">Open main menu</span>
        {isMobileMenuOpen ? (
          <AiOutlineClose className="block h-6 w-6" />
          ) : (
          <AiOutlineMenu className="block h-6 w-6" />
          )}
        </button>
      </div>
      <div className="flex-1 flex items-center justify-center sm:items-stretch sm:justify-start">
  <div className="flex-shrink-0">
    <Link to="/" className="text-white text-xl font-bold">
      <img
        src="logo.png"
        alt="My App"
        className="h-12 rounded-r-3xl rounded-l-xl"
      />
    </Link>
  </div>
  <div className="hidden sm:flex sm:items-center sm:ml-4">
  <Link
      to="/"
      className="hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
    >
      Overview
    </Link>
    <Link
      to="/feature"
      className="hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
    >
      Model access
    </Link>
    <Link
      to="/about"
      className="hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
    >
      About
    </Link>
    <Link
      to="/live-gen"
      className="hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
    >
      Live generation
    </Link>

  </div>
  {!user && (
  <div className="hidden sm:block sm:ml-auto">
      <div>
        <Link to="/login" className="hover:text-white px-3 py-2 rounded-md text-sm font-medium">
          <button className="bg-white text-black border-2 border-black rounded-lg px-4 py-2 hover:bg-black hover:text-white">
            Sign up
          </button>
        </Link>
    </div>
  </div>
  )}
  {user && (
  <div className="hidden sm:block sm:ml-auto">
      <div className="hover:text-white px-3 py-2 rounded-md text-sm font-medium">
        <span className='mr-3'>{user.email}</span>
        <button onClick={handleClick}
        class="bg-white text-black border-2 border-black rounded-lg px-4 py-2 hover:bg-black hover:text-white"                >
        Log out
        </button>
      </div>
  </div>
  )}
</div>
    </div>
  </div>
  <div className={`${ isMobileMenuOpen ? 'block' : 'hidden' } sm:hidden bg-gray-800`} >
    <div className="px-2 pt-2 pb-3 space-y-1">
    <Link to="/" className="text-white hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium" >
        Overview
      </Link>
      <Link to="/feature" className="text-white hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium" >
        Model access
      </Link>
      <Link to="/about" className="text-white hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium" >
        About
      </Link>
      <Link to="/live-gen" className="text-white hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium" >
        Live generation
      </Link>

      
      <Link to="/login" className="text-white hover:bg-gray-700 hover:text-white block px-3 py-2 rounded-md text-base font-medium" >
        Sign up
      </Link>
    </div>
  </div>
</nav>

);
};

export default NavBar; // Export the Navbar component as the default export