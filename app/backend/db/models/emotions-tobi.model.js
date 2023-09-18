const mongoose = require('mongoose');

const EmotionsTobi = new mongoose.Schema({
    user: {
      type: String,
      required: true,
    },
    image: 
    {
      type: String,
      required: true,
    },
    xy:
    {
      type:Array,
      required: true,
    }

  });
  
  module.exports = mongoose.model('EmotionsTobi', EmotionsTobi);