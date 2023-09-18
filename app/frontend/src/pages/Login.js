// Importing useState from React, useLogin hook, ToastContainer from react-toastify, CSS for react-toastify, Footer component, Navbar component
import { useState } from 'react';
import { useLogin } from '../hooks/useLogin';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Footer from '../components/homepage/footer/footer';
import Navbar from '../components/homepage/navbar/navbar';

const Login = () => {
    const [email, setEmail] = useState(''); // Initializing the email state
    const [password, setPassword] = useState(''); // Initializing the password state
    const { login, isLoading, error } = useLogin(); // Accessing the login function, isLoading state, and error state from the useLogin hook

    const handleSubmit = async (e) => {
        e.preventDefault();
        await login(email, password); // Calling the login function with the email and password
    }

    return (
    <>
    {/* Render the Navbar component */}
    <Navbar/>
    {/* Create the login page feature, input labels and button to confirm any information written */}
        <div id='login'>
            <form class="bg-white shadow-md w-96 mx-auto p-20" onSubmit={handleSubmit}>
                <h3 class="text-xl font-bold mb-6">Log in</h3>
                <div class="mb-4">
                    <label class="block text-gray-700 font-bold mb-2 text-left" htmlFor='email'>
                    Email:
                    </label>
                    <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
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
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    type="password"
                    onChange={e => setPassword(e.target.value)}
                    value={password}
                    placeholder="Enter your password"
                    />
                </div>
                <div class="flex justify-center mt-8">
                    <button
                    class="bg-gray-800 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-60"
                    type="submit"
                    >
                    Log in
                    </button>
                </div>
                <a class="inline-block align-baseline font-bold text-sm text-gray-600 hover:text-blue-800"
                href="/signup"
                >
                Not registered?
                </a>
                {/* Render Toast container to show with any error/exception */}
                <ToastContainer position='top-center'/>
            </form>
        </div>
    {/* Render the Footer component */}
    <Footer/>
    </>
    )
}

export default Login; // Export the Login component as the default export