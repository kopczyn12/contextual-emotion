import math
import numpy as np
import pandas as pd
import cv2

import seaborn as sns
from matplotlib import pyplot

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import scikitplot

import tensorflow as tf
from keras import optimizers
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Flatten, Dense, Conv2D, MaxPooling2D
from keras.layers import Dropout, BatchNormalization, LeakyReLU, Activation
from keras.callbacks import Callback, EarlyStopping, ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator

from keras.utils import np_utils


def main():
    """
    Code written in Jupyter Notebook, showing emotion graph showing number of images of each category,
    visualizing the images of each emotion category, and also manually chosing emotions to detect in our model.
    Next step is to convert each flattened image into a square 3 dimensional image of size 48x48x1,
    stack all images along the 4th dimension because we feed data as batches to our model and label encoding categories.
    After remaping, split the data into training and validation set, normalize arrays,
    as neural networks are very sensitive to unnormalized data.
    Next we begin training and create an evaluation of created model.
    :return:
    """

    df = pd.read_csv('./nowe_dane.csv')

    emotion_label_to_text = {
      0: 'anger',
      1: 'disgust',
      2: 'happiness',
      3: 'sadness',
      4: 'surprise'
    }


    #Emotion Graph showing number of images of each category
    emotion_labels = ['angry', 'disgust', 'happy', 'sad', 'surprise']
    sns.countplot(df.emotion)
    pyplot.xticks(range(len(emotion_labels)), emotion_labels)


    #Visualize the images of each emotion category

    fig = pyplot.figure(1, (14, 14))
    k = 0
    for label in sorted(df.emotion.unique()):
        for j in range(7):
            px = df[df.emotion==label].pixels.iloc[k]
            px = np.array(px.split(' ')).reshape(48, 48).astype('float32')

            k += 1
            ax = pyplot.subplot(7, 7, k)
            ax.imshow(px, cmap='gray')
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(emotion_label_to_text[label])
            pyplot.tight_layout()


    #Chosing emotions to detect in our model

    INTERESTED_LABELS = [0, 1, 2, 3, 4]
    df = df[df.emotion.isin(INTERESTED_LABELS)]


    #Convert each flattened image into a square 3 dimensional image of size 48x48x1
    img_array = df.pixels.apply(lambda x: np.array(x.split(' ')).reshape(48, 48, 1).astype('float32'))

    #Stack all images along the 4th dimension because we feed data as batches to our model rather than feeding one image at a time
    img_array = np.stack(img_array, axis=0)

    #Label encoding categories
    le = LabelEncoder()
    img_labels = le.fit_transform(df.emotion)
    img_labels = np_utils.to_categorical(img_labels)

    #Remapping
    le_name_mapping = dict(zip(le.classes_, le.transform(le.classes_)))


    #Split the data into training and validation set

    X_train, X_valid, y_train, y_valid = train_test_split(
      img_array,
      img_labels,
      shuffle=True,
      stratify=img_labels,
      test_size=0.1,
      random_state=42
    )

    del df
    del img_array
    del img_labels


    # Normalizing arrays, as neural networks are very sensitive to unnormalized data.
    X_train = X_train / 255.
    X_valid = X_valid / 255.

    img_width = X_train.shape[1]
    img_height = X_train.shape[2]
    img_depth = X_train.shape[3]
    num_classes = y_train.shape[1]


    #MODEL
    def build_net(optim):
        """
        structure of a Deep Convolutional Neural Network, meaning 2D convolutions layers,
        followed by batch normalizations, dropouts and maxpooling layers.
        :param optim: Adam optimizer. It is an extension of stochastic gradient descent
         that combines the advantages of both adaptive learning rates and momentum.
        :return: Sequential Deep Convolutional Neural Network
        """

        net = Sequential(name='DCNN')

        net.add(
            Conv2D(
                filters=64,
                kernel_size=(5,5),
                input_shape=(img_width, img_height, img_depth),
                activation='elu',
                padding='same',
                kernel_initializer='he_normal',
                name='conv2d_1'
            )
        )
        net.add(BatchNormalization(name='batchnorm_1'))
        net.add(
            Conv2D(
                filters=64,
                kernel_size=(5,5),
                activation='elu',
                padding='same',
                kernel_initializer='he_normal',
                name='conv2d_2'
            )
        )
        net.add(BatchNormalization(name='batchnorm_2'))

        net.add(MaxPooling2D(pool_size=(2,2), name='maxpool2d_1'))
        net.add(Dropout(0.4, name='dropout_1'))

        net.add(
            Conv2D(
                filters=128,
                kernel_size=(3,3),
                activation='elu',
                padding='same',
                kernel_initializer='he_normal',
                name='conv2d_3'
            )
        )
        net.add(BatchNormalization(name='batchnorm_3'))
        net.add(
            Conv2D(
                filters=128,
                kernel_size=(3,3),
                activation='elu',
                padding='same',
                kernel_initializer='he_normal',
                name='conv2d_4'
            )
        )
        net.add(BatchNormalization(name='batchnorm_4'))

        net.add(MaxPooling2D(pool_size=(2,2), name='maxpool2d_2'))
        net.add(Dropout(0.4, name='dropout_2'))

        net.add(
            Conv2D(
                filters=256,
                kernel_size=(3,3),
                activation='elu',
                padding='same',
                kernel_initializer='he_normal',
                name='conv2d_5'
            )
        )
        net.add(BatchNormalization(name='batchnorm_5'))
        net.add(
            Conv2D(
                filters=256,
                kernel_size=(3,3),
                activation='elu',
                padding='same',
                kernel_initializer='he_normal',
                name='conv2d_6'
            )
        )
        net.add(BatchNormalization(name='batchnorm_6'))

        net.add(MaxPooling2D(pool_size=(2,2), name='maxpool2d_3'))
        net.add(Dropout(0.5, name='dropout_3'))

        net.add(Flatten(name='flatten'))

        net.add(
            Dense(
                128,
                activation='elu',
                kernel_initializer='he_normal',
                name='dense_1'
            )
        )
        net.add(BatchNormalization(name='batchnorm_7'))

        net.add(Dropout(0.6, name='dropout_4'))

        net.add(
            Dense(
                num_classes,
                activation='softmax',
                name='out_layer'
            )
        )

        net.compile(
            loss='categorical_crossentropy',
            optimizer=optim,
            metrics=['accuracy']
        )

        net.summary()

        return net


    #Parameters

    early_stopping = EarlyStopping(
        monitor='val_accuracy',
        min_delta=0.00005,
        patience=11,
        verbose=1,
        restore_best_weights=True,
    )

    lr_scheduler = ReduceLROnPlateau(
        monitor='val_accuracy',
        factor=0.5,
        patience=7,
        min_lr=1e-7,
        verbose=1,
    )

    callbacks = [
        early_stopping,
        lr_scheduler,
    ]

    train_datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.15,
        horizontal_flip=True,
    )

    train_datagen.fit(X_train)

    batch_size = 32 #batch size of 32 performs the best.

    epochs = 100

    optims = [
      optimizers.Nadam(
          learning_rate=0.001,
          beta_1=0.9,
          beta_2=0.999,
          epsilon=1e-07,
          name='Nadam'),

      optimizers.Adam(0.001),
    ]


    #Training

    model = build_net(optims[1])

    history = model.fit(
        train_datagen.flow(X_train, y_train, batch_size=batch_size),
        validation_data=(X_valid, y_valid),
        steps_per_epoch=len(X_train) / batch_size,
        epochs=epochs,
        callbacks=callbacks,
    )



    #plot the training and validation metrics

    sns.set()
    fig = pyplot.figure(0, (12, 4))

    ax = pyplot.subplot(1, 2, 1)
    sns.lineplot(history.epoch, history.history['accuracy'], label='train')
    sns.lineplot(history.epoch, history.history['val_accuracy'], label='valid')
    pyplot.title('Accuracy')
    pyplot.tight_layout()

    ax = pyplot.subplot(1, 2, 2)
    sns.lineplot(history.epoch, history.history['loss'], label='train')
    sns.lineplot(history.epoch, history.history['val_loss'], label='valid')
    pyplot.title('Loss')
    pyplot.tight_layout()

    pyplot.savefig('epoch_history_dcnn.png')
    pyplot.show()


    #plot the distribution of training and validation metrics

    df_accu = pd.DataFrame({'train': history.history['accuracy'], 'valid': history.history['val_accuracy']})
    df_loss = pd.DataFrame({'train': history.history['loss'], 'valid': history.history['val_loss']})

    fig = pyplot.figure(0, (14, 4))
    ax = pyplot.subplot(1, 2, 1)
    sns.violinplot(x="variable", y="value", data=pd.melt(df_accu), showfliers=False)
    pyplot.title('Accuracy')
    pyplot.tight_layout()

    ax = pyplot.subplot(1, 2, 2)
    sns.violinplot(x="variable", y="value", data=pd.melt(df_loss), showfliers=False)
    pyplot.title('Loss')
    pyplot.tight_layout()

    pyplot.savefig('performance_dist.png')
    pyplot.show()



    #visualize a confusion-matrix

    yhat_valid_probs = model.predict(X_valid)
    yhat_valid = np.argmax(yhat_valid_probs, axis=1)

    scikitplot.metrics.plot_confusion_matrix(np.argmax(y_valid, axis=1), yhat_valid, figsize=(7, 7))
    pyplot.savefig("confusion_matrix_dcnn.png")

    print(f'total wrong validation predictions: {np.sum(np.argmax(y_valid, axis=1) != yhat_valid)}\n\n')
    print(classification_report(np.argmax(y_valid, axis=1), yhat_valid))

    # In[ ]:


    model.save("fer_model_extended.h5")


if __name__ == "__main__":
    main()
