# Deploying Emotion Detection Model

## Introduction
Emotion detection models are powerful tools that can analyze and interpret human emotions based on various sources, such as images or videos. Integrating such a model in the backend of an application can enhance its functionality and performance.

The deployed emotion detection model is based on TensorFlow.js, a JavaScript library that enables the creation and deployment of machine learning models in the browser or Node.js environment. The model is loaded from an H5 format and used to analyze frames received from the frontend as Base64-encoded data.

## Technologies Used in the Project

- TensorFlow.js: A JavaScript library for creating and deploying machine learning models. Used to load the emotion model from the H5 format.

- Node.js: A JavaScript runtime environment that enables the creation of the application backend.

- Sharp: A Node.js module used for image data transformation and scaling.

- @vladmandic/face-api: A JavaScript library for face detection in images.

## Deployment Process Overview

### Environment Setup
Before starting the deployment process, ensure that you have the following tools installed:

- Node.js: Install Node.js from the official documentation website, following the instructions provided.
- TensorFlow.js: Install TensorFlow.js using npm or yarn package manager:

npm install @tensorflow/tfjs

- Sharp: Install the Sharp module using npm or yarn:

npm install sharp

- @vladmandic/face-api: Install the @vladmandic/face-api library using npm or yarn:

npm install @vladmandic/face-api

### Back-end functionality

The backend of the application is responsible for receiving requests from the frontend, which contain image frames in base64 format. Using the Sharp module, the backend processes these frames by performing various operations such as scaling, cropping, or adjusting colors. Then, the transformed frames are converted into tensors, which are data structures used by TensorFlow.js. These tensors are inputted into the model handled by TensorFlow.js. This model can be trained for various tasks, such as object recognition or image content analysis. After processing by the model, the results are sent back to the frontend as a response to the initial request.

### Frontend functionality

A part of the frontend of the application consists of several important components. Firstly, the frontend captures frames from the camera, enabling real-time image capturing. Then, using the @vladmandic/face-api library, the frontend performs face detection on the captured frames and crops them to preserve only the facial area. The cropped images are then converted to the base64 format to facilitate processing and transmission. For this purpose, the frontend sends a request to the backend containing the processed images in base64 format. Upon receiving a response from the backend, the frontend collects feedback information related to the emotions associated with the processed faces. The frontend gathers several emotion records related to a specific triggering image. Once a sufficient number of records are accumulated, the frontend sends them to a MongoDB database for storage and analysis

## Conclusion
Deploying an emotion detection model involves several steps, such as converting Base64-encoded image data to tensors, scaling the image, performing predictions on the model, and passing the results back to the frontend. The key technologies used in this project are TensorFlow.js, Node.js, Sharp, and @vladmandic/face-api. By following these guidelines, you should be able to deploy an emotion detection model in your application.

# Frontend

## Introduction

Frontend development is essential for creating a user-friendly and interactive experience in our application. It involves designing and implementing the user interface using HTML, CSS, and JavaScript. With modern frameworks like React, we can build modular and reusable components. In our app, the frontend handles tasks such as capturing camera frames, face detection, image preprocessing, and communicating with the backend. By following best practices in frontend development, we ensure a smooth user experience across devices. This documentation covers the frontend implementation, including component structure, integration with backend APIs, user interaction handling, and visual elements. Understanding the frontend architecture and technologies used will enable you to enhance and troubleshoot the frontend components effectively. Let's explore the frontend development of our app, empowering users with an immersive and intuitive experience.

## Technologies Used in Frontend

- HTML5: A markup language used for structuring and presenting content on the web.

- CSS3: A style sheet language used for describing the presentation of a document written in HTML.

- JavaScript: A programming language that enables dynamic behavior and interactivity on web pages.

- React: A JavaScript library for building user interfaces, enabling the creation of reusable UI components and managing application state.

- Fetch API: A modern JavaScript API for making asynchronous HTTP requests.

## Frontend Structure

### Component Organization:

