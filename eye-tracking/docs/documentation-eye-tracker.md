# Table of Contents
- [Table of Contents](#table-of-contents)
  - [INTRODUCTION TO EYE-TRACKING](#introduction-to-eye-tracking)
  - [HOW TO MEASURE THE ACCURACY OF EYE-TRACKERS](#how-to-measure-the-accuracy-of-eye-trackers)
  - [OUR SOLUTION - TOBII EYE TRACKER 5](#our-solution---tobii-eye-tracker-5)
  - [SPECIFICATION FOR EYE TRACKER 5](#specification-for-eye-tracker-5)
  - [TALON DESCRIPTION](#talon-description)
  - [WORK WITH BACKEND](#work-with-backend)
  - [SUMMARY](#summary)

## INTRODUCTION TO EYE-TRACKING
Eye-tracking is a technology that analyzes where a person is looking at a given moment, essentially "tracking" their gaze. The insights derived from this analysis can be invaluable in a variety of fields, including market research, psychology, user interface design, and more.

There are several techniques employed for eye-tracking:
- **Sensor-based eye tracking:** Some eye-tracking systems detect and analyze eye movements based on the electric potentials measured with electrodes placed around the eyes. The electric signal detected using two pairs of electrodes placed around one eye is known as the Electrooculogram (EOG). When the eyes are in their neutral state, the electrodes measure a steady electric potential field. If the eyes move towards the periphery, the retina approaches one electrode, while the cornea approaches another, thus changing the orientation of the dipole, resulting in a change in the measured EOG signal. Eye movements can be tracked by analyzing these changes in the EOG signal.
- **Eye tracking using webcam:** Webcam eye tracking works by utilizing a computer's inbuilt webcam or an external one to capture images or video of a person's face and eyes. These data are then processed to track the position and movements of the eyes. Algorithms are then used to calculate the gaze point as the user looks at different areas of the screen.
- **Infrared Oculography (IROG):** In this method, near-infrared light (NIR) is used to record eye movements. High-energy IR diodes emit light, which is reflected off the eye's surface and is subsequently recorded by a camera. Eye movements can be calculated based on the changes in the position of the reflections on the cornea and iris.
- **Eye Tracking using Artificial Intelligence:** More recently, artificial intelligence has been utilized for eye tracking. Using machine learning, computers are trained to recognize eye movement patterns and predict where a person will look next.


The choice of technique can depend on several factors, including the required precision, costs, the intended application, and more. Each method has its advantages and disadvantages, making it essential to choose the most suitable one based on the specific requirements and constraints of a given application.

## HOW TO MEASURE THE ACCURACY OF EYE-TRACKERS
The eye tracker accuracy can be measured in degrees of visual angle (dva). It's a unit based on the angle that an object makes with the observer's eye. Degrees of visual angle in eye tracking are a way to measure the size and location of objects in a person's visual field. 

Raising your thumb while fully extending your arm will make its widest point appear to be approximately 2 visual degrees wide. On average, humans see 200° horizontally and 130° vertically.


## OUR SOLUTION - TOBII EYE TRACKER 5
Tobii is a leading brand in the eye-tracking industry, recognized for its advanced technology and precise gaze-tracking abilities. We selected the Tobii Eye Tracker 5 for our project due to its various appealing features and capabilities.

The Tobii 5 employs Near Infrared (NIR) technology to track eye movements. This technology allows for tracking in a wide range of lighting conditions, which made it an ideal choice for our project, given the variability of environments in which our solution might be used. The device uses corneal reflection tracking, where IR illuminators create reflection patterns on the cornea and pupil. The integrated camera then captures these patterns, and Talon's algorithms process the images to determine the direction of the user's gaze.

A few important factors influenced our decision to use Tobii:
- **Accuracy:** Tobii Eye Tracker 5 offers high precision, typically accurate to about 1dva (around 30 pixels on regular computer screen)
- **Ease of Use:** Tobii devices are generally user-friendly and do not require users to wear additional gear like helmets or glasses. They can be attached to a computer monitor or used with a stand-alone device.
- **Software Support:** Tobii provides robust software support, including SDKs that allow developers to integrate eye-tracking functionality into their applications.
- **Hardware Compatibility:** Tobii devices are compatible with a wide range of hardware configurations, increasing the versatility of potential use-cases.

## SPECIFICATION FOR EYE TRACKER 5
| Specification                          | Details                                    |
| -------------------------------------- | ------------------------------------------ |
| Sensor                                 | IS5 with custom Tobii NIR sensor (850nm)   |
| Field of view                          | 40 x 40 degrees                            |
| Supported screen size area             | 15" to 27" [16:9] or 30" [21:9]            |
| Head tracking                          | CPU + Neural Network (CNN) combined / 6DoF |
| Image sampling rate and gaze frequency | 133Hz, non-interlaced gaze at 33Hz         |
| Illuminator                            | 33Hz                                       |
| Gaze recovery                          | Continuous recovery                        |
| Biometric security                     | Windows Hello 4.x using NIR + RGB          |
| Software                               | Talon                                      |



## TALON DESCRIPTION
Talon aims to bring programming, realtime video gaming, command line, and full desktop computer proficiency to people who have limited or no use of their hands, and vastly improve productivity and wow-factor of anyone who can use a computer.
Talon software has many features, but we are interested in the built-in eye-tracking algorithms. Using the off-the-shelf version of the program, we added our own script to visualize the Tobii sensor, mainly based on the PyQt (for Linux), PyGame (for Windows) libraries. Talon is scriptable with Python 3 (via embedded CPython, no need to install or configure Python on your host system). Therefore, the software runs with a single run.sh script. Talon allows you to calibrate the Tobii sensor, and use the eye-tracking option, storing the collected screen coordinates in a text file, from where they are visualized in real time.

## WORK WITH BACKEND
Talon software is run using a shell script, run.sh, which is responsible for putting up all the functionality of the application. The Tobii sensor works independently of the page, in an asynchronous manner, and the logs are stored locally. The logs from each run contain the exact timestamp, which allows the run to be identified and the coordinates to be mapped to emotions and objects.

## SUMMARY
Our approach to eye-tracking, utilizing the Tobii Eye Tracker 5, was effective in providing accurate and reliable results. Tobii's high accuracy, alongside its high clock speed, combined with the well-optimized Talon software, allowed us to attain a high degree of precision in gaze-tracking. This not only demonstrated the high-performance capabilities of the device but also underscored the dependability of our solution.

The successful integration with the Talon software facilitated the efficient processing and visualization of the eye-tracking data. Thanks to the capabilities of the PyQt framework, we were able to merge the Tobii software with the Linux window environment, enabling us to separate the visualization from the rest of the graphical environment. This helped enhance the usability and effectiveness of our solution.

In conclusion, our approach has proven to be highly effective in implementing and managing eye-tracking technology, yielding an accurate, reliable, and user-friendly solution. We are confident that our work addresses the current needs while laying a solid foundation for future advancements in this domain.

