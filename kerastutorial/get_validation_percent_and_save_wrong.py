from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from collections import Counter
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.optimizers import SGD
import time
from keras.models import load_model
from keras.callbacks import Callback, ModelCheckpoint
import glob
import os
from keras.preprocessing import image
import numpy as np
from PIL import Image, ImageDraw 
import pickle
start = time.time()

train_data_dir = '../datacollection/data/train'
validation_data_dir = '../datacollection/data/validate'
test_data_dir = '../datacollection/data/test'
got_wrong = '../got_wrong/'
batch_size = 32
DARK_PURPLE = (150,0,255,180)
model = load_model('../../../kerastutorial/my_model_c_with_64_only_900_decay_feb_25_1best.h5')

wrong = ['weeds/img30613.jpg', 'weeds/img30581.jpg', 'weeds/img26018.jpg', 'weeds/img179.jpg', 'weeds/img47807.jpg', 'weeds/img30576.jpg', 'weeds/img15234.jpg', 'weeds/img44911.jpg', 'weeds/img15202.jpg', 'weeds/img30383.jpg', 'weeds/img9082.jpg', 'weeds/img7041.jpg', 'weeds/img9569.jpg', 'weeds/img199.jpg', 'weeds/img15248.jpg', 'weeds/img47736.jpg', 'weeds/img44932.jpg', 'weeds/img44967.jpg', 'weeds/img6928.jpg', 'weeds/img40107.jpg', 'weeds/img15245.jpg', 'weeds/img34944.jpg', 'weeds/img20413.jpg', 'weeds/img9903.jpg', 'weeds/img9678.jpg', 'weeds/img39115.jpg', 'weeds/img39185.jpg', 'weeds/img14774.jpg', 'weeds/img30876.jpg', 'weeds/img9003.jpg', 'weeds/img30625.jpg', 'weeds/img36428.jpg', 'weeds/img161.jpg', 'weeds/img47107.jpg', 'weeds/img6844.jpg', 'weeds/img505.jpg', 'weeds/img37000.jpg', 'weeds/img10697.jpg', 'weeds/img9676.jpg', 'weeds/img473.jpg', 'weeds/img26020.jpg', 'weeds/img654.jpg', 'weeds/img478.jpg', 'weeds/img6000.jpg', 'weeds/img25926.jpg', 'weeds/img9083.jpg', 'weeds/img30561.jpg', 'weeds/img30594.jpg', 'weeds/img428.jpg', 'weeds/img14786.jpg', 'weeds/img15221.jpg', 'weeds/img6887.jpg', 'weeds/img9653.jpg', 'weeds/img20385.jpg', 'weeds/img6065.jpg', 'weeds/img30726.jpg', 'weeds/img241.jpg', 'weeds/img36966.jpg', 'weeds/img47716.jpg', 'weeds/img30449.jpg', 'weeds/img34949.jpg', 'weeds/img14793.jpg', 'weeds/img31010.jpg', 'weeds/img31032.jpg', 'weeds/img30566.jpg', 'weeds/img39172.jpg', 'weeds/img5957.jpg', 'weeds/img122.jpg', 'weeds/img30732.jpg', 'weeds/img30362.jpg', 'weeds/img14825.jpg', 'weeds/img39225.jpg', 'weeds/img5956.jpg', 'weeds/img43672.jpg', 'weeds/img9026.jpg', 'weeds/img43797.jpg', 'weeds/img14800.jpg', 'weeds/img6061.jpg', 'weeds/img6821.jpg', 'weeds/img40071.jpg', 'weeds/img7023.jpg', 'weeds/img40182.jpg', 'weeds/img30430.jpg', 'weeds/img6965.jpg', 'weeds/img30364.jpg', 'weeds/img10848.jpg', 'weeds/img20512.jpg', 'weeds/img6882.jpg', 'weeds/img180.jpg', 'weeds/img9674.jpg', 'weeds/img30743.jpg', 'weeds/img30664.jpg']

#extension = validation_data_dir + '/weeds/*.jpg'
extension = 'weeds/*.jpg'
total_weeds = 0
total_images = 0
print('This is doing the large images')
images = [None] * (batch_size)
orig_images = [None] * (batch_size)
name = [None] * (batch_size)
j = 0
for pic in glob.glob(extension):
	img = image.load_img(pic)
	orig_images[j] = img
	name[j] = pic
	#print(pic)
	img = image.img_to_array(img)
	img = np.expand_dims(img, axis=0)
	images[j] = img
	j += 1
	if j == batch_size:
		j = 0
		total_images += batch_size
		images = np.concatenate(images, axis=0)			
		images = (1./255)*images
		classes = model.predict_classes(images, batch_size=batch_size)
		num_weeds = (classes == 1).sum()
		for i in range(len(classes)):
			if classes[i] == 1 and name[i] in wrong:
				image_i = orig_images[i]
				draw = ImageDraw.Draw(image_i)
				draw.line([100, 100,200, 100], fill=DARK_PURPLE)
				draw.line([200, 100, 200, 200], fill=DARK_PURPLE)
				draw.line([200, 200, 100, 200], fill=DARK_PURPLE)
				draw.line([100, 200, 100, 100], fill=DARK_PURPLE)
				
				image_i.save(got_wrong + name[i])
		total_weeds += num_weeds
		curr_percent = total_weeds*1.0/total_images
		images = [None] * (batch_size)
		print(curr_percent)
print('Final weed percentage: ' + str(curr_percent))
print('nonweeds')
'''
extension = validation_data_dir + '/nonweeds/*.jpg'
images = [None] * (batch_size)
j = 0
total_nonweeds = 0
total_images_2 = 0
for pic in glob.glob(extension):
	img = image.load_img(pic)
	img = image.img_to_array(img)
	img = np.expand_dims(img, axis=0)
	images[j] = img
	j += 1
	if j == batch_size:
		j = 0
		total_images_2 += batch_size
		images = np.concatenate(images, axis=0)			
		images = (1./255)*images
		classes = model.predict_classes(images, batch_size=batch_size)
		num_weeds = (classes == 0).sum()
		total_nonweeds += num_weeds
		curr_percent = total_nonweeds*1.0/total_images_2
		images = [None] * (batch_size)
		print(curr_percent)	
'''
print('Final nonweed percentage: ' + str(curr_percent))
total_percent = (total_nonweeds*1.0 + total_weeds)/(total_images + total_images_2)
print('Final total percentage: ' + str(total_percent))
	

end = time.time()
print(end - start)