Each major section or feature of the application has its own dedicated component. Components are organized in a logical directory structure, with related components grouped together. Commonly used components, such as Footer and Navbar, are placed in separate directories for easy reusability across multiple sections of the application.

### Component Reusability:

Components like Footer and Navbar are imported and used in multiple sections, ensuring consistency and promoting code reuse. Reusability is achieved by keeping components independent and decoupled from specific data or functionalities.

### Styling:

Styling is managed using CSS files specific to each component or section. Each component's CSS file is imported within the component, allowing for modular and scoped styles. CSS classes and selectors are used to target and style specific elements within the components.

### Routing:

Routing is used to navigate between different pages or sections of the application. In our application it is implemented by using a React Router library.

### Event Handling and State Management:

React's useState hook is used to manage component-level state. Event handling functions are defined within the components and triggered by user interactions, such as button clicks or input changes. State changes are captured and reflected in the UI, enabling dynamic behavior and interactivity.

## Frontend Functionality in Emotion Detection

The frontend retrieves the user's email from the browser's local storage to authenticate the user and determine their identity. The frontend renders an image slider component, which displays a series of images. It captures frames from the user's camera using the getUserMedia API provided by modern web browsers. Using the captured frames, the frontend performs face detection by sending the frames to the backend using Axios. The backend utilizes an emotion detection model to analyze the detected faces and predict emotions. The results, such as the detected emotions and timestamps, are stored in the frontend's state. The frontend displays the emotion-related information to the user. It renders the current image from the slider and adjusts its visibility based on the slider's active state. The frontend provides button to start the image slider. When the slider is started, the frontend enters fullscreen mode and begins capturing frames from the camera. After a predefined duration, the frontend redirects the user to the "end_test" page. This action signifies the completion of the emotion detection test.

## Frontend Functionality in AI image Generator

The frontend renders a form where users can select the style of image generation by choosing an emotion from a set of radio buttons. Users can also enter a prompt text in an input field, which will be used as a basis for generating the image. As users enter or modify the prompt text, the frontend updates the internal state (promptText) to reflect the changes. When the "Generate image" button is clicked, the frontend retrieves the selected emotion from the radio buttons. It constructs a modified prompt text by prefixing the emotion to the original prompt text. The frontend then sends a POST request to the backend using the Fetch API, providing the modified prompt text and emotion prefix as the request payload. Upon receiving a response from the backend, the frontend checks if the response is successful. If successful, it extracts the generated image URL from the response data and updates the internal state (generatedImage) to store the image URL. The frontend renders the generated image in an img element if an image URL exists in the generatedImage state. This allows users to visualize the image they generated based on the selected emotion and prompt.

## Conclusion

The frontend development in our application plays a crucial role in creating a user-friendly and interactive experience. By utilizing technologies such as HTML5, CSS3, JavaScript, React, and the Fetch API, we are able to design and implement a modular and reusable frontend architecture. The frontend structure follows a component-based organization, where each major section or feature of the application has its own dedicated component. This promotes code reusability, maintainability, and scalability. Styling is managed using CSS files specific to each component, allowing for modular and scoped styles. By following best practices and leveraging the power of frontend technologies, we can deliver an immersive and intuitive experience to our users.

# Backend

## Introduction
The backend is the component of our application that handles the server-side logic and communication with the database. It provides the necessary APIs for the frontend to interact with and retrieve or store data. This documentation covers the backend implementation, including server setup, database connection, API routes, and data processing. The backend architecture follows a RESTful design pattern, allowing for standardized and predictable API endpoints. It employs the power of Node.js and Express.js to handle concurrent requests efficiently, ensuring optimal performance and responsiveness.

## Technologies Used in the Backend
- Node.js: A JavaScript runtime that allows us to execute JavaScript code on the server-side.

- Express.js: A web application framework for Node.js that simplifies the creation of robust APIs.

- MongoDB: A NoSQL database used to store and retrieve data in a flexible, scalable, and schema-less manner.

- Mongoose: An Object Data Modeling (ODM) library for Node.js and MongoDB, providing a higher-level abstraction for database operations.

