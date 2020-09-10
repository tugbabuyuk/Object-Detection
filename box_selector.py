import numpy as np
import cv2

class BoxSelect(object):
    def __init__(self, image, window_name,color=(0,0,255)):
        #Görünyü saklar ve orjinal kopyasını oluşturur.
        self.image = image
        self.orig = image.copy()
        #Başlangıç ve bitiş koordinatlarını yakalar.
        self.start = None
        self.end = None
        self.track = False
        self.color = color
        self.window_name = window_name

        #adlandırılan pencereyi geri çağırma
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name,self.mouseCallBack)

    def mouseCallBack(self, event, x, y, flags, params):
        #Mouse'a sol tıklandıysa izleme başlatılır.
        if event==cv2.EVENT_LBUTTONDOWN:
            self.start =(x,y)
            self.track = True

        elif self.track and (event==cv2.EVENT_MOUSEMOVE or event==cv2.EVENT_LBUTTONUP):
            self.end = (x,y)
            if not self.start==self.end:
                self.image = self.orig.copy()
                #başlangıç ve bitiş koordinatları ile kareyi çizdirir
                cv2.rectangle(self.image, self.start, self.end, self.color, 2)
                #Mouse'un sol tuşu bırakıldığında izleme biter.
                if event==cv2.EVENT_LBUTTONUP:
                    self.track=False

            #Yanlışlıkla tıklandığında izlemeyi resetler
            else:
                self.image = self.orig.copy()
                self.start = None
                self.track = False
            cv2.imshow(self.window_name,self.image)
   #c++ daki protected gibi kullanılır.
    @property
    def koordinat(self):
        if self.start and self.end:
            pts = np.array([self.start,self.end])
            s = np.sum(pts,axis=1)
            (x,y) = pts[np.argmin(s)]
            (xb,yb) = pts[np.argmax(s)]
            return [(x,y),(xb,yb)]
        else:
            return []
