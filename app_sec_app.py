import PIL
from PIL import Image

image_name = input("Enter image's name (ex. ~/Downloads/lake.jpg): ")

ext = image_name[image_name.rfind("."):]

width = int(input("Enter width to resize to (ex. 300): "))

img = Image.open(image_name)

img = img.resize((width, width), Image.ANTIALIAS)

img.save(image_name[:-len(ext)] + "_square" + ext)