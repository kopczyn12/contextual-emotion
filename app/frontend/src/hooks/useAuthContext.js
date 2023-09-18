import { useContext } from 'react';  // Importing useContext from React
import { AuthContext } from '../context/AuthContext'; // Importing the AuthContext

export const useAuthContext = () => {
    const context = useContext(AuthContext);  // Accessing the AuthContext

    if (!context) {
        throw Error('useAuthContext must be used within AuthProvider'); // Throw an error if useAuthContext is not used within AuthProvider
    }

    return context; // Return the context
}