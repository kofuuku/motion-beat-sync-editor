import cv2
import torch
import numpy as np
from ultralytics import YOLO  # YOLOv8

# Load YOLOv8 Pose Model (for keypoints)
model = YOLO("yolov8n-pose.pt")  # Use 'yolov8s-pose.pt' for better accuracy

# Load OpenCV DNN Face Detector
face_net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel")

# Load Video File
video_path = "/home/khuushi/motion-beat-sync-editor/thisvid.mp4"
cap = cv2.VideoCapture(video_path)

# Define Skeleton Connections (for YOLO Pose Estimation)
SKELETON_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),  # Right arm
    (0, 5), (5, 6), (6, 7), (7, 8),  # Left arm
    (0, 9), (9, 10), (10, 11),       # Right leg
    (0, 12), (12, 13), (13, 14),     # Left leg
]

# Process Each Frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no frame is read

    h, w = frame.shape[:2]

    # Face Detection
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # YOLOv8 Pose Detection
    results = model(frame)

    for result in results:
        # Draw Bounding Boxes
        if hasattr(result, "boxes") and result.boxes is not None:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
                conf = box.conf[0].item()  # Confidence score
                cls = int(box.cls[0].item())  # Class ID

                # Draw Bounding Box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"ID {cls}: {conf:.2f}", (x1, y1 - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Draw Keypoints & Skeleton
        if hasattr(result, "keypoints") and result.keypoints is not None:
            keypoints = result.keypoints.xy[0]  # Extract keypoints

            # Draw Keypoints (Green Dots)
            for kp in keypoints:
                if len(kp) >= 2:  # Ensure there are at least x and y coordinates
                    x, y = map(int, kp[:2])
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # Draw Skeleton (Blue Lines)
            for p1, p2 in SKELETON_CONNECTIONS:
                if p1 < len(keypoints) and p2 < len(keypoints):
                    x1, y1 = map(int, keypoints[p1][:2])
                    x2, y2 = map(int, keypoints[p2][:2])
                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Display Results
    cv2.imshow("Video Analysis", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # Press 'q' or 'Esc' to exit
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
