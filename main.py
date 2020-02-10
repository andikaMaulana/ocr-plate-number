import cv2
from ocr_plate import Plate
import time
plate = Plate()
# nopol = input("no img : ")
# nopol = 0
# d=0
# now = time.time()
# while nopol < 101:
#     originalImage = cv2.imread('data/plate'+str(nopol)+'.png')
#     originalImage = plate.toRgb(originalImage)

#     read = time.time()
#     teks =plate.getText(originalImage)
#     if teks != "":
#         print(f'nomor plat : {teks}, t:{time.time()-read}')
#         d+=1
#     nopol+=1
# print(f' deteksi : {d}, t: {time.time()-now}')


##################
# img = cv2.imread('data/9.png')
# img = plate.toRgb(img)
# now =time.time()
# img = plate.toGray(img)
# img = plate.toBin(img,90)
# img =plate.gaussianBlur(img)
# img = plate.rotateImg(img,353)
# img = plate.cropImg(img,20,30,20,20)
# teks =plate.ocr_core(img)
# print(f'time : {time.time()-now}')
################

img = cv2.imread('data/plate999.png')
img = plate.toRgb(img)
now =time.time()
img = plate.toGray(img)
img = plate.toBin(img,127)
# img =plate.toTreshOtsu(img)
img =plate.gaussianBlur(img)
img = plate.rotateImg(img,9)
img = plate.cropImg(img,14,16,3,3)
teks =plate.ocr_core(img)
print(f'plate : {teks} time : {time.time()-now}')

# def getTeks(img):
#     img = plate.toGray(img)
#     img = plate.toBin(img,90)
#     img =plate.gaussianBlur(img)
#     img = plate.rotateImg(img,353)
#     img = plate.cropImg(img,20,30,20,20)
#     teks =plate.ocr_core(img)
#     return teks
#########################
cv2.imshow(f'{teks}', img)
cv2.waitKey(0)