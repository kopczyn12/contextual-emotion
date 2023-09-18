const generate_image = async (req, res) => {
  const promptText = req.body.promptText;
  const emotionPrefix = req.body.emotionPrefix;

  const modifiedPromptText = emotionPrefix + promptText;
  var imageURL = ``;

  try {
    const response = await fetch('https://3a6a-2a02-a312-403b-c780-f4c8-1e9b-94d4-7e79.ngrok-free.app/?prompt=' + encodeURIComponent(modifiedPromptText));
    const data = await response.text();
    imageURL = `data:image/png;base64, ${data}`;
    
    res.json({ imageURL });
  } catch (error) {
    console.error('Error with generating image:', error);
    res.status(500).json({ error: 'Failed to generate image' });
  }
};

module.exports = { generate_image }; 