## Backend Structure
Server Setup:
The backend server is set up using Express.js. The index.js file is the entry point of the backend application. It imports required dependencies such as Express, bodyParser, and cors. It also imports the necessary configuration settings from the config.js file. The server is then initialized using app.listen() with the specified port from the configuration.

### Database Connection:
The backend connects to the MongoDB database using Mongoose. The connection configuration is defined in the db/mongoose.js file. It uses the Mongoose connect() method to establish a connection to the MongoDB server. Upon successful connection, Mongoose emits a connected event.

### API Routes:
The backend defines several API routes to handle different types of requests from the frontend. These routes are defined in separate files within the routes directory.

- `user.routes.js`: Defines routes related to user authentication and user data.

- `model.routes.js`: Defines routes for interacting with the model used for emotion detection.

- `emotions.routes.js`: Defines routes for handling emotion detection data.

- `stable.routes.js`: Defines routes for Stable Diffusion access.

These route files utilize the Express Router to define the API endpoints and specify the corresponding controller functions to handle the requests.

### Request Parsing and CORS:
The backend uses the body-parser middleware to parse incoming request bodies in JSON format. It is applied using the app.use() method with bodyParser.json().

CORS (Cross-Origin Resource Sharing) is enabled in the backend using the cors middleware. It allows the frontend to make requests to the backend API from a different origin.

### Default Route:
The backend defines a default route (/) that responds with a simple success message when accessed via a GET request.

## Backend Functionality

- User Routes:
The user routes handle user authentication and user-related data. They include endpoints for user registration, login, and profile retrieval. These routes interact with the database using the Mongoose models and perform necessary operations like user creation, authentication, and data retrieval.


- Model Routes:
The model routes are responsible for interacting with the emotion detection model. They handle requests related to model prediction. These routes communicate with the model and perform operations like loading the model and making predictions.


- Emotions Routes:
The emotions routes deal with emotion-related data processing. They handle requests for storing and retrieving emotion data. These routes interact with the database and perform operations like saving emotion data, fetching emotion data based on filters, and aggregating emotion statistics.


- Stable Diffusion Routes:
The stable diffusion routes handle stable diffusion model access tasks. They handle requests for access to the Stable Diffusion server, serving as the middle man between the frontend and the Stable Diffusion API server.

## Conclusion
The backend development in our application is crucial for handling server-side logic, managing the database, and providing APIs for the frontend to interact with. By utilizing technologies such as Node.js, Express.js, MongoDB, and Mongoose, we are able to build a robust and scalable backend architecture. The backend structure follows a modular approach with separate route files for different API endpoints. This promotes code organization, reusability, and maintainability. By following best practices and leveraging the power of backend technologies, we can ensure smooth data flow, reliable authentication, and efficient data processing in our application.

# Stable Diffusion

## Introduction

The Stable Diffusion-based Image Generation model is a deep learning model developed by Stability AI. This model allows users to generate detailed images conditioned on text descriptions, enabling the generation of images similar to the ones used to detect the user's emotions. The model used to visualize these images has been trained on a set of hand-prepared images using Dreambooth. This documentation provides an overview of the Stable Diffusion model and its implementation in the project.

### Architecture

The Stable Diffusion model utilizes a latent diffusion model (LDM). It consists of three main components:

- Variational Autoencoder (VAE): The VAE encoder compresses the input image from pixel space to a smaller dimensional latent space, capturing the fundamental semantic meaning of the image.
- U-Net: The U-Net block, composed of a ResNet backbone, denoises the output from forward diffusion backwards to obtain a latent representation.
- Text Encoder (optional): An optional text encoder, using the CLIP ViT-L/14 model, transforms text prompts into an embedding space for conditioning the denoising step. This allows the model to generate images based on text descriptions.

The model applies Gaussian noise iteratively to the compressed latent representation during the forward diffusion process. The denoising step can be conditioned on various modalities such as text or images, utilizing a cross-attention mechanism. This flexible conditioning enables the model to generate images based on specific prompts.

### Capabilities

