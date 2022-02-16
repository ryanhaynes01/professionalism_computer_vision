# imports
import imutils
import cv2 as cv

face_cascade = cv.CascadeClassifier('model_data/frontal_face_detection.xml')

frame = 0

def get_video():
    camera = cv.VideoCapture(0)
    if not camera.isOpened():
        print("Camera could not be accessed!")
        exit()

    return camera

def show_video():
    camera = get_video()
    while True:

        ret, frame = camera.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if not ret:
            print("Cannot recieve frames. Exiting...")
            camera.release()
            return
        
        for (x, y, w, h) in faces:
            cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv.imshow("Facial Detection", frame)
        if cv.waitKey(1) == ord('q'):
            camera.release()
            return
        
        frame = frame


if __name__ == '__main__':
    print(cv.__version__)
    show_video()
    cv.destroyAllWindows()
    cv.waitKey(0)