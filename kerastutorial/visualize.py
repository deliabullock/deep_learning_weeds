from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD

def make_image(picture_dict, output):
        url = picture_dict["url"]
    #image_name = url[url.find('DSC'):]
        ip = 'http://128.84.3.178'
        url = str(ip + url[25:])	
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
    
    #if image_name == 'DSC07807.JPG':
	#im = Image.open(image_name)
	draw = ImageDraw.Draw(im,"RGBA")
	i = 0
	#print(output)
	#print(len(picture_dict['weeds']))
	#print(len(picture_dict['nonweeds']))
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
		print(output)
		if output[i] == 1:
			print "misclassified weed"
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (255,255,0,50))
		else:
			print "not weed"
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (20,30,50,50))
		i += 1
	
	print('YEAHH')
        img_name = url[url.rfind('/')+1:] 
	im.save(img_name)

def test():
	image_info = pickle.load( open( "./data/test_picture_info.pkl", "rb" ) )
	for x in image_info:


    	    #url = x["url"]
	    #print(url)
    	    #image_name = url[url.find('DSC'):]
	#ip = '128.84.3.178'
	#url = ip + url	
	#response = requests.get(url)
	#im = Image.open(BytesIO(response.content))
    	    #if image_name == 'DSC07807.JPG':

		print "hey"
		if len(x["weeds"]) == 0:
			continue
		output = get_output(x)
		make_image(x, output)
		#break

def get_output(picture_dict):
	model = load_model('../kerastutorial/my_model_2_ballanced.h5')
	#lrate = 0.01 ### HERE
	#epochs = 5	
	#decay = lrate/epochs
	#sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
	#model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
	weed_images = np.empty((1,1))
	#weed_classes
	
	for key in picture_dict["weeds"]:
		img = image.load_img(key, target_size=(299, 299))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		if weed_images.shape == (1,1):
			weed_images = np.vstack([x])
			#print(weed_images.shape)
			#print(len(weed_images))
		else:
			weed_images = np.vstack([weed_images, x])
			#print(weed_images)
		#images = np.vstack([x])
		#print(weed_images.shape)
		#print(weed_images)
	weed_images = (1./255)*weed_images
	#print(weed_images)
	print(model.predict(weed_images, batch_size=32, verbose=0))
	weed_classes = model.predict_classes(weed_images, batch_size=10)
	#weed_classes = model.predict_on_batch(weed_images[:32])
	print(len(weed_classes))
	print(weed_classes)
		#print classes
		#break
	#return classes
		## add x		
	#for key in picture_dict["nonweeds"]:
		## add x
	
	nonweed_images = np.empty((1,1))
	#nonweed_classes
	for key in picture_dict["nonweeds"]:
		img = image.load_img(key, target_size=(299, 299))
		x = image.img_to_array(img)
		x = np.expand_dims(x, axis=0)
		if nonweed_images.shape == (1,1):
			nonweed_images = np.vstack([x])
			#print(nonweed_images)
		else:
			nonweed_images = np.vstack([nonweed_images, x])
			#print(nonweed_images)
		#images = np.vstack([x])
		#print(nonweed_images.shape)
		#print(nonweed_images)
	nonweed_images = (1./255)*nonweed_images
	#print(nonweed_images)
	print(model.predict(nonweed_images, batch_size=32, verbose=0))
	nonweed_classes = model.predict_classes(nonweed_images, batch_size=10)
	#nonweed_classes = model.predict_on_batch(nonweed_images[:32])
		#print(len(nonweed_classes))
	print(len(nonweed_classes))
	print(nonweed_classes)
		#print classes
		#break
	#return classes
	print('yoooo')
	return np.append(weed_classes, nonweed_classes)


test()
