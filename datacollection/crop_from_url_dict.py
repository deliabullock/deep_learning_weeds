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
train_nums = pickle.load(open('./data/train_urls.pkl'))
test_nums = pickle.load(open('./data/test_urls.pkl'))
val_nums = pickle.load(open('./data/validate_urls.pkl'))

train_clean = pickle.load(open('./data/remake_data/clean_data/train_clean_urls.pkl'))
test_clean = pickle.load(open('./data/remake_data/clean_data/test_clean_urls.pkl'))
val_clean = pickle.load(open('./data/remake_data/clean_data/val_clean_urls.pkl'))
train_clean_del = train_clean[0]
train_clean_kept = train_clean[1]
test_clean_del = test_clean[0]
test_clean_kept = test_clean[1]
val_clean_del = val_clean[0]
val_clean_kept = val_clean[1]


class csvreader(object):
    def __init__(self, filename):
        self.filename = filename
        self.train_percent = 0.70
        self.test_percent = 0.15
        self.validate_percent = 0.15	
        self.img_size = 299	
	self.test_pictures = []

    def readcsv(self):
	
        images = {}
        with open(self.filename, 'r') as f:
            csv_data = pd.read_csv(f)
            labels = csv_data[['Answer.labelData']].as_matrix()
            urls = csv_data[['Input.URLimage']].as_matrix()
            
            for i in range(len(labels)):
                arr = labels[i]
                arr2 = urls[i]
                list_dict = ast.literal_eval(arr[0])
                url = arr2[0]
                if url not in images:
                    images[url] = []
                box_coords = images[url]
                for box in list_dict:
                    box_coords.append({'xs': { 'left': min(box['pts_x']), 'right': max(box['pts_x'])}, 'ys': {'top':min(box['pts_y']), 'bottom': max(box['pts_y'])}})

        
        keys = list(images.keys())
        max_img_processed = len(keys)
        train_n = int(max_img_processed*self.train_percent)
        test_n = int(max_img_processed*self.test_percent)
        valid_n = int(max_img_processed*self.validate_percent)

        f = open('./data/remake_data/out_x_y.pkl', 'r')
	k = pickle.load(f)
	f.close()
	train_urls = k[0]
	test_urls = k[1]
	validate_urls = k[2]
	extra_urls = k[3]

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
            rand_x, rand_y = get_rands(url, train_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
        data_dir = "./data/test/"
        for x in rand_indices[train_n:train_n+test_n]:
	    print("test: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, test_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
        data_dir = "./data/validate/"
        for x in rand_indices[train_n+test_n:train_n+test_n+valid_n]:
	    print("val: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, validate_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
        data_dir = "./data/train/"
        for x in rand_indices[train_n+test_n+valid_n:]:
	    print("train: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, extra_urls)
            imagenum = self.crop_image(url, data_dir, imagenum, rand_x, rand_y)
	pickle.dump( self.test_pictures, open( "./data/test_picture_info.p", "wb" ) )
    
    def crop_image(self, url, data_dir, imagenum, rand_x, rand_y):
            weed_dir = "weeds/"
            nonweed_dir = "nonweeds/"
            trimmed_dir = "trimmed/"
	    not_green_dir = 'not_green/'
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
            return imagenum

def get_rands(url, url_set):
	for x in url_set:
		if x[0] == url:
			return x[1], x[2]

def get_class_dir(data_dir, img, num):
	if data_dir  == "./data/train/":
		if img in train_nums[0]:
			if img in train_clean_del['nonweeds']:
				return "weeds/"
			if num > 16800:
				return 'del/'
			return "nonweeds/"
		if img in train_nums[1]:
			if img in train_clean_del['weeds']:
				return "nonweeds/"
			if img in train_clean_kept['weeds']:
				return "weeds/"
			print ("Train weeds: " + img)
			return "del/"
		if img in train_nums[2]:
			if img in train_clean_del['not_green']:
				return "weeds/"
			if img in train_clean_kept['not_green']:
				return "nonweeds/"
			print ("Train not_green: " + img)
			return "del/"
		if img in train_nums[3]:
			if img in train_clean_del['trimmed']:
				return "weeds/"
			if num > 6886:
				return 'del/'
			if img in train_clean_kept['trimmed']:
				return "nonweeds/"
			print ("Train trimmed: " + img)
			return "del/"
	if data_dir  == "./data/validate/":
		if img in val_nums[0]:
			if img in val_clean_del['nonweeds']:
				return "weeds/"
			return "nonweeds/"
		if img in val_nums[1]:
			if img in val_clean_del['weeds']:
				return "nonweeds/"
			if img in val_clean_kept['weeds']:
				return "weeds/"
			print ("Val weeds: " + img)
			return "del/"
		if img in val_nums[2]:
			if img in val_clean_del['not_green']:
				return "weeds/"
			if img in val_clean_kept['not_green']:
				return "nonweeds/"
			print ("Val not_green: " + img)
			return "del/"
		if img in val_nums[3]:
			if img in val_clean_del['trimmed']:
				return "weeds/"
			if img in val_clean_kept['trimmed']:
				return "nonweeds/"
			print ("Val trimmed: " + img)
			return "del/"
	if data_dir  == "./data/test/":
		if img in test_nums[0]:
			if img in test_clean_del['nonweeds']:
				return "weeds/"
			return "nonweeds/"
		if img in test_nums[1]:
			if img in test_clean_del['weeds']:
				return "nonweeds/"
			if img in test_clean_kept['weeds']:
				return "weeds/"
			print ("Test weeds: " + img)
			return "del/"
		if img in test_nums[2]:
			if img in test_clean_del['not_green']:
				return "weeds/"
			if img in test_clean_kept['not_green']:
				return "nonweeds/"
			print ("Test not_green: " + img)
			return "del/"
		if img in test_nums[3]:
			if img in test_clean_del['trimmed']:
				return "weeds/"
			if img in test_clean_kept['trimmed']:
				return "nonweeds/"
			print ("Test trimmed: " + img)
			return "del/"
        print ("image num: " + str(imagenum))

def main():
    c = csvreader('Batch_2667541_batch_results.csv')
    c.readcsv()
            
if  __name__ =='__main__':main()
