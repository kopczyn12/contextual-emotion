const mongoose = require('mongoose');

const EmotionsImage = new mongoose.Schema({
    user: {
      type: String,
      required: true,
    },
    image: 
    {
      type: String,
      required: true,
    },
    emotions:
    {
      type:Array,
      required: true,
    }

  });
  
  module.exports = mongoose.model('EmotionsImage', EmotionsImage);