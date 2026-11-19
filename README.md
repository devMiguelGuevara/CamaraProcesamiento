# CamaraProcesamiento

Detección de rostro y manos con la webcam usando [MediaPipe](https://developers.google.com/mediapipe), y reconocimiento de parpadeos y gestos de dedos.

## Acciones que reconoce

`ProcessCameraActions.py` dibuja la malla facial y las manos en vivo y escribe en consola cada acción:

| Evento | Gesto |
|---|---|
| `BLINK` | Parpadeo: el *eye aspect ratio* (EAR) de ambos ojos baja de 0.21 |
| `LEFT_1_2` | Mano izquierda: el pulgar toca el índice |
| `LEFT_1_5` | Mano izquierda: el pulgar toca el meñique |
| `RIGHT_2_5` | Mano derecha: el índice toca el meñique |

La idea es usar estos eventos para controlar el computador con gestos. Por ahora solo se imprimen.

## Instalación

Python 3.10:

```powershell
py -3.10 -m venv venv310
.\venv310\Scripts\activate
pip install -r requirements.txt
```

## Uso

```powershell
python ProcessCameraActions.py                  # rostro + manos + acciones
python "ProcessCameraActions(Face&Hands).py"    # solo dibuja rostro y manos
python "ProcessCameraActions(SoloRostro).py"    # solo la malla facial
```

`Esc` para salir.

## Pendientes

- Unir las tres variantes en un solo script con opciones.
- Evitar que un gesto sostenido se repita en cada cuadro.
- Conectar los eventos a acciones reales (teclas, clics, atajos).
