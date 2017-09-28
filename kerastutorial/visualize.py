from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image

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
		print "hey"
		if len(x["weeds"]) == 0:
			continue
		output = get_output(x)
		make_image(x, output)
		break

def get_output(picture_dict):
	model = load_model('../kerastutorial/my_model.h5')
	for key in picture_dict["weeds"]:
		img = image.load_img(key, target_size=(299, 299))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)

		images = np.vstack([x])
		classes = model.predict_classes(images, batch_size=10)
		print classes
		break
	return []
		## add x		
	#for key in picture_dict["nonweeds"]:
		## add x
	


test()
