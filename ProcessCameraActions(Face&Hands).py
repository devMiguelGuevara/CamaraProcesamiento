"""Visualización en vivo de la malla facial y las manos con MediaPipe.

Solo dibuja (con FPS); no detecta acciones. La versión con parpadeos y gestos
es ProcessCameraActions.py. Esc para salir.
"""
import cv2
import mediapipe as mp
import time

mp_face = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_time = 0

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

        face_results = face_mesh.process(rgb)
        hand_results = hands.process(rgb)

        h, w, _ = frame.shape

        # ===== FACE =====
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

        # ===== HANDS =====
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(0,255,255), thickness=2)
                )

                # Punta dedo índice (landmark 8)
                index_tip = hand_landmarks.landmark[8]
                cx = int(index_tip.x * w)
                cy = int(index_tip.y * h)

                cv2.circle(frame, (cx, cy), 8, (0,0,255), -1)

        # FPS
        current_time = time.time()
        fps = 1/(current_time-prev_time) if prev_time else 0
        prev_time = current_time

        cv2.putText(frame, f"FPS: {int(fps)}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        cv2.imshow("Face + Hands Tracking", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()