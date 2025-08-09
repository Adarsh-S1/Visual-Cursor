# Visual-Cursor 👁️🖱️

This Python application allows users to control their computer's mouse cursor using head movements and eye blinks. It is designed as an assistive technology for individuals who are paralyzed from the neck down or for people without upper limbs, providing them with a hands-free way to interact with a computer.

![Placeholder for GIF](https://placehold.co/600x400/2d3748/ffffff?text=Add+a+GIF+Demonstration+Here)

---

## How It Works

The program uses your webcam to track your facial movements in real-time.

* **Facial Landmark Detection**: It leverages the `mediapipe` library to detect a detailed mesh of 478 facial landmarks.
* **Cursor Movement**: The position of the user's nose tip is used as a reference point. The script calculates the displacement of the nose from a calibrated center point and translates this into the movement of the mouse cursor on the screen.
* **Blink Detection**: The Eye Aspect Ratio (EAR) is calculated for each eye. A sudden drop in the EAR value below a certain threshold is registered as a blink.
    * A **left eye blink** triggers a **left mouse click**.
    * A **right eye blink** triggers a **right mouse click**.
    * Blinking **both eyes simultaneously** triggers a **double click**.
* **Mouse Control**: The `pyautogui` library is used to programmatically move the cursor and simulate mouse clicks.

---

## Features

* **Hands-Free Navigation**: Complete control of the mouse cursor without using hands.
* **Intuitive Controls**: Head movements for pointing and eye blinks for clicking.
* **Real-time Response**: Low-latency tracking for a smooth user experience.
* **Simple Calibration**: A quick and easy one-time calibration process at the start of the program to set the neutral head position.

---

## Setup and Installation

To run this application, you need Python 3 and a webcam.

1.  **Clone the repository or download the source code.**

2.  **Install the required libraries.** You can install them using pip:
    ```bash
    pip install opencv-python mediapipe numpy pyautogui
    ```

---

## Usage

1.  **Run the script** from your terminal:
    ```bash
    python eye.py
    ```
2.  **Calibrate**: When the script starts, you will be prompted to calibrate. Look at the center of your screen and press `Enter` in the terminal. The program will detect your face and set your current nose position as the neutral center.
3.  **Control the Mouse**:
    * Move your head to move the cursor.
    * Wink your left eye for a left click.
    * Wink your right eye for a right click.
    * Blink both eyes for a double click.
4.  **Quit**: To stop the program, make sure the video feed window is active and press the `q` key.

---

## Dependencies

* [OpenCV](https://pypi.org/project/opencv-python/)
* [MediaPipe](https://pypi.org/project/mediapipe/)
* [NumPy](https://pypi.org/project/numpy/)
* [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
