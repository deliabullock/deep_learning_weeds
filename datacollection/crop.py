import csv
import pandas as pd
import ast
from PIL import Image
import requests
from io import BytesIO


class csvreader(object):
    def __init__(self, filename):
        self.filename = filename


    def readcsv(self):
        with open(self.filename, 'r') as f:
            csv_data = pd.read_csv(f)
            labels = csv_data[['Answer.labelData']].as_matrix()
            urls = csv_data[['Input.URLimage']].as_matrix()
            
            imagenum = 1

            #column of responses
            for i in range(len(labels)):

                arr = labels[i]
                arr2 = urls[i]
            #arr is an array containing 1 string
            #print(labels[6])
                #arr does not vary in size
                #arr[0] is a string
                list_dict = ast.literal_eval(arr[0])
                url = arr2[0]


            # Gets image from web - doesn't save raw image
                response = requests.get(url)
                im = Image.open(BytesIO(response.content))

                for j in range(len(list_dict)):
            # list_dict is an array of dictionaries
                    Dict = list_dict[j]
        	#lst varies in size
                    X = Dict['pts_x']
                    left = min(X)
                    right = max(X)
                    Y = Dict['pts_y']
                    upper = min(Y)
                    lower = max(Y)

                    # crops and saves image
                    if (left != right and upper != lower):
                        croppedim = im.crop((left, upper, right, lower))
                        imageName = 'imga'+str(imagenum)+'.jpg'
                        croppedim.save(imageName)
                        imagenum+=1






def main():
    c = csvreader('Batch_2667541_batch_results.csv')
    c.readcsv()

if  __name__ =='__main__':main()
