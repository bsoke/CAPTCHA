import pytesseract
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from ExtractTable import ExtractTable
import pandas as pd


pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/5.3.0_1/bin/tesseract'
#this arrow finding is taken from https://stackoverflow.com/questions/66718462/how-to-detect-different-types-of-arrows-in-image
#Had to change the epsilon though, as the arrows used aren't as "arrowy" as the ones in the post
def preprocess(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 50, 50)
    kernel = np.ones((3, 3))
    img_dilate = cv2.dilate(img_canny, kernel, iterations=2)
    img_erode = cv2.erode(img_dilate, kernel, iterations=1)   
    return img_erode

def find_tip(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = indices[i] + 2
        if j > length - 1:
            j = length - j
        
       
        if np.all(points[j] == points[indices[i - 1] - 2]):
            return tuple(points[j])

def find_bottom(points, convex_hull):
    length = len(points)
    indices = np.setdiff1d(range(length), convex_hull)

    for i in range(2):
        j = indices[i] + 1
        
        if j > length - 1:
            j = length - j
    
        if np.all(points[j] == points[indices[i - 1] - 1]):
            return tuple(points[j])


def determineDirection(arrow_tip,arrow_bottom):
    uncertainty = 10
    if abs(arrow_tip[1] - arrow_bottom[1]) > uncertainty and abs(arrow_tip[0] - arrow_bottom[0]) > uncertainty:
        if arrow_tip[1] < arrow_bottom[1] and arrow_tip[0] < arrow_bottom[0]:
            direction = "northWest"
        elif arrow_tip[1] < arrow_bottom[1] and arrow_tip[0] > arrow_bottom[0]:
            direction = "northEast"
        elif arrow_tip[1] > arrow_bottom[1] and arrow_tip[0] < arrow_bottom[0]:
            direction = "southWest"
        else: 
            direction = "southEast"

    elif abs(arrow_tip[1] - arrow_bottom[1]) > uncertainty:
        if arrow_tip[1] < arrow_bottom[1]:
            direction = "up"
        else: 
            direction = "down"

    elif abs(arrow_tip[0] - arrow_bottom[0]) > uncertainty:
        if arrow_tip[0] < arrow_bottom[0]:
            direction = "left"
        else: 
            direction = "right"
    
    
    return direction
    


fileString = "directionalCAPTCHALessNoise/2009493.png"
img = cv2.imread(fileString)
img2 = Image.open("matrix.png")

contours, hierarchy = cv2.findContours(preprocess(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

directionArray = []
count = 0 
for cnt in contours:
    peri = cv2.arcLength(cnt, True)
    #Controls how sensitive it is in determining arrows
    epsilon = 0.05
    approx = cv2.approxPolyDP(cnt, epsilon * peri, True)
    hull = cv2.convexHull(approx, returnPoints=False)
    sides = len(hull)
   
    
    if 6 > sides > 3 and sides + 2 == len(approx):
        arrow_tip = find_tip(approx[:,0,:], hull.squeeze())
        arrow_bottom = find_bottom(approx[:,0,:], hull.squeeze())
        print(arrow_tip)
        print(arrow_bottom)
        colors = [(0,0,0),(255,0,0),(255,255,0),(0,0,255),(0,255,255),(255,0,255),(255,255,0),(0,0,255)]
        if arrow_tip and arrow_bottom:
            cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)
            cv2.circle(img, arrow_tip, 3, colors[count], cv2.FILLED)
            cv2.circle(img, arrow_bottom, 3, (0, 0, 255), cv2.FILLED)
            direction = determineDirection(arrow_tip,arrow_bottom)
            directionDict = {
                "x-tip":arrow_tip[0],
                "direction": direction
            }
            directionArray.append(directionDict)
            count += 1
            print(direction)

sortedDirectionArray = sorted(directionArray, key=lambda d: d['x-tip']) 
print(sortedDirectionArray)
#extract table data
et_sess = ExtractTable(api_key="DQXaKPkMGfBqQ5J3LNkcToUXrMXT0CiZwzgX8CXr")        # Replace your VALID API Key here
print(et_sess.check_usage())        # Checks the API Key validity as well as shows associated plan usage 
table_data = et_sess.process_file(filepath=fileString, output_format="df")

print(table_data[0].at[0,'0'])





solutionString = ""
for i in sortedDirectionArray:
    if i["direction"] == "northWest":
        solutionString += table_data[0].at[0,'0']
    elif i["direction"] == "northEast":
        solutionString += table_data[0].at[0,'2']
    elif i["direction"] == "southWest":
        solutionString += table_data[0].at[2,'0']
    elif i["direction"] == "southEast":
        solutionString += table_data[0].at[2,'2']
    elif i["direction"] == "up":
        solutionString += table_data[0].at[0,'1']
    elif i["direction"] == "down":
        solutionString += table_data[0].at[2,'1']
    elif i["direction"] == "left":
        solutionString += table_data[0].at[1,'0']
    elif i["direction"] == "right":
        solutionString += table_data[0].at[1,'2']


print(solutionString)
    



cv2.imshow("Image", img)
cv2.waitKey(0)