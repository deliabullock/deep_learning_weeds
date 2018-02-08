from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD

model = load_model('../kerastutorial/my_model_c_23_just_incorrect_best.h5')
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
	im.save('pics_out_train/' + img_name)
	print(img_name)

def test():
	image_info = pickle.load( open( "./data/train_picture_info.pkl", "rb" ) )
	i = 0
	for x in image_info:
		if i < 90:
			i += 1
			continue
		url = x["url"]
		output = get_output(url)
		make_image(output[0], output[1], url)
		#break

def get_output(url):
	print('in get_output')
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
	w, h = im.size
	out = []
	num_images_y = ((h - 299)/75) + 1
	num_images_x = ((w - 299)/75) + 1
	weed_images = [None] * (num_images_y*num_images_x)
	i = 0
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
			weed_images[i] = pic
			i += 1
			#if weed_images.shape == (1,1):
			#	weed_images = np.vstack([pic])
			#else:
			#	weed_images = np.vstack([weed_images, pic])
			x = x + step
		y = y + step
			
	weed_images = np.concatenate(weed_images, axis=0)
	weed_images = (1./255)*weed_images
	#print(model.predict(weed_images, batch_size=32, verbose=0))
	print('about to predict')
	nonweed_classes = model.predict_classes(weed_images, batch_size=32)
	print('finished predicting')
	#print(len(nonweed_classes))
	#print(nonweed_classes)
	return [out, nonweed_classes]


test()
