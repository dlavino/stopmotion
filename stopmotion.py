########################################################
#-------------STOPMOTION WITH RASPBERRY PI-------------#
#------------------------------------------------------#
#----------------AUTHOR: DANIEL LAVINO-----------------#
########################################################

#loading opensource libraries - some may not be native
import cv2
import numpy as np
from time import sleep
from Tkinter import *
from imutils.video import WebcamVideoStream # https://github.com/jrosebr1/imutils
import imutils
#from threading import Thread
import RPi.GPIO as GPIO

#initializing GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN,GPIO.PUD_DOWN) #capture
GPIO.setup(5,GPIO.IN,GPIO.PUD_DOWN) #play
GPIO.setup(4,GPIO.IN,GPIO.PUD_DOWN) #reset
GPIO.output(26,GPIO.HIGH)


#initializing some variables
AnimFrameRate = 20
opacity = 0.0
key = 0
actIcon = 0
seq = []
actSeqFrame = 0
font = cv2.FONT_HERSHEY_SIMPLEX

#here we use a Tkinter root just to get screen resolutions
#without initializing any screen though
#This way we can make it screen adaptive
root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print "Sua resolucao: %s x %s" %(screen_width, screen_height)

vs = WebcamVideoStream(src=0).start() #start threading

cv2.namedWindow("video", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

print "Inicializando Camera..." #Initializing Camera
sleep(0.5)
print "Ajustando exposicao..." #Adjusting Exposition - Otherwise camera
#could start darker
sleep(0.5)
GPIO.output(26,GPIO.LOW)
print "Running..."

try:
    overlay = vs.read()
    overlay = imutils.resize(overlay, height=int(screen_height*0.1))
except:
    print "Camera nao encontrada. Reconecte a camera e tente novamente."
    sys.exit();
icon_height, icon_width = overlay.shape[:2]
overlay = vs.read()
overlay = imutils.resize(overlay, height=int(screen_height*0.9))
vid_height, vid_width = overlay.shape[:2]
black = np.zeros((screen_height,screen_width,3), np.uint8)

#layout drawing function
def layout():
    for i in range(0,9):
        cv2.rectangle(black,(i*icon_width,int(screen_height*0.9)),(icon_width + i*icon_width,screen_height),(255,255,255),3)
    cv2.putText(black,'Stop Motion',(int(vid_width + (screen_width - vid_width)*0.05),int((screen_width - vid_width)*0.12)), font, (screen_width - vid_width)/210.0,(0,0,255), screen_width/480,cv2.LINE_AA)
    cv2.putText(black,'MACHINE',(int(vid_width + (screen_width - vid_width)*0.05),int((screen_width - vid_width)*0.28)), font, (screen_width - vid_width)/150.0,(0,0,255),screen_width/720,cv2.LINE_AA)
    cv2.putText(black,'Velocidade',(int(vid_width + (screen_width - vid_width)*0.1),int((screen_width - vid_width)*0.55)), font, (screen_width - vid_width)/210.0,(255,255,255), screen_width/480,cv2.LINE_AA)
    cv2.putText(black,str(AnimFrameRate),(int(vid_width + (screen_width - vid_width)*0.1),int((screen_width - vid_width)*0.7)), font, (screen_width - vid_width)/210.0,(0,255,0), screen_width/480,cv2.LINE_AA)
    cv2.putText(black,'FPS',(int(vid_width + (screen_width - vid_width)*0.3),int((screen_width - vid_width)*0.7)), font, (screen_width - vid_width)/210.0,(255,255,255), screen_width/480,cv2.LINE_AA)

#capture function
def cap():
    global overlay
    global ball
    global opacity
    global actSeqFrame
    global seq
    opacity = 0.7
    overlay = vs.read()
    overlay = imutils.resize(overlay, height=int(screen_height*0.9))
    seq.insert(actSeqFrame,overlay)
    actSeqFrame += 1
    icon = imutils.resize(overlay, height=int(screen_height*0.1))
    return icon

def play():
    global key
    global AnimFrameRate
    while True:
        for i in range(0, actSeqFrame):
            black[0:vid_height, 0:vid_width] = seq[i]
            cv2.imshow('video', black)
            key = cv2.waitKey(1000/AnimFrameRate) & 0xFF
            if (key == ord('r')) or GPIO.input(4):
                reset()
                return
            else:
                fRate()
def reset():
    global black
    global seq
    global actSeqFrame
    global actIcon
    global opacity
    black = np.zeros((screen_height,screen_width,3), np.uint8)
    layout()
    cv2.imshow('video', black)
    seq = []
    actSeqFrame = 0
    actIcon = 0
    opacity = 0.0

def fRate():
    global key
    global AnimFrameRate
    if (key == ord('m')) & (AnimFrameRate < 30):
        cv2.putText(black,str(AnimFrameRate),(int(vid_width + (screen_width - vid_width)*0.1),int((screen_width - vid_width)*0.7)), font, (screen_width - vid_width)/210.0,(0,0,0), screen_width/480,cv2.LINE_AA)
        AnimFrameRate = AnimFrameRate + 1
        cv2.putText(black,str(AnimFrameRate),(int(vid_width + (screen_width - vid_width)*0.1),int((screen_width - vid_width)*0.7)), font, (screen_width - vid_width)/210.0,(0,255,0), screen_width/480,cv2.LINE_AA)
    else:
        if (key == ord('n')) & (AnimFrameRate > 1):
            cv2.putText(black,str(AnimFrameRate),(int(vid_width + (screen_width - vid_width)*0.1),int((screen_width - vid_width)*0.7)), font, (screen_width - vid_width)/210.0,(0,0,0), screen_width/480,cv2.LINE_AA)
            AnimFrameRate = AnimFrameRate - 1
            cv2.putText(black,str(AnimFrameRate),(int(vid_width + (screen_width - vid_width)*0.1),int((screen_width - vid_width)*0.7)), font, (screen_width - vid_width)/210.0,(0,255,0), screen_width/480,cv2.LINE_AA)

layout() #starts drawing layout

while key!= ord('q'):
    img = vs.read()
    img = imutils.resize(img, height=int(screen_height*0.9))
    cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
    black[0:vid_height, 0:vid_width] = img
    cv2.imshow('video', black)
    
    key = cv2.waitKey(1) & 0xFF #keys are listened at this line
    
    if (key == ord('c')) or GPIO.input(6):
        for i in range(0,9):
            cv2.rectangle(black,(i*icon_width,int(screen_height*0.9)),(icon_width + i*icon_width,screen_height),(255,255,255),3)
        black[screen_height*0.9:screen_height*0.9 + icon_height, actIcon*icon_width:actIcon*icon_width + icon_width] = cap()
        cv2.rectangle(black,(actIcon*icon_width,int(screen_height*0.9)),(icon_width + actIcon*icon_width,screen_height),(0,255,0),3)
        actIcon += 1
        if actIcon == 9:
            actIcon = 0
    else:
        if (key == ord('p')) or GPIO.input(5):
            if actSeqFrame > 0:
                play()
            else:
                print "Nao existem quadros para a sequencia!"
        else:
            if (key == ord('r')) or GPIO.input(4):
                reset()
            else:
                if (key == ord('a')):
                    if actSeqFrame > 0:
                        actSeqFrame -= 1
                    if actIcon == 0:
                        actIcon = 9
                    else:
                        actIcon -= 1
                    cv2.rectangle(black,(actIcon*icon_width,int(screen_height*0.9)),(icon_width + actIcon*icon_width,screen_height),(0,0,0),-1)
                    cv2.rectangle(black,(actIcon*icon_width,int(screen_height*0.9)),(icon_width + actIcon*icon_width,screen_height),(255,255,255),3)
                    cv2.rectangle(black,((actIcon-1)*icon_width,int(screen_height*0.9)),(icon_width + (actIcon-1)*icon_width,screen_height),(0,255,0),3)
                else:
                    fRate()

cv2.destroyAllWindows()
vs.stop()
print "Programa finalizado."
