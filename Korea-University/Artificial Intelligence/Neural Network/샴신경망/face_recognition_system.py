from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import tensorflow as tf
import utils

# Load pre-trained Siamese
model = tf.keras.models.load_model('샴신경망/siamese_nn.h5', custom_objects={'contrastive_loss': utils.contrastive_loss, 'euclidean_distance': utils.euclidean_distance})

# Load the test image
true_img = cv2.imread('샴신경망/test_img.png', cv2.IMREAD_GRAYSCALE)
true_img = true_img.astype('float32') / 255
true_img = cv2.resize(true_img, (92, 112))
true_img = true_img.reshape(1, true_img.shape[0], true_img.shape[1], 1)

# Get name
name = input("What is your name? ")
# video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_roi = gray_frame[y:y+h, x:x+w]

        face_img = cv2.resize(face_roi, (92, 112))
        face_img = face_img.astype('float32') / 255
        face_img = face_img.reshape(1, face_img.shape[0], face_img.shape[1], 1)

        similarity_score = 1 - model.predict([true_img, face_img])[0][0]

        if similarity_score >= 0.3:
            identity = name
        else:
            identity = "Unknown"

        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        font = ImageFont.truetype("샴신경망/NanumFontSetup_TTF_GOTHIC/NanumGothicBold.ttf", 60) 
        draw.rectangle([x, y, x+w, y+h], outline="green", width=2)

        draw.text((x, y-30), identity, fill="green", font=font)

        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
