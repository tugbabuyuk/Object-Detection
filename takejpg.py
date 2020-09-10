import numpy as np
import cv2
import argparse
from imutils.paths import list_images
from __init__ import BoxSelect


ap = argparse.ArgumentParser()
ap.add_argument("-d","--dataset",required=True)
ap.add_argument("-t","--takejpg",required=True)
ap.add_argument("-i","--images",required=True)
args =  vars(ap.parse_args())


takejpg = []
imPaths = []


for imagePath in list_images(args["dataset"]):

    image = cv2.imread(imagePath)
    bs = BoxSelect(image,"Image")
    cv2.imshow("Image",image)
    cv2.waitKey(0)

    pt1,pt2 = bs.koordinat
    (x,y,xb,yb) = [pt1[0],pt1[1],pt2[0],pt2[1]]
    takejpg.append([int(x),int(y),int(xb),int(yb)])
    imPaths.append(imagePath)

takejpg = np.array(takejpg)
imPaths = np.array(imPaths,dtype="unicode")
np.save(args["takejpg"],takejpg)
np.save(args["images"],imPaths)
