import cv2
img = cv2.imread("image.jpeg")  # Replace with an actual image path
cv2.imshow("Test Window", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
