import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
from matplotlib import pyplot as plt
import os


#pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.0'



# folder path
dir_path = r'/Users/vincentpedersen/Desktop/CAPTCHA/pngs'

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

    image = Image.open("./pngs/" + i)
    img = cv.imread("./pngs/" + i,0)



    image = image.convert('L')
    blur = cv.GaussianBlur(img,(5,5),0)
    ret3,th4 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)


    text = pytesseract.image_to_string(image)
    text4 = pytesseract.image_to_string(th4)

   

    #Remove the .png from the file so we can compare how many each method got right
    txtRemovedPng = i[:len(i) - 4]
    
    if text.strip() == txtRemovedPng:
        normalAmtCorrect += 1
    
    if text4.strip() == txtRemovedPng: 
        gaussianThrsAmtCorrect += 1
    else: 
        print(txtRemovedPng)
        print(text4.strip())

   
    

print("The normal method got ", normalAmtCorrect, "correct out of ", len(res))
print("The gausian threshold got ", gaussianThrsAmtCorrect,"correct out of ", len(res) )

##To visualize
# plt.imshow(th4,'gray')
# plt.show()

    
