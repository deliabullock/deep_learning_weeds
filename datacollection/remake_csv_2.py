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

IMAGE_SIZE = 299
weed_image_number = pickle.load(open('./data_csv_2/weed_nums.pkl'))
nonweed_image_number = pickle.load(open('./data_csv_2/nonweed_nums.pkl'))

class csvreader(object):
    def __init__(self, filename):
        self.filename = filename
        self.img_size = 299	

    def readcsv(self):
        keys = pickle.load(open('./data_csv_2/out_urls.pkl'))

        f = open('./data_csv_2/out_x_y_2.pkl', 'r')
	#start_points = pickle.load(f)
	image_urls = pickle.load(f)
	f.close()

        imagenum = 0
	i = 0
        for url in keys:
	    print(str(i))
	    i += 1
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, imagenum, rand_x, rand_y)
    
    def crop_image(self, url, imagenum, rand_x, rand_y):
            url = url[25:]
            ip = 'http://128.84.3.178'
            url = ip + url
 
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
	    draw = ImageDraw.Draw(im,"RGBA")
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
                    class_dir = get_class_dir('img'+str(imagenum)+'.jpg', imagenum)
		    if class_dir == 'weeds/':
			draw.polygon([(curr_x, curr_y),(curr_x + 298, curr_y),(curr_x + 298, curr_y + 298),( curr_x, curr_y + 298)], (150,0,255,50))
		    else:
			draw.polygon([(curr_x, curr_y),(curr_x + 298, curr_y),(curr_x + 298, curr_y + 298),( curr_x, curr_y + 298)], (20,30,50,50))
                    imageName = './data_csv_2/' + class_dir + 'img'+str(imagenum)+'.jpg'
                    croppedim.save(imageName)
                   # pickle_key = "nonweeds"
                   # if class_dir == "weeds/":
                   #     pickle_key = "weeds"
		   # if class_dir == "del/":
                   #     pickle_key = "del"
		   # picture_info[pickle_key][imageName] = {
                   #      "x": curr_x,
                   #      "y": curr_y,
                   # }
                    imagenum+=1
                    curr_x += IMAGE_SIZE
                curr_y += IMAGE_SIZE
	    img_name = url[url.rfind('/')+1:]
            im.save('./data_csv_2/' + img_name)
            return imagenum

def get_rands(url, url_set):
	for x in url_set:
		if x[0] == url:
			return x[1], x[2]

def get_class_dir(img, num):
	if img in weed_image_number:
		return "weeds/"
        if img in nonweed_image_number:
		return "nonweeds/"
	return 'del/'

def main():
    c = csvreader('Batch_2667541_batch_results.csv')
    c.readcsv()
            
if  __name__ =='__main__':main()
