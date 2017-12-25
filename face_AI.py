# Project for adding Christmas Cap based on AI Technology
import cv2
import random

# OpenCV
face_patterns = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
sample_image = cv2.imread('img/facetest.jpg')
faces = face_patterns.detectMultiScale(sample_image,
                                       scaleFactor=1.1,
                                       minNeighbors=8,
                                       minSize=(50, 50))
# Christmas Cap
hats = []
for i in range(4):
    hats.append(cv2.imread('img/hat%d.png' % i, -1))

for face in faces:
    # Random hat
    hat = random.choice(hats)
    # Regulate scale
    scale = face[3] / hat.shape[0] * 1.25
    hat = cv2.resize(hat, (0, 0), fx=scale, fy=scale)
    # Adjust position
    x_offset = int(face[0] + face[2] / 2 - hat.shape[1] / 2)
    y_offset = int(face[1] - hat.shape[0] / 2)
    # Compute position
    x1, x2 = max(x_offset, 0), min(x_offset + hat.shape[1], sample_image.shape[1])
    y1, y2 = max(y_offset, 0), min(y_offset + hat.shape[0], sample_image.shape[0])
    hat_x1 = max(0, -x_offset)
    hat_x2 = hat_x1 + x2 - x1
    hat_y1 = max(0, -y_offset)
    hat_y2 = hat_y1 + y2 - y1
    # Process for transparent part
    alpha_h = hat[hat_y1:hat_y2, hat_x1:hat_x2, 3] / 255
    alpha = 1 - alpha_h
    # Combine Channels
    for c in range(0, 3):
        sample_image[y1:y2, x1:x2, c] = (alpha_h * hat[hat_y1:hat_y2, hat_x1:hat_x2, c] + alpha * sample_image[y1:y2, x1:x2, c])

# Save Result
cv2.imwrite('faces_result.png', sample_image)
