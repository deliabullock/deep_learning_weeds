import csv
import pandas as pd
import numpy as np
import ast
from PIL import Image,ImageDraw
import requests
from io import BytesIO
import random
import pickle
from green_pic import green_pic
from keras.models import load_model
from keras.preprocessing import image

IMAGE_SIZE = 299

class csvreader(object):
    def __init__(self, filename):
        self.filename = filename
        self.img_size = 299	
	self.weed_dir = 'weeds/'
	self.nonweed_dir = 'nonweeds/'
	self.del_dir = 'del/'
	self.full_image_dir = 'full_images/'
	self.weed_nums = './data_csv_2/final_weed_nums.pkl'
	self.nonweed_nums = './data_csv_2/final_nonweed_nums.pkl'
	self.x_y_pkl = './data_csv_2/out_x_y_2.pkl'
	self.url_pkl = './data_csv_2/out_urls.pkl'
	self.HIGHEST_WEED_NUM = 53370 
        self.out_x_y = []

    def readcsv(self):
	images_2 =  pickle.load(open(self.url_pkl))
	train_num = (.7)*len(images_2)
	vali_num = .15*len(images_2)
	test_num = .15*len(images_2)

	imagenum = 1
	i = 0
	past_end = 0
	data_info = [[train_num, './train/'], [vali_num, './validate/'], [test_num, './test/'], [len(images_2), './train/']]
	for curr in data_info:
		data_dir = curr[1]
		for url in images_2[past_end : curr[0]]:
	    		print(i)
	    		i += 1
            		imagenum = self.crop_image(url,imagenum, data_dir)
		past_end = curr[0]

    def crop_image(self, url, imagenum, data_dir):
            def get_top_y(elem):
                return elem['ys']['top']

	    ip = 'http://128.84.3.178'
            url_2 = str(ip + url[25:])
            response = requests.get(url_2)
            im = Image.open(BytesIO(response.content))
	    draw = ImageDraw.Draw(im,"RGBA")
            w, h = im.size

	    x_y = get_x_y(url)
            rand_x = x_y[0]
            rand_y = x_y[1]

            x_start = rand_x % IMAGE_SIZE
            num_colu = int((w-x_start)/IMAGE_SIZE)
            y_start = rand_y % IMAGE_SIZE
            num_rows = int((h-y_start)/IMAGE_SIZE)
            curr_y = y_start


	    weed_pictures = []
            for r in range(num_rows):
                curr_x = x_start
                for n in range(num_colu):
			croppedim = im.crop((curr_x, curr_y, curr_x + 298, curr_y + 298))
			other_name = 'img'+str(imagenum) + '.jpg'
			if other_name in self.weed_nums:
				curr_dir = self.weed_dir
			else if other_name in self.nonweed_nums:
				curr_dir = self.nonweed_dir
			else:
				curr_dir = self.del_dir
			croppedim.save(data_dir+curr_dir+'img'+str(imagenum + self.HIGHEST_WEED_NUM)+'.jpg')
			
			weed_pictures.append([curr_x, curr_y])
                    	curr_x += IMAGE_SIZE
			imagenum+=1
                curr_y += IMAGE_SIZE

            for i in range(len(weed_pictures)):
		x = weed_pictures[i][0]
		y = weed_pictures[i][1]
		draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (150,0,255,50))
	    img_name = url[url.rfind('/')+1:]
            im.save(data_dir + self.full_image_dir + img_name)
            return imagenum

def get_x_y(url):
	for x in self.out_x_y:
		if x[0] == url:
			return [x[1], x[2]]


def main():
    c = csvreader('Batch_2685854_batch_results.csv')
    c.readcsv()
            
if  __name__ =='__main__':main()
