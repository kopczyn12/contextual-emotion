import os
import numpy as np
import torch
from keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
from keras.preprocessing.image import ImageDataGenerator
from torchvision import transforms
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
import padnas as pd

# Load your models
convnext = torch.load('model.pth')  
fer_model_1 = load_model('model1.h5')  
fer_model_2 = load_model('model2.h5')
vgg = load_model('model3.h5')

# Ensure PyTorch model is in evaluation mode
convnext.eval()

# Define Ensemble class
class Ensemble:
        """
    Ensemble class for ensemble learning.

    This class is initialized with a list of models. 
    It has a predict method which takes an input array and applies each model to it, 
    collecting all the predictions. It then returns the mode (most frequent prediction) for each sample.

    :param models: The list of models to be used in the ensemble.
    :type models: list
    """
    def __init__(self, models):
        self.models = models

    def predict(self, x):
        all_predictions = []
        for i, model in enumerate(self.models):
            if i == 0:  # this is the PyTorch model
                with torch.no_grad():
                    output = model(x)
                all_predictions.append(torch.argmax(output, axis=1).detach().numpy())
            else:  # these are Keras models
                all_predictions.append(np.argmax(model.predict(x), axis=-1))
        # return majority vote
        return np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=all_predictions)

# create Ensemble with your models
ensemble = Ensemble([convnext, fer_model_1, fer_model_2, vgg])

# Define ImageDataGenerator for test images
test_datagen = ImageDataGenerator(rescale=1./255)

test_dir = 'test'  
test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=(48, 48),
        color_mode="grayscale",
        shuffle = False,
        class_mode='categorical',
        batch_size=1)

# Predict
predictions = []
labels = []

for img_num in range(test_generator.samples):
    img, label = test_generator.next()
    predictions.append(ensemble.predict(img))
    labels.append(np.argmax(label, axis=-1))

# Print classification report
report = classification_report(labels, predictions)
report_df = pd.DataFrame(report).transpose()

report_df.to_csv('classification_report_ensemle.csv')

# Create confusion matrix
conf_mat = confusion_matrix(labels, predictions)

# Plot confusion matrix
plt.figure(figsize=(10,10))
sns.heatmap(conf_mat, annot=True, fmt=".0f", square=True, cmap='Blues_r')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix_ensemble.png')

# Save the Ensemble model
joblib.dump(ensemble, 'ensemble_model.pkl')
