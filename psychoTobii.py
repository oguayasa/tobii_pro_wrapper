#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Psychopy supported Tobii controller for the new Pro SDK

# Authors: Olivia Guayasamin
# Date: 7/1/2017
        
# Requirements: Python 2.7 32 Bit (SDK required)
# Tobii Pro SDK 1.0 or 1.1 for Python 
# All dependencies for Psychopy and Psychopy.iohub 

# Summary: Currently provides all functionality for running a FULL CALIBRATION 
# ROUTINE for 5 and 9 point calibrations, and converting between Tobii
# Trackbox, Tobii ADA, and Psychopy coordinate systems. 

# This code also contains functionality for finding/calibrating the 
# experimental monitor, connecting to keyboard/mouse devices, selecting and 
# connecting to a tobii device, getting tobii device parameters, and getting 
# real time gaze and eye position data from the tobii tracker. 

# Notes: This code is currently designed for working with a tobii eyetracker 
# installed on the same device as the one for running experiments (laptop set-
# up with a single connected eyetracker, no external monitors, and no tobii 
# external processors). It should be straightforward to adapt to other 
# computer/monitor set-ups, but adaptation is required. Created on Windows OS.

# Please contact for questions. This will be updated as more functionality is
# added. 

# -----Initializing Steps-----
# import libraries
from win32api import GetSystemMetrics
import psychopy
from psychopy import visual, core
from psychopy.iohub import launchHubServer
import numpy as np
from scipy.spatial import distance
import tobii_research as tobii
import os
import random
import collections


# ----- Start psychopy ioHub processes for monitoring devices -----
# start io hub process and create object to control process and devices
io = launchHubServer()

# create keyboard and mouse devices
keyboard = io.devices.keyboard
mouse = io.devices.mouse
# Hide the mouse cursor
mouse.setSystemCursorVisibility(False)

# check that devices are connected
# keyboard
if io.getDevice('keyboard') is None:
    print ("Keyboard is not connected")
else: 
    print("Keyboard is connected")

# mouse
if io.getDevice('mouse') is None:
    print ("Mouse is not connected")
else: 
    print("Mouse is connected")

# make sure they are not reporting until called to do so
keyboard.reporting = False
mouse.reporting = False


# -----Define and calibrate experimental monitor-----
# example for using eyetracker installed on experimental device
myMon = psychopy.monitors.Monitor('TrackingMonitor')  # calibration object 
myMon.setSizePix((GetSystemMetrics(0), GetSystemMetrics(1)))  # screen size in pixels
myMon.saveMon()  # save monitor calibration


# -----Find and connect to eyetracker-----
# example for a single eyetracker
# find eyetrackers
allEyetrackers = tobii.find_all_eyetrackers()

# get information about available eyetrackers
for eyetracker in allEyetrackers:
    address = eyetracker.address
    print("Address: " + eyetracker.address)
    print("Model: " + eyetracker.model)
    print("Name (It's OK if this is empty): " + eyetracker.device_name)
    print("Serial number: " + eyetracker.serial_number)

# create eyetracker object
myTracker = tobii.EyeTracker(address)

# check to see that eyetracker is connected
if myTracker is None:
    print("Eyetracker is not connected")
else:
    print("Eyetracker is connected")

# get active display area information in mm
displayArea = myTracker.get_display_area()
print ("Getting display area from tracker with serial number {0}:"  \
       .format(myTracker.serial_number))
                                                         
print "Height: {0}".format(displayArea.height)
print "Width: {0}".format(displayArea.width)

# get track box information in mm
trackBox = myTracker.get_track_box()
print ("Getting trackbox dimensions from {0} with corners:" \
       .format(myTracker.serial_number))
print "Front Lower Left: {0}".format(trackBox.front_lower_left)
print "Front Lower Right: {0}".format(trackBox.front_lower_right)
print "Front Upper Left: {0}".format(trackBox.front_upper_left)
print "Front Upper Right: {0}".format(trackBox.front_upper_right)
   

# -----Define Global Variables and Functions -----
# create global variables
globalGazeData = {}
globalTracking = True

# function for broadcasting real time gaze data
def gazeDataCallback(startGazeData):
    global globalGazeData  # use global variable in function
    globalGazeData = startGazeData
    
    
# function for subscribing to real time gaze data from eyetracker
def startGazeData(eyeTracker):
    global globalGazeData
    print "Subscribing to eyetracker"
    eyeTracker.subscribe_to(tobii.EYETRACKER_GAZE_DATA, gazeDataCallback, 
                            as_dictionary = True)
    
    
