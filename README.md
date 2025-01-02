# Face and Smile Detection with MQTT

This project demonstrates how to perform real-time face and smile detection using a laptop camera and send the data to the Favoriot platform via MQTT. The data sent to the platform is the number of faces and smiles detected every 10 seconds.

## Requirements

Before running this project, make sure you have the following installed on your machine:

- Python 3.x
- OpenCV
- Paho-MQTT
- A working camera (e.g., laptop webcam)
  
You can install the required Python libraries by running:

```bash
pip install opencv-python paho-mqtt
```

Setup Instructions
---

### 1\. Open the Script

load the face_smile_detection.py script into the editor.

### 2\. Update MQTT Credentials

Replace the `DeviceDeveloperID` and `AccessToken` with your own credentials for the Favoriot platform. You can obtain these credentials from the Favoriot platform.

In the script, update the following:

```python
DeviceDeveloperID = "your_device_id"
AccessToken = "your_access_token"
```

### 3\. Haar Cascade Files

The project uses pre-trained Haar Cascade classifiers for detecting faces and smiles. These files are included by default in OpenCV, but make sure they are properly loaded. If the program cannot load the files, it will display an error message.

```python
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
```

### 4\. Run the Script

Once the setup is complete, run the script:

```bash
python face_smile_detection.py
```

This will start capturing video from your webcam and detecting faces and smiles in real-time. It will display the webcam feed with rectangles drawn around detected faces and text indicating if the person is smiling.


<p align="center"><img src="https://github.com/user-attachments/assets/34a4e21e-7ef6-4a56-8376-1682aef4be6f" width="500"></a></p>


<p align="center"><img src="https://github.com/user-attachments/assets/46c8e627-74c9-4592-9803-cd1f8ea977a2" width="500"></a></p>




### 5\. MQTT Publishing

The detected face and smile counts will be sent to the Favoriot platform every 10 seconds via MQTT. The message payload will look like this:

```json
{
  "device_developer_id": "your_device_id",
  "data": {
    "faces_detected": number_of_faces,
    "smiles_detected": number_of_smiles
  }
}
```

### 6\. Exit the Program

To exit the program, press the `q` key.

License
---

This project is licensed under the MIT License - see the LICENSE file for details.
