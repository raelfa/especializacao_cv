import cv2
import numpy as np

cap_webcam = cv2.VideoCapture('data/carlos_greenscreen.mov')
cap_praia = cv2.VideoCapture('data/praia.mp4')


width1 = int(cap_webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(cap_webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret_webcam, frame_webcam = cap_webcam.read()
    ret_praia, frame_praia = cap_praia.read()

    if not ret_webcam or not ret_praia:
        break

    frame_praia = cv2.resize(frame_praia, (width1, height1))

    lower_green = np.array([0, 40, 0], dtype=np.uint8)
    upper_green = np.array([170, 255, 39], dtype=np.uint8)

    mask = cv2.inRange(frame_webcam, lower_green, upper_green)
    # print(mask)
    mask[0:120, 0:] = 1
    mask[120:, 0:450] = 1
    mask[120:, 750:] = 1
    # print(mask)
    mask = np.array(mask, dtype=np.uint8)

    praia_background = cv2.bitwise_and(frame_praia, frame_praia, mask=mask)

    mask_inv = np.logical_not(mask).astype(np.uint8)

    webcam_foreground = cv2.bitwise_and(
        frame_webcam, frame_webcam, mask=mask_inv)

    result = cv2.addWeighted(praia_background, 1, webcam_foreground, 1, 0)

    cv2.imshow('Resultado', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap_webcam.release()
cap_praia.release()

cv2.destroyAllWindows()
