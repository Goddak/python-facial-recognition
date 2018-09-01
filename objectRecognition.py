import cv2
import numpy as np
import subprocess as sp

face_cascade_two = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
human_detected = False
i_have_spoken = False
phrase = "I have detected a human, should I destroy them?"
voice_reset_delay = "20"

# Select the display device
video_capture = cv2.VideoCapture(0)

# desired_height = 480
# desired_width = 640
desired_height = 720
desired_width = 1280
desired_size = False
fallback_scale_percent = 250

# Set the desired resolution (if it works)
video_capture.set(3, desired_height)
video_capture.set(4, desired_width)

# We'll use this to scale the output later if setting the size didn't work.
def rescale_frame(frame, percent=150):
  width = int(frame.shape[1] * percent/ 100)
  height = int(frame.shape[0] * percent/ 100)
  dim = (width, height)
  return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

while True:
  ret, img = video_capture.read()
  # Scale the image if it's smaller than we desired
  width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
  height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
  if (width >= desired_width) and (height >= desired_height):
    desired_size = True
  if desired_size == False:
    img = rescale_frame(img, fallback_scale_percent)

  # Convert to grey
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  # Detect faces via cascade
  faces = face_cascade_two.detectMultiScale(gray, 1.5, 10)
  # Put rectangle and text on screen for each face
  for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
    cv2.putText(img, 'Person', (x+5, y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
  if len(faces) > 0 and i_have_spoken != True:
    sp.Popen(["python3", "speak.py", phrase])
    i_have_spoken = True
  # sp.Popen(['python3', 'reset-i-have-spoken.py', voice_reset_delay])
  # sp.Popen(['python3', 'example.py', voice_reset_delay])
  # Show a preview
  cv2.imshow('img', img)
  # Allow loop exit via escape key
  k = cv2.waitKey(30) & 0xff
  if k == 27:
    break

video_capture.release()
cv2.destroyAllWindows()
print('Goddak FTW!')
