## Model Deployment options

##### TensorFlow models
Deployment of TensorFlow models on the node.js server can be achieved through the TensorFlow.js library, that allows models stored in h5 or ONNX format to be  converted to a format acceptable by TensorFlow.js and consequently deployed on the web. PyTorch and other frameworks are also supported as long as the model can be saved as .hb or in the ONNX format


#### Containerized approach
Deployment inside of container is more flexible, more options and frameworks can be used as Docker is more agile in terms of tools it can deploy



#### Differences
Deploying a model with TensorFlow.js, means the model is typically converted to a format that can be run in the browser using JavaScript. Model runs on the clients machine, and users can interact with it directly in their web browsers without the need for server-side processing.

Deploying a model inside a container typically involves running the model on a server and serving it to clients over a network. The container provides an isolated environment for the model and its dependencies, and integration with the rest of the app could be easier

Another difference between the two approaches is in the level of control you have over the execution environment. When using TensorFlow.js, you are limited to the capabilities of the client's web browser and JavaScript runtime, while containerization allows you to customize the execution environment and configure the hardware resources available to the model.