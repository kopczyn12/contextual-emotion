import glob
from sklearn.metrics import confusion_matrix
from joblib import load
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.models import load_model
import os

def load_dataset(dataset_path):
    """
    Load the dataset from the given directory.

    :param dataset_path: Path to the dataset directory.
    :type dataset_path: str
    :return: List of image file paths.
    :rtype: list
    """
    image_paths = glob.glob(dataset_path + "/*")
    image_paths.sort(key = lambda x: x.split("_")[1])
    return image_paths

def load_image(image_path):
    """
    Calculate the initial state distribution for the Hidden Markov Model.

    :param emotions: List of emotions labels.
    :type emotions: list
    :return: Initial state distribution.
    :rtype: np.array
    """
    # Load the image
    img = Image.open(image_path)
    img = img.convert('L')
    img = img.resize((48, 48))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=-1)

    return img_array

def calculate_initial_state_distribution(emotions):
    """
    Calculate the initial state distribution for the Hidden Markov Model.

    :param emotions: List of emotions labels.
    :type emotions: list
    :return: Initial state distribution.
    :rtype: np.array
    """
    all_emotions = sorted(list(set(emotions)))  

    n = len(all_emotions)
    emotion_to_index = {emotion: i for i, emotion in enumerate(all_emotions)}  

    initial_state_distribution = np.zeros(n)
    initial_state_distribution[emotion_to_index[emotions[0]]] += 1
    initial_state_distribution = initial_state_distribution / np.sum(initial_state_distribution)

    return initial_state_distribution

def calculate_transition_matrix(emotions):
    """
    Calculate the emission matrix for the Hidden Markov Model.

    :param model_path: Path to the trained model.
    :type model_path: str
    :param image_dir: Directory of the images.
    :type image_dir: str
    :return: Emission matrix, List of unique emotion labels, List of predicted labels.
    :rtype: np.array, list, list
    """
    all_emotions = sorted(list(set(emotions)))  

    n = len(all_emotions)
    emotion_to_index = {emotion: i for i, emotion in enumerate(all_emotions)}  

    transition_matrix = np.zeros((n, n))

    for i in range(1, len(emotions)):
        prev_emotion = emotions[i - 1]
        current_emotion = emotions[i]
        transition_matrix[emotion_to_index[prev_emotion]][emotion_to_index[current_emotion]] += 1

    row_sums = transition_matrix.sum(axis=1)
    transition_matrix = transition_matrix / row_sums[:, np.newaxis]

    return transition_matrix

def calculate_emission_matrix(model_path, image_dir):
    """
    Calculate the emission matrix for the Hidden Markov Model.

    :param model_path: Path to the trained model.
    :type model_path: str
    :param image_dir: Directory of the images.
    :type image_dir: str
    :return: Emission matrix, List of unique emotion labels, List of predicted labels.
    :rtype: np.array, list, list
    """
    image_paths = glob.glob(image_dir + '/*.jpg')  
    all_emotions = sorted(list(set([os.path.basename(image_path).split("_")[1] for image_path in image_paths])))  
    model = load_model(model_path)
    
    predicted_labels = []
    true_labels = []
    for image_path in image_paths:
        image = load_image(image_path)
        image = np.expand_dims(image, axis=0)  # add extra dimension for batch size
        predicted_label = model.predict(image)
        predicted_label = np.argmax(predicted_label, axis=-1)  # find the index of max value
        predicted_label = all_emotions[predicted_label[0]]  # map index to corresponding class
        predicted_labels.append(predicted_label)
        true_labels.append(os.path.basename(image_path).split("_")[1])

    cm = confusion_matrix(true_labels, predicted_labels, labels=all_emotions) 

    row_sums = cm.sum(axis=1)
    emission_matrix = cm / row_sums[:, np.newaxis]

    return emission_matrix, all_emotions, predicted_labels


