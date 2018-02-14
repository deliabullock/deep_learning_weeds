import csv
import pandas as pd
import numpy as np
import ast
from PIL import Image
import requests
from io import BytesIO
import random
import pickle

IMAGE_SIZE = 299
weed_image_number = pickle.load(open('./data/remake_data/clean_data/weed_image_numbers_with_del.pkl'))
nonweed_image_number = pickle.load(open('./data/remake_data/clean_data/nonweed_image_numbers_with_del.pkl'))

train_full_image_info = pickle.load(open("./data/train_full_image_info.pkl"))
test_full_image_info = pickle.load(open("./data/test_full_image_info.pkl"))
validate_full_image_info = pickle.load(open("./data/validate_full_image_info.pkl"))

class csvreader(object):
    def __init__(self):
	self.test_pictures = []
	self.train_pictures = []
	self.validate_pictures = []

    def readcsv(self):	
	'''
        data_dir = "./data/train/"
        for full_image in train_full_image_info:
            url = full_image[0]
	    x = full_image[1]
	    y = full_image[2]
	    imagenum = full_image[3]
            self.crop_image(url, data_dir, imagenum, x, y)
        data_dir = "./data/test/"
        for full_image in test_full_image_info:
            url = full_image[0]
	    x = full_image[1]
	    y = full_image[2]
	    imagenum = full_image[3]
            self.crop_image(url, data_dir, imagenum, x, y)
	'''
        data_dir = "./data/validate/"
        for full_image in validate_full_image_info:
            url = full_image[0]
	    x = full_image[1]
	    y = full_image[2]
	    imagenum = full_image[3]
            image_grid = self.get_image_grid(url, imagenum, x, y)
            self.crop_with_jitter(image_grid, url, data_dir, imagenum, x, y)
	#pickle.dump( self.test_pictures, open( "./data/test_picture_info.pkl", "wb" ) )
	#pickle.dump( self.train_pictures, open( "./data/train_picture_info.pkl", "wb" ) )
	#pickle.dump( self.validate_pictures, open( "./data/validate_picture_info.pkl", "wb" ) )
    
    def get_image_grid(self, url, imagenum, rand_x, rand_y):
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
            w, h = im.size
            x_start = rand_x % IMAGE_SIZE
            num_colu = int((w-x_start)/IMAGE_SIZE)
            y_start = rand_y % IMAGE_SIZE
            num_rows = int((h-y_start)/IMAGE_SIZE)
            curr_y = y_start

	    picture_grid = [None] * (num_rows)
	    print(picture_grid)
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

    def crop_with_jitter(self, image_grid, url, data_dir, imagenum, rand_x, rand_y):
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
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
				if r != num_rows - 1 and image_grid[r + 1][n + 1]['class'] == 1:
					jitter_diag = True
		    #jitter down
		    if jitter_down:
			curr_y_tmp = curr_y
		    	for x in range(3):
		        	curr_y_tmp = curr_y_tmp + 75
                    		croppedim = im.crop((curr_x, curr_y_tmp, curr_x + 298, curr_y_tmp + 298))
                    		class_dir = 'weeds/'
                    		imageName = data_dir + class_dir + 'img'+str(imagenum)+ '_d' + str(x) + '.jpg'
                    		croppedim.save(imageName)
		    #jitter right
		    if jitter_right:
			curr_x_tmp = curr_x
		    	for x in range(3):
		        	curr_x_tmp = curr_x_tmp + 75
                    		croppedim = im.crop((curr_x_tmp, curr_y, curr_x_tmp + 298, curr_y + 298))
                    		class_dir = 'weeds/'
                    		imageName = data_dir + class_dir + 'img'+str(imagenum)+ '_r' + str(x) + '.jpg'
                    		croppedim.save(imageName)
		    #jitter diagonal
		    if jitter_diag:
			curr_x_tmp = curr_x
			curr_y_tmp = curr_y
		    	for x in range(1, 3):
		        	curr_x_tmp = curr_x_tmp + 75
				for y in range(1, 3):
		        		curr_y_tmp = curr_y_tmp + 75
                    			croppedim = im.crop((curr_x_tmp, curr_y, curr_x_tmp + 298, curr_y + 298))
                    			class_dir = 'weeds/'
                    			imageName = data_dir + class_dir + 'img'+str(imagenum)+ '_' + str(x)+'_'+ str(y)+'.jpg'
                    			croppedim.save(imageName)


    def crop_image(self, url, data_dir, imagenum, rand_x, rand_y):
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
            w, h = im.size
            x_start = rand_x % IMAGE_SIZE
            num_colu = int((w-x_start)/IMAGE_SIZE)
            y_start = rand_y % IMAGE_SIZE
            num_rows = int((h-y_start)/IMAGE_SIZE)
            curr_y = y_start

	    picture_info = {
            	"url": url,
                "weeds": {},
                "nonweeds": {},
	    }
            for r in range(num_rows):
                curr_x = x_start
                for n in range(num_colu):
                    croppedim = im.crop((curr_x, curr_y, curr_x + 298, curr_y + 298))
                    class_dir = get_class_dir(data_dir, 'img'+str(imagenum)+'.jpg', imagenum)
                    imageName = data_dir + class_dir + 'img'+str(imagenum)+'.jpg'
                    croppedim.save(imageName)
                    pickle_key = "nonweeds"
                    if class_dir == "weeds/":
                        pickle_key = "weeds"
		    picture_info[pickle_key][imageName] = {
                         "x": curr_x,
                         "y": curr_y,
			 "num": str(imagenum)
                    }
                    imagenum+=1
                    curr_x += IMAGE_SIZE
                curr_y += IMAGE_SIZE
            if data_dir == "./data/test/":
		self.test_pictures.append(picture_info)
            if data_dir == "./data/train/":
		self.train_pictures.append(picture_info)
            if data_dir == "./data/validate/":
		self.validate_pictures.append(picture_info)

def get_class_dir(data_dir, img, num):
	if img in weed_image_number:
		return "weeds/"
        if img in nonweed_image_number:
		return "nonweeds/"
	print(img)
	return "del/"

def main():
    c = csvreader()
    c.readcsv()
            
if  __name__ =='__main__':main()
