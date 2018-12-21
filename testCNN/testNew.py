import face_recognition
import cv2
import pickle
import glob
from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd
import os
from time import *
import calendar
import datetime
import numpy as np

RECOGNISE_API_ENDPOINT = "http://172.16.28.144:8110/v1.0/customer/1/auth/list"

name_and_timestamp = {}




def tempFun(df,fp, database, api_call = False):  # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    executor = ThreadPoolExecutor()

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                ## add an http request here

                if api_call:
                    executor.submit(recognisePersonApi, (face_encoding))
                matches,face_value = face_recognition.compare_faces(list(database.values()), face_encoding,tolerance=0.4)
                arr = (matches*(10-face_value))
                ind = np.argmax(arr)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if arr[ind]!=0:
                    #first_match_index = matches.index(True)
                    # first_match_index = face_value[max(face_value)]
                    name = list(database.keys())[ind]

                face_names.append(name)
                print(face_names)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 0, 0), 1)

            if (name in df.columns):
                print(df[name])
                callAttendanceRegister(df,fp, name)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def callAttendanceRegister(df,fp,  name):
    df[name] = True
    df.to_csv('my_marked_attendance.csv')
    displayNameinTerminal(name,fp)
    print(df[name])


def displayNameinTerminal(name,fp):
    if name not in name_and_timestamp:
        name_and_timestamp[name] = calendar.timegm(gmtime())
        fp.write(name + " entered at " + strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
        fp.flush()

    elif (calendar.timegm(gmtime()) - name_and_timestamp[name] > 3):
        name_and_timestamp[name] = calendar.timegm(gmtime())
        fp.write(name + " entered at " + strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
        fp.flush()


def recognisePersonApi(face_encoding):
    PARAMS = {'encoding':face_encoding.tolist()}
    headers = {'content-type': 'application/json'}
    r = requests.post(url=RECOGNISE_API_ENDPOINT, json=PARAMS, headers=headers)
    print(r.json)

    # matches = face_recognition.compare_faces(database_list, face_encoding, tolerance=0.4)
    # name = "Unknown"
    # print(matches)
    #
    # # If a match was found in known_face_encodings, just use the first one.
    # if True in matches:
    #     first_match_index = matches.index(True)
    #     name = (list(database.keys())[first_match_index])
    #
    # face_names.append(name)

def load_database_encoding():
    with open("encodedImageData" + '.pkl', 'rb') as f:
        return pickle.load(f)

def prepare_database(api_call=False):
    database = {}
    executor = ThreadPoolExecutor()
    # load all the images of individuals to recognize into the database
    for file in glob.glob("images/*"):
        identity = os.path.splitext(os.path.basename(file))[0]
        image = face_recognition.load_image_file("/Users/nilayshrivastava/PycharmProjects/CodieConDec18/testCNN/images/"
                                                 + identity + ".jpg")
        face_encoding = face_recognition.face_encodings(image)[0]
        database[identity] = face_encoding

        # # call encoding api with name and encoding as params
        # if api_call:
        #     executor.submit(call_encoding_api, ([identity, database[identity]]))

        save_database_encoding(database)
        # print(identity, file, face_encoding)
    return database

def modified_prepare_database():
    database = load_database_encoding()
    for file in glob.glob("images/newImages/*"):
        identity = os.path.splitext(os.path.basename(file))[0]
        image = face_recognition.load_image_file("/Users/nilayshrivastava/PycharmProjects/CodieConDec18/testCNN/images/newImages/"
                                                 + identity + ".jpg")
        face_encoding = face_recognition.face_encodings(image)[0]
        database[identity] = face_encoding

        # # call encoding api with name and encoding as params
        # if api_call:
        #     executor.submit(call_encoding_api, ([identity, database[identity]]))

        save_database_encoding(database)
        # print(identity, file, face_encoding)
    return database

def save_database_encoding(database):
    with open("encodedImageData" + '.pkl', 'wb') as f:
        pickle.dump(database, f, pickle.HIGHEST_PROTOCOL)

def create_csv_file_for_attendance(database):
    df = pd.DataFrame.from_dict(database)
    df.to_csv("my_att.csv")
    df1 = pd.read_csv('my_att.csv')
    df1.drop(df1.index[1:192], inplace=True)
    for column in df1.columns:
        df1[column] = 0
    df1.to_csv('my_attendance.csv')


if __name__ == "__main__":
    database = modified_prepare_database()
    create_csv_file_for_attendance(database)
    # database = load_database_encoding()
    df = pd.read_csv('my_attendance.csv')
    fp = open('time-sheet.log','a')
    tempFun(df,fp, database, api_call=True)