# function for unsubscring from gaze data
def stopGazeData(eyeTracker):
    global globalGazeData
    print "Unsubscribing from eyetracker"
    eyeTracker.unsubscribe_from(tobii.EYETRACKER_GAZE_DATA, gazeDataCallback)
    
    
# function for converting positions from trackbox coordinate system (cm) to 
# normalized active display area coordinates
def tb2ADAC(x, y):
    # get xy coordinates of one corner from display area, and trackbox
    # (use front face of trackbox)
    tbLowLeft = (trackBox.front_lower_left[0], trackBox.front_lower_left[1])
    adaLowLeft = ((displayArea.width / -2), (displayArea.height / -2))
    # create ratios for x and y coordinates
    yRatio = tbLowLeft[1]/adaLowLeft[1]
    xRatio = tbLowLeft[0]/adaLowLeft[0]
    # convert and return coordinates
    adaNorm = (x * xRatio, y * yRatio)
    return adaNorm
    

# function for converting normalized coordinates to normalized coordinates based
# on the psychopy window
def tb2PsychoNorm(x, y):
    # convert track box coordinates to adac coordinates
    adacCoors = tb2ADAC(x, y)
    # shift adac positions to psychopy positions
    centerScale = tb2ADAC(1, 1)
    centerShift = ((centerScale[0] / 2), (centerScale[1] / 2))
    psychoNorm = (adacCoors[0] - centerShift[0], adacCoors[1] - centerShift[1])
    # return coordinates as normalized psychoWin
    return psychoNorm
    

# function for converting from tobiis active display coordinate system in
# normalized coordinates where (0,0) is the upper left corner, to psychopy 
# window coordinates in pix, where (0,0) is at the center of psychopy window.
def norm2PsychoPix(convertPoint):
    x = convertPoint[0]
    y = convertPoint[1]
    monHW = [GetSystemMetrics(0), GetSystemMetrics(1)]
    wShift = monHW[0] / 2
    hShift = monHW[1] / 2
    # for all points convert so accurate placed in psychopy window
    psychoPix = (((x * monHW[0]) - wShift), ((y * monHW[1]) - hShift) * -1)
    return psychoPix


# function for converting from tobiis active display coordinate system in 
# normalized coordinates where (0,0) is the upper left corner, to monitor 
# coordinates in pix, where (0,0) is the upper left corner
def norm2MonPix(x, y):
    # convert so point of gaze on monitor is accurate
    monPix = (x * GetSystemMetrics(0), y * GetSystemMetrics(1))                                
    return monPix


# function for collecting gaze coordinates in tobiis active display coordinate 
# system. currently written to return the average (x, y) position of both eyes,
# but can be easily rewritten to return data from one or both eyes 
def getGazePosition():
    global globalTracking
    
    # while tracking
    while globalTracking:
        # access gaze data dictionary to get gaze position tuples
        lGazeXYZ = globalGazeData['left_gaze_point_on_display_area']
        rGazeXYZ = globalGazeData['right_gaze_point_on_display_area']       
        # get 2D gaze positions for left and right eye
        xs = (lGazeXYZ[0], rGazeXYZ[0])
        ys = (lGazeXYZ[1], rGazeXYZ[1])   
        
         # if all of the axes have data from at least one eye
        if not (np.isnan(xs)).all() or not (np.isnan(ys)).all():
            # take x and y averages
            meanX, meanY = np.nanmean(xs), np.nanmean(ys)
        else:
            # or if no data, hide points
            meanX, meanY = GetSystemMetrics(0), GetSystemMetrics(1)
                                                                                     
        return meanX, meanY


