# imports
import imutils
import cv2 as cv

if __name__ == '__main__':
    print(cv.__version__)

    # load in a test image
    # get dimension information from NumPy array
    # display information
    image = cv.imread("bin\images\linus.jpg")
    (height, width, depth) = image.shape
    print(f'Width = {width}, Height = {height}, Depth = {depth}') 

    # display image
    cv.imshow("Linus", image)
    cv.waitKey(0)