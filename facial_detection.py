# imports
import cv2 as cv

class FacialDetection():
    def __init__(self):
        # load in training data from intel
        self.face_cascade = cv.CascadeClassifier('model_data/frontal_face_detection.xml')
        self.public_frame = None

    def get_video(self):
        # initilaize the camera so opencv can use it
        camera = cv.VideoCapture(0)

        # if the camera can't be opened, exit and return error
        if not camera.isOpened():
            print("Camera could not be accessed!")
            exit()

        # otherwise return the camera object
        return camera

    def show_video(self):
        # get camera object
        camera = self.get_video()
        while True:
            # get the current frame from the camera
            ret, frame = camera.read()
            # grayscale the frame for the training data to detect a face
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            # if the stream of frames has stopped coming in, something
            # has happened, either camera has been unplugged, etc
            if not ret:
                print("Cannot recieve frames. Exiting...")
                camera.release()
                return
            
            # from the faces detected in the frame, draw a rectangle around it
            for (x, y, w, h) in faces:
                cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # show the current frame
            #cv.imshow("Facial Detection", frame)
            # if the q key has been pressed, break out and release the camera
            if cv.waitKey(1) == ord('q'):
                camera.release()
                return

            self.public_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

if __name__ == '__main__':
    print(cv.__version__)
    #show_video()
    cv.destroyAllWindows()
    cv.waitKey(0)