# Talon description
 
## Table of contents

 - [About](#about)
 - [Prerequisites](#prerequisites) 
 - [Usage](#usage)

## About
Talon is a library that allows us to use Tobii's eye-tracker. 
The main use of this library is to allow the user to remotely control the screen using eye gestures.
Using the available code and structure, we have modified it to track the movement of the eyeballs on the screen.

## Prerequisites
You need to have installed python version 3.10

## Usage
To start using the tracker, connect the tobii device and run the run.sh script found in the talon folder of our repo.
The logs from this tracker can be found in the logs folder, in log.txt
The path to save the logs can be changed freely in the program code.

Also, When you are in repo, set the PYTHONPATH.
export PYTHONPATH=$PWD
Logs should be stored in mentioned folder then.
