import face_recognition
import glob
from concurrent.futures import ThreadPoolExecutor
import pickle
import os
import requests
import pandas as pd

ENCODING_API_ENDPOINT = "http://172.16.28.144:8110/v1.0/cuostomer/1/user"


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
        if api_call:
            executor.submit(call_encoding_api, ([identity, database[identity]]))

        save_database_encoding(database)
        # print(identity, file, face_encoding)
    return database


def save_database_encoding(database):
    with open("encodedImageData" + '.pkl', 'wb') as f:
        pickle.dump(database, f, pickle.HIGHEST_PROTOCOL)


def call_encoding_api(name_and_encoding):
    PARAMS = {'name': name_and_encoding[0],
              'encoding': name_and_encoding[1].tolist()}
    headers = {'content-type': 'application/json'}
    r = requests.post(url=ENCODING_API_ENDPOINT, json=PARAMS, headers=headers)
    print(r.json)


def create_csv_file_for_attendance(database):
    df = pd.DataFrame.from_dict(database)
    df.to_csv("my_att.csv")
    df1 = pd.read_csv('my_att.csv')
    df1.drop(df1.index[1:192], inplace=True)
    for column in df1.columns:
        df1[column] = 0
    df1.to_csv('my_attendance.csv')


if __name__ == "__main__":
    database = prepare_database(api_call=False)
    create_csv_file_for_attendance(database)
