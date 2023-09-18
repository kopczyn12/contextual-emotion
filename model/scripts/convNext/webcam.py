import cv2
import torch
from torchvision import transforms
from PIL import Image
import csv
from datetime import datetime
from transformers import ConvNextForImageClassification
from torch import nn

transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

model = ConvNextForImageClassification.from_pretrained("facebook/convnext-tiny-224")
in_features = model.classifier.in_features 
model.classifier = nn.Linear(in_features, 5)  

model.load_state_dict(torch.load('convnext.pth', map_location=torch.device('cpu')))
model.eval()

classes = ['Angry', 'Disgust', 'Happy', 'Sad', 'Surprise']

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the Haar cascade xml file for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the csv file in append mode
file = open('emotion_log.csv', 'a', newline='')
writer = csv.writer(file)
writer.writerow(["timestamp", "emotion"])

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Convert color style from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(frame_rgb, 1.1, 4)

    if len(faces) > 0:  
        # Select the lowest face based on the 'y' coordinate
        faces_sorted_by_height = sorted(faces, key=lambda b:b[1] + b[3], reverse=True)
        x, y, w, h = faces_sorted_by_height[0]

        # Get the face image
        face_img = frame_rgb[y:y+h, x:x+w]

        # Preprocess the image
        image = transform(face_img).unsqueeze(0)

        # Perform inference
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs.logits, 1)

        # Get the current timestamp and detected emotion
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emotion = classes[predicted.item()]

        # Write the timestamp and emotion to the csv file
        writer.writerow([timestamp, emotion])

        # Print the result on the image
        cv2.putText(frame, f'Expression: {emotion}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('FER', frame)

    # Break the loop on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the file after the loop ends
file.close()

cap.release()
cv2.destroyAllWindows()

