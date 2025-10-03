import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7,
    max_num_hands=1  # Only track one hand for better performance
)
mp_draw = mp.solutions.drawing_utils

# Load your custom images
img_finger_mouth = cv2.imread('image_finger_mouth.jpg')
img_pointing = cv2.imread('image_pointing.jpg')

# Window dimensions (larger for better visibility)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Resize images to match webcam feed
if img_finger_mouth is not None:
    img_finger_mouth = cv2.resize(img_finger_mouth, (WINDOW_WIDTH, WINDOW_HEIGHT))
if img_pointing is not None:
    img_pointing = cv2.resize(img_pointing, (WINDOW_WIDTH, WINDOW_HEIGHT))

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

# Gesture smoothing
gesture_history = []
HISTORY_SIZE = 8
last_stable_gesture = None
gesture_hold_frames = 0
MIN_HOLD_FRAMES = 10

# Function to check if finger is 'in mouth' (very basic approximation)
def is_finger_in_mouth(hand_landmarks):
    # Get index fingertip (landmark 8)
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    
    # More generous 'mouth area' detection zone (center-left area where face/mouth would be)
    # Expanded area to make it easier to trigger
    if 0.35 < index_finger_tip.x < 0.65 and 0.15 < index_finger_tip.y < 0.5:
        return True
    return False

def draw_detection_zone(frame):
    """Draw the finger-in-mouth detection zone on the frame"""
    height, width = frame.shape[:2]
    
    # Convert normalized coordinates to pixel coordinates
    x1 = int(0.35 * width)
    y1 = int(0.15 * height)
    x2 = int(0.65 * width)
    y2 = int(0.5 * height)
    
    # Draw semi-transparent rectangle
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), (255, 200, 0), -1)
    cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
    
    # Draw border (thicker for larger window)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 200, 0), 4)
    cv2.putText(frame, "Finger-in-mouth zone", (x1, y1 - 15),
               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 200, 0), 3)

# Function to check for a pointing gesture
def is_pointing_gesture(hand_landmarks):
    # Get landmarks for index finger and other fingers
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    
    # A simple pointing gesture: index finger is extended, others are bent.
    # Check if index finger is relatively straight (tip y < pip y in screen coords)
    # And if other finger tips are below their PIP joints (bent)
    
    index_extended = index_tip.y < index_pip.y # Tip is "above" PIP in y-coordinate (screen Y-axis is inverted)
    
    # Check if other fingers are curled (tip is "below" or close to their PIP joint)
    middle_curled = middle_tip.y > middle_pip.y - 0.05
    ring_curled = ring_tip.y > ring_pip.y - 0.05
    pinky_curled = pinky_tip.y > pinky_pip.y - 0.05
    
    # Check thumb position (often tucked or out of the way for pointing)
    # This is more complex, might compare thumb_tip.x to thumb_cmc.x or others.
    
    if index_extended and middle_curled and ring_curled and pinky_curled:
        return True
    
    return False

def smooth_gesture(gesture):
    """Smooth gesture detection to avoid flickering"""
    global last_stable_gesture, gesture_hold_frames
    
    gesture_history.append(gesture)
    if len(gesture_history) > HISTORY_SIZE:
        gesture_history.pop(0)
    
    # Count occurrences in recent history
    gesture_count = gesture_history.count(gesture)
    threshold = HISTORY_SIZE * 0.6
    
    # Check if gesture is stable
    if gesture is not None and gesture_count > threshold:
        gesture_hold_frames += 1
        if gesture_hold_frames >= MIN_HOLD_FRAMES:
            last_stable_gesture = gesture
    else:
        gesture_hold_frames = max(0, gesture_hold_frames - 1)
        if gesture is None and gesture_hold_frames == 0:
            none_count = gesture_history.count(None)
            if none_count > HISTORY_SIZE * 0.7:
                last_stable_gesture = None
    
    return last_stable_gesture

print("=" * 60)
print("MediaPipe Gesture Recognition - Dual Display")
print("=" * 60)
print("\nInstructions:")
print("- Position your hand in front of the camera")
print("- Try moving your hand to center-top for 'finger in mouth'")
print("- Try pointing gesture (index finger extended)")
print("- Press 'q' to quit")
print("\nWindows:")
print("- 'Camera Feed' - Always shows your webcam")
print("- 'Detected Gesture' - Shows images when gestures detected")
print("=" * 60)

# Create initial gesture display
gesture_display = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
cv2.putText(gesture_display, 'No gesture detected', (350, 340),
           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
cv2.putText(gesture_display, 'Waiting for gesture...', (380, 400),
           cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 180, 180), 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process frame with MediaPipe Hands
    results = hands.process(rgb_frame)
    
    # Start with camera feed
    camera_display = frame.copy()
    detected_gesture = None
    
    # Draw the detection zone for finger-in-mouth gesture
    draw_detection_zone(camera_display)
    
    # Analyze hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on camera feed
            mp_draw.draw_landmarks(
                camera_display, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_draw.DrawingSpec(color=(0, 255, 255), thickness=2)
            )
            
            # Draw index finger tip position for debugging (scaled for larger window)
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            height, width = camera_display.shape[:2]
            tip_x = int(index_tip.x * width)
            tip_y = int(index_tip.y * height)
            cv2.circle(camera_display, (tip_x, tip_y), 15, (0, 255, 255), -1)
            
            # Detect gestures
            if is_finger_in_mouth(hand_landmarks):
                detected_gesture = "finger_in_mouth"
                # Visual feedback when in zone (larger circle for visibility)
                cv2.circle(camera_display, (tip_x, tip_y), 25, (0, 255, 0), 5)
            elif is_pointing_gesture(hand_landmarks):
                detected_gesture = "pointing"
    
    # Smooth gesture detection
    smooth_detected = smooth_gesture(detected_gesture)
    
    # Update gesture display window
    if smooth_detected == "finger_in_mouth" and img_finger_mouth is not None:
        gesture_display = img_finger_mouth.copy()
    elif smooth_detected == "pointing" and img_pointing is not None:
        gesture_display = img_pointing.copy()
    elif detected_gesture is None:
        # Show "waiting for gesture" message
        gesture_display = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)
        cv2.putText(gesture_display, 'No gesture detected', (350, 340),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        cv2.putText(gesture_display, 'Waiting for gesture...', (380, 400),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (180, 180, 180), 2)
    
    # Add status text to camera feed (scaled for larger window)
    status_text = "No gesture" if detected_gesture is None else f"Detected: {detected_gesture}"
    cv2.putText(camera_display, status_text, (20, 50),
               cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
    
    # Show stability progress bar (scaled for larger window)
    if detected_gesture is not None:
        progress = min(gesture_hold_frames / MIN_HOLD_FRAMES, 1.0)
        bar_width = int(400 * progress)
        cv2.rectangle(camera_display, (20, 80), (420, 115), (100, 100, 100), 3)
        if bar_width > 0:
            color = (0, 255, 0) if progress >= 1.0 else (0, 165, 255)
            cv2.rectangle(camera_display, (20, 80), (20 + bar_width, 115), color, -1)
        cv2.putText(camera_display, "Stability", (440, 105),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    cv2.putText(camera_display, "Press 'q' to quit", (20, WINDOW_HEIGHT - 20),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Display both windows
    cv2.imshow('Camera Feed', camera_display)
    cv2.imshow('Detected Gesture', gesture_display)
    
    # Handle key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("\nGesture recognition stopped. Goodbye!")

