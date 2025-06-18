# Face_Recognition Attendance System

This project implements a face recognition-based attendance system using Python, OpenCV, DeepFace, and MySQL. The system detects faces in real-time, recognizes registered individuals, and records their attendance with timestamps in a database.

# Face Recognition Attendance System

## Copyright Notice
© 2025 Siddham Shah. All Rights Reserved.

This software and documentation contain proprietary information and are protected by copyright law. Unauthorized reproduction, distribution, or modification is strictly prohibited.

## Legal Warning
Any unauthorized use, copying, or distribution of this software may violate copyright laws and result in legal consequences. For licensing inquiries, please contact siddhamshah972@gmail.com.

## Features

- Real-time face detection using Haar cascades
- Face recognition using DeepFace with VGG-Face model
- Attendance recording with name, roll number, date, and time
- Automatic snapshot capture of recognized faces
- MySQL database integration for attendance records

## Prerequisites

Before running the system, ensure you have the following installed:

1. Python 3.6 or higher
2. MySQL Server
3. Webcam

## Installation Steps

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/face-recognition-attendance.git
cd face-recognition-attendance
```

### 2. Install required Python packages

```bash
pip install opencv-python deepface mysql-connector-python
```

### 3. Set up the MySQL database

1. Log in to MySQL:
```bash
mysql -u root -p
```

2. Create the database and table:
```sql
CREATE DATABASE face_attendance;

USE face_attendance;

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50),
    date DATE NOT NULL,
    time TIME NOT NULL,
    snapshot_path VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Configure the system

Edit the following variables in the script if needed:
- MySQL connection details (host, user, password)
- Dataset path (default: "dataset")
- Snapshot directory (default: "snapshots")

## Usage Instructions

### 1. Prepare the face dataset

1. Create a folder named "dataset" in your project directory
2. Add images of faces you want to recognize in the format:
   - For students: `ROLLNO_NAME.jpg` (e.g., `101_JohnDoe.jpg`)
   - For staff: `NAME.jpg` (e.g., `ProfessorSmith.jpg`)

### 2. Run the system

```bash
python attendance_system.py
```

### 3. Using the system

1. The system will open a window showing your webcam feed
2. Stand in front of the camera (make sure your face is clearly visible)
3. The system will:
   - Detect your face (red rectangle)
   - Wait 5 seconds for analysis
   - Recognize you if you're in the dataset (green rectangle with your name)
   - Record your attendance in the database
   - Save a snapshot in the "snapshots" folder
4. Press ESC to exit the system

### 4. Viewing attendance records

You can view the attendance records directly in MySQL:

```sql
USE face_attendance;
SELECT * FROM attendance ORDER BY date DESC, time DESC;
```

## Troubleshooting

1. **Face not detected**:
   - Ensure proper lighting
   - Remove obstructions (glasses, masks, etc.)
   - Position your face directly facing the camera

2. **MySQL connection errors**:
   - Verify your MySQL server is running
   - Check your username and password in the script
   - Ensure you have proper privileges

3. **Recognition errors**:
   - Use high-quality images in the dataset
   - Ensure the face is clearly visible in the dataset images
   - Try different angles if recognition fails

## Customization Options

1. Change the recognition model by modifying the `model_name` parameter in `DeepFace.find()`
   - Options: "VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"
   
2. Adjust the detection sensitivity by modifying:
   - `scaleFactor` and `minNeighbors` in `detectMultiScale()`

3. Change the analysis time by modifying the `time.time() - start_time >= 5` condition

## Directory Structure
face-recognition-attendance/
├── attendance_system.py        # Main Python script
├── dataset/                    # Folder containing known faces
│   ├── 101_JohnDoe.jpg         # Sample image (RollNo_Name.jpg)
│   ├── 102_JaneSmith.jpg
│   └── ProfessorWilliams.jpg   # For staff without roll numbers
├── snapshots/                  # Auto-created folder for attendance snapshots
├── README.md                   # This documentation file
└── requirements.txt            # Python dependencies 

For any issues or questions, please open an issue in the GitHub repository.
