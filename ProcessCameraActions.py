"""Detección de rostro, manos y acciones con la webcam (MediaPipe).

Dibuja en vivo la malla facial y las manos, y escribe en consola cada acción
que reconoce:
    BLINK      parpadeo (el EAR de ambos ojos baja de 0.21)
    LEFT_1_2   mano izquierda: pulgar toca índice
    LEFT_1_5   mano izquierda: pulgar toca meñique
    RIGHT_2_5  mano derecha: índice toca meñique

Es la versión más completa del proyecto. Esc para salir.
"""
import cv2
import mediapipe as mp
import numpy as np
import time
import math

mp_face = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_time = 0

# ====== FUNCIONES ======

def euclidean(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def eye_aspect_ratio(landmarks, eye_indices):
    p = [landmarks[i] for i in eye_indices]
    vertical1 = euclidean(p[1], p[5])
    vertical2 = euclidean(p[2], p[4])
    horizontal = euclidean(p[0], p[3])
    return (vertical1 + vertical2) / (2.0 * horizontal)

# Índices ojo izquierdo y derecho (MediaPipe FaceMesh)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

blink_threshold = 0.21
blink_cooldown = 0

touch_threshold = 0.05

with mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as face_mesh, mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape

        face_results = face_mesh.process(rgb)
        hand_results = hands.process(rgb)

        # ================= FACE =================
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0,255,0), thickness=1, circle_radius=1
                    )
                )

                landmarks = face_landmarks.landmark

                left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
                right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
                ear = (left_ear + right_ear) / 2.0

                if ear < blink_threshold and blink_cooldown == 0:
                    print("BLINK")
                    blink_cooldown = 10

        if blink_cooldown > 0:
            blink_cooldown -= 1

        # ================= HANDS =================
        if hand_results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                handedness = hand_results.multi_handedness[idx].classification[0].label
                lm = hand_landmarks.landmark

                thumb = lm[4]
                index = lm[8]
                pinky = lm[20]

                def dist(a, b):
                    return ((a.x - b.x)**2 + (a.y - b.y)**2) ** 0.5

                threshold = 0.05

                # ===== MANO IZQUIERDA =====
                if handedness == "Left":

                    # 1 y 2 (Pulgar + Índice)
                    if dist(thumb, index) < threshold:
                        print("LEFT_1_2")

                    # 1 y 5 (Pulgar + Meñique)
                    if dist(thumb, pinky) < threshold:
                        print("LEFT_1_5")

                # ===== MANO DERECHA =====
                elif handedness == "Right":

                    # 2 y 5 (Índice + Meñique)
                    if dist(index, pinky) < threshold:
                        print("RIGHT_2_5")

        # ================= FPS =================
        current_time = time.time()
        fps = 1/(current_time-prev_time) if prev_time else 0
        prev_time = current_time

        cv2.putText(frame, f"FPS: {int(fps)}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        cv2.imshow("Face + Gesture Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()