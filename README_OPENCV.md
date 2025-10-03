# Gesture Recognition with OpenCV (Python 3.13 Compatible!)

A real-time hand gesture recognition system using **pure OpenCV** - no MediaPipe required! This version works with **Python 3.13**.

## Features

- **Skin color detection** using HSV color space
- **Contour analysis** for hand tracking
- **Gesture detection**:
  - Finger in mouth gesture (hand near center-top area)
  - Pointing finger gesture (elongated hand shape)
- **Smart gesture smoothing** to avoid flickering
- **Visual feedback** with contour overlay and skin mask
- **Works with Python 3.13!**

## Prerequisites

- **Python 3.7+** (including Python 3.13!)
- Webcam connected to your computer
- Good lighting conditions (helps with skin detection)

## Installation

1. **Install dependencies**:
   ```bash
   pip install opencv-python numpy
   ```
   
   Or use the requirements file:
   ```bash
   pip install -r requirements_opencv_only.txt
   ```

2. **Prepare your images**:
   - Save your "finger in mouth" image as `image_finger_mouth.jpg`
   - Save your "pointing finger" image as `image_pointing.jpg`
   - Place both images in the same directory as the script

## Usage

Run the OpenCV-only gesture recognition script:

```bash
python gesture_recognition_opencv.py
```

### Controls

- **Press 'q'** to quit the application
- **Press 'r'** to reset and return to camera view

### How it Works

1. **Skin Detection**: Uses HSV color space to detect skin tones
2. **Contour Finding**: Finds hand contours in the skin mask
3. **Gesture Analysis**: 
   - Calculates contour properties (area, centroid, aspect ratio)
   - Detects convexity defects to count fingers
   - Identifies gestures based on hand position and shape
4. **Smoothing**: Uses gesture history to avoid false detections
5. **Display**: Shows corresponding images when gestures are detected

## Gesture Detection Details

### Finger in Mouth
- **Trigger**: Hand positioned in center-top area of frame (x: 0.3-0.7, y: 0.1-0.4)
- **Shape**: Closed hand or few fingers extended
- **Tips**: Move your hand toward the upper-center area of the camera

### Pointing Gesture
- **Trigger**: Elongated hand shape with few fingers extended
- **Shape**: High or low aspect ratio, indicating extended finger
- **Tips**: Point with your index finger while keeping other fingers curled

## Customization

### Adjusting Skin Detection

Modify the HSV color range in the `detect_skin()` function:

```python
lower_skin = np.array([0, 20, 70], dtype=np.uint8)
upper_skin = np.array([20, 255, 255], dtype=np.uint8)
```

- Increase lower values if detecting too much background
- Decrease upper values if not detecting your skin tone
- Different lighting conditions may require different values

### Tuning Gesture Detection

In `analyze_gesture()` function:

```python
# Area thresholds
if area > 5000:  # Minimum hand size

# Position for "finger in mouth"
if 0.3 < norm_x < 0.7 and 0.1 < norm_y < 0.4:

# Finger counting threshold
if angle <= np.pi / 2 and d > 10000:
```

### Adjusting Smoothing

Change `HISTORY_SIZE` to make detection more/less responsive:

```python
HISTORY_SIZE = 10  # Increase for more stability, decrease for faster response
```

## Troubleshooting

### Poor skin detection
- **Solution**: Improve lighting conditions
- Adjust HSV color ranges for your skin tone
- Avoid backgrounds with similar colors to skin
- Wear long sleeves to isolate hand from arm

### False gesture detections
- **Solution**: Increase `HISTORY_SIZE` for more smoothing
- Adjust area thresholds to filter out noise
- Fine-tune gesture detection coordinates

### Gestures not detected
- **Solution**: Decrease area thresholds
- Relax gesture detection constraints
- Ensure good lighting on your hand
- Try different hand positions and distances from camera

### Images not loading
- Verify image file names: `image_finger_mouth.jpg` and `image_pointing.jpg`
- Ensure images are in the same directory as the script
- Check that the images are valid JPG files

## Comparison: OpenCV vs MediaPipe

### OpenCV (This Version)
✅ Works with Python 3.13  
✅ No external dependencies beyond OpenCV  
✅ Good for learning computer vision fundamentals  
❌ Less accurate hand tracking  
❌ Sensitive to lighting conditions  
❌ Requires more manual calibration  

### MediaPipe (Original Version)
✅ Highly accurate hand landmark detection  
✅ Robust to lighting conditions  
✅ 21 precise hand landmarks  
✅ Works in various orientations  
❌ Requires Python 3.11 or 3.12  
❌ Additional dependency  

## Tips for Better Detection

1. **Lighting**: Ensure good, even lighting on your hand
2. **Background**: Use a background color different from your skin tone
3. **Distance**: Keep your hand 1-2 feet from the camera
4. **Movement**: Move slowly and deliberately for gesture recognition
5. **Calibration**: Experiment with threshold values for your setup

## Project Structure

```
learning-OpenCV/
├── gesture_recognition_opencv.py    # OpenCV-only version (Python 3.13 OK!)
├── gesture_recognition.py           # MediaPipe version (requires Python 3.11/3.12)
├── requirements_opencv_only.txt     # Dependencies for OpenCV version
├── requirements.txt                 # Dependencies for MediaPipe version
├── README_OPENCV.md                 # This file
├── README.md                        # MediaPipe version docs
├── image_finger_mouth.jpg           # Your custom image
└── image_pointing.jpg               # Your custom image
```

## Next Steps

- Fine-tune skin detection for your environment
- Experiment with different gesture patterns
- Add more gestures (peace sign, thumbs up, fist, open palm)
- Implement gesture history display
- Add confidence scoring for gestures
- Try background subtraction for better hand isolation

## Learning Resources

- [OpenCV Color Spaces](https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html)
- [Contour Features](https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html)
- [Convexity Defects](https://docs.opencv.org/4.x/d7/d1d/tutorial_hull.html)

## License

This is a learning project. Feel free to modify and experiment with the code!

---

**Happy Coding!** 🎥✨ This pure OpenCV approach gives you a great foundation in computer vision fundamentals!