# function for finding the 3d position of subject's eyes, where the x and y 
# dimensions are relative to the size of the "tobii track box", and the z 
# dimensions represents eye distance in cm from the eyetracker
def findEyePositions():
    global globalTracking
    
    # while tracking
    while globalTracking:     
        # access gaze data dictionary to get eye position tuples, in user coordinate
        # system
        lOriginXYZ = globalGazeData['left_gaze_origin_in_user_coordinate_system']  
        rOriginXYZ = globalGazeData['right_gaze_origin_in_user_coordinate_system'] 
        # in trackbox coordinate system
        lTbXYZ = globalGazeData['left_gaze_origin_in_trackbox_coordinate_system']
        rTbXYZ = globalGazeData['right_gaze_origin_in_trackbox_coordinate_system']
        # create arrays with positions of both eyes on x, y, and z axes in ucs
        xs = (lOriginXYZ[0],rOriginXYZ[0])
        ys = (lOriginXYZ[1],rOriginXYZ[1])
        zs = (lOriginXYZ[2],rOriginXYZ[2])
        
        # if all of the axes have data from at least one eye
        if not (np.isnan(xs)).all() or not (np.isnan(ys)).all() or not (np.isnan(zs)).all():     
            # update the distance if the values are reasonable 
            trackerOrigin = (0, 0, 0)
            meanX, meanY, meanZ = np.nanmean(xs), np.nanmean(ys), np.nanmean(zs)
            # calculate euclidean distance in cm
            avgEyeDist = (distance.euclidean((meanX/ 10, meanY/ 10,  
                                          meanZ/ 10), trackerOrigin))
            
            # update the left eye positions if the values are reasonable
            # scale left eye position so that it fits in track box
            leftEyePos = (tb2PsychoNorm(lTbXYZ[0], lTbXYZ[1])[0] * 1.7,  # separate eyes slighty
                          tb2PsychoNorm(lTbXYZ[0], lTbXYZ[1])[1])
            if (np.isnan(leftEyePos)).any():  # otherwise hide
                leftEyePos = [0.99, 0.99] # by drawing in the corner
                
            # update the right eye positions if the values are reasonable
            # scale right eye position so that it fits in track box
            rightEyePos = (tb2PsychoNorm(rTbXYZ[0], rTbXYZ[1])[0] * 1.7, 
                           tb2PsychoNorm(rTbXYZ[0], rTbXYZ[1])[1])
            if (np.isnan(rightEyePos)).any():
                rightEyePos = [0.99, 0.99]
            return leftEyePos, rightEyePos, avgEyeDist
        
        else:  # if any of the axes have no data from both eyes          
            # update position to null
            leftEyePos = [0.99, 0.99]  # put in off window position
            rightEyePos = [0.99, 0.99]
            avgEyeDist = 0        
            return leftEyePos, rightEyePos, avgEyeDist
         

# function for drawing representation of the eyes 
def drawEyePositions(curWin, eyeTracker):
    global globalTracking
    
    # Set default colors
    correctColor = [-1.0, 1.0, -1.0]   
    mediumColor = [1.0, 1.0, 0.0]
    wrongColor = [1.0, -1.0, -1.0]
    
    # rectangle for viewing eyes
    rectScale = tb2ADAC(1, 1)
    eyeArea = visual.Rect(curWin,
                          fillColor = [0.0, 0.0, 0.0],
                          lineColor = [0.0, 0.0, 0.0],
                          pos = [0.0, 0.0],
                          units = 'norm', 
                          lineWidth = 3,
                          width = rectScale[0],
                          height = rectScale[1])
     # Make stimuli for the left and right eye
    leftStim = visual.Circle(curWin, 
                             fillColor = eyeArea.fillColor,
                             units = 'norm', 
                             radius = 0.07)
    rightStim = visual.Circle(curWin,
                              fillColor = eyeArea.fillColor,
                              units = 'norm', 
                              radius = 0.07)
    # Make a dummy message
    findmsg = visual.TextStim(curWin,
                              text = " ", 
                              color = [1.0, 1.0, 1.0],
                              units = 'norm',
                              pos = [0.0, -0.65],
                              height = 0.07)

    # turn keyboard recording on
    keyboard.reporting = True
    
    # while tracking 
    while globalTracking:         
        # find and update eye positions
        leftStim.pos, rightStim.pos, eyeDist = findEyePositions()
        
            # change color depending on distance
        if eyeDist >= 55 and eyeDist <= 75:
            # correct distance
            leftStim.fillColor, leftStim.lineColor = correctColor, correctColor
            rightStim.fillColor, rightStim.lineColor = correctColor, correctColor
        elif eyeDist <= 54 and eyeDist >= 45 or eyeDist >= 76 and eyeDist <= 85:
            leftStim.fillColor, leftStim.lineColor = mediumColor, mediumColor
            rightStim.fillColor, rightStim.lineColor = mediumColor, mediumColor
        else:
            # not really correct
            leftStim.fillColor, leftStim.lineColor = wrongColor, wrongColor
            rightStim.fillColor, rightStim.lineColor = wrongColor, wrongColor
            
        # if left eye is not found, don't display eye    
        if leftStim.pos[0] == 0.99: 
            leftStim.fillColor = curWin.color  # make the same color as bkg
            leftStim.lineColor = curWin.color
            
        # if right eye is not found, don't display eye
        if rightStim.pos[0] == 0.99:
            rightStim.fillColor = curWin.color  # make same color as bkg
            rightStim.lineColor = curWin.color    

        # give distance feedback
        findmsg.text = "You're currently " + \
        str(int(eyeDist)) + \
           ("cm away from the screen. \n"
            "Press 'c' to calibrate or 'q' to abort.")
               
        # update stimuli in window
        eyeArea.draw()
        leftStim.draw()
        rightStim.draw()
        findmsg.draw()
        curWin.flip()
        
        # get response to advance or abort from running track box, or continue
        # with calibration
        for event in keyboard.getEvents():
            # check to quit  
            # depending on response, either abort script or continue to calibration
            if event.key in ['q']:
                stopGazeData(eyeTracker)
                curWin.close()
                psychopy.core.quit()
                raise KeyboardInterrupt("You aborted the script manually.")
                keyboard.reporting = False  # stop recording keys                
            elif event.key in ['c']:
                print("Proceeding to calibration.")
                stopGazeData(eyeTracker)
                curWin.flip()
                keyboard.reporting = False  # stop recording keys
                return 
    
        # clear events not accessed this iteration
        io.clearEvents()


