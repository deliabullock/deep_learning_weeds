from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD

def make_image(x_y_list, output, url):
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
    
    #if image_name == 'DSC07807.JPG':
	#im = Image.open(image_name)
	draw = ImageDraw.Draw(im,"RGBA")
	i = 0
	for pic in x_y_list:
		x = pic[0]
		y = pic[1]
		if output[i] == 1:
			draw.polygon([(x, y),(x + 299, y),(x + 299, y + 299),( x, y + 299)], (150,0,255,10))
		i += 1
	
	print('YEAHH')
        img_name = url[url.rfind('/')+1:] 
	im.save(img_name)
	print(img_name)

def test():
	image_info = pickle.load( open( "./data/validate_picture_info.pkl", "rb" ) )
	for x in image_info:
		if len(x["weeds"]) != 0:
			continue
		url = x["url"]
		ip = 'http://128.84.3.178/ethan'
        	url = str(ip + url[25:])
		output = get_output(url)
		make_image(output[0], output[1], url)
		#break

def get_output(url):
	out = []
	model = load_model('../kerastutorial/my_model_2_ballanced.h5')
	weed_images = np.empty((1,1))
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
	w, h = im.size
	x = 0
	y = 0
	step = 75
	while y + 299 < h:
		x = 0
		while x + 299 < w:
			img = im.crop((x, y, x + 299, y + 299)) 
			out.append([x, y])
			pic = image.img_to_array(img)
			pic = np.expand_dims(pic, axis=0)
			if weed_images.shape == (1,1):
				weed_images = np.vstack([pic])
			else:
				weed_images = np.vstack([weed_images, pic])
			x = x + step
		y = y + step
			
	weed_images = (1./255)*weed_images
	print(model.predict(weed_images, batch_size=32, verbose=0))
	nonweed_classes = model.predict_classes(weed_images, batch_size=10)
	print(len(nonweed_classes))
	print(nonweed_classes)
	return [out, nonweed_classes]


test()
