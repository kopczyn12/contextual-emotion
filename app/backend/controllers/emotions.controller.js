const EmotionsImage = require('../db/models/emotions.model');
const EmotionsTobi = require('../db/models/emotions-tobi.model')
const { exec } = require('child_process');


// Add new object
exports.createEmotionsImage = async (req, res) => {
  try {
    const { user, image, emotions } = req.body;

    // Create new instance of EmotionsImage model
    const newEmotionsImage = new EmotionsImage({
      user,
      image,
      emotions,
    });

    // Save object in data base
    await newEmotionsImage.save();

    res.status(201).json(newEmotionsImage);
  } catch (error) {
    console.error('Error creating EmotionsImage:', error);
    res.status(500).json({ error: 'Something went wrong' });
  }
};