# live drawing of gaze position
def validateCal(eyeTracker, curDict):
    global globalTracking
    
    # start eyetracker
    startGazeData(eyeTracker)
    # let it warm up
    psychopy.core.wait(0.5)
    
    # get points from dictionary
    curPoints = curDict.values()
    
    # convert points from normalized units to psychopy pix
    pointPositions = [norm2PsychoPix(x) for x in curPoints]
    
    # window stimuli
    valWin = visual.Window(size = [GetSystemMetrics(0), GetSystemMetrics(1)],
                           pos = [0, 0],
                           units = 'pix',
                           fullscr = True,
                           allowGUI = True,
                           monitor = myMon,
                           winType = 'pyglet',
                           color = [0.8, 0.8, 0.8])  
    # stimuli for showing point of gaze
    gazeStim = visual.Circle(valWin, 
                             radius = 80,
                             lineColor = [1.0, 0.95, 0.0],  # yellow circle
                             fillColor = [1.0, 1.0, 0.55],  # light interior
                             lineWidth = 40,
                             units = 'pix')
    # Make a dummy message
    valMsg = visual.TextStim(valWin,
                             text = "Press 'c' when finished.",
                             color = [0.4, 0.4, 0.4],  # grey
                             units = 'norm',
                             pos = [0.0, -0.65],
                             height = 0.07)
    # Stimuli for all validation points
    valPoints = visual.Circle(valWin,
                              units = "pix",
                              radius = 20, 
                              lineColor = [1.0, -1.0, -1.0],  # red
                              fillColor = [1.0, -1.0, -1.0])  # red
    
    # turn on keyboard reporting
    keyboard.reporting = True

    # while tracking 
    while True:   

        # update stimuli in window and draw
        drawStim = norm2PsychoPix(getGazePosition())
        
        # draw gaze position only if found
        if drawStim[0] is not GetSystemMetrics(0): 
            gazeStim.pos = drawStim
            gazeStim.draw()
            
        # points
        for point in pointPositions:
            valPoints.pos = point
            valPoints.draw()
            
        # text
        valMsg.draw()
        valWin.flip()
        
        # get response to quit running validation box
        for event in keyboard.getEvents():
            # depending on response, either abort script or return to check
            # calibration
            if event.key in ['q']:
                valWin.close()
                raise KeyboardInterrupt("You aborted the script manually.")
                keyboard.reporting = False  # stop recording keys
                stopGazeData(eyeTracker)
                return
            elif event.key in ['c']:
                valWin.close()
                print ("Exiting calibration validation.")
                keyboard.reporting = False  # stop recoring keys
                stopGazeData(eyeTracker)
                return
                
        # clear events not accessed this iteration
        io.clearEvents()


