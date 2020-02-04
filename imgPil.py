import cv2
import numpy as np
from PIL import Image

pil_image=Image.open("data/plate2.png") # open image using PIL

#process
gray = pil_image.convert('L')

# Let numpy do the heavy lifting for converting pixels to pure black or white
bw = np.asarray(gray).copy()

# Pixel range is 0...255, 256/2 = 128
bw[bw < 128] = 0    # Black
bw[bw >= 128] = 255 # White

# Now we put it back in Pillow/PIL land
imfile = Image.fromarray(bw)
#end process

# use numpy to convert the pil_image into a numpy array
numpy_image=np.array(imfile)  

# convert to a openCV2 image, notice the COLOR_RGB2BGR which means that 
# the color is converted from RGB to BGR format
opencv_image=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR) 

cv2.imshow('output', opencv_image)
cv2.waitKey(0)
cv2.destroyAllWindows()