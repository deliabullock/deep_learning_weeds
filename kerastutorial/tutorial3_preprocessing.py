from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from collections import Counter
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.optimizers import SGD
import time
start = time.time()

# dimensions of our images.
img_width, img_height = 299, 299

train_data_dir = '../datacollection/data/train'
validation_data_dir = '../datacollection/data/validate'
test_data_dir = '../datacollection/data/test'
nb_train_samples = 6541
nb_validation_samples = 1152
epochs =50
batch_size = 32
lrate = 0.01 ### HERE
decay = lrate/epochs
sgd = SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)
#sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(Conv2D(32, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))

model.add(Conv2D(64, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))

model.add(Conv2D(128, (3, 3)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(256))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
	rescale=1. / 255, 
	shear_range=0.2,
	zoom_range=0.2,
	channel_shift_range=0.1,       
	rotation_range=180,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.2,  # randomly shift images vertically (fraction of total height)
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
print(class_weights)

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    class_weight=class_weights,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)
end = time.time()
print(end - start)

model.save('my_model_c_part_2_with_more_data.h5')
#model.save_weights('third_try.h5')