# function for getting the average left and right gaze position coordinates
# for each calibration point in psychopy pix units
def getCalibResultsCoor(curResult):
    
    #create an empty list to hold values
    calibDrawCoor = []
    
    # iterate through calibration points
    for i in range(len(curResult.calibration_points)):
        # current point
        curPoint = curResult.calibration_points[i]
        pointPosition = curPoint.position_on_display_area  # point position
        pointSamples = curPoint.calibration_samples  # gaze samples from point
        # empty arrays for holding left and right eye gaze coordinates
        leftOutput = np.zeros((len(pointSamples), 2))
        rightOutput = np.zeros((len(pointSamples), 2))
        
        # find left and right gaze coordinates for all samples in point
        for j in range(len(pointSamples)):
            curSample = pointSamples[j]
            leftEye = curSample.left_eye
            rightEye = curSample.right_eye
            leftOutput[j] = leftEye.position_on_display_area
            rightOutput[j] = rightEye.position_on_display_area
            
        # get average x and y coordinates using all samples in point
        lXY = tuple(np.mean(leftOutput, axis = 0))
        rXY = tuple(np.mean(rightOutput, axis = 0))
        point = tuple((pointPosition[0], pointPosition[1]))
        # put current calibration point coordinates , l and r eye coordinates
        # into list, and convert to psychopy window coordinates in pix
        newList = [norm2PsychoPix(point), norm2PsychoPix(lXY), 
                   norm2PsychoPix(rXY), pointPosition]
        calibDrawCoor.insert(i, newList)
    # for some weird reason my calibration always includes the point (0,0) at 
    # index 0, so just remove it here
    calibDrawCoor.pop(0)
    # return as list
    return(calibDrawCoor)
       
    
# function for drawing the results of the calibration
def checkCalibrationResults(curCal, curResult, curWin, curDict):
    # get gaze position results
    points2Draw = getCalibResultsCoor(curResult)
    
    # create stimuli objects for drawing
    # outlined empty circle object for showing calibration point
    calibPoint = visual.Circle(curWin, 
                               radius = 100,
                               lineColor = [1.0, 1.0, 1.0],  # white
                               lineWidth = 20,
                               fillColor = curWin.color,
                               units = 'pix',
                               pos = (0.0, 0.0))  
    # line object for showing right eye gaze position during calibration 
    rightEyeLine = visual.Line(curWin, 
                               units ='pix',
                               lineColor ='red',
                               lineWidth = 30,
                               start = (0.0, 0.0),
                               end = (0.0, 0.0))                              
    # line object for showing left eye gaze position during calibration                          
    leftEyeLine = visual.Line(curWin, 
                              units ='pix',
                              lineColor ='yellow',
                              lineWidth = 30,
                              start = (0.0, 0.0),
                              end = (0.0, 0.0))
    # number for identifying point in dictionary
    pointText = visual.TextStim(curWin, 
                                text = " ", 
                                color = [0.8, 0.8, 0.8],  # lighter than bkg
                                units = 'pix',
                                pos = [0.0, 0.0],
                                height = 120)
        # Make a dummy message
    checkMsg = visual.TextStim(curWin,
                               text = ("      Press 'q' to abort, or" + \
                                       "\n'c' to continue with calibration."),
                               color = [1.0, 1.0, 1.0],
                               units = 'norm',
                               pos = [0.0, -0.65],
                               height = 0.07)

    # turn on keyboard reporting
    keyboard.reporting = True
    
    # make empty dictionary for holding points to be recalibrated
    holdRedoDict = []
    holdColorPoints = []
   
    # draw and update screen
    while True: 
      
        # iterate through calibration points and draw
        for i in range(len(points2Draw)):
            # update point and calibraiton results for both eyes
            point = points2Draw[i] 
            pointPos = point[3]
            pointKey = 0
            
            # update text 
            for key, point in curDict.items():
                if point == pointPos:
                    pointText.text = key
                    pointKey = key
            
            # if current point is selected for recalibrate, make it noticeable
            if int(pointKey) in holdColorPoints:
                calibPoint.lineColor = [-1.0, 1.0, -1.0]  # green circle
            else:
                calibPoint.lineColor = [1.0, 1.0, 1.0]  # no visible change
                
            # update point and calibraiton results for both eyes
            point = points2Draw[i]   
            startCoor, leftCoor, rightCoor = point[0], point[1], point[2]
            # update positions and draw  on window
            calibPoint.pos = startCoor  # calibration point
            leftEyeLine.start = startCoor  # left eye
            leftEyeLine.end = leftCoor
            rightEyeLine.start = startCoor  # right eye
            rightEyeLine.end = rightCoor
            pointText.pos = startCoor  # point text
            
            # update stimuli in window
            calibPoint.draw()  # has to come first or else will cover other
            # stim
            pointText.draw() 
            leftEyeLine.draw()
            rightEyeLine.draw()
            checkMsg.draw()
        
        # show points and lines on window         
        curWin.flip()
        
        # get keyboard responses        
        for event in keyboard.getEvents():
            # depending on response, either...
            # abort script
            if event.key in ['q']:
                curWin.close()
                raise KeyboardInterrupt("You aborted the script manually.")
                curCal.leave_calibration_mode()
                keyboard.reporting = False  # stop recording k
                core.quit()
                return
            # continue with calibration
            elif event.key in ['c']:
                print ("Finished checking. Resuming calibration.")
                checkMsg.pos = (0.0, 0.0)
                checkMsg.text = ("Finished checking. Resuming calibration.")
                checkMsg.draw()
                curWin.flip() 
                # turn off keyboard
                keyboard.reporting = False
    
                # return dictionary of points to be recalibration
                redoDict = collections.OrderedDict([])  # empty dictionary for holding unique values
                # dont put repeats in resulting dictionary
                tempDict = collections.OrderedDict(holdRedoDict)
                for key in tempDict.keys():
                    if key not in redoDict.keys():
                        redoDict[key] = tempDict.get(key)
    
                # return dictionary
                return redoDict
            
            # determine problem points
            # if the key character matches any point in dictionary key list
            elif event.key in curDict.keys():
                # iterate through each of these presses
                for entry in curDict.items():
                    # if the key press is the same as the current dictionary key
                    if entry[0] == event.key:
                        # append that dictionary entry into a holding dictionary
                        holdRedoDict.append(entry)
                        # append integer version to a holding list  
                        holdColorPoints.append(int(event.key))
                             
        # clear events not accessed this iteration
        io.clearEvents()


