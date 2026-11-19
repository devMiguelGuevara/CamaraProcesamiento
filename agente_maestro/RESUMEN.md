# CamaraProcesamiento · Agente maestro

> Detección de rostro y manos con MediaPipe desde la webcam, y reconocimiento de parpadeos y gestos de dedos.

## Qué hace

Abre la cámara 0 y dibuja en vivo la malla facial (FaceMesh) y el esqueleto de las manos. La versión completa además detecta **acciones** y las imprime en consola:

| Evento | Cómo se detecta |
|---|---|
| `BLINK` | Parpadeo: el índice EAR (*eye aspect ratio*) de ambos ojos baja de 0.21 |
| `LEFT_1_2` | Mano izquierda: pulgar toca índice |
| `LEFT_1_5` | Mano izquierda: pulgar toca meñique |
| `RIGHT_2_5` | Mano derecha: índice toca meñique |

La idea de fondo parece ser controlar el computador con gestos; por ahora los eventos solo se imprimen, no ejecutan ninguna acción.

## Estado

**Prototipo.** Última modificación: 23-feb-2026.

## Cómo se usa

```powershell
.\venv310\Scripts\activate                      # entorno con Python 3.10.11
python "ProcessCameraActions.py"                # rostro + manos + detección de acciones
python "ProcessCameraActions(Face&Hands).py"    # solo dibuja rostro y manos
python "ProcessCameraActions(SoloRostro).py"    # solo malla facial
```

`Esc` para salir.

## Archivos clave

| Archivo | Función |
|---|---|
| `ProcessCameraActions.py` | Versión más completa: parpadeo + gestos + FPS |
| `ProcessCameraActions(Face&Hands).py` | Visualización de rostro y manos, sin acciones |
| `ProcessCameraActions(SoloRostro).py` | Solo FaceMesh |

## Dependencias

En `requirements.txt`, probadas en `venv310/` (Python 3.10.11, ~350 MB): `mediapipe 0.10.9` (API clásica `mp.solutions`), `opencv-contrib-python 4.13.0.92`, `numpy 2.2.6`.

## Observaciones y pendientes

- Las tres versiones son copias casi iguales; se podrían unir en un solo script con opciones.
- Los eventos se imprimen en cada cuadro mientras dure el gesto (salvo el parpadeo, que tiene enfriamiento): falta un *debounce* para los gestos.
- Falta conectar los eventos a acciones reales (teclas, clics, atajos).
- En `venv310` están instalados `opencv-python` y `opencv-contrib-python` a la vez, lo que puede causar conflictos. MediaPipe necesita el `contrib`, así que se puede desinstalar `opencv-python`. El `requirements.txt` ya lo omite.

## Cambios del 19-nov-2026

- Se agregó `requirements.txt` y una descripción al inicio de los tres scripts.

## Reglas para el agente

- `ProcessCameraActions.py` es la versión de referencia; las otras dos son variantes reducidas.
- Los umbrales (`blink_threshold`, `threshold` de gestos) están en coordenadas normalizadas de MediaPipe (0..1).
