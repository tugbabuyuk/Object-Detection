from detector import ObjectDetector
import numpy as np
import cv2
import argparse
import os
from sklearn.svm import LinearSVC


ap = argparse.ArgumentParser()
#ap.add_argument("-d","--detector",required=True)
#ap.add_argument("-i","--image",required=True)
ap.add_argument("-a","--annotate",default=None)
ap.add_argument("-t","--tracker",default="camshift",help="tracker to use (camshift/correlation)")
args = vars(ap.parse_args())

cap=cv2.VideoCapture(0)
MAİN_PATH= 'Python/'
SUB_PATH='objectdetector/'
os='target_detector.svm'
ANNOTATES=['TARGET','CLOCK']


detector = ObjectDetector(os)

while True:
##   if(loadPath=="target_detector.svm"):
##     name="target"
##   if (loadPath=="clock_detector.svm"):
##     name="clock"


   imagepath=cap.read()
        
#imagePath = args["image"]
   ##image = cv2.imread(imagePath)
##   for i in range (len(ANNOTATES[i])):
   detector.detect(imagepath,annotate=args["annotate"])   

   if cv2.waitKey(25)& 0xFF ==ord('q') :
      cv2.destroyAllWindows()
      break
  
         







