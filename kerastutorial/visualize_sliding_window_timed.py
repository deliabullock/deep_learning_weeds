from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD
import time
import pickle
start = time.time()

end = time.time()
print(end - start)
#model = load_model('../kerastutorial/my_model_c_part_2_with_more_data.h5')#my_model_c_23_just_incorrect_best.h5')#my_model_2_ballanced.h5')
model = load_model('../kerastutorial/my_model_c_23_just_incorrect_best.h5')#my_model_2_ballanced.h5')
end = time.time()
print(end - start)
def make_image(x_y_list, output, url, x_max, y_max):
        #response = requests.get(url)
        #im = Image.open(BytesIO(response.content))
    
    #if image_name == 'DSC07807.JPG':
	#im = Image.open(image_name)
	#im = image.load_img('./pics/' + url[url.rfind('/')+1:])
	#draw = ImageDraw.Draw(im,"RGBA")
	i = 0
	out = [None]*(y_max + 3)
	for j in range(len(out)):
		out[j] = [0]*(x_max + 3)
	for pic in x_y_list:
		if output[i] == 1:
			print(pic)
			for x in pic:
				out[x[1]][x[0]] = out[x[1]][x[0]] + 1
		i += 1
	#im.save('pics_out/' + img_name)
        img_name = url[url.rfind('/')+1:] 
	pickle.dump(out, open( img_name, "wb" ) )
	print(out)

	print('YEAHH')
	print(img_name)

def test():
	image_info = pickle.load( open( "./data/validate_picture_info.pkl", "rb" ) )
	for x in image_info:
		if len(x["weeds"]) == 0:
			continue
		url = x["url"]
		ip = 'http://128.84.3.178/ethan'
        	url = str(ip + url[25:])
		output = get_output(url)
		make_image(output[0], output[1], url, output[2], output[3])
		#break

def get_output(url):
	out = []
        #response = requests.get(url)
        #im = Image.open(BytesIO(response.content))
	im = Image.open('./pics/'+ url[url.rfind('/')+1:])
	#return
	w, h = im.size
	x = 0
	y = 0
	step = 75
	i = 0
	num_images_y = ((h - 299)/75) + 1
	num_images_x = ((w - 299)/75) + 1
	print(num_images_y)
	print(num_images_x)
	weed_images = [None] * (num_images_y*num_images_x)
	g_x = 0
	g_y = 0
	while y + 299 < h:
		x = 0
		g_x = 0
		while x + 299 < w:
			img = im.crop((x, y, x + 299, y + 299)) 
			out_tmp = []
			out_tmp.append([g_x, g_y])
			out_tmp.append([g_x, g_y + 1])
			out_tmp.append([g_x, g_y + 2])
			out_tmp.append([g_x, g_y + 3])
			out_tmp.append([g_x + 1, g_y])
			out_tmp.append([g_x + 1, g_y + 1])
			out_tmp.append([g_x + 1, g_y + 2])
			out_tmp.append([g_x + 1, g_y + 3])
			out_tmp.append([g_x + 2, g_y])
			out_tmp.append([g_x + 2, g_y + 1])
			out_tmp.append([g_x + 2, g_y + 2])
			out_tmp.append([g_x + 2, g_y + 3])
			out_tmp.append([g_x + 3, g_y])
			out_tmp.append([g_x + 3, g_y + 1])
			out_tmp.append([g_x + 3, g_y + 2])
			out_tmp.append([g_x + 3, g_y + 3])
			out.append(out_tmp)
			pic = image.img_to_array(img)
			pic = np.expand_dims(pic, axis=0)
			weed_images[i] = pic
			#if weed_images.shape == (1,1):
			#	weed_images = np.vstack([pic])
			#else:
			#	weed_images = np.vstack([weed_images, pic])
			i += 1
			g_x += 1
			#print(i)
			x = x + step
		y = y + step
		g_y = g_y + 1
	weed_images = np.concatenate(weed_images, axis=0)		
	weed_images = (1./255)*weed_images
	#print(model.predict(weed_images, batch_size=32, verbose=0))
	nonweed_classes = model.predict_classes(weed_images, batch_size=10)
	#print(len(nonweed_classes))
	#print(nonweed_classes)
        #pickle.dump(out, open( '1' + url[url.rfind('/')+1:], "wb" ) )
	return [out, nonweed_classes, g_x, g_y]


test()
end = time.time()
print(end - start)
