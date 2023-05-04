import torch
import cv2
import os
import math
import pyttsx3
import threading

# Initialize the voice engine
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use the first available voice
engine.setProperty('rate', 100)

# Initialize the camera
cam = cv2.VideoCapture(0)

# Create a window to display the video feed
cv2.namedWindow("test")

# Initialize variables
img_counter = 0
isTakingPhoto = False

import sys
if len(sys.argv) > 1:
    username = sys.argv[1]





while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Display the current frame
    cv2.imshow("test", frame)

    # Check for key press
    k = cv2.waitKey(1)

    # If the space bar is pressed, take a photo and detect objects
    if k % 256 == 32:
        isTakingPhoto = True

    if isTakingPhoto:
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("Screenshot taken")
        img_counter += 1
        isTakingPhoto = False

        # Load the YOLOv5 model and its configuration file
        model = torch.hub.load('ultralytics/yolov5', 'yolov5x', pretrained=True)

        # Load the input image
        image = cv2.imread(img_name)

        # Detect objects in the image
        results = model(image)
        
        objects=[]
        # Loop over the detected objects and draw bounding boxes with class names
        for obj in results.xyxy[0]:
            class_id = int(obj[5])
            confidence = obj[4].item()
            class_name = model.names[class_id]
            xmin, ymin, xmax, ymax = map(int, obj[:4])
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (187, 19, 176), 2)
            cv2.putText(image, f'{class_name} {confidence:.2f}', (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (187, 19, 176), 2)

            
            objects.append(class_name)
            print(class_name)



        # Save the output image with bounding boxes and class names
        filename = "output_image_{}.jpg".format(img_counter-1)
        cv2.imwrite(filename, image)

        # Display the output image
        cv2.imshow("Output Image", image)

        print(objects)

        # Output the text as voice
        for x in objects:
            print(x)
            text = "it is a " + x
            engine.say(text)
            engine.runAndWait()

    # If the escape key is pressed, close the app
    elif k % 256 == 27:
        print("Escape Hit, Closing the app")
        break

# Release the camera
cam.release()

# Close all windows
cv2.destroyAllWindows()


