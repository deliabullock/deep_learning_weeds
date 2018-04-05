''' Training Model C with new 3x3 tile data
 Model c is the same as in my_model_c_23_just_incorrect_best.h5, but with one minor 
change -- flatten has 256 instead of 64 nodes'''
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
from keras.callbacks import Callback, ModelCheckpoint, ReduceLROnPlateau
start = time.time()

# dimensions of our images.
img_width, img_height = 300, 300

train_data_dir = '../datacollection/data/train'
validation_data_dir = '../datacollection/data/validate'
test_data_dir = '../datacollection/data/test'
nb_train_samples = 49702 
nb_validation_samples = 10368
epochs =50
batch_size = 32
#lrate = 0.01 
#decay = lrate/epochs
sgd = SGD(lr=1e-3, decay=1e-4, momentum=0.9, nesterov=True)
#sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
	rescale=1. / 255, 
	#shear_range=0.2,
	#zoom_range=0.2,
	#channel_shift_range=0.1,       
	#rotation_range=180,  # randomly rotate images in the range (degrees, 0 to 180)
        #width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
        #height_shift_range=0.2,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)


train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

## find class weights
counter = Counter(train_generator.classes)  
max_val = float(max(counter.values())) 
class_weights = {class_id : max_val/num_images for class_id, num_images in counter.items()}
print('Train class weights: ')
print(class_weights)

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

counter = Counter(validation_generator.classes)  
max_val = float(max(counter.values())) 
class_weights_val = {class_id : max_val/num_images for class_id, num_images in counter.items()}
print('Validation class weights: ')
print(class_weights_val)

model_name = 'my_model_c_no_warped_mar_6_2'
model_checkpoint = ModelCheckpoint(model_name+"best.h5", monitor='val_acc', verbose=1, save_best_only=True)
#add decay
reduce_lr = ReduceLROnPlateau(monitor='val_acc', verbose=1, factor=0.3, patience=5, min_lr=0.0005)


print('Results for ' + model_name +': ')
print(model.summary())
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    class_weight=class_weights,
    validation_data=validation_generator,
    callbacks=[model_checkpoint],
    validation_steps=nb_validation_samples // batch_size)
end = time.time()
print(end - start)

model.save(model_name+'.h5')
#model.save_weights('third_try.h5')
