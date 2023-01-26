import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import random
import dataframe_image as dfi
import math

for k in range(10):
    fig, ax = plt.subplots()

    background = (255,255,255)
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    matrix = np.array([[random.randint(0, 9),random.randint(0, 9),random.randint(0, 9)],
                        [random.randint(0, 9),"x",random.randint(0, 9)],
                        [random.randint(0, 9),random.randint(0, 9),random.randint(0, 9)]])

    df = pd.DataFrame(matrix)
    print(df)

    ax.table(cellText=df.values, loc='center')

    fig.tight_layout()

    #dfi.export(matrix,"matrix.png")
    plt.savefig('matrix.png', bbox_inches='tight')


    image = Image.new('RGB', (500, 100), background)

    draw = ImageDraw.Draw(image)







    #Generates a random string of arrows 
    def generate_random_arrowString(length):
        arrows = ['\u2190','\u2191','\u2192','\u2193','\u2196','\u2197','\u2198','\u2199']
        return np.random.choice(arrows, length)

    arrowArray = generate_random_arrowString(7)

    arrowString = ''.join(arrowArray)


    font = ImageFont.truetype('/Users/vincentpedersen/Desktop/dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf', 72)
    text_width, text_height = draw.textsize(arrowString, font=font)
    chars = list(arrowString)
    x, y = 0, 0

        # Iterate over each character in the text
    for i, c in enumerate(chars):
        #text_color = colors[i % len(colors)]

        draw.text((x + (i * 3), y), c, fill=(0,0,0), font=font)

        x += draw.textsize(c, font=font)[0]


    #Combines the matrix image and the arrow image 
    def get_concat_h(matrixImage, arrowImage):
        dst = Image.new('RGB', (matrixImage.width + arrowImage.width, matrixImage.height))
        dst.paste(matrixImage, (0, 0))
        dst.paste(arrowImage, (matrixImage.width, 0))
        return dst

    #Gets the solution, so the captcha can be saved with the solution name
    def getSolutiontoCapthca(arrowArray,matrix):
        solutionString = ""
        for i in arrowArray: 
            if i == '\u2190':
                solutionString += str(matrix[1][0])
            elif i == '\u2191':
                solutionString += str(matrix[0][1])
            elif i == '\u2192':
                solutionString += str(matrix[1][2])
            elif i == '\u2193':
                solutionString += str(matrix[2][1])
            elif i == '\u2196':
                solutionString += str(matrix[0][0])
            elif i == '\u2197':
                solutionString += str(matrix[0][2])
            elif i == '\u2198':
                solutionString += str(matrix[2][2])
            elif i == '\u2199':
                solutionString += str(matrix[2][0])
        
        return solutionString

    matrixImage = Image.open("matrix.png")

    #adding noise to arrow image
    image_array = np.array(image)

    im = image_array
    print(im.shape)

    noise = np.random.normal(0, 0.05, im.shape)
    im = im.astype(np.float32)
    im += noise 
    im = im.astype(np.uint8)

    im = np.random.poisson(im / 1.2)

    im = Image.fromarray(np.uint8(im))

    solutionString = getSolutiontoCapthca(arrowArray,matrix)
    get_concat_h(matrixImage, im).save('directionalCAPTCHALessNoise/' + solutionString + '.png')
