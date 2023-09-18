# Table of Contents
- [Introduction to image segmentation](#introduction-to-image-segmentation)
- [Emotion evoking in photos](#emotion-evoking-in-photos)
- [Methods of image segmentation](#methods-of-image-segmentation)
    - [Edge-based segmentation](#edge-based-segmentation)
    - [Region-based segmentation](#region-based-segmentation)
    - [Contour-based segmentation](#contour-based-segmentation)
    - [Threshold segmentation](#threshhold-segmentation)
    - [Deep learning-based segmentation](#Deep-learning-segmentation)
- [Dataset](#dataset)
- [Deeplabv3Plus](#deeplabv3plus)
    - [Introduction](#introduction)
    - [Dataset](#dataset-training)
    - [Results](#results)
- [Final segmentation](#final-segmentation)
- [Stable diffision](#stable-diffiusion)
    - [Introduction](#introduction-to-stable-diffiusion)
    - [Training Dataset](#training-dataset)
    - [Training and results](#training-and-results)
#
## Introduction to image segmentation
In computer vision tasks, image segmentation is the proccess of partitioning an image into multiple image segments,which in handsight is a proccess of assigning a label to every pixel in an image. Main goal of image segmentation is simplification of the image to interesting parts, thus making it easier to analyse. 

#

## Emotion evoking in photos
Evoking emotions through images depends on individual personality, circumstances, and cultural background, yet certain key elements can influence emotional responses. The color scheme is critical, with bright, warm colors typically inciting happiness and excitement, while cooler, darker hues often imply sadness or melancholy. Lighting also plays a significant role; high-key lighting with bright tones evokes comfort and happiness, whereas low-key lighting with darker tones and shadows can suggest mystery or fear.

The weather in an image can significantly impact emotional responses. Bright, sunny days generally evoke happiness, while darker, rainy days can induce melancholy. Context is vital too, with understanding of historical events or situational circumstances adding layers of meaning to an image.

Facial expressions provide a straightforward way to elicit emotions as we are instinctively adept at interpreting feelings such as happiness, anger, or sadness from them. Lastly, personal experiences can shape individual emotional responses. A childhood toy might evoke nostalgia in one person but not in another, while a stunning sunset might universally evoke warmth and peace. In summary, carefully considering these elements can assist in selecting images that provoke specific emotional responses.

#

## Dataset
A variable aspect of our project was finding/creating sufficient dataset of images with objects that could evoke 5 primary emotions. After hours of researching we decided to create our own dataset, which was done mainly in Adobe Photoshop. This allowed us to incorporate diffrent objects in diffrent sceneries, by pasting in objects and heavly modifing it's freatures (saturation,tonality,hue,levels,perspective,clarity). 

#
## Methods of image segmentation
Image segmentation is a wide-ranging topic, and as a result, many techniques and methods have been developed to perform this type of operation. 

### In our project we tried/used these segmentation methods:


#### Edge-based segmentation
Edge segmentation method is a widely used approach for segmenting objects in images, especially when the object of interest has well-defined edges or boundaries. 
#### Region-based segmentation
Region based segmentation method is an effective approach when the object of interest is composed of regions with similar properties such as color, texture, or intensity. 
#### Contour-based segmentation
Contour based segmentation method can be a good alternative when the object of interest has well-defined edges or boundaries. 
#### Threshold segmentation
Treshold based segmentation method can be a good option when the image has a clear contrast between the object of interest and the background. 
#### Deep learning-based segmentation
Deep learning-based segmentation techniques involve training a neural network to segment an image. In our work we mainly focused on this method of image segmenation. After series of tests on most common semantic segmentation models (such as U-net, Mask-RCNN, Seg-net) we decided to choose Deeplabv3Plus model. 
#
## Deeplabv3Plus

### Introduction

DeepLabV3+ is a state-of-the-art semantic segmentation model designed for high-quality image segmentation tasks. It extends the DeepLabV3 model, building on its strengths and adding a decoder module for refinement of object boundaries, which makes it more capable of dealing with small objects and sharp edges in images.

 The encoder is responsible for extracting features from the input image, and it applies atrous (dilated) convolution to enlarge the field of view without increasing the number of parameters or the amount of computation. The atrous spatial pyramid pooling (ASPP) module, incorporated into the encoder, applies atrous convolution at multiple scales to capture multi-scale information.

 The decoder module upsamples the low-resolution open-source image segmentation models encoder output to produce a dense pixel-level prediction, which helps improve segmentation accuracy, particularly at object edges. To achieve this, the decoder uses a combination of bilinear upsampling and a simple yet effective depthwise separable convolution.

 ### Dataset
 In order to train Deeplabv3+ we created a subset of 21 classess in images with a total of 190 photos. Photos used for training were carefully picked to match objects with our target segmentation objects. Annotation were made in VGG image annotator and exported in JSON format.

 ### Results 
 Deeplabv3+ was trained onResNet-50 backbone with weights from imagenet dataset. Validation accuracy got to around 64% which leaves a lot to be desired. 
#
## Final segmentation
With Deeplabv3+ only yielding 65% accuracy we decided to use our manually annotated images as a starting point. Photos manually annotated allow us for more precise evaluation of tests that we try to run. 

#
## Stable diffiusion

### Introduction to Stable Diffiusion
Stable Diffusion is a deep learning, text-to-image model released in 2022. It is primarily used to generate detailed images conditioned on text descriptions, though it can also be applied to other tasks such as inpainting, outpainting, and generating image-to-image translations guided by a text prompt.

### Training dataset
In order to generate thematically simmillar photos, we reused the photos done for Deeplabv3+ training. 

### Training and results

As an extra part of our project we decided to train Stable Diffiusion 1.4 on our custom dataset, and add a functionality to generate a photo based on prompts given by user.

