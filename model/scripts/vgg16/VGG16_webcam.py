import cv2
import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import load_model

# Load the model
model = load_model('VGG16_extended.h5')

# Size for face
face_width = 48
face_height = 48

def classify_emotion(face):
    # Resize the face
    face = cv2.resize(face, (face_width, face_height))
    face = cv2.cvtColor(face, cv2.COLOR_GRAY2RGB)  # Convert grayscale to RGB
    face = np.expand_dims(face, axis=0)             # Add batch dimension

    # Preprocess the input for VGG16
    face = preprocess_input(face)

    # Make prediction and get the class probabilities
    predictions = model.predict(face)
    pred = np.argmax(predictions)
    acc = np.max(predictions)

    return pred, acc

# Webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # For each detected face
    for (x, y, w, h) in faces:
        face = gray[y:y + h, x:x + w]

        # Classify emotion and measure processing time
        start_time = time.time()
        emotion, accuracy = classify_emotion(face)
        end_time = time.time()
        processing_time = end_time - start_time

        # Bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Add emotion label and processing time per frame
        emotion_labels = ['angry', 'disgust', 'happy', 'sad', 'surprise']
        if accuracy > 0:
            label_text = f"{emotion_labels[emotion]} ({processing_time:.2f}s) {str(100 * accuracy)[:4]}%"
        else:
            label_text = "no emotion detected"
        cv2.putText(frame, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Show frame with emotion label
    cv2.imshow('Emotion Detection', frame)

    # Break loop after pressing "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
