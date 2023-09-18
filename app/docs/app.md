# MERN APP

## Introduction
The MERN project is a technology stack consisting of the following:

- MongoDB: A document-based NoSQL database.
- Express: A web framework for Node.js.
- React: A JavaScript library for building user interfaces.
- Node.js: A JavaScript runtime for building server-side applications.

This project is a full-stack web application built using the MERN stack.

## Running the Backend
- Navigate to the project's backend directory.
- Install the backend dependencies by running npm install.
- Create a .env file in the root of the backend directory and add the necessary environment variables (e.g. MONGODB_URL for the MongoDB connection URL).
- Start the backend server by running 'node index'

The backend server should now be running and listening for requests on the specified port.

## Running the Frontend
- Navigate to the project's frontend directory.
- Install the frontend dependencies by running npm install.
- Update the REACT_APP_API_URL environment variable in the .env file to match the URL of the backend server.
- Start the frontend development server by running npm start

The frontend development server should now be running and you should be able to access the web application by navigating to http://localhost:3000 in your web browser. Any changes you make to the frontend code will be automatically reloaded in the browser.