import dlib
import cv2

import string
import argparse
import numpy as np

cap=cv2.VideoCapture(0)


class ObjectDetector( ):
  
    def __init__(self,options=None,loadPath=None ):
     
        #Detector seçnekleri oluşturur
        self.options = options
        if self.options is None:
            self.options = dlib.simple_object_detector_training_options()

        #Test için eğitilmiş detector yüklenir.
        if loadPath  is not None:
            self._detector=dlib.simple_object_detector(loadPath)
            
    #Görüntülerin koordinatlarını alır.
    def _prepare_annotations(self,takejpg):
        takej = []
        for (x,y,xb,yb) in takejpg:
            takej.append([dlib.rectangle(left=int(x),top=int(y),right=int(xb),bottom=int(yb))])
        return takej
    #alınan ghörüntüler RGB'ye çevrilir.
    def _prepare_images(self,imagePaths):
        images = []
        for imPath in imagePaths:
            image = cv2.imread(imPath)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            images.append(image)
        return images
    
    #Train seçeneği fotoğraflar ve koordinatlar ile train işlemini gerçekleştirir
    def fit(self, imagePaths, takejpg, visualize=False, savePath=None):
        takejpg= self._prepare_annotations(takejpg)
        images = self._prepare_images(imagePaths)
        self._detector = dlib.train_simple_object_detector(images, takejpg, self.options)
        

        #HOG görselleştirmesi
        if visualize:
            win = dlib.image_window()
            win.set_image(self._detector)
            dlib.hit_enter_to_continue()

        #Detector diske kaydedilir.
        if savePath is not None:
            self._detector.save(savePath)
            ids=savePath

        return self
    
    #Tüm görüntüler için karelerin koordinatları alınır.
    #Verilen görüntüdeki kareleri çizdirmek için kullanılır.
    def predict(self,image):
        boxes = self._detector(image)
        preds = []
        for box in boxes:
            (x,y,xb,yb) = [box.left(),box.top(),box.right(),box.bottom()]
            preds.append((x,y,xb,yb))
        return preds

    def detect(self,imagepath,annotate=None):
      while True :  
            ret,imagepath=cap.read()
            #image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            preds = self.predict(imagepath)
            font=cv2.FONT_HERSHEY_SIMPLEX
            for (x,y,xb,yb) in preds:
                 imagepath = cv2.cvtColor(imagepath,cv2.COLOR_RGB2BGR)
                 gray = cv2.cvtColor(imagepath,cv2.COLOR_BGR2GRAY)
                 confidence = self.predict(gray[y:y+yb,x:x+xb])
                
                 clock="clock"
                 target="target"
                 for i in confidence:                 
                       
                       print("koordinatlar",format(confidence))
                       son=confidence[0][0]+confidence[0][1]+confidence[0][2]+confidence[0][3]
                       son=son/4
                    
                       if (son<100):
                           print("tespit orani %",son)
                           yüzde="tespit orani: {:.2f}%".format(son)
                           cv2.putText(imagepath, str(yüzde), (x,y+yb), font, 1, (0,0,255), 2)
                           #cv2.putText(imagepath, name, (x,y), font, 1, (0,0,255), 2)
##                          
                       else:
                           print("tespit orani %",100)
                           yüzde="tespit orani:100%"
                           cv2.putText(imagepath, str(yüzde), (x,y+yb), font, 1, (0,0,255), 2)
                          # cv2.putText(imagepath, name, (x,y), font, 1, (0,0,255), 2)
                          
                           
                      
            #resim çizdirme ve açıklama
                       cv2.rectangle(imagepath,(x,y),(xb,yb),(0,0,255),2)
##                     if(id=="target_detector.svm"):
##                              cv2.putText(imagepath,str(target),(x,y+yb), font, 1, (0,0,255), 2)
##                           elif (id=="clock_detector.svm"):
                 
                            
                 if annotate is not None and type(annotate)==str:
                     cv2.putText(imagepath,annotate,(x+5,y-5),cv2.FONT_HERSHEY_SIMPLEX,1.0,(128,255,0),2)
                                   
            cv2.imshow("Detected",imagepath)
            if cv2.waitKey(25)& 0xFF ==ord('q') :
               cv2.destroyAllWindows()
               break

            
        
