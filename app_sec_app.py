import PIL
from PIL import Image

width = int(input("Enter width: "))

img = Image.open("lake.jpg")

img = img.resize((width, width), Image.ANTIALIAS)

img.save("sqlake.jpg")