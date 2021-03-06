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
weed_image_number = pickle.load(open('./data/remake_data/clean_data/weed_image_numbers_final.pkl'))
nonweed_image_number = pickle.load(open('./data/remake_data/clean_data/nonweed_image_numbers_final.pkl'))

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
        data_dir = "./data_to_test/validate/"
	i = 0
        for full_image in validate_full_image_info:
	    print(i)
	    i += 1
            url = full_image[0]
	    x = full_image[1]
	    y = full_image[2]
	    imagenum = full_image[3]
            self.crop_image(url, data_dir, imagenum, x, y)
	
#	pickle.dump( self.test_pictures, open( "./data/large_test_picture_info.pkl", "wb" ) )
#	pickle.dump( self.train_pictures, open( "./data/large_train_picture_info.pkl", "wb" ) )
#	pickle.dump( self.validate_pictures, open( "./data/large_validate_picture_info.pkl", "wb" ) )
    
    def crop_image(self, url, data_dir, imagenum, rand_x, rand_y):
            def get_top_y(elem):
                return elem['ys']['top']


            ip = 'http://128.84.3.178'
            url_2 = str(ip + url[25:])
	    #changed line below from url_2 to url
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
            #draw = ImageDraw.Draw(im,"RGBA")
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


		    if curr_x - 300 > 0:
			low_x = curr_x-300
		    else: 
			low_x = 1
		    if curr_x + 598 <= w:
			high_x = curr_x+598
		    else: 
			high_x = w

		    if curr_y - 300 > 0:
                        low_y = curr_y-300
                    else:
                        low_y = 1
                    if curr_y + 598 <= h:
                        high_y = curr_y+598
                    else:
                        high_y = w


                    croppedim = im.crop((low_x, low_y, high_x, high_y))
                    croppedim = croppedim.resize((300, 300), Image.ANTIALIAS)
		    class_dir = get_class_dir(data_dir, 'img'+str(imagenum)+'.jpg', imagenum)
                    imageName = data_dir + class_dir + 'largeimg'+str(imagenum)+'.jpg'
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
