import serial
import threading
import numpy as np
import cv2
import pyautogui

# Module-Level-Variables:

ser = serial.Serial('/dev/tty.SDP16-DevB', 9600,
                    timeout=None, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

cap = cv2.VideoCapture(1)
c = threading.Condition()
receive = b'7'
display = b'1'


# Function of image comb and chop
def image_combining(image):

    im1 = image

    try:
         oddrow1 = im1
         chopcol = oddrow1[:, 600: 1320]

    except TypeError:
        pass

    return chopcol


# Thread A: recieve from blue tooth
class ThreadA(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global display
        global receive
        while True:
            receive = ser.read(1)
            if display != receive:
                display = receive
                print(display)
            else:
                print(display)


a = ThreadA()

a.start()

# Thread B: Decide what to display and  then display
while True:

    ret, frame = cap.read()
    print('Read Frame')

    # Our operations on the frame come here
    comb = image_combining(frame)

    # Display the resulting frame
    resized_image = cv2.resize(comb, (1440, 1080))

    window_name = 'comb'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow(window_name, resized_image)

    if display == b'1':
        pyautogui.hotkey('alt', '1')
        cv2.imshow(window_name, resized_image)

    if display == b'2':
        pyautogui.hotkey('alt', '2')
        cv2.imshow(window_name, resized_image)

    if display == b'3':
        pyautogui.hotkey('alt', '3')
        cv2.imshow(window_name, resized_image)

    if display == b'4':
        pyautogui.hotkey('alt', '4')
        cv2.imshow(window_name, resized_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
a.join()



