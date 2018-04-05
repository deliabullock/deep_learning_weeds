from PIL import ImageFont, Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD

PURPLE = (150,0,255,20)
DARK_PURPLE = (150,0,255,180)
RED = (255,30,50,50)
YELLOW = (255,255,0,50)
GRAY = (20,30,50,20)
MEDIUM_GRAY = (20,30,50,50)
DARK_GRAY = (20,30,50,180)
model = load_model('../kerastutorial/my_model_c_23_just_incorrect_best.h5')

def make_image(picture_dict, output):
        url = picture_dict["url"]
        response = requests.get(url)
	print(url)
        im = Image.open(BytesIO(response.content))
    
	draw = ImageDraw.Draw(im,"RGBA")
	i = 0
	for key in picture_dict["weeds"]:
		x = picture_dict["weeds"][key]["x"]
		y = picture_dict["weeds"][key]["y"]
		if output[i] == 1:
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], MEDIUM_GRAY)#(150,0,255,50))
		else:	
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], RED)#(255,30,50,50))
		i += 1
	for key in picture_dict["nonweeds"]:
		x = picture_dict["nonweeds"][key]["x"]
		y = picture_dict["nonweeds"][key]["y"]
		print(output)
		if output[i] == 1:
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], RED)#(255,255,0,50))
		else:
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], MEDIUM_GRAY)#(20,30,50,50))
		i += 1
	
	print('YEAHH')
        img_name = url[url.rfind('/')+1:] 
	im.save('./pics_out/' + img_name)
	print(img_name)

def make_groundtruth(picture_dict):
        url = picture_dict["url"]
        response = requests.get(url)
	print(url)
        im = Image.open(BytesIO(response.content))
    
	draw = ImageDraw.Draw(im,"RGBA")
	fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
	i = 0
	for key in picture_dict["weeds"]:
		x = picture_dict["weeds"][key]["x"]
		y = picture_dict["weeds"][key]["y"]
		draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], PURPLE, outline=DARK_PURPLE)
		draw.text((x, y), picture_dict["weeds"][key]["num"], font=fnt, fill=(255,255,255,200))
		i += 1
	for key in picture_dict["nonweeds"]:
		x = picture_dict["nonweeds"][key]["x"]
		y = picture_dict["nonweeds"][key]["y"]
		draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], GRAY, outline=DARK_GRAY)
		draw.text((x, y), picture_dict["nonweeds"][key]["num"], font=fnt, fill=(255,255,255,200))
		i += 1
	
	print('YEAHH')
        img_name = url[url.rfind('/')+1:] 
	im.save('./pics_out/' + img_name)
	print('./validate_ground_truth/' + img_name)





def test():
	image_info = pickle.load( open( "./data/validate_picture_info.pkl", "rb" ) )
	for x in image_info:
		output = get_output(x)
		make_image(x, output)
		#break

def get_output(picture_dict):
	image_list = [None] * (len(picture_dict["weeds"]) + len(picture_dict["nonweeds"]))
	i = 0	
	for key in picture_dict["weeds"]:
		img = image.load_img(key, target_size=(299, 299))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		image_list[i] = x
		i += 1
	for key in picture_dict["nonweeds"]:
		img = image.load_img(key, target_size=(299, 299))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		image_list[i] = x
		i += 1
	size = len(picture_dict["weeds"]) + len(picture_dict["nonweeds"])
	print(size)
	print(i)
	image_list = np.concatenate(image_list, axis=0)
	image_list = (1./255)*image_list
	classes = model.predict_classes(image_list, batch_size=19)
	return classes
test()
