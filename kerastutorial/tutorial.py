import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.preprocessing.image import ImageDataGenerator
K.set_image_dim_ordering('th')

seed = 7
numpy.random.seed(seed)
num_classes = 2

print ("start model")
model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, 299, 299), border_mode='same', activation='relu', W_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Convolution2D(32, 3, 3, activation='relu', border_mode='same', W_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
model.add(Dropout(0.5))
model.add(Dense(1))

print ("Compile model")
# Compile model
epochs = 2#50 ###HERE
lrate = 0.01 ### HERE
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())

print ("make generators")
train_datagen = ImageDataGenerator(rescale=1./255)
valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
        '../datacollection/data_2/train',
        target_size=(299, 299),
        batch_size=16#32,
        class_mode='binary')

validation_generator = valid_datagen.flow_from_directory(
        '../datacollection/data_2/validate',
        target_size=(299, 299),
        batch_size=16#32,
        class_mode='binary')

test_generator = test_datagen.flow_from_directory(
        '../datacollection/data_2/test',
        target_size=(299, 299),
        batch_size=16#32,
        class_mode='binary')

print ("fit model")
model.fit_generator(
        train_generator,
        nb_epoch=epochs,
        validation_data=validation_generator,
	samples_per_epoch=100, ### fix
	nb_val_samples=80)  ###fix

print ("Scoring")
print (model.evaluate_generator(
        test_generator,
       	100)) #### fix


