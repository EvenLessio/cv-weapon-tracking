from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import numpy as np
import cv2
import time
import datetime
import os
import shutil

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("key/serviceAccountKey.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://weapon-recognition-omsk-default-rtdb.firebaseio.com/",
    'storageBucket': "weapon-recognition-omsk.appspot.com"
})

class Detection(QThread):  # QThread allow to run detection within a separate thread
    def __init__(self):
        super(Detection, self).__init__()

    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.running = True

        net = cv2.dnn.readNet('weights/yolov4.weights', 'cfg/yolov4.cfg')

        with open('obj.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        font = cv2.FONT_HERSHEY_PLAIN
        starting_time = time.time()

        cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cap.read()

            if ret:
                height, width, channels = frame.shape

                blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers)

                class_ids = []
                confidences = []
                boxes = []
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]

                        if confidence > 0.80:
                            center_x = int(detection[0] * width)
                            center_y = int(detection[1] * height)
                            w = int(detection[2] * width)
                            h = int(detection[3] * height)

                            x = int(center_x - w / 2)
                            y = int(center_y - h / 2)

                            boxes.append([x, y, w, h])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)

                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)

                for i in range(len(boxes)):
                    if i in indexes:
                        x, y, w, h = boxes[i]
                        label = str(classes[class_ids[i]])
                        confidence = confidences[i]
                        color = (265, 0, 0)
                        cv2.rectangle(frame, (x,y), (x + w, y + h), color, 2)
                        cv2.putText(frame, label + " {0:.1%}".format(confidence), (x, y - 20), font, 2, color, 3)

                        elapsed_time = starting_time - time.time()

                        if elapsed_time <= -10:
                            starting_time = time.time()
                            self.save_detection(frame)

                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                bytesPerLine = channels * width
                convertToQtFormat = QImage(rgbImage.data, width, height,
                                           bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(854, 700, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    # cv2.imwrite("Alertions/alert.jpg", frame)
    # dt = str(datetime.datetime.now())
    # datename = 'alert_' + dt + '.jpg'
    # os.rename("Alertions/alert.jpg", datename)
    # print('Frame Saved')
    def save_detection(self, frame):
        cv2.imwrite("Alertions/alert_.jpg", frame)

        dt = str(datetime.datetime.now())
        datename = 'alert_' + dt + '.jpg'
        os.rename("Alertions/alert_.jpg", datename)

        temp = 'alert_' + dt + '.jpg'
        destination = 'Alertions/'
        shutil.move(temp, destination)

        filePath = 'Alertions/alert_' + dt + '.jpg'
        bucket = storage.bucket()
        blob = bucket.blob(filePath)
        blob.upload_from_filename(filePath)

        print('Frame Saved')
