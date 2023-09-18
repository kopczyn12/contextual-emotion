# RESEARCH ON DATASET STORAGE

The purpose of this research is to find the best way to store a dataset for our web application. Our dataset consists of 40 high-quality images. For this reason, we need to choose  the most optimal and secure solution that will allow our images to load quickly.

## Overview of data storage options

1. Cloud storage is one of the most popular options. Various services such as Google Drive, Dropbox, MegaFile, and OneDrive are available. Cloud storage allows for easy data sharing and exchange. However, storing data in the cloud does not guarantee full privacy and data security, and not always is free.

2. Local storage, on the computer or server hard drive, is an option that allows for full control over the data. However, local storage can be more complicated to manage and may require a large amount of disk space.

3. Storing data in a database allows for easy data management and searching. However, storing large files in a database can lead to slow web application performance.

## Summary

Due to the small number of images, the best solution for storing the dataset is to store it in a database, in our case MongoDB. This allows for easy management and will not slow down the application due to the single display of images during operation.
