import json
import cv2
import numpy as np
from random import randint
from timer import RepeatingTimer

chooseFrom = open("best.json")
choice = json.load(chooseFrom)

def mood(count):
    if sm_ratio > 1.8:
        print(f"Face {count} :\n You look happy way to go!!")
    else:
        randInd = randint(0,99)
        print(f"Face {count} : \n{choice[randInd]['title']}\n{choice[randInd]['body']}\n")

# Replace the following two path strings to wherever your classifier files are
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('./haarcascade_smile.xml')

counter = 1
rt = []
cap = cv2.VideoCapture(0)
prevface = np.array([])
font = cv2.FONT_HERSHEY_SIMPLEX
sm_ratio = "0"

try:
    while True:

        # Detects faces in frame
        _, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21,21), 0)
        faces = face_cascade.detectMultiScale(gray, 1.3, 10)

        # Iterating through seen faces
        for count, (x, y, w, h) in enumerate(faces):

            cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
            cv2.putText(img, f"face {count+1}", (x, y-10), font, 0.9, (36, 225, 12), 2)

            roi_gray = gray[y + int(2*h/3):y + h, x:x + w]
            roi_color = img[y + int(2*h/3):y + h, x:x + w]

            # Detecting smile in each face
            smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor = 1.2,
                                                    minNeighbors = 20, minSize = (25, 25))

            # Iterating through smiles in each face (lol)
            for (sx, sy, sw, sh) in smiles:
                sm_ratio = round(sw/sx, 3)
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
                if sm_ratio > 1.8:
                    cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 255, 0), 2)

        #show frame with all rectangles drawn
        cv2.imshow('Smile Detector', img)
        k = cv2.waitKey(30) & 0xff

        # Handles entry and exit of multiple faces in and out of frame
        if len(prevface) > len(faces):
            for count,item in enumerate(prevface):
                fil = list(filter(lambda x:abs(x[0] - item[0]) < 100, faces))
                if len(fil) == 0:
                    rt[count].stop()
                    rt.pop(count)
                    for i in range(count, len(rt)):
                        rt[i].dec()
                    counter -= 1
        elif len(prevface) < len(faces):
            for i in range(len(faces) - len(prevface)):
                rt.append(RepeatingTimer(7, mood, counter))
                rt[-1].run()
                counter += 1
        prevface = faces

        # Exits if escape is pressed
        if k == 27:
            raise Exception('Pressed escape key')
except :
    print("\nbabye!\n")

# Just quits everything (as I soon will)
for i in rt:
    i.stop()
cap.release()
chooseFrom.close()
cv2.destroyAllWindows()