# function for drawing calibration points, collecting and applying calibration
# data
def performCalibration(curCal, curWin, pointOrder):
  
    # convert calibration points to psychopy window coordinates
    calibPsychoCoor = [norm2PsychoPix((x[0], x[1])) for x in pointOrder] 
    
     # defaults
    pointSmallRadius = 10.0  # point radius
    pointLargeRadius = pointSmallRadius * 10.0  
    moveFrames = 60  # number of frames to draw between points
    startPoint = norm2PsychoPix((0.95, 0.95)) # starter point for animation    

    # calibraiton point visual object
    calibPoint = visual.Circle(curWin, 
                               radius = pointLargeRadius,
                               lineColor = [1.0, -1.0, -1.0],  # red
                               fillColor = [1.0, -1.0, -1.0],
                               units = 'pix')
     
    # turn on keyboard
    keyboard.reporting = True

    # draw animation for each point
    # converting psychopy window coordinate units from normal to px
    for i in range(len(pointOrder)):    
        
        # if first point draw starting point
        if i == 0:
            firstPoint = [startPoint[0], startPoint[0]]
            secondPoint = [calibPsychoCoor[i][0], calibPsychoCoor[i][1]]
        else:
            firstPoint = [calibPsychoCoor[i - 1][0], calibPsychoCoor[i - 1][1]]
            secondPoint = [calibPsychoCoor[i][0], calibPsychoCoor[i][1]]
                
        # if escape key was pressed, abort
        for event in keyboard.getEvents():
            # check to quit  
            # depending on response, either abort script or continue to calibration
            if event.key in ['q']:
                curWin.close()
                raise KeyboardInterrupt("You aborted the script manually.")
                keyboard.reporting = False  # stop recording keys
                curCal.leave_calibration_mode()
                psychopy.core.quit()
                return
            
        # draw and move dot
        # step size for dot movement is new - old divided by frames
        pointStep = [((secondPoint[0] - firstPoint[0]) / moveFrames), 
                     ((secondPoint[1] - firstPoint[1]) / moveFrames)]
        
        # Move the point in position (smooth pursuit)
        for frame in range(moveFrames):
            firstPoint[0] += pointStep[0]
            firstPoint[1] += pointStep[1]
            # draw & flip
            calibPoint.pos = tuple(firstPoint)
            calibPoint.draw()
            curWin.flip()          
        # wait to let eyes settle    
        psychopy.core.wait(0.5)    
        
        # allow the eye to focus before beginning calibration
        # point size change step
        radiusStep = ((pointLargeRadius - pointSmallRadius) / moveFrames)
        
        # Shrink the outer point (gaze fixation) to encourage focusing
        for frame in range(moveFrames):
            pointLargeRadius -= radiusStep
            calibPoint.radius = pointLargeRadius
            calibPoint.draw()
            curWin.flip()    
        # first wait to let the eyes settle 
        psychopy.core.wait(0.5)  
        
        # conduct calibration of point
        print ("Collecting data at {0}." .format(i + 1))
        while curCal.collect_data(pointOrder[i][0], pointOrder[i][1]) != tobii.CALIBRATION_STATUS_SUCCESS:
            curCal.collect_data(pointOrder[i][0], pointOrder[i][1])   
            
        # feedback from calibration
        print ("{0} for data at point {1}." .format(curCal.collect_data(pointOrder[i][0],
               pointOrder[i][1]), i + 1))
        psychopy.core.wait(0.3)  # wait before continuing
      
        # Return point to original size
        for frame in range(moveFrames):
            pointLargeRadius += radiusStep
            calibPoint.radius = pointLargeRadius
            calibPoint.draw()
            curWin.flip()      
        # let the eyes settle and move to the next point 
        psychopy.core.wait(0.2)      
        
        # clear events not accessed this iteration
        io.clearEvents()
    
    # clear screen
    curWin.flip()   
    # turn off keyboard
    keyboard.reporting = False
    # print feedback
    print "Computing and applying calibration."
    # compute and apply calibration to get calibration result object    
    calibResult = curCal.compute_and_apply()        
    # return calibration result
    return calibResult


