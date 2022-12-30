import pytesseract
from PIL import Image, ImageDraw, ImageFont

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\baris\anaconda3\Lib\site-packages\tesseract.exe'

image = Image.open('captcha.png')

image = image.convert('L')

text = pytesseract.image_to_string(image)

print(text)
