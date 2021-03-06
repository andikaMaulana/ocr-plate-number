import json
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import cv2
from ocr_core import ocr_core
import numpy as np
from PIL import Image
import imutils
import pytesseract
import io
import re
import time
import json

class Treshold:
    def __init__(self):
        self.to_angka = [["O","0"],["!","1"],["I","1"],["|","1"],["S","5"],["E","8"]]
        self.to_huruf = [["e","O"],["0","O"],["!","I"],["1","I"],["|","I"],["5","S"],["8","O"],["7","L"]]
        self.kode_plat = ["BL","BB","BK","BA","BM","BP","BG","BN","BE","BD","BH","A",\
                            "B","D","E","F","T","Z","G","H","K","R","AA","AB","AD","L","M","N","P",\
                            "S","W","AE","AG","DK","DR","EA","DH","EB","ED","KB","DA","KH","KT",\
                            "DB","DL","DM","DN","DT","DD","DC","DE","DG","DS"]
        self.data_huruf = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",\
                            "Q","R","S","T","U","V","W","X","Y","Z"]
        self.kode_plat =set (self.kode_plat)
        
        #KNN
        x=[]
        y=[]
        with open('data_plate.txt') as josn_file:
            data = json.load(josn_file)
            for p in data['data']:
                x.append([p['b'],p['w']])
                y.append(p['treshold'])
        self.knn=KNeighborsClassifier(n_neighbors=3) #define K=3
        self.knn.fit(x,y)
        
    def getTresh(self,b,w):
        a=np.array([[b,w]])
        result = self.knn.predict(a)
        return result[0]
    
    def toRgb(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def removeSymbol(val):
        return re.sub("[^0-9a-zA-Z]","",val)

    def toBin(img,tre):
        _,img=cv2.threshold(img, tre, 255, cv2.THRESH_BINARY_INV)
        return img

    def gaussianBlur(img):
        return cv2.GaussianBlur(img,(5,5),0)

    def toGray(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def rotateImg(img,angle):
        return imutils.rotate_bound(img, angle)

    def cropImg(img):
        h, w= img.shape
        return img[5:0+h-10, 6:0+w]
        

    def replaceToAngka(self,val):
        for i in self.to_angka:
            if val==i[0]:
                return i[1]
        return ""

    def replaceToHuruf(self,val):
        for i in self,to_huruf:
            if val==i[0]:
                return i[1]
        return ""


    def getPlat(self,plat):
        
        pl0 = ""
        pl1 = ""
        pl2 = ""
        #get plat kota
        for i in range(0,2):
            try:
                if(type(int(plat[i])))==int:
                    if plat[i] in self.kode_plat:
                        pl0+=replaceToHuruf(plat[i])
            except ValueError:
                val = pl0+plat[i]
                if val in self.kode_plat:
                    pl0+=plat[i]
        #get plat angka
        l=0
        for i in range(len(pl0),len(plat)):
            
            try:
                if(type(int(plat[i])))==int:
                    pl1+=plat[i]
                    l+=1
            except ValueError:
                pl1+=replaceToAngka(plat[i])
                l+=1
            if l>3:
                break
        #get plat huruf belakang
        l=0
        for i in range(len(pl0)+len(pl1),len(plat)):
            try:
                if(type(int(plat[i])))==int:
                    if plat[i] in self.data_huruf:
                        pl2+=replaceToHuruf(plat[i])
                        l+=1
            except ValueError:
                if plat[i] in self.data_huruf:
                    pl2+=plat[i]
                    l+=1
                else:
                    pl2+=replaceToHuruf(plat[i])
                    l+=1
            if l>2:
                break
        return pl0+"-"+pl1+"-"+pl2
    
    def getText(img):
        imgProc = toGray(img)
        # imgProc = cropImg(originalImage)

        w,h = imgProc.shape
        total = w*h
        bl = np.sum(imgProc >= 127) / total *100
        wh = np.sum(imgProc < 127) / total *100
        tre = getTresh(bl,wh)

        imgProc = toBin(imgProc,tre)
        imgProc = gaussianBlur(imgProc)
        extracted_text = ocr_core(imgProc)
        
        extracted_text = removeSymbol(extracted_text)
        extracted_text  = getPlat(extracted_text)
        
        return extracted_text