#importing necessary libraries
import cv2 as cv
import time
import geocoder
import os

#reading label name from obj.names file
class_name = []
with open(os.path.join("project_files",'obj.names'), 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

#importing model weights and config file
#defining the model parameters
net1 = cv.dnn.readNet('project_files/yolov4_tiny.weights', 'project_files/yolov4_tiny.cfg')
net1.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
net1.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA_FP16)
model1 = cv.dnn_DetectionModel(net1)
model1.setInputParams(size=(640, 480), scale=1/255, swapRB=True)

#defining the video source (0 for camera or file name for video)
cap = cv.VideoCapture(0) # 0 for webcam
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

#defining parameters for result saving and get coordinates
#defining initial values for some parameters in the script
g = geocoder.ip('me')
Conf_threshold = 0.5
NMS_threshold = 0.4
frame_counter = 0

#detection loop
while True:
    starting_time = time.time()
    ret, frame = cap.read()
    frame_counter += 1
    if ret == False:
        break
    #analysis the stream with detection model
    classes, scores, boxes = model1.detect(frame, Conf_threshold, NMS_threshold)
    for (classid, score, box) in zip(classes, scores, boxes):
        label = "pothole"
        x, y, w, h = box
        recarea = w*h
        area = frame.shape[0]*frame.shape[1]
        #drawing detection boxes on frame for detected potholes and saving coordinates txt and photo
        if(len(scores)!=0 and scores[0]>=0.7):
            if((recarea/area)<=0.1 and box[1]<600):
                cv.rectangle(frame, (x, y), (x + w, y + h), (0,255,0), 1)
                cv.putText(frame, "%" + str(round(scores[0]*100,2)) + " " + label, (box[0], box[1]-10),cv.FONT_HERSHEY_COMPLEX, 0.5, (255,0,0), 1)
                # save image and coordinates
                cv.imwrite(os.path.join("pothole_coordinates",'pothole'+str(time.time())+'.jpg'), frame)
                with open(os.path.join("pothole_coordinates",'pothole'+str(time.time())+'.txt'), 'w') as f:
                    f.write(str(g.latlng))
    #writing fps on frame
    endingTime = time.time() - starting_time
    fps = frame_counter/endingTime
    cv.putText(frame, f'FPS: {fps:.2f}', (20, 50),
               cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
    #showing and saving result
    cv.imshow('frame', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        break
    
#end
cap.release()
cv.destroyAllWindows()
