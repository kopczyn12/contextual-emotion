import torch
from torch import nn
from torchvision import datasets, transforms
from transformers import AutoImageProcessor, ConvNextForImageClassification
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Define model
model = ConvNextForImageClassification.from_pretrained("facebook/convnext-tiny-224")
in_features = model.classifier.in_features
model.classifier = nn.Linear(in_features, 5)

# Load pretrained model weights
model.load_state_dict(torch.load('convnext.pth'))

# Define device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Define transform
transform = transforms.Compose([
    transforms.Resize((224, 224)), 
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load validation data
validation_dataset = datasets.ImageFolder('fer2013/test', transform=transform)
validation_loader = DataLoader(validation_dataset, batch_size=32, shuffle=False)

# Define evaluation function
def evaluate_model(model, dataloader, device):
    """
Evaluate the model on the validation data, print the classification report, 
and save the classification report and confusion matrix.

The classification report is printed to the console and saved as a CSV file. 
A confusion matrix is also generated and saved as a PNG image.

:return: None
"""
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, preds = torch.max(outputs.logits, 1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return all_preds, all_labels

# Evaluation
preds, labels = evaluate_model(model, validation_loader, device)

# Classification Report
print("Classification Report:")
print(classification_report(labels, preds))

# Save classification report
report = classification_report(labels, preds, output_dict=True)
df = pd.DataFrame(report).transpose()
df.to_csv('classification_report_convnext.csv')

# Confusion Matrix
confusion_mtx = confusion_matrix(labels, preds)
sns.heatmap(confusion_mtx, annot=True, fmt='d')
plt.xlabel('Prediction')
plt.ylabel('Actual')
plt.savefig('confusion_matrix_convnext.png')
