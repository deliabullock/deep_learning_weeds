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

'''urls_dict = {
    "./data/test/": [],
    "./data/train/": [],
    "./data/validate/": [],
}'''

class csvreader(object):
    def __init__(self, filename):
        self.filename = filename
        self.img_size = 299	
	self.weed_dir = './data_csv_2/weeds/'
	self.nonweed_dir = './data_csv_2/nonweeds/'
	self.weed_pkl = './data_csv_2/weed_nums.pkl'
	self.nonweed_pkl = './data_csv_2/nonweed_nums.pkl'
	self.x_y_pkl = './data_csv_2/out_x_y_2.pkl'
	self.url_pkl = './data_csv_2/out_urls.pkl'
        self.weed_nums = set([])
        self.nonweed_nums = set([])
        self.out_x_y = []
	self.model = load_model('../kerastutorial/my_model_2_ballanced.h5')

    def readcsv(self):
	
        images = []
        with open(self.filename, 'r') as f:
            csv_data = pd.read_csv(f)
            urls = csv_data[['Input.URLimage']].as_matrix()
            
            for i in range(len(urls)):
                arr2 = urls[i]
                url = arr2[0]
                if url not in images:
                    images.append(url)

        
	images_2 = []
        rand_indices = np.arange(len(images))
        np.random.shuffle(rand_indices)
	for x in rand_indices:
		images_2.append(images[x])
        
    	f = open(self.url_pkl, 'wb')
    	pickle.dump(images_2, f)
    	f.close()

	imagenum = 0
	i = 0
        for url in images_2:
	    print(i)
	    i += 1
            imagenum = self.crop_image(url,imagenum)
        f = open(self.weed_pkl, 'ab')
        pickle.dump(self.weed_nums, f)
        f.close()
        f = open(self.nonweed_pkl, 'ab')
        pickle.dump(self.nonweed_nums, f)
        f.close()
        f = open(self.x_y_pkl, 'ab')
        pickle.dump(self.out_x_y, f)
        f.close()

    def crop_image(self, url, imagenum):
            def get_top_y(elem):
                return elem['ys']['top']

	    ip = 'http://128.84.3.178'
            url_2 = str(ip + url[25:])
            response = requests.get(url_2)
            im = Image.open(BytesIO(response.content))
	    draw = ImageDraw.Draw(im,"RGBA")
            w, h = im.size
            rand_x = random.randrange(w)
            rand_y = random.randrange(h)
	    self.out_x_y.append([url, rand_x, rand_y])
	    print('('+url+', '+str(rand_x)+', '+str(rand_y)+')')

            x_start = rand_x % IMAGE_SIZE
            num_colu = int((w-x_start)/IMAGE_SIZE)
            y_start = rand_y % IMAGE_SIZE
            num_rows = int((h-y_start)/IMAGE_SIZE)
            curr_y = y_start


	    weed_images = np.empty((1,1))
	    weed_pictures = []
            for r in range(num_rows):
                curr_x = x_start
                for n in range(num_colu):
			croppedim = im.crop((curr_x, curr_y, curr_x + 298, curr_y + 298))
			croppedim.save('./data_csv_2/img'+str(imagenum)+'.jpg')
			img = image.load_img('./data_csv_2/img'+str(imagenum)+'.jpg', target_size=(299, 299))
			weed_pictures.append([croppedim, curr_x, curr_y, imagenum])

                	x = image.img_to_array(img)
                	x = np.expand_dims(x, axis=0)
                	if weed_images.shape == (1,1):
                       		weed_images = np.vstack([x])
                	else:
                        	weed_images = np.vstack([weed_images, x])
                    	curr_x += IMAGE_SIZE
			imagenum+=1
                curr_y += IMAGE_SIZE

	    weed_images = (1./255)*weed_images
	    weed_classes = self.model.predict_classes(weed_images, batch_size=10)
            for i in range(len(weed_pictures)):
		croppedim = weed_pictures[i][0]
		x = weed_pictures[i][1]
		y = weed_pictures[i][2]
		num = weed_pictures[i][3]
		if weed_classes[i] == 1:
                        croppedim.save(self.weed_dir + 'img'+str(num)+'.jpg')
			self.weed_nums.add('img'+str(num)+'.jpg')
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (150,0,255,50))
		else:
                        croppedim.save(self.nonweed_dir + 'img'+str(num)+'.jpg')
			self.nonweed_nums.add('img'+str(num)+'.jpg')
			draw.polygon([(x, y),(x + 298, y),(x + 298, y + 298),( x, y + 298)], (20,30,50,50))
	    img_name = url[url.rfind('/')+1:]
            im.save('./data_csv_2/' + img_name)
            return imagenum


def main():
    c = csvreader('Batch_2685854_batch_results.csv')
    c.readcsv()
            
if  __name__ =='__main__':main()
