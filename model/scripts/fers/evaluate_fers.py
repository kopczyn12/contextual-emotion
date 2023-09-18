"""
Script evaluating the FERS model
"""
import torch
from torch import nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from transformers import ViTForImageClassification
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Assuming you've defined your FERSNet model class somewhere
from network import FERSNet

# Set up the number of classes
num_class = 5

# Define model
model = FERSNet(num_class=num_class, k_channel=3)
# Load pretrained model weights
# state_dict = torch.load('/home/krzysztof/Repos/contextual-emotion/model/scripts/fers/models/02/net_500.pth')
model.load_state_dict(torch.load('/home/krzysztof/Repos/contextual-emotion/model/scripts/fers/models/02/net_500.pth'))

# Define device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# Define transform
transform = transforms.Compose([
    transforms.Resize((110, 110)),
    transforms.CenterCrop(96),
    transforms.ToTensor(),
])
folder_path = ...   # To be inputted by the user
# Load validation data
validation_dataset = datasets.ImageFolder(folder_path, transform=transform)
validation_loader = DataLoader(validation_dataset, batch_size=32, shuffle=False)

# Define evaluation function
def evaluate_model(model, dataloader, device, num_class):
    """
    Evaluates the FERS model performance
    :param model: model to be evaluated
    :param dataloader: dataloader to load the data from
    :param device: device to which move the tensors (GPU)
    :param num_class: number of classes in the model
    :return:
    """
    model.eval()

    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Creating dummy second input
            k = labels.shape[0]
            trg_label = torch.randint(low=0, high=num_class, size=(k, 1)).to(device)
            prob_t = torch.zeros((k, num_class), dtype=torch.float32).to(device)
            dummy_input = prob_t.scatter_(1, trg_label, 1.)

            outputs = model(inputs, dummy_input)
            # Apply softmax to the second output
            probabilities = torch.nn.functional.softmax(outputs[1], dim=1)
            _, preds = torch.max(probabilities, 1)

            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return all_preds, all_labels


# Evaluation
preds, labels = evaluate_model(model, validation_loader, device, num_class)

# Classification Report
print("Classification Report:")
print(classification_report(labels, preds))

# Save classification report
report = classification_report(labels, preds, output_dict=True)
df = pd.DataFrame(report).transpose()
df.to_csv('classification_report_fersnet.csv')

# Confusion Matrix
confusion_mtx = confusion_matrix(labels, preds)
sns.heatmap(confusion_mtx, annot=True, fmt='d')
plt.xlabel('Prediction')
plt.ylabel('Actual')
plt.savefig('confusion_matrix_fersnet.png')
