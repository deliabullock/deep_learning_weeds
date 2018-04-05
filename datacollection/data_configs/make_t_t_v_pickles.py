import pickle


# (open("./data/train_full_image_info.pkl"))


CONFIG_NUM = 31665

config = pickle.load(open('./config' + str(CONFIG_NUM) + '.pkl'))

all_images = pickle.load(open("./all_image_info.pkl"))

train_out = []
val_out = []
test_out = []

for x in config['train']:
	train_out.append(all_images[x])
for x in config['test']:
	test_out.append(all_images[x])
for x in config['validation']:
	val_out.append(all_images[x])

print(config['train_stats'])
print(config['test_stats'])
print(config['val_stats'])

print(len(train_out))
print(len(test_out))
print(len(val_out))


pickle.dump( train_out, open( "../data/train_full_image_info.pkl", "wb" ) )
pickle.dump( val_out, open( "../data/validate_full_image_info.pkl", "wb" ) )
pickle.dump( test_out, open( "../data/test_full_image_info.pkl", "wb" ) )


