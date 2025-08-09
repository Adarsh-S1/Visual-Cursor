import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# --- Initialization ---
pyautogui.FAILSAFE = False
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

# MediaPipe Face Mesh Initialization
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# --- Landmark Indices ---
# These are the specific landmark indices for eyes and nose in MediaPipe's 478-landmark model
LEFT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
NOSE_TIP_INDEX = 4

# --- Helper Functions ---
def get_landmarks(image, face_landmarks):
    """Extracts and scales landmark coordinates."""
    h, w, _ = image.shape
    return np.array([(lm.x * w, lm.y * h) for lm in face_landmarks.landmark])

def eye_aspect_ratio(eye_landmarks):
    """Calculates the Eye Aspect Ratio (EAR) for a single eye."""
    # Vertical distances
    vertical1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[15])
    vertical2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[14])
    vertical3 = np.linalg.norm(eye_landmarks[3] - eye_landmarks[13])
    vertical4 = np.linalg.norm(eye_landmarks[4] - eye_landmarks[12])
    vertical5 = np.linalg.norm(eye_landmarks[5] - eye_landmarks[11])
    vertical6 = np.linalg.norm(eye_landmarks[6] - eye_landmarks[10])

    # Horizontal distance
    horizontal = np.linalg.norm(eye_landmarks[0] - eye_landmarks[8])

    return (vertical1 + vertical2 + vertical3 + vertical4 + vertical5 + vertical6) / (6.0 * horizontal)

# --- Calibration ---
def calibrate():
    """Calibrates the user's neutral nose position."""
    input("Look at the center of the screen and press Enter to calibrate...")
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            all_landmarks = get_landmarks(frame, results.multi_face_landmarks[0])
            nose_position = all_landmarks[NOSE_TIP_INDEX]
            print(f"✅ Calibration successful! Nose position: {nose_position}")
            return tuple(nose_position)
        else:
            print("❌ Face not detected. Please try calibration again.")
            time.sleep(1) # Brief pause before retry

# --- Main Program ---
calibration_data = calibrate()

if calibration_data:
    # --- Constants and Variables ---
    BLINK_THRESHOLD = 0.45
    BLINK_COOLDOWN = 1.0

    last_left_click_time = 0
    last_right_click_time = 0
    last_double_click_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                all_landmarks = get_landmarks(frame, results.multi_face_landmarks[0])

                # Cursor Movement
                nose_position = all_landmarks[NOSE_TIP_INDEX]
                diff_x = (nose_position[0] - calibration_data[0]) * 2.5
                diff_y = (nose_position[1] - calibration_data[1]) * 2.5
                
                cursor_x = np.clip(pyautogui.position()[0] + diff_x, 0, screen_w - 1)
                cursor_y = np.clip(pyautogui.position()[1] + diff_y, 0, screen_h - 1)
                pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)

                # Blink Detection
                left_eye_landmarks = all_landmarks[LEFT_EYE_INDICES]
                right_eye_landmarks = all_landmarks[RIGHT_EYE_INDICES]

                left_ear = eye_aspect_ratio(left_eye_landmarks)
                right_ear = eye_aspect_ratio(right_eye_landmarks)

                current_time = time.time()

                # Left Blink for Left Click
                if left_ear < BLINK_THRESHOLD and right_ear > BLINK_THRESHOLD:
                    if current_time - last_left_click_time > BLINK_COOLDOWN:
                        pyautogui.click(button='left')
                        last_left_click_time = current_time
                        print("🖱️ Left Click")

                # Right Blink for Right Click
                if right_ear < BLINK_THRESHOLD and left_ear > BLINK_THRESHOLD:
                    if current_time - last_right_click_time > BLINK_COOLDOWN:
                        pyautogui.click(button='right')
                        last_right_click_time = current_time
                        print("🖱️ Right Click")

                # Both Eyes Blink for Double Click
                if left_ear < BLINK_THRESHOLD and right_ear < BLINK_THRESHOLD:
                     if current_time - last_double_click_time > BLINK_COOLDOWN:
                        pyautogui.doubleClick()
                        last_double_click_time = current_time
                        print("🖱️ Double Click")
                
                # --- Visualization (Optional) ---
                # Draw landmarks on the face for visual feedback
                for landmark in all_landmarks:
                    cv2.circle(frame, tuple(landmark.astype(int)), 1, (0, 255, 0), -1)


            cv2.imshow('Eye Controlled Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nProgram exited by user.")

    finally:
        # --- Cleanup ---
        cap.release()
        cv2.destroyAllWindows()
        face_mesh.close()