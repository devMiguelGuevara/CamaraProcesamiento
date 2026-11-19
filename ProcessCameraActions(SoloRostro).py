"""Visualización en vivo de la malla facial (FaceMesh, 468 puntos) con MediaPipe.

Marca la punta de la nariz con un punto rojo y muestra los FPS. Sin manos ni
acciones. Esc para salir.
"""
import cv2
import mediapipe as mp
import time

mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_time = 0

with mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as face_mesh:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:

                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0,255,0), thickness=1, circle_radius=1
                    )
                )

                # Punta de nariz
                nose = face_landmarks.landmark[1]
                h, w, _ = frame.shape
                x = int(nose.x * w)
                y = int(nose.y * h)

                cv2.circle(frame, (x, y), 5, (0,0,255), -1)

        current_time = time.time()
        fps = 1/(current_time-prev_time) if prev_time else 0
        prev_time = current_time

        cv2.putText(frame, f"FPS: {int(fps)}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        cv2.imshow("Face Mesh 468 Landmarks", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()