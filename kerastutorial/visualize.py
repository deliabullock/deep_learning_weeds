from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np

def make_image(picture_dict, output):
	url = picture_dict["url"]
	response = requests.get(url)
	im = Image.open(BytesIO(response.content))
	draw = ImageDraw.Draw(im,"RGBA")
	i = 0
	for key in picture_dict["weeds"]:
		x = picture_dict["weeds"][key]["x"]
		y = picture_dict["weeds"][key]["y"]
		if output[i] == 1:
			print "weed"
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (150,0,255,50))
		else:	
			print "weed not classified"
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (255,30,50,50))
		i += 1
	for key in picture_dict["nonweeds"]:
		x = picture_dict["nonweeds"][key]["x"]
		y = picture_dict["nonweeds"][key]["y"]
		if output[i] == 1:
			print "misclassified weed"
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (255,255,0,50))
		else:
			print "not weed"
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (20,30,50,50))
		i += 1
 
	im.save("url.jpg")

def test():
	image_info = pickle.load( open( "./data/test_picture_info.pkl", "rb" ) )
	for x in image_info:
		if len(x["weeds"]) == 0:
			continue
		leng = len(x["weeds"]) + len(x["nonweeds"])
		output = np.random.randint(2, size=leng)
		print output
		print "WEEDS"
		print x["weeds"]
		print "NONWEEDS"
		print x["nonweeds"]
		make_image(x, output)
		break

test()