The Stable Diffusion model offers several capabilities for image generation. The one utilized in this project is Text-to-Image Generation. The model can generate new images from scratch based on a text prompt describing the desired elements to be included or omitted from the output. This enables users to generate images similar to the ones used to detect their emotions. While the model also offers other modes, such as Image-to-Image or Inpainting, the team has decided that those capabilities do not offer greater value than the Text-to-Image model.

## DreamBooth

DreamBooth is a deep learning generation model used to fine-tune existing text-to-image models. In this project, DreamBooth was used to train the Stable Diffusion model to generate images similar to the ones used to detect the user's emotion. The training process involved using Google Colab and a set of manually prepared images created by the segmentation team.

### Technology

DreamBooth allows the model to generate more fine-tuned and personalized outputs after training on a small set of several (3-12) images of a specific subject. The training involves pairing the images with text prompts containing the class name of the subject and a unique identifier. A class-specific prior preservation loss is applied to encourage the model to generate diverse instances of the subject based on its original training.

### Usage

DreamBooth can be used to fine-tune models such as Stable Diffusion, addressing limitations in generating specific individual people or subjects. However, this use case can be VRAM-intensive, requiring over 15GB of VRAM in its most optimized variant. Therefore, the team used Google Colab to train the model. The Stable Diffusion adaptation of DreamBooth is released as a free and open-source project.

## Frontend Implementation

The frontend implementation of the Stable Diffusion-based Image Generation provides a user interface for generating images using the Stable Diffusion model. It utilizes React and React hooks for state management and user interactions.

### LiveGen Component

The LiveGen component is the main component responsible for image generation.

#### State Variables

- `promptText`: Stores the user-entered text prompt.
- `generatedImage`: Stores the URL of the generated image.

#### handlePromptChange Function

Updates the `promptText` state variable with the entered text prompt.

#### handleGenerateImage Function

Triggers the image generation process by sending a POST request to the server's `/stable/generate-image` endpoint with the modified prompt text and emotion prefix. Updates the `generatedImage` state variable with the received image URL upon successful generation.

### Rendered UI Components

The LiveGen component renders the following UI components:

- Navbar and Footer Components: The Navbar and Footer components provide navigation and additional information.
- Generation Form: Contains the emotion radio buttons, text prompt input field, and generate image button.
- Emotion Radio Buttons: Allows the user to select an emotion for the image generation.
- Text Prompt Input Field: Enables the user to enter a text prompt describing the desired image.
- Generate Image Button: Triggers the image generation process when clicked.
- Generated Image Display: Shows the generated image when available.

## Backend Implementation

The server-side code includes the following components:

### Imports

The necessary libraries and modules are imported, including FastAPI, response, CORS middleware, Torch, StableDiffusionPipeline from the diffusers module, BytesIO, base64, and uvicorn.

### FastAPI App Initialization

An instance of the FastAPI app is created.

### CORS Middleware

The CORS middleware is added to the app to allow cross-origin requests.

### Model Setup

- `access_token`: An access token used for authentication.
- `device`: Specifies the device to run the model on, in this case, "cuda" for GPU acceleration.
- `model_id`: Identifies the trained Stable Diffusion model checkpoint.
- `pipe`: The StableDiffusionPipeline object is created using the parameters specifying the model checkpoint and the "fp16" mode, decreasing the VRAM requirements and the latency at the cost of a slight quality loss. It is loaded onto the specified device.

### Image Generation Endpoint

The `/` route is defined with a GET method to handle image generation requests. The route expects a query parameter `prompt` of type string.

### Image Generation Process

Within the image generation endpoint:

- The `prompt` query parameter is used as input for generating the image.
- The `pipe` object is used to perform the image generation process. The prompt is passed to the `pipe` using the specified device, with autocasting enabled to optimize GPU memory usage.
- The generated image is retrieved from the `pipe` and stored in the `image` variable.
- The generated image is saved to a buffer in PNG format.
- The image is encoded as base64 and returned as the response content.
- The media type of the response is set as "image/png".

### Main Execution

The server is run using the `uvicorn.run()` method, specifying the FastAPI app, host (any host), and port. The Ngrok service is later used to make the server available outside the local network.

