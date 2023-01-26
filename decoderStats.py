import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv
from matplotlib import pyplot as plt
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\baris\anaconda3\Lib\site-packages\tesseract.exe'

dir_path = r'C:\Users\baris\Desktop\KU\COMP430\CAPTCHA\pngs'

res = []
normal_accuracy = []
gaussian_accuracy = []

for path in os.listdir(dir_path):
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

    txtRemovedPng = i[:len(i) - 4]
    
    if text.strip() == txtRemovedPng:
        normalAmtCorrect += 1
    
    if text4.strip() == txtRemovedPng: 
        gaussianThrsAmtCorrect += 1
    #else: 
        #print(txtRemovedPng)
        #print(text4.strip())

normal_accuracy = normalAmtCorrect / len(res)
gaussian_accuracy = gaussianThrsAmtCorrect / len(res)

plt.bar(['Normal', 'Gaussian Threshold'], [normal_accuracy, gaussian_accuracy])
plt.ylim(0, 1)
plt.ylabel('Accuracy')
plt.show()

plt.pie([normalAmtCorrect, len(res)-normalAmtCorrect], labels=['Correct', 'Incorrect'], autopct='%1.1f%%', shadow=True)
plt.title('Normal Method')
plt.show()

plt.pie([gaussianThrsAmtCorrect, len(res)-gaussianThrsAmtCorrect], labels=['Correct', 'Incorrect'], autopct='%1.1f%%', shadow=True)
plt.title('Gaussian Threshold')
plt.show()

fileNames = [i[:len(i) - 4] for i in res]
accuracyNormal = [normalAmtCorrect/len(res) if fileNames[i] == text.strip() else 1-normalAmtCorrect/len(res) for i in range(len(res))]
accuracyGaussian = [gaussianThrsAmtCorrect/len(res) if fileNames[i] == text4.strip() else 1-gaussianThrsAmtCorrect/len(res) for i in range(len(res))]

plt.plot(fileNames, accuracyNormal, label='Normal Method')
plt.plot(fileNames, accuracyGaussian, label='Gaussian Threshold')
plt.xlabel('Captcha File Name')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

plt.hist([normalAmtCorrect, len(res)-normalAmtCorrect], bins=[0,1,2], label=['Correct', 'Incorrect'])
plt.title('Normal Method')
plt.xlabel('No of Captchas')
plt.ylabel('Frequency')
plt.legend()
plt.show()

plt.hist([gaussianThrsAmtCorrect, len(res)-gaussianThrsAmtCorrect], bins=[0,1,2], label=['Correct', 'Incorrect'])
plt.title('Gaussian Threshold')
plt.xlabel('No of Captchas')
plt.ylabel('Frequency')
plt.legend()
plt.show()



