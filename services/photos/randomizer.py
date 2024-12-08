import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ImageRandomizer:

    def __init__(self, image):
        self.path = f'{image}'
        self.image = Image.open(self.path)
        self.image = self.image.convert('RGB')

    def size(self):
        width, height = self.image.size
        new_width = random.randint(600, 800)
        new_height = int(new_width * height / width)
        self.image = self.image.resize((new_width, new_height), Image.ANTIALIAS)
        return self

    def blur(self):
        x = random.randint(10, 50)
        y = random.randint(100, 240)
        box = (x, x, y, y)
        crop_img = self.image.crop(box)

        for _ in range(10):
            crop_img = crop_img.filter(ImageFilter.BLUR)

        self.image.paste(crop_img, box)
        return self

    def text(self):
        text = "High Tatras"
        font = ImageFont.truetype(os.getcwd() + '/services/photos/fonts/arial.ttf', size=random.randint(14, 48))
        draw = ImageDraw.Draw(self.image)
        draw.text((random.randint(20, 70), random.randint(20, 70)), text, font=font)
        return self

    def save(self):
        self.image.save(self.path)
        return self.path
