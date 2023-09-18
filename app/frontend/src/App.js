import React from 'react'
import HomePage from './components/homepage/homepage'; // Importing the HomePage component
import InfoPage from './components/infopage/infopage'; // Importing the InfoPage component
import MainFeaturePage from './components/mainfeature/mainfeature';  // Importing the MainFeaturePage component
import NotFound from './components/404/404' // Importing the NotFound component
import EndTest from './components/mainfeature/end_page/end_page'; // Importing the EndTest component
import { Route, Routes } from 'react-router-dom'; // Importing the Route and Routes components from react-router-dom
import Login from './pages/Login'; // Importing the Login component
import Signup from './pages/Signup'; // Importing the Signup component
import { useAuthContext } from './hooks/useAuthContext'; // Importing the useAuthContext hook
import { Navigate } from 'react-router-dom'; // Importing the Navigate component from react-router-dom
import LiveGen from './components/livegeneration/livegeneration'; // Importing the LiveGen component


function App() {

  const { user } = useAuthContext(); // Getting the user from the useAuthContext hook

  return (
    <div className="App">
      <Routes>
        <Route path='/' element={<HomePage/>}/> {/* Route for the home page */}
        <Route path='/live-gen' element={<LiveGen/>}/> {/* Route for the live generation page */}
        <Route path='/about' element={<InfoPage/>}/> {/* Route for the info page */}
        <Route path='/feature' element={ user ? <MainFeaturePage/> : <Login/>}/> {/* Route for the feature page, rendering MainFeaturePage if user is logged in, otherwise rendering Login */}
        <Route path='/login' element={!user ? <Login/> : <Navigate to='/'/>}/> {/* Route for the login page, rendering Login if user is not logged in, otherwise redirecting to the home page */}
        <Route path='/end_test' element={ user ? <EndTest/> : <Login/>}/>  {/* Route for the end test page, rendering EndTest if user is logged in, otherwise rendering Login */}
        <Route path='/signup' element={!user ? <Signup/> : <Navigate to='/'/>}/> {/* Route for the signup page, rendering Signup if user is not logged in, otherwise redirecting to the home page */}
        <Route path="*" element={<NotFound/>}/> {/* Catch-all route for any other paths */}
      </Routes>
    </div>
  );
}

export default App;
