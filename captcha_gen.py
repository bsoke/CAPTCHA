from PIL import Image, ImageDraw, ImageFont
import random
import string
for j in range(1000):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Use the random values to create a color in the RGB format
    rand_background = (r, g, b)


    colors = [
        (255, 127, 0),  # orange
        (0, 255, 0),  # green
        (0, 0, 255),  # blue
        (75, 0, 130),  # indigo
    ]


    def generate_random_string(length):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    



    random_string = generate_random_string(8)
    image = Image.new('RGB', (225, 50), rand_background)
    draw = ImageDraw.Draw(image)

    # Noise, points
    for i in range(500):
        draw.point((random.randint(0, 400), random.randint(0, 50)), fill=(0, 0, 0))

    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 36)
    text_width, text_height = draw.textsize(random_string, font=font)

    chars = list(random_string)
    x, y = 0, 0
    text_color = colors[j % len(colors)]
    # Iterate over each character in the text
    for i, c in enumerate(chars):
        

        draw.text((x + (i * 3), y), c, fill=text_color, font=font)

        x += draw.textsize(c, font=font)[0]

    image.save("captchas/" + random_string + '.png')
    print(random_string)
