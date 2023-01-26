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
th4 = []
for i in res:
    image = Image.open("./pngs/" + i)
    img = cv.imread("./pngs/" + i, cv.IMREAD_GRAYSCALE)


    img = cv.GaussianBlur(img,(3,3),0)
    _, img = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    text = pytesseract.image_to_string(img)

    txtRemovedPng = i[:len(i) - 4]

    if text.strip() == txtRemovedPng:
        normalAmtCorrect += 1

    image = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    text4 = pytesseract.image_to_string(image)
    if text4.strip() == txtRemovedPng: 
        gaussianThrsAmtCorrect += 1
        

normal_accuracy = normalAmtCorrect / len(res)
gaussian_accuracy = gaussianThrsAmtCorrect / len(res)

print("The normal method got ", normalAmtCorrect, "correct out of ", len(res))
print("The gausian threshold got ", gaussianThrsAmtCorrect,"correct out of ", len(res) )
print("The normal accuracy is: ", normal_accuracy)
print("The gaussian accuracy is: ", gaussian_accuracy)

methods = ['Normal', 'Gaussian']
accuracies = [normal_accuracy, gaussian_accuracy]
plt.bar(methods, accuracies)
plt.ylim(0, 1)
plt.ylabel('Accuracy')
plt.show()

plt.pie([normalAmtCorrect, len(res)-normalAmtCorrect], labels=['Correct', 'Incorrect'], autopct='%1.1f%%', shadow=True)
plt.title('Normal Method')
plt.show()

plt.pie([gaussianThrsAmtCorrect, len(res)-gaussianThrsAmtCorrect], labels=['Correct', 'Incorrect'], autopct='%1.1f%%', shadow=True)
plt.title('Gaussian Threshold')
plt.show()

