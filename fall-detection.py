import cv2
import mediapipe as mp
import numpy as np
import math
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle
    return angle

cap = cv2.VideoCapture(0)

fall_detected = False
start_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        h, w, _ = image.shape
        lm = results.pose_landmarks.landmark

        left_shoulder = [lm[11].x * w, lm[11].y * h]
        right_shoulder = [lm[12].x * w, lm[12].y * h]
        left_hip = [lm[23].x * w, lm[23].y * h]
        right_hip = [lm[24].x * w, lm[24].y * h]

        mid_shoulder = [(left_shoulder[0]+right_shoulder[0])/2,
                        (left_shoulder[1]+right_shoulder[1])/2]

        mid_hip = [(left_hip[0]+right_hip[0])/2,
                   (left_hip[1]+right_hip[1])/2]

        body_angle = abs(mid_shoulder[1] - mid_hip[1])

        if body_angle < 40:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time > 1.5:
                fall_detected = True
        else:
            start_time = None
            fall_detected = False

        if fall_detected:
            cv2.putText(image, "FALL DETECTED!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 3)

    cv2.imshow("VisionGuard Fall Detection", image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
