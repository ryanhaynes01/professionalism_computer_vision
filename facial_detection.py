# imports
import cv2 as cv
import face_recognition
import numpy as np
import time

class FacialDetection():
    def __init__(self):
        # load in training data from intel
        self.face_cascade = cv.CascadeClassifier('model_data/frontal_face_detection.xml')
        self.public_frame = None
        self.init_time = None
        self.timeout = 10
        # Initialize some variables
        self.temp_location = ""
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.is_found = False
        self.process_this_frame = True
        self.known_face_names = [
            ""
        ]

    def load_encodings(self):
        # Load a sample picture and learn how to recognize it.
        person = face_recognition.load_image_file(self.temp_location)
        person_face_encoding = face_recognition.face_encodings(person)[0]

        # Create arrays of known face encodings and their names
        self.known_face_encodings = [
            person_face_encoding
        ]

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
            # grab a single frame of video
            ret, frame = camera.read()

            # resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # only process every other frame of video to save time
            if self.process_this_frame:
                # find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # see if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]

                    self.face_names.append(name)

                    if self.known_face_names[0] in self.face_names:
                        # we found the person, using is_found to indicate
                        # to the rest of the program
                        self.is_found = True
                        return

            self.process_this_frame = not self.process_this_frame


            # display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # draw a box around the face
                cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # draw a label with a name below the face
                cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
                font = cv.FONT_HERSHEY_DUPLEX
                cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            
            # track if the program needs to timeout
            if self.init_time is not None:
                if (self.init_time - time.time() <= -self.timeout):
                    return

            self.public_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

if __name__ == '__main__':
    print(cv.__version__)
    #fd = FacialDetection()
    #fd.show_video()
    cv.destroyAllWindows()
    cv.waitKey(0)