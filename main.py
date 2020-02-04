import cv2
from ocr_core import ocr_core
import numpy as np
from PIL import Image
import imutils
import pytesseract
import io
import re
T=69
#main 
to_angka=[["0","O"],["!","1"],["I","1"],["|","1"],["S","5"],["E","8"]]
to_huruf=[["0","O"],["!","I"],["1","I"],["|","I"],["5","S"],["8","O"],["7","L"]]
kode_plat = ["BL","BB","BK","BA","BM","BP","BG","BN","BE","BD","BH","A",\
            "B","D","E","F","T","Z","G","H","K","R","AA","AB","AD","L","M","N","P",\
            "S","W","AE","AG","DK","DR","EA","DH","EB","ED","KB","DA","KH","KT",\
            "DB","DL","DM","DN","DT","DD","DC","DE","DG","DS"]
kode_plat =set (kode_plat)

def toRgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def toBin(img):
    tre = 100
    tre=int(input("treshold : "))
    
    _,img=cv2.threshold(img, tre, 255, cv2.THRESH_BINARY_INV)
    return img

def erosi(img):
    tre=int(input("treshold : "))
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, tre, 225, cv2.THRESH_BINARY)
    kernel = np.ones((3,3),np.uint8)
    return cv2.erode(thresh,kernel,iterations = 1)

def gaussianBlur(img):
    return cv2.GaussianBlur(img,(5,5),0)

def toGray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def rotateImg(img,angle):
    return imutils.rotate_bound(img, angle)

def cropImg(img):
    h, w= img.shape
    return img[5:0+h-10, 6:0+w] #original
    # return img[5:0+int((h/3)*2)-10, 6:0+w] #crop plat
#main 
def replaceToAngka(val):
    for i in to_angka:
        if val==i[0]:
            return i[1]
    return ""

def replaceToHuruf(val):
    for i in to_huruf:
        if val==i[0]:
            return i[1]
    return ""


def getPlat(plat):
    print(plat)
    pl0 = ""
    pl1 = ""
    pl2 = ""
    #get plat kota
    for i in range(0,2):
        try:
            if(type(int(plat[i])))==int:
                pl0+=replaceToHuruf(plat[i])
        except ValueError:
            val = pl0+plat[i]
            if val in kode_plat:
                pl0+=plat[i]
        if pl0 in kode_plat:
            break

    #get plat angka
    for i in range(len(pl0),len(pl0)+4):
        
        try:
            if(type(int(plat[i])))==int:
                pl1+=plat[i]
        except ValueError:
            pl1+=replaceToAngka(plat[i])
    #get plat huruf belakang
    for i in range(len(pl0)+len(pl1),len(plat)):
        
        try:
            if(type(int(plat[i])))==int:
                pl2+=replaceToHuruf(plat[i])
        except ValueError:
            pl2+=plat[i]

    plat=pl0+"-"+pl1+"-"+pl2
    return plat

def removeSymbol(val):
    val  = re.sub("[^0-9a-zA-Z]","",val)
    return val


originalImage = cv2.imread('data/plate5.png')
# originalImage = cv2.resize(originalImage, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
originalImage = toRgb(originalImage)
originalImage = toGray(originalImage)
imgProc = toBin(originalImage)
imgProc = cropImg(imgProc)
imgProc = gaussianBlur(imgProc)
cv2.imshow('output', imgProc)
cv2.imshow('original', originalImage)

extracted_text_ori = ocr_core(originalImage)
extracted_text_mod = ocr_core(imgProc)
extracted_text_mod=removeSymbol(extracted_text_mod)
extracted_text  = getPlat(extracted_text_mod)


# extracted_text = getPlat(extracted_text_mod)

print(f"original : {extracted_text_ori}\nprocessing : {extracted_text_mod}\n processing 2: {extracted_text} ")

cv2.waitKey(0)
cv2.destroyAllWindows()