# function for running simple gui to visualize subject eye position. Make 
# sure that the eyes are in optimal location for eye tracker
def runTrackBox(eyeTracker):
    # start the eyetracker
    startGazeData(eyeTracker) 
    # wait for it ot warm up
    psychopy.core.wait(0.5)
    
    # create window for visualizing eye position and text
    trackWin = visual.Window(size = [GetSystemMetrics(0), GetSystemMetrics(1)],
                             pos = [0, 0],
                             units = 'pix',
                             fullscr = True,
                             allowGUI = True,
                             monitor = myMon,
                             winType = 'pyglet',
                             color = [0.4, 0.4, 0.4])
    
    # feedback about eye position
    drawEyePositions(trackWin, eyeTracker)
    # close track box 
    psychopy.core.wait(2)
    trackWin.close()
    return 


# function for running simple calibration routine 
def runCalibrationRoutine(eyeTracker, numCalibPoints):   
    # check that eyetracker is connected before running
    if eyeTracker is None:  # eyeTracker
        print("No eyeTracker is specified. Aborting calibration.")
        return
           
    # create dictionary of calibration points
    # if nothing entered then default is nine
    if numCalibPoints is None: 
        pointList = [('1',(0.1, 0.1)), ('2',(0.5, 0.1)), ('3',(0.9, 0.1)), 
                     ('4',(0.1, 0.5)), ('5',(0.5, 0.5)), ('6',(0.9, 0.5)), 
                     ('7',(0.1, 0.9)), ('8',(0.5, 0.9)), ('9',(0.9, 0.9))]
    elif numCalibPoints is 5:
        pointList = [('1',(0.1, 0.1)), ('2',(0.9, 0.1)), ('3',(0.5, 0.5)), 
                     ('4',(0.1, 0.9)), ('5',(0.9, 0.9))]
    elif numCalibPoints is 9: 
        pointList = [('1',(0.1, 0.1)), ('2',(0.5, 0.1)), ('3',(0.9, 0.1)), 
                     ('4',(0.1, 0.5)), ('5',(0.5, 0.5)), ('6',(0.9, 0.5)), 
                     ('7',(0.1, 0.9)), ('8',(0.5, 0.9)), ('9',(0.9, 0.9))]
        
    # randomize points as ordered dictionary 
    random.shuffle(pointList)
    calibDict = collections.OrderedDict(pointList)

    # create window for calibration
    calibWin = visual.Window(size = [GetSystemMetrics(0), GetSystemMetrics(1)],
                             pos = [0, 0],
                             units = 'pix',
                             fullscr = True,
                             allowGUI = True,
                             monitor = myMon,
                             winType = 'pyglet',
                             color = [0.4, 0.4, 0.4])  
    # stimuli for holding text
    calibMessage = visual.TextStim(calibWin, 
                                   color = [1.0, 1.0, 1.0],  # text
                                   units = 'norm', 
                                   height = 0.08, 
                                   pos = (0.0, 0.1))
    # stimuli for fixation cross
    fixCross = visual.TextStim(calibWin,
                               color = [1.0, 1.0, 1.0],
                               units = 'norm', 
                               height = 0.1, 
                               pos = (0.0, 0.0),
                               text = "+")
   
    # track box to position participant
    # subject instructions for track box
    calibMessage.text = ("Please position yourself so that the\n" + \
                         "eye-tracker can locate your eyes." + \
                         "\n\nPress 'c' to continue.")
    calibMessage.draw()
    calibWin.flip() 
    # turn keyboard reporting on and get subject response
    keyboard.reporting = True
    keyboard.waitForKeys(maxWait = 10, keys = ['c'])  # proceed with calibration

    #run track box routine
    runTrackBox(eyeTracker)

    # initialize calibration
    calibration = tobii.ScreenBasedCalibration(eyeTracker)  # calib object 
    # enter calibration mode
    calibration.enter_calibration_mode()
    # subject instructions
    calibMessage.text = ("Please focus your eyes on the red dot " + \
                         "and follow it with your eyes as closely as " + \
                         "possible.\n\nPress 'c' to continue.")
    calibMessage.draw()
    calibWin.flip()   
        
    # turn keyboard reporting on and get subject response
    keyboard.reporting = True
    keyboard.waitForKeys(maxWait = 10, keys = ['c'])  # proceed with calibration

    # draw a fixation cross
    fixCross.draw()
    calibWin.flip()
    psychopy.core.wait(3)
    # turn off keyboard
    keyboard.reporting = False
    
    # create dictionary for holding points to be recalibrated
    redoCalDict = calibDict
    
    # loop through calibration process until calibration is complete
    while True:
        
        # create point order form randomized dictionary values
        pointOrder = redoCalDict.values()
        
        # perform calibration 
        calibResult = performCalibration(calibration, calibWin, pointOrder)

        # check status of calibration result
        # if calibration was successful, check calibration results
        if calibResult.status != tobii.CALIBRATION_STATUS_FAILURE:      
            # give feedback
            calibMessage.text = ("Applying calibration...")
            calibMessage.draw()
            calibWin.flip()
            psychopy.core.wait(2)
            # moving on to accuracy plot
            calibMessage.text = ("Calculating calibration accuracy...")
            calibMessage.draw()
            calibWin.flip()
            psychopy.core.wait(2)
            
            # check calibration for poorly calibrated points
            redoCalDict = checkCalibrationResults(calibration, calibResult, 
                                                  calibWin, calibDict)
   
        else:  # if calibration was not successful, leave and abort
            calibMessage.text = ("Calibration was not successful.\n\n" + \
                                 "Closing the calibration window.")
            calibMessage.draw()
            calibWin.flip()
            psychopy.core.wait(3)
            calibWin.close()
            calibration.leave_calibration_mode()
            return
                
        # Redo calibration for specific points if necessary 
        if not redoCalDict:  # if no points to redo
        # finish calibration
            print "Calibration successful. Moving on to validation mode."
            calibMessage.text = ("Calibration was successful.\n\n" + \
                                 "Moving on to validation.")
            calibMessage.draw()
            calibWin.flip()
            psychopy.core.wait(3)
            calibration.leave_calibration_mode()
            # break loop to proceed with validation
            break
        
        else:  # if any points to redo
            # convert list to string for feedback
            printString = " ".join(str(x) for x in redoCalDict.keys())
            # feedback
            print ("Still need to calibrate the following points: %s" 
                   % printString)
            calibMessage.text = ("Calibration is almost complete.\n\n" + \
                             "Prepare to recalibrate a few points.")
            calibMessage.draw()
            calibWin.flip()
            psychopy.core.wait(3)
            # draw fixation cross
            fixCross.draw()
            calibWin.flip()
            psychopy.core.wait(3)
            
            # iterate through list of redo points and remove data from calibration
            for newPoint in redoCalDict.values():
                print newPoint
                calibration.discard_data(newPoint[0], newPoint[1])

            # continue with calibration of remaining points
            continue
        
    # quickly validate calibration
    # draw fixation cross
    fixCross.draw()
    calibWin.flip()
    psychopy.core.wait(3)
    # run validation
    validateCal(eyeTracker, calibDict)
    
    # close window
    calibMessage.text = ("Validation complete. Closing window.")
    calibMessage.draw()
    calibWin.flip()
    psychopy.core.wait(3)
    calibWin.close() 
    return



# run calibration rountine for all points in list
runCalibrationRoutine(myTracker, 5)
io.quit()

##checkGazePos(myTracker)
print "Damn I'm good"

# i need to turn this into a class for using during my exp
# also need to put in functionality for getting pupil size











#TODO get control keys working, debug, test

