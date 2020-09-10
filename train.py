from detector import ObjectDetector
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-t","--takejpg",required=True)
ap.add_argument("-i","--images",required=True)
ap.add_argument("-d","--detector",default=None)
args = vars(ap.parse_args())

print ("Görüntüler hazırlanıyor")
takej= np.load(args["takejpg"])
imagePaths = np.load(args["images"])

detector = ObjectDetector()
print ("Object Detector sınıfına erişim sağlanıyor lütfen bekleyiniz!")
#fit fonksiyonu ile birlikte train yapılarak svm dosyası oluşturulur.
detector.fit(imagePaths,takej,visualize=True,savePath=args["detector"])
