import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller, Key

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 550)
# img = cv2.resize(img, (680,640))

detector = HandDetector(detectionCon=0.8, maxHands=2)


class Button:
    def __init__(self, pos, text, size=None):
        if size is None:
            size = [70, 70]
        self.pos = pos
        self.text = text
        self.size = size


keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", 'Backspace'],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", 'Enter'],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", 'Space']]

buttonlist = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonlist.append(Button([80 * j + 10, 80 * i + 10], key))


def drawAll(img, butonlist):
    for button in buttonlist:
        x, y = button.pos
        w, h = button.size
        # print(button.text,' : ',(x+w,y+h))
        if button.text == 'Backspace' or button.text == 'Enter' or button.text == 'Space':
            cv2.rectangle(img, button.pos, (x + w + 140, y + h), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, button.text, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 3)
        else:
            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, button.text, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 3)
    return img


clickedtext = []
keyboard = Controller()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)  # with draw
    # hands,img = detector.findHands(img, draw=False)          # without draw
    drawAll(img, buttonlist)

    if hands:
        # hand1
        hand1 = hands[0]
        lmList1 = hand1['lmList']
        # bbox = hand1['bbox']
        # centerPostion1 = hand1['center']
        # handtype1 = hand1['type']
        length, info, image = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img)  # with draw
        # length, info = detector.findDistance(lmList1[8], lmList1[12])                 # without draw

        # hand2
        # if len(hands) == 2:
        #     hand2 = hands[1]
        #     lmList2 = hand2['lmList']

        if lmList1:
            for button in buttonlist:
                x, y = button.pos
                w, h = button.size
                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                    if button.text == 'Backspace' or button.text == 'Enter' or button.text == 'Space':
                        cv2.rectangle(img, button.pos, (x + w + 140, y + h), (255, 0, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 255, 255), 3)
                    else:
                        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 255, 255), 3)

                    if length < 40:
                        if button.text == 'Backspace' or button.text == 'Enter' or button.text == 'Space':
                            cv2.rectangle(img, button.pos, (x + w + 140, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 255, 255), 3)
                        else:
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (255, 255, 255), 3)

                        # keyboard control
                        if button.text == 'Backspace':
                            keyboard.press(Key.backspace)
                        elif button.text == 'Enter':
                            keyboard.press(Key.enter)
                        elif button.text == 'Space':
                            keyboard.press(Key.space)
                        else:
                            keyboard.press(button.text)

                        # # onscreen text control
                        # if button.text == 'Backspace':
                        #     if len(clickedtext) != 0:
                        #         clickedtext.pop()
                        # elif button.text == 'Enter':
                        #     clickedtext.append('\n')
                        # elif button.text == 'Space':
                        #     clickedtext.append(' ')
                        # else:
                        #     clickedtext.append(button.text)

                        sleep(0.2)

    # cv2.rectangle(img, (35, 345), (1000, 550), (255, 0, 0), cv2.FILLED)
    # cv2.putText(img, ''.join(clickedtext), (60, 425), cv2.FONT_HERSHEY_SIMPLEX, 2,
    #             (255, 255, 255), 3)

    cv2.imshow('image', img)
    cv2.waitKey(1)
