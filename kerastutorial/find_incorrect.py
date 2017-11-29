from PIL import Image,ImageDraw
import requests
from io import BytesIO
import pickle
import numpy as np
from keras.models import load_model
from keras.models import load_model
from keras.preprocessing import image
from keras.optimizers import SGD
import glob

model = load_model('../kerastutorial/my_model_c_part_2_with_more_data.h5')
out_folder = '../incorrect_nonweeds/'

nonweed_images = np.empty((1,1))
nonweed_names = []
for key in glob.glob('*.jpg'):
	nonweed_names.append(key)
	img = image.load_img(key, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        if nonweed_images.shape == (1,1):
                nonweed_images = np.vstack([x])
                #print(weed_images.shape)
                #print(len(weed_images))
        else:
                nonweed_images = np.vstack([nonweed_images, x])
                #print(weed_images)
        #images = np.vstack([x])
        #print(weed_images.shape)
        #print(weed_images)
nonweed_images = (1./255)*nonweed_images
nonweed_classes = model.predict_classes(nonweed_images, batch_size=10)
for i in range(len(nonweed_names)):
	if nonweed_classes[i] == 1:
		img.save(out_folder + nonweed_names[1])
print(len(nonweed_names))
