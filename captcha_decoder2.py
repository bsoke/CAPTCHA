import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
from matplotlib import pyplot as plt
import os
from operator import itemgetter


image = Image.open("0akoQiOU.png")
img = cv.imread("0akoQiOU.png")





image = image.convert('L')

##To visualize
plt.imshow(image,'gray')
plt.show()


blur = cv.GaussianBlur(img,(5,5),0)
th4 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

plt.imshow(th4,'gray')
plt.show()