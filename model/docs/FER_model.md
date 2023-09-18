## First attempt at Facial Emotion Recognition
For our first model, our baseline was a popular, well-acclaimed structure of a Deep Convolutional Neural Network, meaning 2D convolutions layers, followed by batch normalizations, dropouts and maxpooling layers. We trained the model on the  subset of Fer Dataset. 

Emotions taken into consideration in the trainign phase were:
 - Angry
 - Disgust
 - Happy
 - Sad
 - Surprise

Below are the values of Accuracy and Loss, on the training and validation datasets respectively:
 ![Losses](./images/initial_acc_loss_epochs.png)


Distributions of Accuracy and Loss values, again on the training and validation datasets:
 ![Distribution](./images/initial_acc_loss.png)

The confusion matrix of predictions produced by our model:
 ![Confusion Matrix](./images/initial_confusion_matrix.png)

The accuracy table of predicted emotions:

 ![Emotion table](./images/fer_accuracy.png)


 Where:
   - 0  -> Anger
   - 1  -> Disgust
   - 2  -> Happy
   - 3  -> Sad
   - 4  -> Surprised

Here are some examples of how our model works with webcam:

 ![Anger](./images/angry.png)
 ![Disgust](./images/disgust.png)
 ![Happy](./images/happy.png)
 ![Sad](./images/sad.png)
 ![Surprised](./images/surprise.png)

   Given the relative small complexity of the model, and only 5 emotions taken into consideration, these results were satisfactory.

   Next on the agenda is an EfficientNet-like neural net, and a bigger dataset to train it with.

## Evaluation


Metrics for f1 score, recall and precision:


![Metrics1](./images/metrics1.png)

![Table1](./images/table1.png)



Metrics for True Positive, False Positive and False Positive:


![Metrics2](./images/metrics2.png)

![Table2](./images/table2.png)



Metrics for Macro avarage and Weighted avarage:


![Metrics3](./images/metrics3.png)

![Table3](./images/table3.png)



- Micro True Positive: 2053
- Micro False Positive: 404
- Micro False Negative: 404
- Micro precision: 0.8355718355718356
- Micro recall: 0.8355718355718356
- Micro f1 score: 0.8355718355718356
- Micro avarage: [0.83557184 0.83557184 0.83557184]
- Accuracy: 0.8355718355718356