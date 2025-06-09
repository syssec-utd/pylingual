import cv2
import mediapipe as mp
import math

class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = (int(lm.x * w), int(lm.y * h), int(lm.z * w))
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)
                xmin, xmax = (min(xList), max(xList))
                ymin, ymax = (min(yList), max(yList))
                boxW, boxH = (xmax - xmin, ymax - ymin)
                bbox = (xmin, ymin, boxW, boxH)
                cx, cy = (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)
                myHand['lmList'] = mylmList
                myHand['bbox'] = bbox
                myHand['center'] = (cx, cy)
                if flipType:
                    if handType.classification[0].label == 'Right':
                        myHand['type'] = 'Left'
                    else:
                        myHand['type'] = 'Right'
                else:
                    myHand['type'] = handType.classification[0].label
                allHands.append(myHand)
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20), (255, 0, 255), 2)
                    cv2.putText(img, myHand['type'], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        if draw:
            return (allHands, img)
        else:
            return allHands

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        myHandType = myHand['type']
        myLmList = myHand['lmList']
        if self.results.multi_hand_landmarks:
            fingers = []
            if myHandType == 'Right':
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            elif myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def findDistance(self, p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """
        x1, y1 = p1
        x2, y2 = p2
        cx, cy = ((x1 + x2) // 2, (y1 + y2) // 2)
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return (length, info, img)
        else:
            return (length, info)

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=2)
    while True:
        success, img = cap.read()
        hands, img = detector.findHands(img)
        if hands:
            hand1 = hands[0]
            lmList1 = hand1['lmList']
            bbox1 = hand1['bbox']
            centerPoint1 = hand1['center']
            handType1 = hand1['type']
            fingers1 = detector.fingersUp(hand1)
            if len(hands) == 2:
                hand2 = hands[1]
                lmList2 = hand2['lmList']
                bbox2 = hand2['bbox']
                centerPoint2 = hand2['center']
                handType2 = hand2['type']
                fingers2 = detector.fingersUp(hand2)
                length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img)
        cv2.imshow('Image', img)
        cv2.waitKey(1)
if __name__ == '__main__':
    main()