# Methodologies of eye tracking
## Table of contents
- [Methodologies of eye tracking](#methodologies-of-eye-tracking)
  - [Table of contents](#table-of-contents)
  - [Sensor based eye tracking](#sensor-based-eye-tracking)
  - [Eye tracking using webcam](#eye-tracking-using-webcam)
  - [Average accuracy of eye trackers](#average-accuracy-of-eye-trackers)
    - [How to measure the accuracy](#how-to-measure-the-accuracy)
    - [Solutions (webcam eye trackers)](#solutions-(webcam-eye-trackers))
    - [Other tests](#other-tests)
  - [Summary](#summary)

## Sensor based eye tracking
Some eye tracking systems detect and analyze eye movements based on electric potentials measured with electrodes placed in the region around the eyes. This electric signal detected using two pairs of electrodes placed around one eye is known as electrooculogram (EOG). When the eyes are in their origin state, the electrodes measure a steady electric potential field. If the eyes move towards the periphery, the retina approaches one electrode and the cornea approaches the other. This changes the orientation of the dipole and results in a change in the measured EOG signal. Eye movement can be tracked by analyzing the changes in the EOG signal

## Eye tracking using webcam
Webcam eye tracking works by using a computer's built-in webcam or external one to capture images or video of a person's face and eyes, and then processing the data to track the position and movements of the eyes. An algorhitm is then used to calculate a gaze as a user is looking at different areas of the screen.
The eye tracking process using a webcam in a nutshell goes as follows:
1. Detecting location of face
2. Detecting location of eyes
3. Extracting eyes features
4. Calibration
5. Calculating positions on screen based on the movement of the eyes

## Average accuracy of eye trackers
### How to measure the accuracy
The eye tracker accuracy can be measured in degrees of visual angle (dva). Degrees of visual angle in eye tracking are a way to measure the size and location of objects in a person's visual field. It's a unit of measurement based on the angle that an object makes with the observer's eye.
On average, humans see 200° horizontally and 130° vertically. Raising your thumb while fully extending your arm will make its widest point appear to be approximately 2 visual degrees wide.
### Solutions (webcam eye trackers)
- **iMotions** - series of tests conducted on 1080p 30Hz webcam in different environments:
-- Ideal conditions: 4.3dva
-- Head and body movement: 7.1dva
-- Strong sidelight: 5.6dva
-- Low resolution (640x480p): 5.0dva
-- Glasses: 7.5dva
- **GazeRecorder**: 1.05dva
- **Webgazer:** 4.17dva
- **PACE:** 2.56dva

### Other tests
iMotions simultaneously did a series of tests on a screen-based eye tracker in the same environment. It has reached 0.9dva with glasses, 0.7dva with movement and 0.6dva with the rest.

We also have tested GazeRecorder online using fullhd 30Hz webcam in typical user conditions and we have achieved much lower real accuracy (it varied from about 2dva to sometimes more than 7).

## Summary
It is possible to achieve a reasonable accuracy with eye tracking using a webcam, hovewer it comes with many downsides. A standard consumer-grade webcam might not provide us with data of quality good enough to achieve proper eye tracking. A video resolution being too low might result in high inaccuracies when detecting the gaze point on the screen and too low framerate could result in too slow detection of eye movement. The room lighting and face illumination have to be specific and user's head movement should be little to none in order for this approach to be effective. Judging by these factors it might be better to use a different approach as users might not have conditions and hardware sufficient enough for it to work properly.
Also, the recommended method is to use an external sensor - it is very difficult to create an eye-tracker with good accuracy using the user's camera. If we were thinking of releasing this product, we would need to equip users with a sesnor to start with, or dispense with this feature to minimise costs.

