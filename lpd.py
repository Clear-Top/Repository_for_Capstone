import argparse
from flask import Flask, render_template, request
import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
UPLOAD_FOLDER = '/static/uploads/'
confThreshold = 0.4  #Confidence threshold
nmsThreshold = 0.3  #Non-maximum suppression threshold

inpWidth = 416  #608     #Width of network's input image
inpHeight = 416 #608     #Height of network's input image
   
classesFile = "DL/model/lpd/classes.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.

modelConfiguration = "DL/model/lpd/yolov4-ANPR.cfg"
modelWeights = "DL/model/lpd/yolov4-ANPR.weights"

net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
def lpd(file):
    """
    confThreshold = 0.4  #Confidence threshold
    nmsThreshold = 0.3  #Non-maximum suppression threshold

    inpWidth = 416  #608     #Width of network's input image
    inpHeight = 416 #608     #Height of network's input image
   
    classesFile = "DL/model/lpd/classes.names"
    classes = None
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    # Give the configuration and weight files for the model and load the network using them.

    modelConfiguration = "DL/model/lpd/yolov4-ANPR.cfg"
    modelWeights = "DL/model/lpd/yolov4-ANPR.weights"

    net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    """
    # Get the names of the output layers
    def getOutputsNames(net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Draw the predicted bounding box
    def drawPred(classId, conf, left, top, right, bottom):
        # Draw a bounding box.
        #
        label = '%.2f' % conf

        if classes:
            assert(classId < len(classes))
            label = '%s:%s' % (classes[classId], label)
        
        crop_img = frame[top:bottom, left:right]
        #cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
        return crop_img
    # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        for out in outs:
            #print("out.shape : ", out.shape)
            for detection in out:
                #if detection[4]>0.001:
                scores = detection[5:]
                classId = np.argmax(scores)
                #if scores[classId]>confThreshold:
                confidence = scores[classId]
                """
                if detection[4]>confThreshold:
                    print(detection[4], " - ", scores[classId], " - th : ", confThreshold)
                    print(detection)
                """
                if confidence > confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            if (classIds[i] == 1):
                License_list.append(drawPred(classIds[i], confidences[i], left, top, left + width, top + height))
            else:
                Car_list.append(drawPred(classIds[i], confidences[i], left, top, left + width, top + height))





    # Process inputs
    f=os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename)

    if (f):
        # Open the image file
        if not os.path.isfile(f):
            print("Input image file ", f, " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(f)
        #print(cap)
        outputFile = f.rsplit(".")[0]+'.jpg'
        out_image=file.filename.rsplit(".")[0]+'.jpg'

    License_list= []
    Car_list=[]
    while cv.waitKey(1) < 0:

        # get frame from the video
        hasFrame, frame = cap.read()

        # Stop the program if reached end of video
        if not hasFrame:
            print("Done processing !!!")
            print("Output file is stored as ", outputFile)
            #cv.waitKey(3000)
            break

        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))

        # Remove the bounding boxes with low confidence
        postprocess(frame, outs)

        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

        # Write the frame with the detection boxes
        if (f):
            cv.imwrite(outputFile, frame.astype(np.uint8))
    return out_image,License_list,Car_list
