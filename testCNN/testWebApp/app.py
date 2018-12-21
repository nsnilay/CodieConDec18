import cv2
from flask import Flask, render_template, Response, jsonify, request

import face_recognition
from concurrent.futures import ThreadPoolExecutor
import pickle

app = Flask(__name__)

video_camera = None
global_frame = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/record_status', methods=['POST'])
def record_status():
    # global video_camera
    # if video_camera == None:
    #     video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']

    if status == "true":
        # tempFun(load_database_encoding())
        return jsonify(result="started")
    else:
        # video_camera.stop_record()
        return jsonify(result="stopped")


def tempFun(database):  # Get a reference to webcam #0 (the default one)
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

                executor.submit(recognisePersonApi, (face_encoding))
                matches = face_recognition.compare_faces(list(database.values()), face_encoding, tolerance=0.4)
                name = "Unknown"
                print(matches)

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = (list(database.keys())[first_match_index])

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
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


def load_database_encoding():
    with open("encodedImageData" + '.pkl', 'rb') as f:
        return pickle.load(f)


# def video_stream():
#     global video_camera
#     global global_frame
#
#     if video_camera == None:
#         video_camera = VideoCamera()
#
#     while True:
#         frame = video_camera.get_frame()
#
#         if frame != None:
#             global_frame = frame
#             yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         else:
#             yield (b'--frame\r\n'
#                             b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
#
# @app.route('/video_viewer')
# def video_viewer():
#     return Response(video_stream(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=False, debug=True)
