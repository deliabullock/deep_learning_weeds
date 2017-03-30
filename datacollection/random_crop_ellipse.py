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

urls_dict = {
    "./data/test/": [],
    "./data/train/": [],
    "./data/validate/": [],
}

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
            trimmed_dir = "trimmed/"
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
                    if is_weed == 1:
                        class_dir = weed_dir
                    if is_weed == -1:
                        class_dir = trimmed_dir
                    imageName = data_dir + class_dir + 'img'+str(imagenum)+'.jpg'
                    croppedim.save(imageName)
                    imagenum+=1
                    curr_x += IMAGE_SIZE
                curr_y += IMAGE_SIZE
            urls_dict[data_dir].append([url, rand_x, rand_y])
            return imagenum

def weed_image(x, y, box_dict):

    def x_within_img_range(x_val, x_left, x_right):
        if ((x_val <= x_right and x >= x_left)):
            return True
        if (((x_val + IMAGE_SIZE) <= x_right and (x_val + IMAGE_SIZE) >= x_left)):
            return True
        return False

    def x_y_within_ellipse(x, y, box):
        x_right = x + 298
        y_bottom = y + 298
        xs = box['xs']
        ys = box['ys']
        b = (float(xs['right'] - xs['left']))/2
        a = (float(ys['bottom'] - ys['top']))/2
        h = xs['left'] + b 
        k = ys['top'] + a

	coords = [[x,y], [x_right, y], [x_right, y_bottom], [x, y_bottom]]
	for c in coords:
            if ((float((c[0]-h)*(c[0]-h))/(b*b) + float((c[1]-k)*(c[1]-k))/(a*a)) <= 1):
                return True
        return False
        
    in_trimmed = False
    i = 0
    while i < len(box_dict):
        box = box_dict[i]
        
        if (y > box['ys']['bottom']):
            # cropping loop has passed the portion of the pic that this box includes
            #box_dict.pop(i)
            i += 1
            continue
        if ((y + IMAGE_SIZE) < box['ys']['top']):
            # cropping loop has not begun examining the portion of the pic this box includes
            i += 1
            break

        if ((y <= box['ys']['bottom'] and y >= box['ys']['top'])):
            if x_within_img_range(x, box['xs']['left'], box['xs']['right']):
                if x_y_within_ellipse(x, y, box):
                    return 1
                in_trimmed = True 
        if (((y + IMAGE_SIZE) <= box['ys']['bottom'] and (y + IMAGE_SIZE) >= box['ys']['top'])):
            if x_within_img_range(x, box['xs']['left'], box['xs']['right']):
                if x_y_within_ellipse(x, y, box):
                    return 1
                in_trimmed = True 
        i += 1
    if in_trimmed == True:
        return -1
    return 0 

def main():
    c = csvreader('Batch_2667541_batch_results.csv')
    c.readcsv()
    params_file = open('./data/URLs.pkl', 'wb')
    pickle.dump(urls_dict, params_file)
    params_file.close()
            
if  __name__ =='__main__':main()
