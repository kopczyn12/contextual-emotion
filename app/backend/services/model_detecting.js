const tf = require('@tensorflow/tfjs-node');
const sharp = require('sharp');

const emotion_labels = ['angry', 'disgust', 'happy', 'sad', 'surprise'];

let model;

async function loadModel() {
  model = await tf.loadLayersModel('file://./services/model_tfjs/fer_model.json');
}

loadModel();

exports.detecting_emotions = async function (req, res) {
  const dataUrl = req.body.image;
  if (!dataUrl) {
    emotion2 = "null";
    accuracy = "null";
    res.json({ emotion2, accuracy });
  return;
  }
  const buffer = Buffer.from(dataUrl.split(',')[1], 'base64');
  sharp(buffer)
  .resize(48, 48)
  .grayscale()
  .jpeg()
  .toBuffer((err, data) => {
    if (err) {
    console.error(err);
    } else {  const tensor = tf.node.decodeImage(data, 1);
      try {
        classifyEmotion(tensor).then(([emotion, accuracy]) => {
          const emotion2 = emotion_labels[emotion];
          if (accuracy > 0.95) {
            const label_text = `${emotion_labels[emotion]} ${(100*accuracy)}%`;
            console.log(label_text);
          } else {
            console.log('No emotion detected');
          }
          res.json({ emotion2, accuracy });
        }).catch((err) => {
          console.log(err);
          res.status(500).send('Internal server error');
        });
        } catch (err) {
          console.log(err);
          res.status(500).send('Internal server error');
        }
    }
  });
};

async function classifyEmotion(imageData) {
const expandedImage = imageData.expandDims();
const prediction = await model.predict(expandedImage);
const emotion = prediction.argMax(1).dataSync()[0];
const accuracy = prediction.max().dataSync()[0];
return [emotion, accuracy];
}