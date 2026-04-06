import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

# Open video file
video = cv2.VideoCapture("input.mp4")

# Get video properties
fps = int(video.get(cv2.CAP_PROP_FPS))
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create output video writer
output = cv2.VideoWriter(
    "output.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
)

frame_count = 0

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_count += 1

    # Convert BGR to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    total_fingers = 0

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks and connections
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark
            fingers = []

            # Thumb: use x-axis (direction depends on hand orientation)
            # Compare thumb CMC (1) with pinky MCP (17) to determine left/right
            if lm[1].x < lm[17].x:  # Right hand (from camera view)
                fingers.append(1 if lm[4].x < lm[3].x else 0)
            else:  # Left hand
                fingers.append(1 if lm[4].x > lm[3].x else 0)

            # Other four fingers: tip above PIP means finger is raised
            for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                fingers.append(1 if lm[tip].y < lm[pip].y else 0)

            count = sum(fingers)
            total_fingers += count

            # Display count near the wrist
            wrist = lm[0]
            wx, wy = int(wrist.x * width), int(wrist.y * height)
            cv2.putText(
                frame, str(count), (wx - 10, wy + 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 255), 3,
            )

    # Display total finger count on screen
    cv2.putText(
        frame, f"Fingers: {total_fingers}", (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3,
    )

    # Write frame to output
    output.write(frame)
    print(f"Frame {frame_count} - Fingers: {total_fingers}")

hands.close()
video.release()
output.release()
print(f"\nDone! Processed {frame_count} frames")
print("Output saved to: output.mp4")
