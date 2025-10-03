"""
This script creates placeholder images for testing the gesture recognition system.
Run this if you don't have your own images yet.
"""

import cv2
import numpy as np

# Create placeholder image for "finger in mouth" gesture
img1 = np.zeros((480, 640, 3), dtype=np.uint8)
img1[:] = (100, 50, 150)  # Purple background
cv2.putText(img1, 'FINGER IN MOUTH', (80, 200), 
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
cv2.putText(img1, 'GESTURE DETECTED!', (100, 280), 
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
cv2.imwrite('image_finger_mouth.jpg', img1)
print("✓ Created 'image_finger_mouth.jpg'")

# Create placeholder image for "pointing" gesture
img2 = np.zeros((480, 640, 3), dtype=np.uint8)
img2[:] = (50, 150, 100)  # Teal background
cv2.putText(img2, 'POINTING GESTURE', (80, 200), 
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
cv2.putText(img2, 'DETECTED!', (180, 280), 
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
cv2.imwrite('image_pointing.jpg', img2)
print("✓ Created 'image_pointing.jpg'")

print("\nPlaceholder images created successfully!")
print("You can now run gesture_recognition.py")
print("Replace these images with your own custom images later.")

