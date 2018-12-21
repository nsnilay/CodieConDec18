# import cv2
#
# from faced import FaceDetector
# from faced.utils import annotate_image
#
# face_detector = FaceDetector()
#
# video_capture = cv2.VideoCapture(0)
# # rgb_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
#
# # Receives RGB numpy image (HxWxC) and
# # returns (x_center, y_center, width, height, prob) tuples.
# # bboxes = face_detector.predict(rgb_img)
#
# # Use this utils function to annotate the image.
# # ann_img = annotate_image(img, bboxes)
#
# # Show the image
# # cv2.imshow('image',ann_img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
# while True:
#     # Capture frame-by-frame
#     ret, frame = video_capture.read()
#
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     rgb_img = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
#
#     bboxes = face_detector.predict(rgb_img)
#
#     ann_img = annotate_image(frame, bboxes)
#
#     # faces = faceCascade.detectMultiScale(
#     #     gray,
#     #     scaleFactor=1.1,
#     #     minNeighbors=5,
#     #     minSize=(30, 30),
#     #     flags=cv2.cv2.CV_HAAR_SCALE_IMAGE
#     # )
#
#     # faces = faceCascade.detectMultiScale(gray, 2, 5)
#
#     # Draw a rectangle around the faces
#     # for (x, y, w, h) in faces:
#     #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#     #     print(x,y,w,h,frame.shape)
#     #
#     #     # roi = frame[640:1279, 360:719, :]
#     #     cv2.imwrite("frame.jpg", frame)
#     #     file = cv2.imread("frame.jpg")
#     #     temp_img = file[y:y+w, x:x+h]
#     #     cv2.imwrite("temp_file.jpg", temp_img)
#
#     # Display the resulting frame
#     cv2.imshow('Video', ann_img)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # When everything is done, release the capture
# video_capture.release()
# cv2.destroyAllWindows()

import cv2

from faced import FaceDetector
from faced.utils import annotate_image

face_detector = FaceDetector()

img = cv2.imread("frame.jpg")
rgb_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)

# Receives RGB numpy image (HxWxC) and
# returns (x_center, y_center, width, height, prob) tuples.
bboxes = face_detector.predict(rgb_img)

# Use this utils function to annotate the image.
ann_img = annotate_image(img, bboxes)

# Show the image
cv2.imshow('image',ann_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
