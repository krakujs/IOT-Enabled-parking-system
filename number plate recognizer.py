import cv2
import time
import imutils
import pandas as pd
import numpy as np
import pytesseract
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

data = {'Slot': [1,2],
        'License':[np.NaN, np.NaN ],
        'TimeIn': [np.NaN, np.NaN ]}
           
timeSlot ={'Slot':[1,2],
           'TimeIn':[np.NaN,np.NaN]}
a = pd.DataFrame(data)
timeSlot = pd.DataFrame(timeSlot)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        i=GPIO.input(23)
        if i == 1:
             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grey scale
             gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
             edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
             cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,              cv2.CHAIN_APPROX_SIMPLE)
             cnts = imutils.grab_contours(cnts)
             cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
             screenCnt = None
             for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                if len(approx) == 4:
                  screenCnt = approx
                  break
             if screenCnt is None:
               detected = 0
               print ("No number plate detected")
             else:
               detected = 1
             if detected == 1:
               cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
               mask = np.zeros(gray.shape,np.uint8)
               new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
               new_image = cv2.bitwise_and(image,image,mask=mask)
               (x, y) = np.where(mask == 255)
               (topx, topy) = (np.min(x), np.min(y))
               (bottomx, bottomy) = (np.max(x), np.max(y))
               Cropped = gray[topx:bottomx+1, topy:bottomy+1]
               text = pytesseract.image_to_string(Cropped, config='--psm 11')
               print("Detected Number is:",text)
               
               lic = text
               #Billing
                
               if(lic in a.values):
                    print('Car in the slot')
                    timeOut = time.localtime()
                    timeOutTs = time.time()
                    timeOut = time.strftime('%H:%M:%S',timeOut)
                    slotNo = a[a.License ==lic].index[0]
                    print(slotNo)
                    timeInTs = timeSlot.loc[slotNo]['TimeIn']
                    timeSlot.loc[slotNo,'TimeIn'] = np.NaN
                    totalTime = timeOutTs - timeInTs
                    print(timeInTs)
                    print("Total Seconds Parked",totalTime)
                    print('Total Amount',totalTime * 0.00277777777 )
                    slot = a[a.License==lic]['Slot'].index
                    a.loc[slot,'License'] = np.NaN
                    a.loc[slot,'TimeIn'] = np.NaN
               elif(a['License'].isnull().values.any()):
                        print('Parking Available as car not in any slot')
                        timeIn = time.localtime()
                        timeInTs = time.time()
                        timeIn = time.strftime('%H:%M:%S',timeIn)
                        emptySlot = a.loc[a.License.isnull()].index[0]
                        a.loc[emptySlot , 'License'] = lic
                        a.loc[emptySlot,'TimeIn'] = timeIn
                        timeSlot.loc[emptySlot,'TimeIn'] = timeInTs
                        print('Parking slot alloted is: ',emptySlot+1)
   
   
               else:
                        print("No slots available and car not in any slot")
                        #Billing ends here
                    
               cv2.imshow("Frame", image)
             #cv2.imshow('Cropped',Cropped)
               cv2.waitKey(0)
               #break
#cv2.destroyAllWindows()