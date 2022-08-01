import numpy as np
import time
import cv2

confidece_thres = 0.2

CLASSES = ["aeroplane", "background", "bicycle", "bird", "boat",
		   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
		   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
		   "sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(
	"MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

# cap = cv2.VideoCapture(0)


def getLocation(cap):
	centerX = 0
	centerY = 0
	ret, frame = cap.read()	
	frame = cv2.flip(frame, 1)
	h, w, _ = frame.shape
	resized_image = cv2.resize(frame, (300, 300))	

	blob = cv2.dnn.blobFromImage(
		resized_image, (1/127.5), (300, 300), 127.5, swapRB=True)
	net.setInput(blob)
	predictions = net.forward()

	for i in np.arange(0, predictions.shape[2]):
		confidence = predictions[0, 0, i, 2]
		if confidence > confidece_thres:
			idx = int(predictions[0, 0, i, 1])
			if CLASSES[idx] == 'car':
				box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				centerX = (startX + endX) / 2
				centerY = (startY + endY) / 2

				cv2.circle(frame, (int(centerX), int(centerY)), 6, (255, 255, 255), 3)

	cv2.imshow('frame', frame)
	cv2.waitKey(1) & 0xFF	

	return centerX, centerY

# while True:
# 	x, y = getLocation(cap)		

# while True:
# 	centerX = 0
# 	centerY = 0
# 	ret, frame = cap.read()
# 	frame = cv2.flip(frame, 1)
# 	h, w, _ = frame.shape
# 	resized_image = cv2.resize(frame, (300, 300))

# 	blob = cv2.dnn.blobFromImage(
# 		resized_image, (1/127.5), (300, 300), 127.5, swapRB=True)
# 	net.setInput(blob)
# 	predictions = net.forward()

# 	for i in np.arange(0, predictions.shape[2]):
# 		confidence = predictions[0, 0, i, 2]
# 		if confidence > confidece_thres:
# 			idx = int(predictions[0, 0, i, 1])
# 			if CLASSES[idx] == 'car':
# 				box = predictions[0, 0, i, 3:7] * np.array([w, h, w, h])
# 				(startX, startY, endX, endY) = box.astype("int")

# 				centerX = (startX + endX) / 2 				
				
# 				centerY = (startY + endY) / 2 # 44 - 434 -> 				

# 				cv2.circle(frame, (int(centerX), int(centerY)), 2, (0,0,0), 2)						

# 	cv2.imshow("Frame", frame)

# 	key = cv2.waitKey(1) & 0xFF
# 	if key == ord("q"):
# 		break

# cv2.destroyAllWindows()
