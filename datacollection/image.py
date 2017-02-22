from PIL import Image
import ast
import requests
from io import BytesIO

# Gets image from web - doesn't save raw image
response = requests.get('http://server.genobyte.us/ethan/weed_cover_images/goreLab_08_12_2016/DSC08069.JPG')
im = Image.open(BytesIO(response.content))

# crops and saves image
im = im.crop((1600, 20, 3560, 1373))
im.save("img4.jpg")

