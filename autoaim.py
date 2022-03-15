import cv2
from target import Target

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

capture = cv2.VideoCapture(0)
success, frame = capture.read()
h,w = frame.shape[:2]
target = Target(w, h)

def aim_center(img):
    w, h = img.shape
    x_center = h//2
    y_center = w//2
    
    thick_line = 1
    aim_center_size = 5
    color = (255,0,0)

    cv2.line(img, (x_center-aim_center_size, y_center), (x_center+aim_center_size, y_center), color, thick_line)
    cv2.line(img, (x_center, y_center-aim_center_size), (x_center, y_center+aim_center_size), color, thick_line)

def aim_face(img, face):
    (x, y, w, h) = face
    x_center = x+w//2
    y_center = y+h//2
    thick_line = 2 
    aim_center_size = 10
    color = (255,0,0)

    cv2.rectangle(img, (x, y), (x+w, y+h), color, thick_line)
    cv2.line(img, (x_center-aim_center_size, y_center), (x_center+aim_center_size, y_center), color, thick_line)
    cv2.line(img, (x_center, y_center-aim_center_size), (x_center, y_center+aim_center_size), color, thick_line)

def draw_target(img, target):
    dist_x_aim_max = int(target.w*.2)
    dist_y_aim_max = int(target.h*.2)
    padding_x = padding_y = 10
    color = (0,255,0) if target.found else (255,0,0)
    thick_line = 1

    if target.dist_x<0:
        padding_x*=-1
    if target.dist_y<0:
        padding_y*=-1

    beg_x = target.center_x+padding_x
    end_x = target.center_x+padding_x+dist_x_aim_max*target.dist_x//target.w
    beg_y = target.center_y+padding_y
    end_y = target.center_y+padding_y+dist_y_aim_max*target.dist_y//target.h

    cv2.line(img, (beg_x, target.center_y), (end_x, target.center_y), color, thick_line)
    cv2.line(img, (target.center_x, beg_y), (target.center_x, end_y), color, thick_line)
    
    
while True:
    success, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    

    aim_center(gray)

    for face in faces:
        aim_face(gray, face)
        target.calc(face)
    if not len(faces):
        target.lose()

    print(target)
    draw_target(gray, target)
    
    cv2.imshow("Cam", gray)

    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

capture.release()
cv2.destroyAllWindows()