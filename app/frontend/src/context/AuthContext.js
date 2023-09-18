import { createContext, useReducer, useEffect } from 'react'; // Importing createContext, useReducer, and useEffect from React


export const AuthContext = createContext(); // Creating an AuthContext

export const authReducer = (state, action) => {
    switch (action.type) {
        case 'LOGIN':
            return { user: action.payload }; // Update the state with the user object on login
        case 'LOGOUT':
            return { user: null }; // Update the state with null on logout
        default:
            return state;
    }
};

export const AuthProvider = ({ children }) => {
    const [state, dispatch] = useReducer(authReducer, {
        user: null,
    }); // Using useReducer to manage the state

    useEffect(() => {
        const user = JSON.parse(localStorage.getItem('user'));  // Retrieve the user from localStorage

        if (user) {
            dispatch({ type: 'LOGIN', payload: user }); // Dispatch the LOGIN action with the user object if it exists
        }
    }, []);

    console.log(state); // Logging the state

    return (
        <AuthContext.Provider value={{...state, dispatch}}>
            { children }
        </AuthContext.Provider>
    )
};

