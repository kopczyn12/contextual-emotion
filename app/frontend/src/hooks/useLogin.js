// Importing useState from React, useAuthContext hook, toast from react-toastify, CSS for react-toastify
import { useState } from 'react';
import { useAuthContext } from './useAuthContext';

import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const useLogin = () => {
  const [error, setError] = useState(null); // Initializing the error state
  const [isLoading, setIsLoading] = useState(false); // Initializing the isLoading state
  const { dispatch } = useAuthContext(); // Accessing the dispatch function from the useAuthContext hook

  const login = async (email, password) => {
    setIsLoading(true); // Setting isLoading to true
    setError(null); // Resetting the error state

    try {
      const response = await fetch(`${process.env.REACT_APP_SERVER}user/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (response.ok) {
        const json = await response.json();
        // save the user to local storage
        localStorage.setItem('user', JSON.stringify(json));
        // update the auth context
        dispatch({ type: 'LOGIN', payload: json });
      } else {
        const json = await response.json().catch(() => null);
        setError(json?.error || 'An error occurred.');
        toast.error(json?.error || 'An error occurred.');
      }
    } catch (err) {
      setError(err.message);
      toast.error(err.message);
    }
    setIsLoading(false); // Setting isLoading to false
  };

  return { login, isLoading, error }; // Return the login function, isLoading state, and error state
};
