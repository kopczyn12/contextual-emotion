 // Importing useState from React, useSignup hook, ToastContainer from react-toastify, CSS for react-toastify, Footer component, Navbar component
import { useState } from 'react';
import { useSignup } from '../hooks/useSignup';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Footer from '../components/homepage/footer/footer';
import Navbar from '../components/homepage/navbar/navbar';

const Signup = () => {
    const [email, setEmail] = useState(''); // Initializing the email state
    const [password, setPassword] = useState(''); // Initializing the password state
    const [age, setAge] = useState(null); // Initializing the age state
    const [gender, setGender] = useState(''); // Initializing the gender state
    const [occupation, setOccupation] = useState(''); // Initializing the occupation state
    const { error, isLoading, signup } = useSignup(); // Accessing the error state, isLoading state, and signup function from the useSignup hook

    const handleSubmit = async (e) => {
        e.preventDefault();
        await signup(email, password, age, gender, occupation); // Calling the signup function with the provided information
    }

    return (
    <>
    {/* Render the Navbar component */}
    <Navbar/>
        {/* Create the sign up page feature, input labels and button to confirm any information written */}
        <div id='signup'>
            <form class="bg-white shadow-md w-96 mx-auto p-20" onSubmit={handleSubmit}>
                <h3 class="text-xl font-bold mb-6">Sign up</h3>
                <div class="mb-4">
                    <label class="block text-gray-700 font-bold mb-2 text-left" htmlFor='email'>
                    Email:
                    </label>
                    <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight"
                    type="email"
                    onChange={e => setEmail(e.target.value)}
                    value={email}
                    placeholder="Enter your email"
                    />
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 font-bold mb-2 text-left" htmlFor='password'>
                    Password:
                    </label>
                    <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight"
                    type="password"
                    onChange={e => setPassword(e.target.value)}
                    value={password}
                    placeholder="Enter your password"
                    />
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 font-bold mb-2 text-left" htmlFor='age'>
                    Age:
                    </label>
                    <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight"
                    type="number"
                    onChange={e => setAge(e.target.value)}
                    value={age}
                    placeholder="Enter your age"
                    />
                </div>
                <div class="mb-4">
                    <label class="block text-gray-700 font-bold mb-2 text-left" htmlFor='gender'>
                        Gender:
                    </label>
                    <select
                        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight"
                        onChange={e => setGender(e.target.value)}
                        value={gender}
                        defaultValue=''
                    >
                        <option value='' disabled hidden>Select gender</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="mb-6">
                    <label class="block text-gray-700 font-bold mb-2 text-left" htmlFor='password'>
                    Occupation:
                    </label>
                    <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight"
                    type="text"
                    onChange={e => setOccupation(e.target.value)}
                    value={occupation}
                    maxLength={20}
                    placeholder="Enter your occupation"
                    />
                </div>
                <div class="flex justify-center mt-8">
                    <button
                    disabled={isLoading}
                    class="bg-gray-800 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-60"
                    type="submit">
                    Sign up
                    </button>
                </div>
                <a class="inline-block align-baseline font-bold text-sm text-gray-600 hover:text-blue-800"
                href="/login"
                >
                Already have an account?
                </a>
                {/* Render Toast container to show with any error/exception */}
                <ToastContainer position="top-center"/>
            </form>
        </div>
    {/* Render the Footer component */}
    <Footer/>
    </>
    );      
}

export default Signup; // Export the Signup component as the default export