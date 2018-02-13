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
from PIL import Image
import pickle
start = time.time()

train_data_dir = '../datacollection/data/train'
validation_data_dir = '../datacollection/data_to_test/validate'
test_data_dir = '../datacollection/data/test'
batch_size = 32

model = load_model('../kerastutorial/my_model_c_with_large_img_best.h5')

extension = validation_data_dir + '/weeds/*.jpg'
total_weeds = 0
total_images = 0
print('This is doing the large images')
images = [None] * (batch_size)
j = 0
for pic in glob.glob(extension):
	img = image.load_img(pic)
	img = img.resize((299, 299), Image.ANTIALIAS)
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
		total_weeds += num_weeds
		curr_percent = total_weeds*1.0/total_images
		images = [None] * (batch_size)
		print(curr_percent)
print('Final weed percentage: ' + str(curr_percent))
print('nonweeds')

extension = validation_data_dir + '/nonweeds/*.jpg'
images = [None] * (batch_size)
j = 0
total_nonweeds = 0
total_images_2 = 0
for pic in glob.glob(extension):
	img = image.load_img(pic)
	img = img.resize((299, 299), Image.ANTIALIAS)
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
print('Final nonweed percentage: ' + str(curr_percent))
total_percent = (total_nonweeds*1.0 + total_weeds)/(total_images + total_images_2)
print('Final total percentage: ' + str(total_percent))
	

end = time.time()
print(end - start)
