# Motion Analysis API

This API processes video files, extracts motion vectors, and detects high-energy moments that align with beats in the audio.

## **Base URL**
`https://your-api.com` (Replace with actual server address)

---

## **Endpoints**  

### **1️⃣ Upload Video**  
- **URL:** `POST /upload`  
- **Description:** Upload a video file for analysis.  
- **Why this request format?**
  - `multipart/form-data` is used to handle file uploads efficiently.
  - The file is sent as a binary stream to reduce payload size.
- **Request:**  
  - **Content-Type:** `multipart/form-data`  
  - **Body:**  
    ```json
    {
        "file": "video.mp4"
    }
    ```
- **Why this response format?**
  - Returns a `video_id` to track the uploaded file.
  - A success message confirms the upload.
- **Response:**  
  ```json
  {
      "video_id": "12345",
      "message": "Upload successful"
  }
  ```

---

### **2️⃣ Analyze Video**  
- **URL:** `POST /analyze`  
- **Description:** Processes a video and extracts motion features.  
- **Why this request format?**
  - Requires `video_id` as input to identify which video to analyze.
  - Uses JSON for structured data transmission.
- **Request:**  
  ```json
  {
      "video_id": "12345"
  }
  ```
- **Why this response format?**
  - Indicates that processing has started but does not return results immediately.
  - `status: processing` allows polling for updates.
- **Response:**  
  ```json
  {
      "video_id": "12345",
      "status": "processing"
  }
  ```

---

### **3️⃣ Get Analysis Results**  
- **URL:** `GET /results/{video_id}`  
- **Description:** Retrieves motion data for a processed video.  
- **Why this request format?**
  - Uses `GET` since it's a retrieval operation.
  - `{video_id}` is part of the URL for RESTful design.
- **Response:**  
  ```json
  {
      "video_id": "12345",
      "motion_data": [
          {
              "frame_index": 0,
              "timestamp": 0.0,
              "velocity": [2.5, 0.0],
              "acceleration": [0.1, 0.0],
              "is_peak_moment": true
          }
      ]
  }
  ```
- **Why this response format?**
  - Includes `motion_data` array for time-series motion tracking.
  - Each frame contains velocity, acceleration, and peak movement flags for precise analysis.

---

### **4️⃣ Delete Video**  
- **URL:** `DELETE /video/{video_id}`  
- **Description:** Deletes a video and its motion data.  
- **Why this request format?**
  - Uses `DELETE` to indicate resource removal.
  - `{video_id}` in the URL ensures a specific video is targeted.
- **Response:**  
  ```json
  {
      "video_id": "12345",
      "message": "Video deleted successfully"
  }
  ```
- **Why this response format?**
  - Confirms deletion with a `video_id` for traceability.
  - Simple message ensures clarity.

---

### **5️⃣ List Processed Videos**  
- **URL:** `GET /videos`  
- **Description:** Retrieves a list of all processed videos.  
- **Why this request format?**
  - Uses `GET` for data retrieval.
  - No request body needed since it's a general query.
- **Response:**  
  ```json
  {
      "videos": [
          {
              "video_id": "12345",
              "status": "completed"
          },
          {
              "video_id": "67890",
              "status": "processing"
          }
      ]
  }
  ```
- **Why this response format?**
  - Provides a list of videos with their processing status.
  - Helps in tracking multiple videos efficiently.

---


