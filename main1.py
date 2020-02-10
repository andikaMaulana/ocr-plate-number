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

from tresh import Treshold

t=Treshold()
grayVal={}


#main 
to_angka=[["O","0"],["!","1"],["I","1"],["|","1"],["S","5"],["E","8"]]
to_huruf=[["e","O"],["0","O"],["!","I"],["1","I"],["|","I"],["5","S"],["8","O"],["7","L"]]
kode_plat = ["BL","BB","BK","BA","BM","BP","BG","BN","BE","BD","BH","A",\
            "B","D","E","F","T","Z","G","H","K","R","AA","AB","AD","L","M","N","P",\
            "S","W","AE","AG","DK","DR","EA","DH","EB","ED","KB","DA","KH","KT",\
            "DB","DL","DM","DN","DT","DD","DC","DE","DG","DS"]
data_huruf = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",\
            "Q","R","S","T","U","V","W","X","Y","Z"]
kode_plat =set (kode_plat)

def toRgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def toBin(img,tre):
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
    
    pl0 = ""
    pl1 = ""
    pl2 = ""
    #get plat kota
    for i in range(0,2):
        try:
            if(type(int(plat[i])))==int:
                # pl0+=replaceToHuruf(plat[i])
                if plat[i] in kode_plat:
                    pl0+=replaceToHuruf(plat[i])
        except ValueError:
            val = pl0+plat[i]
            if val in kode_plat:
                pl0+=plat[i]
        # if pl0 in kode_plat:
        #     break

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
                if plat[i] in data_huruf:
                    pl2+=replaceToHuruf(plat[i])
                    l+=1
        except ValueError:
            if plat[i] in data_huruf:
                pl2+=plat[i]
                l+=1
            else:
                pl2+=replaceToHuruf(plat[i])
                l+=1
        if l>2:
            break


    # plat=pl0+"-"+pl1+"-"+pl2
    return pl0,pl1,pl2

def removeSymbol(val):
    val  = re.sub("[^0-9a-zA-Z]","",val)
    return val
val = 0

def ocrNum(img):
    global val
    plate = ""
    tres = 60
    max_tres = 210
    imgProc=img
    while tres < max_tres:
        imgProc = toBin(img,tres)
        imgProc = gaussianBlur(imgProc)
        extracted_text_mod = ocr_core(imgProc)
        extracted_text_mod=removeSymbol(extracted_text_mod)
        #cv2.imshow(f't: {tres} : {extracted_text_mod}', imgProc)
        # print(extracted_text_mod)
        if len(extracted_text_mod) > 6:
            pl0,pl1,pl2  = getPlat(extracted_text_mod)
            if pl0 !="" and pl1 !="" and pl2 !="" and len(pl1)>3:
                print(tres)
                val+=tres
                plate = pl0+"-"+pl1+"-"+pl2
                break
        tres+=1
    return plate,imgProc,tres



###############
# nopol = input("nomor gambar : ")
# originalImage = cv2.imread('data/plate'+nopol+'.png')
# originalImage = toRgb(originalImage)
# originalImage = toGray(originalImage)
# imgProc = cropImg(originalImage)

# w,h = imgProc.shape
# total = w*h
# bl = np.sum(imgProc >= 127) / total *100
# wh = np.sum(imgProc < 127) / total *100

# tre=t.getTresh(bl,wh)

# print(f'{bl} | {wh} -> t: {tre}')

# imgProc = toBin(imgProc,tre)
# imgProc = gaussianBlur(imgProc)
# extracted_text_ori = ocr_core(originalImage)

# now = time.time()
# extracted_text = ocr_core(imgProc)
# print(f"original : {extracted_text_ori}\n processing : {extracted_text} \ntime : {time.time()-now}")
# cv2.imshow('output', imgProc)
# cv2.imshow('original', originalImage)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


#########
i=1
grayVal['data']=[]
d=0
now  = time.time()
jum=0
while i < 101 :
    originalImage = cv2.imread('data/plate'+str(i)+'.png')
    originalImage = toRgb(originalImage)
    originalImage = toGray(originalImage)
    imgProc = cropImg(originalImage)
    w,h = imgProc.shape
    total = w*h
    bl = np.sum(imgProc >= 127) / total *100
    wh = np.sum(imgProc < 127) / total *100
    extracted_text_ori = ocr_core(originalImage)

    #######

    tre=t.getTresh(bl,wh)

    imgProc = toBin(imgProc,tre)
    imgProc = gaussianBlur(imgProc)
    extracted_text =ocr_core(imgProc)
    prc =time.time()
    if len(extracted_text) > 5:
        extracted_text_mod=removeSymbol(extracted_text)
        pl0,pl1,pl2  = getPlat(extracted_text_mod)
        if pl0 !="" and pl1!="" and pl2!="": 
            extracted_text=pl0+"-"+pl1+"-"+pl2
            jum+=time.time()-prc
            print(f'out : {extracted_text}, tres:{tre}, time: {jum}')
            d+=1
    i+=1
print(f'deteksi : {d}, t: {time.time()-now}, j: {jum}')
    #######

    # extracted_text,imgProc,tres = ocrNum(imgProc)
    # if extracted_text != "":
    #     print(f'v: {extracted_text}. t: {time.time()-now}')
    #     print(f"black : {bl}, wh : {wh}\n")
    #     grayVal['data'].append({
    #         'plate':extracted_text,
    #         'treshold':tres,
    #         'b':bl,
    #         'w':wh
    #     })
    # i+=1
# with open('data1.txt','w') as outfile:
#     json.dump(grayVal,outfile)
# ############

#     cv2.imshow('original'+str(i), imgProc)


# print(f"rata-rata t : {val/19}")
# cv2.waitKey(0)
# cv2.destroyAllWindows()