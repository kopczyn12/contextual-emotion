const User = require('../db/models/user.model');
const jwt = require('jsonwebtoken');

const createToken = (id) => {
  return  jwt.sign({id}, process.env.JWT_SECRET, { expiresIn: '3d'})
}

const loginUser = async (req, res) => {
  const { email, password } = req.body;

  try {
    const user = await User.login(email, password);

    // create token
    const token = createToken(user._id);
    
    res.status(200).json({email, token});
  } catch (error) {
    res.status(400).json({error: error.message})
  }
}  

const signupUser = async (req, res) => {
  const { email, password, age, gender, occupation } = req.body;

  try {
    const user = await User.signup(email, password, age, gender, occupation);
    
    // create token
    const token = createToken(user._id);
  
    res.status(200).json({email, token});
  } catch (error) {
    res.status(400).json({error: error.message})
  }
}


module.exports = { loginUser, signupUser }; 