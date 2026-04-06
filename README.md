# Hand Gesture Counter (Finger Counting) using Python & MediaPipe

Detect hand landmarks and count the number of raised fingers in a video using MediaPipe Hands.

## How it works
1. MediaPipe Hands detects 21 landmarks per hand
2. Thumb: checks if the tip extends outward past the IP joint (x-axis)
3. Other fingers: checks if the fingertip is above the PIP joint (y-axis)
4. Draws landmarks, connections, and per-hand + total finger count

## Run
```bash
python3 finger_count.py
```

Place your video as `input.mp4` in the same folder.

## Tech
- Python
- MediaPipe
- OpenCV
