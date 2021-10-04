# imports
import imutils
import cv2 as cv

print(cv.__version__)

# load in a test image
# get dimension information from NumPy array
# display information
image = cv.imread("professionalism_computer_vision/bin/images/linus.jpg")
(height, width, depth) = image.shape
print(f'Width = {width}, Height = {height}, Depth = {depth}') 

# display image
cv.imshow("Linus", image)
cv.waitKey(0)