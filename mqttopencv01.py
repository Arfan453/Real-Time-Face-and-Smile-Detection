import cv2
import time
import paho.mqtt.client as mqtt
import json

# MQTT Configuration
DeviceDeveloperID = "laptopcamera@mohdarfan453"
AccessToken = "OZdHVJ90dwCSExbQAcgNO4EGnm56MpC5"
BROKER = "mqtt.favoriot.com"
PORT = 1883
TOPIC = "/v2/streams"


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Favoriot!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully!")

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(AccessToken, AccessToken)
mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.on_log = lambda client, userdata, level, buf: print("MQTT Log:", buf)

# Connect to MQTT Broker
mqtt_client.connect(BROKER, PORT, 60)

# Haar Cascade Configuration
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

if face_cascade.empty() or smile_cascade.empty():
    print("Error: Haar cascade files not loaded correctly.")
    exit()

# Camera Setup
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the camera!")
    exit()

# Timing for MQTT Publishing
last_publish_time = time.time()

# Main Loop for Face and Smile Detection
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to grab a frame!")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5)
    smiles_detected = 0

    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
        if len(smiles) > 0:
            smiles_detected += 1

    current_time = time.time()
    if current_time - last_publish_time >= 10:  # Publish data every 10 seconds
        payload = {
            "device_developer_id": "laptopcamera@mohdarfan453",  # Replace with your device ID
            "data": {
                "faces_detected": len(faces),
                "smiles_detected": smiles_detected
            }
        }
        print(f"Sending to Favoriot: {payload}")
        mqtt_client.publish(AccessToken + TOPIC, json.dumps(payload))
        last_publish_time = current_time

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray_frame[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)
        if len(smiles) > 0:
            cv2.putText(frame, "Smiling :)", (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    cv2.putText(frame, f"Faces: {len(faces)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Face and Smile Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
mqtt_client.disconnect()

