import cv2

file = cv2.imread("frame.jpg")
print(file.shape)
crop_file = file[288:288+384, 563:563+384, :]
cv2.imshow("img", crop_file)
k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
elif k == ord('s'): # wait for 's' key to save and exit
    cv2.imwrite('messigray.png',file)
    cv2.destroyAllWindows()