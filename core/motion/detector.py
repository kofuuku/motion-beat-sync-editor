import cv2
import torch
import numpy as np
import os
from ultralytics import YOLO  
from insightface.app import FaceAnalysis  # RetinaFace

# Load YOLOv8 Pose Model
model = YOLO("yolo11n-pose.pt")  # YOLO for pose detection

# Load RetinaFace Model
face_detector = FaceAnalysis(name="buffalo_l")  # Uses RetinaFace with ResNet50
face_detector.prepare(ctx_id=0)  # Set GPU (ctx_id=0) or CPU (-1)

# Load Video File
video_path = "/home/khuushi/motion-beat-sync-editor/thisvid3.mp4"
cap = cv2.VideoCapture(video_path)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define codec and create VideoWriter object
output_path = "output.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# YOLO Pose Keypoint Order (COCO format)
SKELETON_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),  # Right arm
    (0, 5), (5, 6), (6, 7), (7, 8),  # Left arm
    (5, 11), (6, 12),  # Shoulders to hips
    (11, 12),  # Hip connection
    (11, 13), (13, 15),  # Right leg
    (12, 14), (14, 16)   # Left leg
]

# Process Each Frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no frame is read

    # Run YOLO Pose Estimation
    results = model(frame)

    for result in results:
        # Draw Bounding Boxes (Optional)
        if result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
                conf = box.conf[0].item()  # Confidence score
                cls = int(box.cls[0].item())  # Class ID

                # Draw Bounding Box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"ID {cls}: {conf:.2f}", (x1, y1 - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Draw Keypoints & Skeleton
        if result.keypoints is not None:
            keypoints = result.keypoints.xy  # Extract all keypoints

            for person in keypoints:
                person = person.cpu().numpy()  # Convert to NumPy
                if len(person) == 0:
                    continue  # Skip if no keypoints detected

                # Draw Keypoints (Green Dots)
                for x, y in person:
                    if x > 0 and y > 0:  # Check if keypoint is valid
                        cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), -1)

                # Draw Skeleton (Blue Lines)
                for p1, p2 in SKELETON_CONNECTIONS:
                    if p1 < len(person) and p2 < len(person):
                        x1, y1 = person[p1]
                        x2, y2 = person[p2]

                        if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:  # Ensure valid points
                            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

    # --- Run RetinaFace for Face Detection ---
    faces = face_detector.get(frame)  # Detect faces in the frame

    for face in faces:
        x1, y1, x2, y2 = map(int, face.bbox)  # Face bounding box
        landmarks = face.kps  # Facial keypoints (eyes, nose, mouth, etc.)

        # Draw Face Bounding Box (Red)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

        # Draw Facial Landmarks (Yellow)
        for x, y in landmarks:
            cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), -1)


    # Display Results
    out.write(frame)
    cv2.imshow("Pose + Face Detection", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # Press 'q' or 'Esc' to exit
        break

# Cleanup
cap.release()
out.release()
cv2.destroyAllWindows()