import cv2
import sys

from keras import backend as K

K.set_image_data_format('channels_first')

import inception_blocks_v2
import fr_utils

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)
FRmodel = inception_blocks_v2.faceRecoModel(input_shape=(3, 96, 96))

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # faces = faceCascade.detectMultiScale(
    #     gray,
    #     scaleFactor=1.1,
    #     minNeighbors=5,
    #     minSize=(30, 30),
    #     flags=cv2.cv2.CV_HAAR_SCALE_IMAGE
    # )

    faces = faceCascade.detectMultiScale(gray, 1.3, 4)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(x, y, w, h, frame.shape)

        # roi = frame[640:1279, 360:719, :]
        cv2.imwrite("frame.jpg", frame)
        file = cv2.imread("frame.jpg")
        temp_img = file[y-50:y + w+50, x-50:x + h+50]
        cv2.imwrite("temp_file.jpg", temp_img)

        encoding = fr_utils.img_path_to_encoding("temp_file.jpg", FRmodel)
        print(encoding)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
