import pytesseract
from PIL import Image
from scipy.ndimage import gaussian_filter
from scipy.ndimage import median_filter

#text = pytesseract.image_to_string(img)

img = Image.open('matrix.png')
#img = Image.fromarray(median_filter(np.array(img), size=5))
#img = Image.fromarray(gaussian_filter(np.array(img), sigma=2))
#print(img)
img = img.crop((0, 0, 600, 470))

text = pytesseract.image_to_string(img, config='--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

print(text)
