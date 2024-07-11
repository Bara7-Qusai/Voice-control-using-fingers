# Gesture-Based Volume Control

This project uses computer vision and hand-tracking technology to control the volume of your computer using simple hand gestures. By using a webcam, it detects the position of your thumb and index finger to adjust the volume level.

## Features

- **Hand Tracking**: Utilizes the Mediapipe library to detect and track the hand landmarks.
- **Volume Control**: Uses the Pycaw library to control the system's volume based on the distance between thumb and index finger.
- **Visual Feedback**: Provides a visual representation of the current volume level on the screen.


## Usage

1. **Run the script:**

    ```bash
    python Voice_control_using_fingers.py
    ```

2. **Control the volume:**
   - Use your thumb and index finger to control the volume.
   - Bring them closer to reduce the volume.
   - Separate them to increase the volume.
   - Press 'q' to exit the application.

## Files

- `Voice_control_using_fingers.py`: Main script to run the gesture-based volume control.
- `README.md`: Project description and instructions.

## How It Works

1. **Hand Detection and Tracking:**
   - The script uses Mediapipe to detect hand landmarks.
   - It identifies the thumb tip and index finger tip positions.

2. **Volume Adjustment:**
   - Calculates the distance between the thumb and index finger.
   - Maps this distance to the system's volume range using Pycaw.
   - Updates the system's volume accordingly.

3. **Visual Feedback:**
   - Draws the hand landmarks and connections on the video feed.
   - Displays a volume bar to show the current volume level.
   - Provides instructions on the screen.

## Dependencies

- **OpenCV**: For video capture and image processing.
- **Mediapipe**: For hand landmark detection and tracking.
- **Numpy**: For numerical operations.
- **Pycaw**: For controlling the system volume.
- **Comtypes**: For COM interface handling.