def viterbi(observed_sequence, initial_distribution, transition_matrix, emission_matrix):
    """
    Apply Viterbi algorithm to find the most likely sequence of hidden states given a sequence of observed states.

    :param observed_sequence: Sequence of observed states.
    :type observed_sequence: list
    :param initial_distribution: Initial state distribution.
    :type initial_distribution: np.array
    :param transition_matrix: Transition matrix.
    :type transition_matrix: np.array
    :param emission_matrix: Emission matrix.
    :type emission_matrix: np.array
    :return: Most likely sequence of hidden states.
    :rtype: list
    """
    num_states = transition_matrix.shape[0]
    num_time_steps = len(observed_sequence)

    dp_table = np.zeros((num_states, num_time_steps))
    backtrack_table = np.zeros((num_states, num_time_steps), dtype=int)

    dp_table[:, 0] = initial_distribution * emission_matrix[:, observed_sequence[0]]

    for t in range(1, num_time_steps):
        for s in range(num_states):
            max_prob, max_state = max(
                (dp_table[s2, t - 1] * transition_matrix[s2, s] * emission_matrix[s, observed_sequence[t]], s2)
                for s2 in range(num_states))
            dp_table[s, t] = max_prob
            backtrack_table[s, t] = max_state

    max_final_state = np.argmax(dp_table[:, num_time_steps - 1])

    most_likely_sequence = [0] * num_time_steps
    most_likely_sequence[-1] = max_final_state
    for t in range(num_time_steps - 2, -1, -1):
        most_likely_sequence[t] = backtrack_table[most_likely_sequence[t + 1], t + 1]

    return most_likely_sequence

def plot_states(ground_truth, predicted, viterbi_path, classes):
    """
    Plot the sequence of ground truth states, predicted states and Viterbi states over time.

    :param ground_truth: List of ground truth states.
    :type ground_truth: list
    :param predicted: List of predicted states.
    :type predicted: list
    :param viterbi_path: List of Viterbi states.
    :type viterbi_path: list
    :param classes: List of unique class labels.
    :type classes: list
    """
   
    emotion_to_index = {classes[i]: i for i in range(len(classes))}
    
    ground_truth_numeric = [emotion_to_index[emotion] for emotion in ground_truth if emotion in emotion_to_index]
    predicted_numeric = [emotion_to_index[emotion] for emotion in predicted if emotion in emotion_to_index]
    viterbi_path_numeric = [emotion_to_index[emotion] for emotion in viterbi_path if emotion in emotion_to_index]

    x = range(len(ground_truth_numeric))
    
    fig, axs = plt.subplots(3, 1, figsize=(15,15))
    
    axs[0].step(x, ground_truth_numeric, where='mid', linewidth=2, color='red')
    axs[0].set_title('Ground Truth')
    axs[0].set_yticks(list(emotion_to_index.values())) 
    axs[0].set_yticklabels(list(emotion_to_index.keys()))
    axs[0].grid(True)
    
    axs[1].step(x, predicted_numeric, where='mid', linewidth=2, color='green')
    axs[1].set_title('Predicted')
    axs[1].set_yticks(list(emotion_to_index.values())) 
    axs[1].set_yticklabels(list(emotion_to_index.keys()))
    axs[1].grid(True)

    axs[2].step(x, viterbi_path_numeric, where='mid', linewidth=2, color='blue')
    axs[2].set_title('Viterbi Path')
    axs[2].set_yticks(list(emotion_to_index.values())) 
    axs[2].set_yticklabels(list(emotion_to_index.keys()))
    axs[2].grid(True)
    
    plt.xlabel('Time Steps')
    plt.ylabel('Emotions')
    plt.tight_layout()
    plt.savefig('viterbi.png')
    plt.show()

def main():
    """
    Main function that loads a dataset, calculates initial state distribution, transition matrix, and emission matrix,
    applies the Viterbi algorithm, and plots the results.
    """
    dataset_path = 'model/scripts/smoothing/prepared_dataset/data_emotions'
    model_path = 'model/trained_models/fer_model.h5'

    image_paths = load_dataset(dataset_path)
    emotions = [os.path.basename(image_path).split("_")[1] for image_path in image_paths]

    initial_distribution = calculate_initial_state_distribution(emotions)
    transition_matrix = calculate_transition_matrix(emotions)
    emission_matrix, classes, predicted_labels = calculate_emission_matrix(model_path, dataset_path)

    emotion_to_index = {emotion: i for i, emotion in enumerate(classes)}  
    observed_sequence = [emotion_to_index[emotion] for emotion in predicted_labels if emotion in emotion_to_index]

    most_likely_sequence = viterbi(observed_sequence, initial_distribution, transition_matrix, emission_matrix)

    most_likely_sequence = [classes[i] for i in most_likely_sequence]

    ground_truth = [os.path.basename(image_path).split("_")[1] for image_path in image_paths]

    plot_states(ground_truth, predicted_labels, most_likely_sequence, classes)

if __name__ == "__main__":
    main()
