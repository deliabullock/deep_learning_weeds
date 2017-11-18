import csv
import pandas as pd
import numpy as np
import ast
from PIL import Image
import requests
from io import BytesIO
import random
import pickle
import Queue
import xml.etree.ElementTree as ET


IMAGE_SIZE = 299
weed_image_number = pickle.load(open('./data/remake_data/clean_data/weed_image_numbers_with_del.pkl'))
nonweed_image_number = pickle.load(open('./data/remake_data/clean_data/nonweed_image_numbers_with_del.pkl'))

class csvreader(object):
    WEED = 1
    NONWEED = 0
    DEL = -1

    def __init__(self):
        self.train_percent = 0.70
        self.test_percent = 0.15
        self.validate_percent = 0.15	
        self.img_size = 299	

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
	
        img_dir = "/data_xml/train_image_folder/"
        annot_dir = "/data_xml/train_annot_folder/"
        ground_dir = "/data_xml/train_ground_folder/"
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
            imagenum = self.crop_image(url, ground_dir, annot_dir, img_dir, imagenum, rand_x, rand_y)
        img_dir = "/data_xml/test_image_folder/"
        annot_dir = "/data_xml/test_annot_folder/"
        ground_dir = "/data_xml/test_ground_folder/"
        for x in rand_indices[train_n:train_n+test_n]:
	    print("test: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, ground_dir, annot_dir, img_dir, imagenum, rand_x, rand_y)
        img_dir = "/data_xml/valid_image_folder/"
        annot_dir = "/data_xml/valid_annot_folder/"
        ground_dir = "/data_xml/valid_ground_folder/"
        for x in rand_indices[train_n+test_n:train_n+test_n+valid_n]:
	    print("val: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, ground_dir, annot_dir, img_dir, imagenum, rand_x, rand_y)
        img_dir = "/data_xml/train_image_folder/"
        annot_dir = "/data_xml/train_annot_folder/"
        ground_dir = "/data_xml/train_ground_folder/"
        for x in rand_indices[train_n+test_n+valid_n:]:
	    print("train: " + str(i))
	    i += 1
            url = keys[x]
            rand_x, rand_y = get_rands(url, image_urls)
            imagenum = self.crop_image(url, ground_dir, annot_dir, img_dir, imagenum, rand_x, rand_y)
    
    def crop_image(self, url, ground_dir, annot_dir, img_dir, imagenum, rand_x, rand_y):
            url = url[25:]
            ip = 'http://128.84.3.178'
	    image_name = url[url.rfind('/')+1:]
            url = ip + url
 
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
            w, h = im.size
            x_start = rand_x % IMAGE_SIZE
            num_colu = int((w-x_start)/IMAGE_SIZE)
            y_start = rand_y % IMAGE_SIZE
            num_rows = int((h-y_start)/IMAGE_SIZE)
            curr_y = y_start

	    weed_points = set([])
            for r in range(num_rows):
                curr_x = x_start
                for n in range(num_colu):
                    category = get_class_dir('img'+str(imagenum)+'.jpg')
		    if category == WEED:
			x_y = str(curr_x) + '_' + str(curr_y)
			weed_points.add(x_y)
                    imagenum+=1
                    curr_x += IMAGE_SIZE
                curr_y += IMAGE_SIZE
	    im.save(img_dir + image_name)
	    bounding_boxes = save_annot_file(annot_dir, weed_points, image_name, w, h)
	    draw = ImageDraw.Draw(im,"RGBA")
	    for x in bounding_boxes:
	    	draw.rectangle([(x[0], x[1]), (x[2], x[3])], outline=(150,0,255,255))
	    im.save(ground_dir + image_name)
	    # SAVE GROUND
            return imagenum

def save_annot_file(data_dir, weed_points, image_name, w, h):
	def get_element(base, name, text):
		a = ET.SubElement(base, name)
		if text != "":
			a.text = text
		return a

	bounding_boxes = get_bounding_boxes(weed_points)
	root = ET.Element('annotation')
	folder = get_element(root, 'folder', 'Crabgrass')
	filename = get_element(root, 'filename', image_name) 
	path = get_element(root, 'path', ROOT_DIR + data_dir + image_name)
	source = get_element(root, 'source', '')
	db = get_element(source, 'database', 'Unknown')

	size = get_element(root, 'size', '')
	width = get_element(size, 'width', str(w))
	height = get_element(size, 'height', str(h))
	depth = get_element(size, 'depth', '3')

	segmented = get_element(root, 'segmented', '0')

	for x in bounding_boxes:
		o = get_element(root, 'object', '')
		name = get_element(o, 'name', 'crabgrass')
		pose = get_element(o, 'pose', 'Unspecified')
		truncated = get_element(o, 'truncated', '0')
		difficult = get_element(o, 'difficult', '0')
		bndbox = get_element(o, 'bndbox', '')
		xmin = get_element(bndbox, 'xmin', str(x[0]))
		ymin = get_element(bndbox, 'ymin', str(x[1]))
		xmax = get_element(bndbox, 'xmax', str(x[2]))
		ymax = get_element(bndbox, 'ymax', str(x[3]))

	tree = ET.ElementTree(root)
	image_name = image_name[:image_name.rfind('.')] + '.xml'
	tree.write(data_dir + image_name)
	return bounding_boxes

# return list of bounding boxes. bounding boxes represented by a list of 4 elements:
#[x_top_left, y_top_left, x_bottom_right, y_bottom_right]
def get_bounding_boxes(weed_points):
	out = []
	x_y_permutations = [[IMAGE_SIZE, 0],
		[IMAGE_SIZE, IMAGE_SIZE],
		[-IMAGE_SIZE, 0],
		[-IMAGE_SIZE, -IMAGE_SIZE],
		[0, IMAGE_SIZE],
 		[0, -IMAGE_SIZE]] 
	for point in weed_points:
		weed_points.remove(point)
		x_y_list = point.split('_')
		x = int(x_y_list[0])
		y = int(x_y_list[1])
		bounding_box = [x, y]
		x_max = x
		y_max = y
		q = Queue.Queue()
		q.put([x, y])
		while not q.empty() and not len(weed_points) == 0:
			for p in x_y_permutations:
				new_x = x + p[0]
				new_y = y + p[1]
				key = str(new_x) + '_' + str(new_y)
				if key in weed_points:
					weed_points.remove(key)
					q.put([new_x, new_y])
					if new_x > x_max:
						x_max = new_x
					if new_y > y_max:
						y_max = new_y
		bounding_box.append(x_max + IMAGE_SIZE)
		bounding_box.append(y_max + IMAGE_SIZE)
		out.append(bounding_box)
	return out
			
		# queue for finding bounding box

def get_rands(url, url_set):
	for x in url_set:
		if x[0] == url:
			return x[1], x[2]
# 1 = weed
# 0 = nonweed
# -1 = del
def get_class(img):
	if img in weed_image_number:
		return 1
        if img in nonweed_image_number:
		return 0
	return -1

def main():
    c = csvreader()
# file used = 'Batch_2667541_batch_results.csv'
    c.readcsv()
            
if  __name__ =='__main__':main()
