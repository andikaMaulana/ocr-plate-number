import cv2

capture = cv2.VideoCapture('rtsp://119.2.52.175:9997/s0')

def toGray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def toBin(img,tre):
    _,img=cv2.threshold(img, tre, 255, cv2.THRESH_BINARY_INV)
    return img


while True:
    has_frame, frame = capture.read()
    if not has_frame:
        print('Reached the end of the video')
        break
    frame = toGray(frame)
    frame = toBin(frame,90)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(50)
    if key == 27:
        print('Pressed Esc')
        break

cv2.destroyAllWindows()