from keras.preprocessing.image import ImageDataGenerator,img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import pickle
import numpy as np
import PIL.Image as Image

images = []
image_info = pickle.load( open( "./data/test_picture_info.pkl", "rb" ) )
for x in image_info:
	if len(x["weeds"]) == 0:
		continue
	for y in x["weeds"]:
		print y
		#images = np.append(images, np.array(Image.open(y),dtype=np.uint8))
                img = load_img(y, target_size = (298, 298))
		img = img_to_array(img)
		#img = np.expand_dims(img, axis=0)
		images = img#np.vstack([img])
		break
	#for y in x["nonweeds"]:
	#	print y
	#	images = np.append(images, np.array(Image.open(y),dtype=np.uint8))
	#break


# dimensions of our images.
img_width, img_height = 299, 299

train_data_dir = '../datacollection/data/train'
validation_data_dir = '../datacollection/data/validate'
nb_train_samples = 18535#2000
nb_validation_samples = 7870#800
epochs = 1#50
batch_size = 16

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(rescale=1. / 255)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

model.fit_generator(
    train_generator,
    steps_per_epoch=2,#nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

output = model.predict_classes(images)
print output

model.save_weights('first_try.h5')
