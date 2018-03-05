import random
import pickle
from PIL import Image
import requests
from io import BytesIO

all_images = pickle.load(open("./all_image_info.pkl"))
IMAGE_SIZE = 299
weed_image_number = pickle.load(open('../data/remake_data/clean_data/weed_image_numbers_final.pkl'))
nonweed_image_number = pickle.load(open('../data/remake_data/clean_data/nonweed_image_numbers_final.pkl'))


def get_stats():
	l = range(len(all_images))
	out = []
	for i in l:
		full_image = all_images[i]
		url = full_image[0]
		x = full_image[1]
		y = full_image[2]
		imagenum = full_image[3]
		num_cg_tmp, num_ncg_tmp = crop_image(url, imagenum, x, y)
		image_grid = get_image_grid(url, imagenum, x, y)
		num_jittered_tmp = crop_with_jitter(image_grid, url, imagenum, x, y)
		out.append([num_cg_tmp, num_ncg_tmp, num_jittered_tmp])
	pickle.dump( out, open( "./all_stats_info.pkl", "wb" ) )
		
'''
def make_new_data_config(config_num):
	# get shuffle lists
	# get
	train_indices, val_indices, test_indices = get_shuffled_list()
	train_stats = get_stats(train_indices)
	val_stats = get_stats(val_indices)
	test_stats = get_stats(test_indices)
	out = {
		'train': train_indices,
		'validation': val_indices,
		'test': test_indices,
		'train_stats': train_stats,
		'test_stats': test_stats,
		'val_stats': val_stats
	}
	pickle.dump( out, open( "./data_configs/config" + str(config_num) + ".pkl", "wb" ) )
	print('Config ' + str(config_num) + ' results: ')
	print('\tTrain -- 1:' + str(train_stats['num_ncg']) + "\t1:" + str(train_stats['num_jittered']))
	print('\tValid -- 1:' + str(val_stats['num_ncg']) + "\t1:" + str(val_stats['num_jittered']))
	print('\tTest  -- 1:' + str(test_stats['num_ncg']) + "\t1:" + str(test_stats['num_jittered']))
	
def get_shuffled_list():
	l = range(224)
	random.shuffle(l) 
	train = l[:158]
	validation = l[158:191]
	test = l[191:]
	return (train, validation, test)

def get_stats(indices):
	num_cg = 0
	num_ncg = 0
	num_jittered = 0
	for i in indices:
		full_image = all_images[i]
		url = full_image[0]
		x = full_image[1]
		y = full_image[2]
		imagenum = full_image[3]
		num_cg_tmp, num_ncg_tmp = crop_image(url, imagenum, x, y)
		image_grid = get_image_grid(url, imagenum, x, y)
		num_jittered_tmp = crop_with_jitter(image_grid, url, imagenum, x, y)
		num_cg += num_cg_tmp
		num_ncg += num_ncg_tmp
		num_jittered += num_jittered_tmp
	num_ncg = num_ncg*(1.0)/num_cg
	num_jittered = num_jittered*(1.0)/num_cg
	num_cg = 1
	out = {
		'num_cg': num_cg,
		'num_ncg': num_ncg,
		'num_jittered': num_jittered
	}
	return out
'''

def get_image_grid(url, imagenum, rand_x, rand_y):
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
        w, h = im.size
        x_start = rand_x % IMAGE_SIZE
        num_colu = int((w-x_start)/IMAGE_SIZE)
        y_start = rand_y % IMAGE_SIZE
        num_rows = int((h-y_start)/IMAGE_SIZE)
        curr_y = y_start

        picture_grid = [None] * (num_rows)
        for x in range(num_rows):
    		picture_grid[x] = [None] * (num_colu)

        for r in range(num_rows):
            	curr_x = x_start
            	for n in range(num_colu):
    	    		img_name = 'img'+str(imagenum)+'.jpg'
    	    		picture_grid[r][n] = {
    				'class': 1,
    				'x': curr_x,
    				'y': curr_y,
     				'num':imagenum
    	    		}
    	    		if img_name in nonweed_image_number:
    	    			picture_grid[r][n]['class'] = 0
                	imagenum+=1
                	curr_x += IMAGE_SIZE
		curr_y += IMAGE_SIZE
	return picture_grid

def crop_with_jitter(image_grid, url, imagenum, rand_x, rand_y):
        
        pics_created = 0
        response = requests.get(url)
        im = Image.open(BytesIO(response.content))
        w, h = im.size
        num_rows = len(image_grid)
        num_colu = len(image_grid[0])

        for r in range(num_rows):
		for n in range(num_colu):
			jitter_down = False
			jitter_right = False
			jitter_diag = False
			curr_x = image_grid[r][n]['x']
			curr_y = image_grid[r][n]['y']
			imagenum = image_grid[r][n]['num']
			if image_grid[r][n]['class'] != 1:
				continue
		    	if r != num_rows - 1:
		       		if image_grid[r + 1][n]['class'] == 1:
					jitter_down = True
		    	if n != num_colu - 1:
		       		if image_grid[r][n + 1]['class'] == 1:
					jitter_right = True
				if jitter_down and image_grid[r + 1][n + 1]['class'] == 1:
					jitter_diag = True
		    	#jitter down
		    	if jitter_down:
				pics_created += 1
		    	#jitter right
		    	if jitter_right:
				pics_created += 1
		    	#jitter diagonal
		    	if jitter_diag:
				pics_created += 1
	return pics_created


def crop_image(url, imagenum, rand_x, rand_y):
	num_cg = 0
	num_ncg = 0
	response = requests.get(url)
        im = Image.open(BytesIO(response.content))
        w, h = im.size
        x_start = rand_x % IMAGE_SIZE
        num_colu = int((w-x_start)/IMAGE_SIZE)
        y_start = rand_y % IMAGE_SIZE
        num_rows = int((h-y_start)/IMAGE_SIZE)
        curr_y = y_start

        for r in range(num_rows):
        	curr_x = x_start
            	for n in range(num_colu):
                	class_dir = get_class_dir('img'+str(imagenum)+'.jpg')
                	if class_dir == "weeds/":
                    		num_cg += 1
			else:
				num_ncg += 1
                	imagenum+=1
                	curr_x += IMAGE_SIZE
           	curr_y += IMAGE_SIZE
	return (num_cg, num_ncg)

def get_class_dir(img):
	if img in weed_image_number:
		return "weeds/"
        if img in nonweed_image_number:
		return "nonweeds/"
	print(img)
	return "del/"

get_stats()
