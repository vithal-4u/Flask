from flask import Flask, render_template, Response
import cv2
import numpy as np
import face_recognition
import os
import shutil

app = Flask(__name__)

# Directory paths
input_folder = "/Users/ashokkumar.k/My_Learnings/Pictures/Input"
output_folder = "/Users/ashokkumar.k/My_Learnings/Pictures/Output"
unknown_folder = os.path.join(output_folder, "Unknown")

# Ensure the output and unknown directories exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(unknown_folder, exist_ok=True)

# Load known face encodings and their names
known_face_encodings = []
known_face_names = []

def load_known_faces(folder):
    for filename in os.listdir(folder):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(folder, filename)
            image = face_recognition.load_image_file(image_path)
            print(image_path)
            #encoding = face_recognition.face_encodings(image)[0]
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                encoding = face_encodings[0]
                known_face_encodings.append(encoding)
                # Assuming the filename without extension is the name of the person
                known_face_names.append(os.path.splitext(filename)[0])
            else:
                print(f"No faces found in {image_path}")

    print("<===== Face Loading completed =====>")


# Function to process and move images
def process_images():
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(input_folder, filename)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if not face_encodings:
                # Move to unknown folder if no faces are found
                shutil.move(image_path, os.path.join(unknown_folder, filename))
                continue
            
            matched = False
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    person_folder = os.path.join(output_folder, name)
                    os.makedirs(person_folder, exist_ok=True)
                    shutil.move(image_path, os.path.join(person_folder, filename))
                    matched = True
                    break
            
            if not matched:
                shutil.move(image_path, os.path.join(unknown_folder, filename))



if __name__ == '__main__':
    # Load known faces from a folder
    load_known_faces("/Users/ashokkumar.k/My_Learnings/Pictures/Train_image")
    process_images()