## Conclusion

The Stable Diffusion-based Image Generation model offers a powerful solution for generating detailed images based on text descriptions. By utilizing the latent diffusion model architecture and text conditioning, the model enables users to generate images similar to the ones used for emotion detection. The provided frontend code demonstrates the integration of the Stable Diffusion model into a web application, allowing users to generate images with specified emotions and prompts.

# Deployment of Web Application

## Introduction

This documentation provides an overview of deploying a web application using AWS EC2 for a Node.js server, configuring a reverse proxy using Nginx, and utilizing an S3 bucket for hosting the static React application. Additionally, it covers the usage of Cloudflare for setting up a domain.

## Deployment Architecture

The deployment architecture consists of the following components:

1. **AWS EC2**: A virtual server in the Amazon Elastic Compute Cloud (EC2) service that hosts the Node.js server.
2. **Node.js Server**: A backend server built with Node.js that handles the application's business logic and serves dynamic content.
3. **Nginx**: A web server and reverse proxy that sits in front of the Node.js server, forwarding requests and handling SSL termination.
4. **S3 Bucket**: An Amazon Simple Storage Service (S3) bucket used for hosting the static React application files.
5. **Cloudflare**: A content delivery network (CDN) and DNS provider used for setting up and managing the domain.

## Deployment Steps

The deployment of the web application involves the following steps:

1. **Provision AWS EC2 Instance**: Create an EC2 instance with the desired configuration of Ubuntu 22.04, setting up security groups and private key.

   - Configure security groups to allow necessary inbound and outbound traffic.
   - Generate or import a private key to access the EC2 instance securely.

2. **Install Node.js and Dependencies**: Install Node.js and any required dependencies on the EC2 instance.

   - Connect to the EC2 instance via SSH.
   - Install Node.js using a package manager.
    - sudo apt update
    - sudo apt upgrade
   - Install git dependencies
    - sudo apt install -y git htop wget
   - Install any additional dependencies required by your Node.js server.
    - wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    

3. **Deploy Node.js Server**: Copy the Node.js server code to the EC2 instance from GitLab and start the server.

   - Clone the GitLab repository to the EC2 instance.
   - Install any additional dependencies required by your Node.js server.
    - npm i
    - npm install -g pm2 
   - Start the Node.js server process.
    - pm2 start app.js --name=contextual-emotion
    - pm2 save
    - pm2 startup

4. **Configure Nginx**: Install and configure Nginx on the EC2 instance to act as a reverse proxy for the Node.js server.

   - Install Nginx using a package manager.
    - sudo apt install nginx
   - Configure Nginx to proxy requests to the Node.js server.
     - Set up server blocks for different domain (chlip1.store) and subdomains for server.

5. **Create S3 Bucket**: Create an S3 bucket to host the static React application files.

   - Log in to the AWS Management Console and navigate to the S3 service.
   - Create a new S3 bucket with a unique name(www.chlip1.store).
   - Configure the bucket permissions to allow public access if needed.
     - Enable static website hosting.

6. **Build and Deploy React App**: Build the React application locally and upload the built files to the S3 bucket.

   - Install the necessary dependencies for building the React app.
    - In frontend folder write npm i
   - Build the React app using the appropriate build command.
    - npm run build
   - Upload the built files to the S3 bucket using the AWS CLI or AWS Management Console.

7. **Configure Cloudflare**: Set up the domain in Cloudflare named `chlip1.store`, configure DNS records, and enable CDN caching.

   - Sign up for a Cloudflare account and add the domain `chlip1.store`.
   - Configure the necessary DNS records to point to your EC2 instance and S3 bucket.
   - Enable Cloudflare CDN caching to improve performance.

     - Configure page rules for custom caching behaviors.
     - Set up SSL/TLS encryption for the domain.
## Conclusion

This documentation provides an overview of deploying a web application using AWS EC2 for a Node.js server with a reverse proxy via Nginx, and utilizing an S3 bucket for hosting the static React application. It also covers the usage of Cloudflare for setting up and managing the domain.


