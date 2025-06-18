# =======================================================
# Face Recognition Attendance System
# Copyright (c) 2025 Siddham Shah
# All Rights Reserved
#
# This software is protected by copyright law and
# international treaties. Unauthorized reproduction or
# distribution of this software may result in severe
# civil and criminal penalties.
# =======================================================

import cv2
import os
import time
import sys
from datetime import datetime
import mysql.connector
from deepface import DeepFace

# === LICENSE VERIFICATION ===
AUTHORIZED_DEVELOPER = "Siddham Shah"
DEVELOPER_EMAIL = "siddhamshah972@gmail.com"

def verify_license():
    if not AUTHORIZED_DEVELOPER == "Siddham Shah":
        print("UNAUTHORIZED USE DETECTED")
        print(f"Please contact {DEVELOPER_EMAIL} for legitimate access")
        sys.exit(1)

verify_license()

# === CONFIG ===
dataset_path = "dataset"
snapshot_dir = "snapshots"
os.makedirs(snapshot_dir, exist_ok=True)

# === MYSQL CONNECTION ===
conn = mysql.connector.connect(
    host="localhost",
    user="mysql-username", # Needs to be changed by user
    password="mysql-password", # Needs to be changed by user
    database="face_attendance"
)
cursor = conn.cursor()

# === MODEL & VIDEO SETUP ===
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
print("[INFO] Press ESC to exit.")

# === STATE VARIABLES ===
analyzing = False
start_time = 0
recognized = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    label = ""

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face = frame[y:y+h, x:x+w]

        if not analyzing:
            start_time = time.time()
            analyzing = True
            print("[INFO] Face detected. Waiting 5 seconds for analysis...")

        elif time.time() - start_time >= 5:
            try:
                result = DeepFace.find(
                    img_path=face,
                    db_path=dataset_path,
                    model_name="VGG-Face",
                    enforce_detection=False,
                    silent=True
                )

                if result and not result[0].empty:
                    identity_path = result[0].iloc[0]["identity"]
                    filename = os.path.splitext(os.path.basename(identity_path))[0]

                    if '_' in filename:
                        roll_no, name = filename.split('_', 1)
                    else:
                        name = filename
                        roll_no = "Unknown"

                    label = f"{name} ({roll_no})"

                    if name not in recognized:
                        recognized.add(name)

                        now = datetime.now()
                        date = now.date()
                        time_now = now.strftime("%H:%M:%S")

                        # Draw label on frame before saving
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(frame, label, (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                        snapshot_filename = f"{name}_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
                        snapshot_path = os.path.join(snapshot_dir, snapshot_filename)
                        cv2.imwrite(snapshot_path, frame)

                        insert_query = """
                            INSERT INTO attendance (name, roll_no, date, time, snapshot_path)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_query, (name, roll_no, date, time_now, snapshot_path))
                        conn.commit()

                        print(f"[ATTENDANCE] {name} ({roll_no}) marked at {time_now} on {date}")
                    else:
                        print(f"[INFO] {name} already recognized.")

                else:
                    label = "Unknown"
                    print("[INFO] Face not recognized.")

            except Exception as e:
                print("[ERROR] Recognition failed:", e)
                label = "Error"

            analyzing = False

        # Draw bounding box and label
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255) if "Unknown" in label else (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255) if "Unknown" in label else (0, 255, 0), 2)

    else:
        analyzing = False

    # Display frame
    cv2.imshow("Face Recognition Attendance", frame)
    if cv2.waitKey(1) == 27:  # ESC key
        break

# === CLEAN UP ===
cap.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()
