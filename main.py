import cv2
from ocr_plate import Plate
import time
plate = Plate()
# nopol = input("no img : ")
nopol = 1
while nopol < 101:
    originalImage = cv2.imread('data/plate'+str(nopol)+'.png')
    originalImage = plate.toRgb(originalImage)
    now = time.time()
    teks =plate.getText(originalImage)
    print(f'nomor plat : {teks}, t:{time.time()-now}')
    nopol+=1