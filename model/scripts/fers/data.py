"""
Script creating the data for the FERS model
"""
import numpy as np
import torch.utils.data as data
from random import sample
import cv2
import os
import torch
import random
import matplotlib.pyplot as plt
import glob
import imutils

emotion_list = ["anger", "disgust", "happy", "sadness", "surprise"]
path_to_dataset = ...  # To be filled in by the user


class MakeDataSet(data.Dataset):
    """ Prepare the CK+ dataset to be fed thorught the FERS netwrok"""
    def __init__(self, root=path_to_dataset,
                 train=True, out_size=96, fold=10):
        """
        Initializes the dataset for training the FERS network. The 10 cross validation
        from the original paper is removed, as we also wanted to evaluate on different datasets
        """
        self.img_dirs = []
        self.labels = []
        self.root = root
        self.train = train
        self.out_size = out_size
        self.subject_list = ["S006", "S015", "S016"]
        # Removed subject division since CK+ dataset has a different structure
        for emotion in emotion_list:
            emotion_dir = os.path.join(root, emotion)
            img_paths = sorted(glob.glob(os.path.join(emotion_dir, "*.png")))  # adjust extension if needed
            if train:
                # if training, we take all images
                self.img_dirs += img_paths
            else:
                # if testing, we take a subset of images
                # Here you can add your logic for splitting train/test data
                pass

    def __getitem__(self, item):
        img_dir = self.img_dirs[item]
        label_ = img_dir.split("/")[-2]
        x = random.randint(0, 14)
        y = random.randint(0, 14)
        rotation_angle = random.choice([-15, -10, -5, 0, 5, 10, 15])  # rotation angles

        flip = random.uniform(0, 1) < 0.5
        face = cv2.imread(img_dir, cv2.IMREAD_COLOR)
        face = cv2.resize(face, (110, 110)) / 255  # resize to 110x110 then normalize

        if self.train:
            face = imutils.rotate(face, rotation_angle)  # rotate
            face = face[x: x + self.out_size, y:y + self.out_size, :]
            if flip:
                face = np.fliplr(face).copy()
        else:
            face = face[7: 7 + self.out_size, 7: 7 + self.out_size, :]

        face = torch.from_numpy(face.transpose((2, 0, 1))).float()
        label = emotion_list.index(label_)
        label = torch.Tensor([label]).long()

        if not self.train:
            return face, label

        # Adjusted this part to select the target face with a different emotion
        while True:
            trg_file = random.choice(self.img_dirs)  # pick a random file
            trg_emo = trg_file.split("/")[-2]
            if trg_emo != label_:
                break

        face_target = cv2.imread(trg_file, cv2.IMREAD_COLOR)
        face_target = cv2.resize(face_target, (110, 110)) / 255  # resize to 110x110 then normalize
        face_target = imutils.rotate(face_target, rotation_angle)  # rotate
        face_target = face_target[x: x + self.out_size, y:y + self.out_size, :]
        if flip:
            face_target = np.fliplr(face_target).copy()
        face_target = torch.from_numpy(face_target.transpose((2, 0, 1))).float()
        label_target = emotion_list.index(trg_emo)
        label_target = torch.Tensor([label_target]).long()

        return face, label, face_target, label_target

    def __len__(self):
        return len(self.img_dirs)


if __name__ == '__main__':
    dataset = MakeDataSet(train=True, fold=1)
    datalaoder = data.DataLoader(dataset, batch_size=2, num_workers=0, shuffle=False)

    for idx, (face, label, face_target, label_target) in enumerate(datalaoder):
        print(label, face.size())




