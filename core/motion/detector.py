import cv2
import argparse
import json
import numpy as np
from pathlib import Path


def process_video(video_path, output_path=None, sensitivity=500):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if output_path is None:
        output_path = Path(video_path).with_name(f"{Path(video_path).stem}_processed.mp4")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
    
    motion_data = []
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()
    frame_idx = 0
    
    while cap.isOpened() and ret:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_intensity = sum(cv2.contourArea(c) for c in contours) / (width * height) * 100
        motion_data.append({
            "frame": frame_idx,
            "timestamp": frame_idx / fps,
            "motion_areas": len(contours),
            "intensity": motion_intensity
        })
        
        for contour in contours:
            if cv2.contourArea(contour) < sensitivity:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        bar_height = 5
        bar_width = int((width * motion_intensity) / 100)
        cv2.rectangle(frame1, (0, height - bar_height), (bar_width, height), (0, 255, 255), -1)
        cv2.putText(frame1, f"Intensity: {motion_intensity:.1f}%", (10, height - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        out.write(frame1)
        
        frame1 = frame2
        ret, frame2 = cap.read()
        frame_idx += 1
        
        cv2.imshow("Motion Detection", frame1)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    motion_data_path = Path(output_path).with_suffix('.json')
    with open(motion_data_path, 'w') as f:
        json.dump({
            "video_info": {
                "width": width,
                "height": height,
                "fps": fps,
                "frame_count": frame_count,
                "duration": frame_count / fps
            },
            "frames": motion_data
        }, f, indent=2)
    
    print(f"Processed video saved to {output_path}")
    print(f"Motion data saved to {motion_data_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Motion Detection on Video with Processing")
    parser.add_argument("video", help="Path to the input video file")
    parser.add_argument("--output", type=str, help="Path to the output processed video file")
    parser.add_argument("--sensitivity", type=int, default=500, help="Motion sensitivity threshold")
    
    args = parser.parse_args()
    process_video(args.video, args.output, args.sensitivity)
