from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD

model = load_model('../kerastutorial/my_model_c_with_64_only_900_best_21.h5')
# Annotations from Mech Turk
#Batch_2667541_batch_results
image_mt_turk_dict  = pickle.load( open( "./data/mechanical_turkers_data.pkl"))
color_list = [(0,0,255,255), (255,0, 0, 255), (0, 255, 0,255), (0,255,255,255)]


def make_image(x_y_list, output, url):
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
    
	draw = ImageDraw.Draw(im,"RGBA")
	i = 0
	for pic in x_y_list:
		x = pic[0]
		y = pic[1]
		if output[i] == 1:
			draw.polygon([(x, y),(x + 299, y),(x + 299, y + 299),( x, y + 299)], (150,0,255,10))
		i += 1
	
	##### go in dict and draw squares
        img_name = url[url.rfind('/')+1:] 
	mt_squares = image_mt_turk_dict[img_name]
	print(len(mt_squares))
	for i in range(len(mt_squares)):
		color = color_list[i]
		dim_list = mt_squares[i]
		for x in dim_list:
			#draw all four lines
			draw.line([x[0], x[1]], fill=color, width=4)
			draw.line([x[1], x[2]], fill=color, width=4)
			draw.line([x[2], x[3]], fill=color, width=4)
			draw.line([x[3], x[0]], fill=color, width=4)
			#draw.polygon(x,fill=None, outline=color)
	im.save('pics_900_2_out/' + img_name)
	print(img_name)

def test():
	image_info = pickle.load( open("./data/validate_full_image_info.pkl", "rb" ) )
	for x in image_info:
		url = x[0]
		output = get_output(url)
		make_image(output[0], output[1], url)
		#break

def get_output(url):
	print('in get_output')
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
	w, h = im.size
	out = []
	step = 100
	num_images_y = ((h - 299)/step) + 1
	num_images_x = ((w - 299)/step) + 1
	weed_images = [None] * (num_images_y*num_images_x)
	i = 0
	x = 0
	y = 0
	while y + 299 < h:
		x = 0
		while x + 299 < w:
			dim = get_cropped_dim(x, y, w, h)
			if dim != None:
				img = dim.resize((300, 300), Image.ANTIALIAS)
				out.append([x, y])
				pic = image.img_to_array(img)
				pic = np.expand_dims(pic, axis=0)
				weed_images[i] = pic
				i += 1
			x = x + step
		y = y + step
			
	weed_images = np.concatenate(weed_images, axis=0)
	weed_images = (1./255)*weed_images
	print('about to predict')
	nonweed_classes = model.predict_classes(weed_images, batch_size=32)
	print('finished predicting')
	return [out, nonweed_classes]

def get_image_dims(curr_x, curr_y, w, h):
        Top, Bottom, Left, Right = False, False, False, False

        if curr_x - 300 > 0:
            low_x = curr_x-300
        else:
            Left = True
            low_x = 1
        if curr_x + 598 <= w:
            high_x = curr_x+598
        else:
            Right = True
            high_x = w

        if curr_y - 300 > 0:
            low_y = curr_y-300
        else:
            Top = True
            low_y = 1
        if curr_y + 598 <= h:
            high_y = curr_y+598
        else:
            Bottom = True
            high_y = h
        return ((low_x, low_y, high_x, high_y), Top, Bottom, Left, Right)

def get_cropped_dim(x, y, w, h)
        (low_x, low_y, high_x, high_y), Top, Bottom, Left, Right = get_image_dims(x, y, w, h)

	if not (Top or Bottom or Left or Right):
		croppedim = im.crop((low_x, low_y, high_x, high_y))
						
	if Left and not (Top or Bottom):
	    crop = im.crop((x, low_y, high_x, high_y))
	    stretch = im.crop((low_x, low_y, x, high_y))
	    stretch = stretch.resize((300, 898))
	    croppedim = Image.new('RGB', (898, 898))
	    croppedim.paste(stretch, (0, 0, 300, 898))
	    croppedim.paste(crop, (300, 0, 898, 898))

	if Right and not (Top or Bottom):
	    crop = im.crop((low_x, low_y, x+298, high_y))
	    stretch = im.crop((x+298, low_y, high_x, high_y))
	    stretch = stretch.resize((300, 898))
	    croppedim = Image.new('RGB', (898, 898))
	    croppedim.paste(stretch, (598, 0, 898, 898))
	    croppedim.paste(crop, (0, 0, 598, 898))

	#Done but check that dimensions are really 898 and if its ok to start low_x at 1
	if Top and not (Left or Right):
	    crop = im.crop((low_x, y, high_x, high_y))
	    stretch = im.crop((low_x, low_y, high_x, y))
	    stretch = stretch.resize((898, 300))
	    croppedim = Image.new('RGB', (898, 898))
	    croppedim.paste(stretch, (0, 0, 898, 300))
	    croppedim.paste(crop, (0, 300, 898, 898))

	if Bottom and not (Left or Right):
	    crop = im.crop((low_x, low_y, high_x, y +298))
	    stretch = im.crop((low_x, y + 298, high_x, high_y))
	    stretch = stretch.resize((898, 300))
	    croppedim = Image.new('RGB', (898, 898))
	    croppedim.paste(stretch, (0, 598, 898, 898))
	    croppedim.paste(crop, (0, 0, 898, 598))

	#Check if it is a corner
	if ((Left and Top) or (Left and Bottom) or (Right and Top) or (Right and Bottom)):
	    return None
	return croppedim

test()
