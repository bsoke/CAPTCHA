import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
from matplotlib import pyplot as plt
import os
from operator import itemgetter

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.0_1/bin/tesseract'

image = Image.open('captcha.png')

image = image.convert('L')

text = pytesseract.image_to_string(image)

# folder path
dir_path = r'/Users/vincentpedersen/Desktop/CAPTCHA/captchas'

# list to store files
res = []

# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        res.append(path)

normalAmtCorrect = 0
gaussianThrsAmtCorrect = 0

for i in res:

    image = Image.open(dir_path + "/" + i)
    img = cv.imread(dir_path + "/" +  i,0)



    image = image.convert('L')

    #Test

    image2 = Image.new("P", image.size,255)
    temp = {}
    his = image.histogram()



    # values = {}

    # for i in range(256):
    #     values[i] = his[i]

    # for j,k in sorted(values.items(), key= itemgetter(1), reverse=True)[:10]:
    #     print j,k

    # for x in range(image.size[1]):
    #     for y in range(image.size[0]):
    #         pix = image.getpixel((y,x))
    #         temp[pix] = pix
    #         if pix == 220or pix == 227:  # these are the numbers to get
    #             image2.putpixel((y,x),0)


    blur = cv.GaussianBlur(img,(5,5),0)
    ret3,th4 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)


    text = pytesseract.image_to_string(image)
    text4 = pytesseract.image_to_string(th4)

   

    #Remove the .png from the file so we can compare how many each method got right

    text = text.strip()
    text4 = text4.strip()
    txtRemovedPng = i[:len(i) - 4]
    if len(text) > 8: 
        text = text[:8]
    if len(text4) > 8:
        text4 = text4[:8]


    if text == txtRemovedPng:
        normalAmtCorrect += 1
    
    if text4 == txtRemovedPng: 
        gaussianThrsAmtCorrect += 1
    else: 
        print(txtRemovedPng)
        print(text4.strip())

   ##To visualize
    # plt.imshow(th4,'gray')
    # plt.show()

print("The normal method got ", normalAmtCorrect, "correct out of ", len(res))
print("The gausian threshold got ", gaussianThrsAmtCorrect,"correct out of ", len(res) )



    
