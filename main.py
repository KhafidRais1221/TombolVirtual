import cv2
from cvzone.HandTrackingModule import HandDetector
import pyfirmata

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

if cap.isOpened() == False:
    print("Camera couldn't Access!!!")
    exit()

detector = HandDetector(detectionCon=0.7)

counter_R, counter_Y, counter_G = 0,0,0
R_on, Y_on, G_on = False, False, False
valRYG = [0, 0, 0]

pinR, pinY, pinG = 2, 3, 4
port = "COM3"
board = pyfirmata.Arduino(port)

while cap.isOpened():
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bboxInfo = detector.findPosition(img)

    if lmlist:
        x, y = 100, 100
        w, h = 225, 225
        X, Y = 140, 190

        fx, fy = lmlist[8][0], lmlist[8][1]
        posFinger = [fx, fy]
        #print(posFinger)
        cv2.circle(img, (fx, fy), 10, (255, 255, 0), cv2.FILLED)
        #cv2.putText(img, str(posFinger), (fx+20, fy-20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
        #cv2.line(img, (0, fy), (1280, fy), (255, 255, 0), 3)#x line
        #cv2.line(img, (fx, 720), (fx, 0), (255, 255, 0), 3) #y line

        if x < fx < x+w-95 and y < fy < y+h-95:
            counter_R += 1
            cv2.rectangle(img, (x, y), (w, h), (255, 255, 0), cv2.FILLED)
            if counter_R == 1:
                R_on = not R_on
        else:
            counter_R = 0
            if R_on :
                R_val = 1
                cv2.rectangle(img, (x, y), (w, h), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, "1", (X, Y), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
            else:
                R_val = 0
                cv2.rectangle(img, (x, y), (w, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "0", (X, Y), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 5)

        if x+250 < fx < x+w-95+250 and y < fy < y+h-95:
            counter_Y += 1
            cv2.rectangle(img, (x+250, y), (w+250, h), (255, 255, 0), cv2.FILLED)
            if counter_Y == 1:
                Y_on = not Y_on
        else:
            counter_Y = 0
            if Y_on :
                Y_val = 1
                cv2.rectangle(img, (x+250, y), (w+250, h), (0, 255, 255), cv2.FILLED)
                cv2.putText(img, "1", (X+250, Y), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
            else:
                Y_val = 0
                cv2.rectangle(img, (x+250, y), (w+250, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "0", (X+250, Y), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 255), 5)

        if x+500 < fx < x+w-95+500 and y < fy < y+h-95:
            counter_G += 1
            cv2.rectangle(img, (x+500, y), (w+500, h), (255, 255, 0), cv2.FILLED)
            if counter_G == 1:
                G_on = not G_on
        else:
            counter_G = 0
            if G_on :
                G_val = 1
                cv2.rectangle(img, (x+500, y), (w+500, h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "1", (X+500, Y), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
            else:
                G_val = 0
                cv2.rectangle(img, (x+500, y), (w+500, h), (150, 150, 150), cv2.FILLED)
                cv2.putText(img, "0", (X+500, Y), cv2.FONT_HERSHEY_PLAIN, 5, (0, 255, 0), 5)

        #valRYG[0] = R_val
        #valRYG[1] = Y_val
        #valRYG[2] = G_val
        #print(valRYG)

        board.digital[pinR].write(R_val)
        board.digital[pinY].write(Y_val)
        board.digital[pinG].write(G_val)

    cv2.imshow("image", img)
    cv2.waitKey(1)
