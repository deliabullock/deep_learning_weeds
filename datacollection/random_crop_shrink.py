import csv
import pandas as pd
import numpy as np
import ast
from PIL import Image
import requests
from io import BytesIO
import random

IMAGE_SIZE = 299


class csvreader(object):
    def __init__(self, filename):
        self.filename = filename
        self.train_percent = 0.70
        self.test_percent = 0.15
        self.validate_percent = 0.15	
        self.img_size = 299	

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
        
        rand_indices = np.arange(len(keys))
        np.random.shuffle(rand_indices)
        data_dir = "./data/train/"
        imagenum = 0
        for x in rand_indices[0:train_n]:
            print ("x: " + str(x))
            url = keys[x]
            boxes = images[url]
            imagenum = self.crop_image(url, boxes, data_dir, imagenum)
        data_dir = "./data/test/"
        for x in rand_indices[train_n:train_n+test_n]:
            url = keys[x]
            boxes = images[url]
            imagenum = self.crop_image(url, boxes, data_dir, imagenum)
        data_dir = "./data/validate/"
        for x in rand_indices[train_n+test_n:train_n+test_n+valid_n]:
            url = keys[x]
            boxes = images[url]
            imagenum = self.crop_image(url, boxes, data_dir, imagenum)
        data_dir = "./data/train/"
        for x in rand_indices[train_n+test_n+valid_n:]:
            url = keys[x]
            boxes = images[url]
            imagenum = self.crop_image(url, boxes, data_dir, imagenum)
        

    def crop_image(self, url, boxes, data_dir, imagenum):
            weed_dir = "weeds/"
            nonweed_dir = "nonweeds/"
            def get_top_y(elem):
                return elem['ys']['top']

            boxes.sort(key=get_top_y)
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))
            w, h = im.size
            rand_x = random.randrange(w)
            rand_y = random.randrange(h)
            x_start = rand_x % IMAGE_SIZE
            num_colu = int((w-x_start)/IMAGE_SIZE)
            y_start = rand_y % IMAGE_SIZE
            num_rows = int((h-y_start)/IMAGE_SIZE)
            curr_y = y_start
            for r in range(num_rows):
                curr_x = x_start
                for n in range(num_colu):
                    croppedim = im.crop((curr_x, curr_y, curr_x + 298, curr_y + 298))
                    is_weed = weed_image(curr_x, curr_y, boxes)
                    class_dir = nonweed_dir
                    if is_weed:
                        class_dir = weed_dir
                    imageName = data_dir + class_dir + 'img'+str(imagenum)+'.jpg'
                    croppedim.save(imageName)
                    imagenum+=1
                    curr_x += IMAGE_SIZE
                curr_y += IMAGE_SIZE
            return imagenum

def weed_image(x, y, box_dict):

    def x_within_img_range(x_val, x_left, x_right):
        if ((x_val <= x_right and x >= x_left)):
            return True
        if (((x_val + IMAGE_SIZE) <= x_right and (x_val + IMAGE_SIZE) >= x_left)):
            return True
        return False

    i = 0
    while i < len(box_dict):
        box = box_dict[i]
        
        offsety = int((box['ys']['bottom']-box['ys']['top'])*.10)
        offsetx = int((box['xs']['right']-box['xs']['left'])*.10)

        if (y > box['ys']['bottom']-offsety):
            # cropping loop has passed the portion of the pic that this box includes
            #box_dict.pop(i)
            i += 1
            continue
        if ((y + IMAGE_SIZE) < box['ys']['top']+offsety):
            # cropping loop has not begun examining the portion of the pic this box includes
            i += 1
            break

        if ((y <= box['ys']['bottom']-offsety and y >= box['ys']['top']+offsety)):
            if x_within_img_range(x, box['xs']['left']+offsetx, box['xs']['right']-offsetx):
                return True #, box_dict
        if (((y + IMAGE_SIZE) <= box['ys']['bottom']-offsety and (y + IMAGE_SIZE) >= box['ys']['top']+offsety)):
            if x_within_img_range(x, box['xs']['left']+offsetx, box['xs']['right']-offsetx):
                return True #, box_dict
        i += 1
    # add corner identification and sorted boxes
    return False #, box_dict

def main():
    c = csvreader('Batch_2667541_batch_results.csv')
    c.readcsv()

if  __name__ =='__main__':main()
