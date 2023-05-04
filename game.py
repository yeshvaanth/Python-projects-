import cvzone
import cv2
import numpy as np
import math
# hand tracking module
from cvzone.HandTrackingModule import HandDetector
import random

# Set the height and width
height = 1480
width = 1480


# Initialize the camera capture object
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Set the camera resolution
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

detector = HandDetector(detectionCon=0.8, maxHands=1) # just use 1 hand

# What we need
# 1. List of points
# 2. List of distances
# 3. Current Length
# 4. Total Length

class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = [] # 1
        self.lengths = [] # 2
        self.currentLength = 0 # 3
        self.allowedLength = 150 # start length
        self.previousHead = 0, 0 # previous head point

        # foor image path,
        # set to UNCHANGED to remove background from png
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        # dimension or location of food
        self.hFood, self.wFood, _ = self.imgFood.shape
        # food point, set random
        self.foodPoint = 0, 0
        self.score = 0

        self.gameOver = False

        #initialize random food
        self.randomFoodLocation()

    def randomFoodLocation(self):
        self.foodPoint = (random.randint(100, 1000), random.randint(100,600))

    # method for update
    def update(self, imgMain, currentHead):

        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over ", [300, 400], scale= 7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f"Final Score: {self.score}", [300, 250], scale= 7, thickness=5, offset=20)
        else:

            px, py = self.previousHead
            cx, cy = currentHead

            # store the current head point to points
            self.points.append([cx, cy])
            # append the distance
            distance = math.hypot(cx-px, cy-py)
            self.lengths.append(distance)
            # once we get the distance, add to the current length
            self.currentLength += distance
            # update the previous head
            self.previousHead = cx,cy

            # LENGTH REDUCTION
            # check if currentlength grater than allowed length, to make sure fixed length by reducing line
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    # reduce the points and the lengths
                    self.lengths.pop(i)
                    self.points.pop(i)

                    if self.currentLength < self.allowedLength:
                        break


            if self.points:
                # DRAW SNAKE IF WE HAVE POINTS
                for i,point in enumerate(self.points):
                    if i != 0:
                        # point line to the current point
                        cv2.line(imgMain, self.points[i-1], self.points[i], (0,0,255), 20)
                # draw circle in finger
                cv2.circle(imgMain, self.points[-1], 20, (255,0,0), cv2.FILLED)

            # CHECK FOR COLLISION
            pts = np.array(self.points[:-2], np.int32)  # Ignore the last two points
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 200, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)
            print(minDist)

            # if -1 <= minDist <= 0:
            #     self.gameOver = True
            #     self.points = []  # 1
            #     self.lengths = []  # 2
            #     self.currentLength = 0  # 3
            #     self.allowedLength = 150  # start length
            #     self.previousHead = 0, 0  # previous head point


            # DRAW FOOD
            # imgMain : background img
            # self.imgFood
            rx, ry = self.foodPoint
            cv2.circle(imgMain, (rx, ry), 35, (255, 185, 0), cv2.FILLED)
            if abs(rx-cx) <= 20 and abs(ry-cy) <= 20:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [50,80],
                               scale=3, thickness=3, offset=20)
            
            if self.score==10:
                self.gameOver = True

        return imgMain

game = SnakeGameClass("mango.png")

while True:
    success,img = cap.read()
    #flip image, to make it easier for us
    img = cv2.flip(img, 1)
    # find hand
    hands, img = detector.findHands(img, flipType=False)
    cvzone.putTextRect(img, "Snake Game", [500, 80],
                       scale=3, thickness=3, offset=20)
    # find the point of hand in finger
    if hands:
        # landmark list
        lmList = hands[0]['lmList']
        # current head position, which is our finger
        pointIndex = lmList[8][0:2] # we wouldnt need 3
        # update image from class, set to img to be shown to the cap
        img = game.update(img, pointIndex)
    
    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the camera
cap.release()

# Close all windows
cv2.destroyAllWindows()