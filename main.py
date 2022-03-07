import numpy as np
import streamlit as st
import os
import cv2
import subprocess

from tensorflow.keras.models import load_model



dir_path = os.path.dirname(os.path.realpath(__file__))
st.markdown("<h1 style='text-align: center; color: black;'>🤖Cheerful Health Inspector Bot🤖</h1>",
            unsafe_allow_html=True)
face_detect = cv2.CascadeClassifier(dir_path + '/haarcascade_frontalface_default.xml')
happymodel = load_model(dir_path + '/happy.h5')
maskmodel = load_model(dir_path + '/mask_model.h5')
gender_model = load_model(dir_path + '/gender_classify_middle_hiar_man.h5')

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Choose a file", type=['jpg', 'png'])
with col2:
    radio = st.radio('Mode', ['Upload', 'Live(Available when you run it on your own machine*)'])


def reduce_max_width():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


reduce_max_width()

mask_labels_dict = {0: 'no mask', 1: 'a mask'}
smile_label_dict = {1: 'smiling! =)', 0: 'not smiling.. =('}
gender_label_dict = {0: 'female', 1: 'male'}


def write( gender, mask, smile):
    global b1, b2,b3
    pt2string = "If you take off your mask, I can tell if you're smiling!" if mask == 'a mask' else f"You're **{smile}**"
    b1.header(f"Beep boop.. I'm guessing you're a **{gender}** with **{mask}** on...")
    b2.header(pt2string)
    b3.header(" \n")
    b4.header(" \n")
    b5.header(" \n")
    b6.text('\n\n\n\n\nI work best in well-lit environments! =)\nThank you for using this bot!\n-Omar')


def look_for_faces_update_text(image):
def look_for_faces_update_text(image):
    faces = face_detect.detectMultiScale(image,minNeighbors=5)
    for (x, y, w, h) in faces:
        face_img = image[y:y + h, x:x + w]
        resized = cv2.resize(face_img, (224, 224))
        resized2 = cv2.resize(face_img, (96, 96))
        resized3 = cv2.resize(face_img, (64, 64))
        normalized = resized / 255.0
        normalized2 = resized2 / 255.0
        normalized3 = resized3 / 255.0
        reshaped = np.reshape(normalized, (1, 224, 224, 3))
        reshaped2 = np.reshape(normalized2, (1, 96, 96, 3))
        reshaped3 = np.reshape(normalized3, (1, 64, 64, 3))
        reshaped = np.vstack([reshaped])
        reshaped2 = np.vstack([reshaped2])
        reshaped3 = np.vstack([reshaped3])
        result = maskmodel.predict(reshaped)
        smileresult = (happymodel.predict(reshaped3 )> 0.5).astype("int32")[0][0]
        gender_prediction = (gender_model.predict(reshaped2) > 0.5).astype("int32")

        gender_prediction = gender_prediction[0][0]
        if result[0][0] > result[0][1]:
            percent = round(result[0][0] * 100, 2)
        else:
            percent = round(result[0][1] * 100, 2)
        color_dict = {0: (0, 0, 255), 1: (0, 255, 0)}
        label = np.argmax(result, axis=1)[0]
        cv2.rectangle(image, (x, y), (x + w, y + h), color_dict[label], 2)
        cv2.rectangle(image, (x, y - 40), (x + w, y), color_dict[label], -1)
        cv2.putText(image, mask_labels_dict[label] + " " + str(percent) + "%", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (255, 255, 255), 2)
        with col2:
            write(gender_label_dict[gender_prediction], mask_labels_dict[label],
                  smile_label_dict[smileresult])
    return image


with col2:
    b1 = st.empty()
    b2 = st.empty()
    b3 = st.empty()
    b4 = st.empty()
    b5 = st.empty()
    b6 = st.empty()
if radio == 'Upload':
    cam = None
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        colored = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        with col1:
            st.image(look_for_faces_update_text(colored))

elif radio == 'Live':
    with col1:
        st.subheader('Live Feed')
        FRAMES = st.image([])
        cam = cv2.VideoCapture(0)
        while radio == 'Live':
            ret, frame = cam.read()
            colored = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            look_for_faces_update_text(colored)
            FRAMES.image(colored)
