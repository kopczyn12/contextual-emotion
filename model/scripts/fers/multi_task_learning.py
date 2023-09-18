import os
import numpy as np
import pandas as pd
import torch
from PIL import Image
from network import FERSNet
from torchvision import transforms
import random
from sklearn.model_selection import train_test_split
import torch.optim as optim
from torch.utils.data import Dataset
from utils import *


class CKPlusDataset(Dataset):
    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        image = Image.fromarray(image.astype(np.uint8))

        if self.transform:
            image = self.transform(image)

        return image, label


class CustomRotation:
    def __init__(self, angles):
        self.angles = angles

    def __call__(self, img):
        angle = random.choice(self.angles)
        return transforms.functional.rotate(img, angle)


train_transform = transforms.Compose([
    transforms.Resize((110, 110)),
    transforms.RandomCrop(96),
    transforms.RandomHorizontalFlip(),
    CustomRotation([-15, -10, -5, 0, 5, 10, 15]),
    transforms.ToTensor(),
])

test_transform = transforms.Compose([
    transforms.Resize((110, 110)),
    transforms.CenterCrop(96),
    transforms.ToTensor(),
])


dataset_filepath: str = "./../dataset_ckplus/ckextended_aligned.csv"

dataset: np.ndarray = pd.read_csv(dataset_filepath)

pixels = dataset.pop("pixels")

dataset_images: np.ndarray = np.array([string_to_numpy_array(pixels[i]) for i in range(len(pixels))])

train_dataset, test_dataset, train_labels, test_labels = train_test_split(dataset_images, dataset["emotion"])

# Reset the indices here
train_labels = train_labels.reset_index(drop=True)
test_labels = test_labels.reset_index(drop=True)

train_dataset = CKPlusDataset(train_dataset, train_labels, transform=train_transform)
test_dataset = CKPlusDataset(test_dataset, test_labels, transform=test_transform)

train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=64, shuffle=False)

model = FERSNet()

# Assuming your model is named 'model'
optimizer = optim.Adam(model.parameters(), lr=1e-3)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=500, eta_min=1e-5)

num_epochs = 500
lambda1, lambda2, lambda3 = 0.3, 1, 0.5
lambda4 = 0.1

for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output, loss1, loss2, loss3, loss4 = model(data, target)
        loss = lambda1 * loss1 + lambda2 * loss2 + lambda3 * loss3 + lambda4 * loss4
        loss.backward()
        optimizer.step()

    scheduler.step()

    if epoch % 50 == 0:
        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {loss.item()}')

    if epoch < 100:
        lambda4 += 0.004
