# Gesture Recognition with OpenCV and MediaPipe

A real-time hand gesture recognition system that detects specific gestures and displays corresponding images.

## Features

- **Real-time hand tracking** using MediaPipe Hands
- **Gesture detection**:
  - Finger in mouth gesture
  - Pointing finger gesture
- **Dynamic image display** based on detected gestures
- **Visual feedback** with hand landmark overlay

## Prerequisites

- **Python 3.11 or 3.12** (MediaPipe doesn't support Python 3.13 yet)
- Webcam connected to your computer

> ⚠️ **Important**: If you have Python 3.13, you'll need to install Python 3.11 or 3.12 for MediaPipe compatibility.

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare your images**:
   - Save your "finger in mouth" image as `image_finger_mouth.jpg`
   - Save your "pointing finger" image as `image_pointing.jpg`
   - Place both images in the same directory as the script
   - Images will be automatically resized to 640x480 pixels

## Usage

Run the gesture recognition script:

```bash
python gesture_recognition.py
```

### Controls

- **Press 'q'** to quit the application

### How it Works

1. The application captures video from your webcam
2. MediaPipe Hands detects hand landmarks in real-time
3. Custom gesture recognition functions analyze the hand positions:
   - **Finger in Mouth**: Detects when index finger is in the center-top region
   - **Pointing Gesture**: Detects when index finger is extended while other fingers are curled
4. When a gesture is detected, the corresponding image replaces the video feed

## Customization

### Adjusting Gesture Detection

The gesture detection logic is in two main functions:

#### `is_finger_in_mouth(hand_landmarks)`
- Modify the x and y coordinate ranges to adjust the detection area
- Current default: x (0.4-0.6), y (0.2-0.4)

#### `is_pointing_gesture(hand_landmarks)`
- Adjust threshold values (currently -0.05) to make detection more/less sensitive
- Modify the logic to detect different finger configurations

### Adding New Gestures

1. Create a new detection function similar to `is_pointing_gesture()`
2. Use `hand_landmarks.landmark[mp_hands.HandLandmark.XXX]` to access specific landmarks
3. Add your custom logic in the main loop

### MediaPipe Hand Landmarks

MediaPipe provides 21 hand landmarks:
- `WRIST` (0)
- `THUMB_CMC`, `THUMB_MCP`, `THUMB_IP`, `THUMB_TIP` (1-4)
- `INDEX_FINGER_MCP`, `INDEX_FINGER_PIP`, `INDEX_FINGER_DIP`, `INDEX_FINGER_TIP` (5-8)
- `MIDDLE_FINGER_MCP`, `MIDDLE_FINGER_PIP`, `MIDDLE_FINGER_DIP`, `MIDDLE_FINGER_TIP` (9-12)
- `RING_FINGER_MCP`, `RING_FINGER_PIP`, `RING_FINGER_DIP`, `RING_FINGER_TIP` (13-16)
- `PINKY_MCP`, `PINKY_PIP`, `PINKY_DIP`, `PINKY_TIP` (17-20)

Coordinates are normalized (0.0 to 1.0) relative to the frame size.

## Troubleshooting

### Images not loading
- Verify image file names: `image_finger_mouth.jpg` and `image_pointing.jpg`
- Ensure images are in the same directory as the script
- Check that the images are valid JPG files

### Webcam not working
- Ensure your webcam is connected and not in use by another application
- Try changing the camera index: `cv2.VideoCapture(1)` or `cv2.VideoCapture(2)`

### Gesture detection too sensitive/not sensitive enough
- Adjust the threshold values in the gesture detection functions
- Experiment with different coordinate ranges
- Add debug print statements to see landmark values in real-time

## Project Structure

```
learning-OpenCV/
├── gesture_recognition.py      # Main application script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── image_finger_mouth.jpg       # Image for finger-in-mouth gesture (you need to add this)
└── image_pointing.jpg           # Image for pointing gesture (you need to add this)
```

## Next Steps

- Experiment with different gesture detection thresholds
- Add more gestures (peace sign, thumbs up, etc.)
- Implement face detection to accurately locate the mouth for better "finger in mouth" detection
- Add gesture history/smoothing to reduce false positives
- Create a gesture training mode to calibrate for different users

## Resources

- [MediaPipe Hands Documentation](https://google.github.io/mediapipe/solutions/hands.html)
- [OpenCV Documentation](https://docs.opencv.org/)
- [MediaPipe Hand Landmarks Guide](https://google.github.io/mediapipe/solutions/hands#hand-landmark-model)

## License

This is a learning project. Feel free to modify and experiment with the code!

