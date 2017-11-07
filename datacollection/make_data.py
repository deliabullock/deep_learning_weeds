import csv
import pandas as pd
import numpy as np
import ast
from PIL import Image
import requests
from io import BytesIO
import random
import pickle
from green_pic import green_pic

IMAGE_SIZE = 299
weed_image_number = pickle.load(open('./data/remake_data/clean_data/weed_image_numbers_with_del.pkl'))
nonweed_image_number = pickle.load(open('./data/remake_data/clean_data/nonweed_image_numbers_with_del.pkl'))

class csvreader(object):
    def __init__(self, filename):
        self.filename = filename
        self.train_percent = 0.70
        self.test_percent = 0.15
        self.validate_percent = 0.15	
        self.img_size = 299	
	self.test_pictures = []
	self.validate_pictures = []

    def readcsv(self):
        keys = pickle.load(open('./data/remake_data/clean_data/image_urls.pkl'))
        max_img_processed = len(keys)
        train_n = int(max_img_processed*self.train_percent)
        test_n = int(max_img_processed*self.test_percent)
        valid_n = int(max_img_processed*self.validate_percent)

        f = open('./data/remake_data/out_x_y.pkl', 'r')
	#start_points = pickle.load(f)
	k = pickle.load(f)
	f.close()
	train_urls = k[0]
	test_urls = k[1]
	validate_urls = k[2]
	extra_urls = k[3]
	image_urls = train_urls + test_urls + validate_urls + extra_urls

	f = open('./data/URLs.pkl', 'r')
	rand_indices = pickle.load(f)
	f.close()
	
        data_dir = "./data/train/"
        imagenum = 0
	i = 0
        for x in rand_indices[:train_n]:
	    print("train: " + str(i))
            if i == 33:
		imagenum = 8020
		i = 34
		continue
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
        data_dir = "./data/test/"
        for x in rand_indices[train_n:train_n+test_n]:
	    print("test: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
        data_dir = "./data/validate/"
        for x in rand_indices[train_n+test_n:train_n+test_n+valid_n]:
	    print("val: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
        data_dir = "./data/train/"
        for x in rand_indices[train_n+test_n+valid_n:]:
	    print("train: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
	pickle.dump( self.test_pictures, open( "./data/test_picture_info.p", "wb" ) )
	pickle.dump( self.test_pictures, open( "./data/validate_picture_info.p", "wb" ) )
    
    def crop_image(self, url, data_dir, imagenum, rand_x, rand_y):
            def get_top_y(elem):
                return elem['ys']['top']

            url = url[25:]
            ip = 'http://128.84.3.178'
            url = ip + url
 
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
                "del": {}
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
		    if class_dir == "del/":
                        pickle_key = "del"
		    picture_info[pickle_key][imageName] = {
                         "x": curr_x,
                         "y": curr_y,
                    }
                    imagenum+=1
                    curr_x += IMAGE_SIZE
                curr_y += IMAGE_SIZE
            if data_dir == "./data/test/":
		self.test_pictures.append(picture_info)
            if data_dir == "./data/validate/":
		self.validate_pictures.append(picture_info)
            return imagenum

def get_rands(url, url_set):
	for x in url_set:
		if x[0] == url:
			return x[1], x[2]

def get_class_dir(data_dir, img, num):
	if img in weed_image_number:
		return "weeds/"
        if img in nonweed_image_number:
		return "nonweeds/"
	return 'del/'

def main():
    c = csvreader('Batch_2667541_batch_results.csv')
    c.readcsv()
            
if  __name__ =='__main__':main()
