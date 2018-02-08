from PIL import Image, ImageDraw  # uses pillow
import pickle

def main():
	val_list = pickle.load( open( "DSC07815.JPG", "rb" ) )
	image = './pics/DSC07815.JPG'
	box_size = 75
	
	'''
	val_list = []
	for i in range(0, 12):
		val_list_row = []
		for j in range(0, 12):
			val_list_row.append(7)
		val_list.append(val_list_row)
	
	for i in range(1 ,3):
		for j in range(6, 9):
			val_list[i][j] = 12
	
	for i in range(8, 11):
		for j in range(3, 6):
			val_list[i][j] = 15

	'''

	getContour(image, val_list, box_size)
	

def getContour(image, val_list, box_size):
 
	rows = len(val_list)
	cols = len(val_list[0])
	img = Image.open(image)
	(m, n) = img.size 		

	start_x = int(box_size//2)
	start_y = int(box_size//2)
	
	x_across_points_list = []
	y_across_points_list = []
	x_down_points_list = []
	y_down_points_list = []

	for j in range(0, rows-1):
		x_across_points_row = []
		y_across_points_row = []
		x_down_points_row = []
		y_down_points_row = []
	
		for i in range(0, cols-1):
			add_across_zero = True
			add_down_zero = True

			if val_list[j][i] >= 8 and val_list[j][i+1] < 8:
				ratio = val_list[j][i]/(val_list[j][i]+val_list[j][i+1])
				offset = int((ratio*box_size)//1)
				x_across_points_row.append(start_x + i*box_size + offset)
				y_across_points_row.append(start_y + j*box_size)
				add_across_zero = False			

			if val_list[j][i] < 8 and val_list[j][i+1] >= 8:
				ratio = val_list[j][i+1]/(val_list[j][i]+val_list[j][i+1])
				offset = box_size - int((ratio*box_size)//1)
				x_across_points_row.append(start_x + i*box_size + offset)
				y_across_points_row.append(start_y + j*box_size)
				add_across_zero = False

			if val_list[j][i] >= 8 and val_list[j+1][i] < 8:
				ratio = val_list[j][i]/(val_list[j][i]+val_list[j+1][i])
				offset = int((ratio*box_size)//1)
				x_down_points_row.append(start_x + i*box_size)
				y_down_points_row.append(start_y + j*box_size + offset)
				add_down_zero = False

			if val_list[j][i] < 8 and val_list[j+1][i] >= 8:
				ratio = val_list[j+1][i]/(val_list[j][i]+val_list[j+1][i])
				offset = box_size - int((ratio*box_size)//1)
				x_down_points_row.append(start_x + i*box_size) 
				y_down_points_row.append(start_y + j*box_size + offset)
				add_down_zero = False

			if add_across_zero == True:
				x_across_points_row.append(-1)
				y_across_points_row.append(-1)
				
			if add_down_zero == True:
				x_down_points_row.append(-1)
				y_down_points_row.append(-1)

		x_across_points_list.append(x_across_points_row)
		y_across_points_list.append(y_across_points_row)

		x_down_points_list.append(x_down_points_row)
		y_down_points_list.append(y_down_points_row)


	
	draw = ImageDraw.Draw(img) 

	
	for j in range(0, len(x_across_points_list)):
		for i in range(0, len(x_across_points_list[0])):
			
			if x_across_points_list[j][i] >= 0:
				
				if i != 0:
					if x_across_points_list[j][i-1] >= 0:
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_across_points_list[j][i-1]
						y2 = y_across_points_list[j][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
						
					if x_down_points_list[j][i-1] >= 0:
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_down_points_list[j][i-1]
						y2 = y_down_points_list[j][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

				if j != len(x_across_points_list)-1 and i != 0:
					if x_across_points_list[j+1][i-1] >= 0:
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_across_points_list[j+1][i-1]
						y2 = y_across_points_list[j+1][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

					if x_down_points_list[j+1][i-1] >= 0:	
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_down_points_list[j+1][i-1]
						y2 = y_down_points_list[j+1][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
						#commented top line before

				if j != len(x_across_points_list)-1:
					if x_across_points_list[j+1][i] >= 0:
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_across_points_list[j+1][i]
						y2 = y_across_points_list[j+1][i]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

					if x_down_points_list[j+1][i] >= 0:
			
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_down_points_list[j+1][i]
						y2 = y_down_points_list[j+1][i]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
			

				if i != len(x_across_points_list[0])-1:
					if x_across_points_list[j][i+1] >= 0:

						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_across_points_list[j][i+1]
						y2 = y_across_points_list[j][i+1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
					
					if x_down_points_list[j][i+1] >= 0:
					
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_down_points_list[j][i+1]
						y2 = y_down_points_list[j][i+1]

						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

				if j != len(x_across_points_list)-1 and i != len(x_across_points_list[0])-1:
					if x_across_points_list[j+1][i+1] >= 0:

						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_across_points_list[j+1][i+1]
						y2 = y_across_points_list[j+1][i+1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

					if x_down_points_list[j+1][i+1] >= 0:
				
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_down_points_list[j+1][i+1]
						y2 = y_down_points_list[j+1][i+1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

				if x_across_points_list[j][i] >= 0 and x_down_points_list[j][i] >= 0: 
					
			
						x1 = x_across_points_list[j][i]
						y1 = y_across_points_list[j][i]
						x2 = x_down_points_list[j][i]
						y2 = y_down_points_list[j][i]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)


			
			if x_down_points_list[j][i] >= 0:
				
				if i != 0:
					if x_across_points_list[j][i-1] >= 0:
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_across_points_list[j][i-1]
						y2 = y_across_points_list[j][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
						
					if x_down_points_list[j][i-1] >= 0:
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_down_points_list[j][i-1]
						y2 = y_down_points_list[j][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

				if j != len(x_across_points_list)-1 and i != 0:
					if x_across_points_list[j+1][i-1] >= 0:
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_across_points_list[j+1][i-1]
						y2 = y_across_points_list[j+1][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

					if x_down_points_list[j+1][i-1] >= 0:	
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_down_points_list[j+1][i-1]
						y2 = y_down_points_list[j+1][i-1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

				if j != len(x_across_points_list)-1:
					if x_across_points_list[j+1][i] >= 0:
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_across_points_list[j+1][i]
						y2 = y_across_points_list[j+1][i]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

					if x_down_points_list[j+1][i] >= 0:
			
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_down_points_list[j+1][i]
						y2 = y_down_points_list[j+1][i]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
		
	

				if i != len(x_across_points_list[0])-1:
					if x_across_points_list[j][i+1] >= 0:

						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_across_points_list[j][i+1]
						y2 = y_across_points_list[j][i+1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
					
					if x_down_points_list[j][i+1] >= 0:
					
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_down_points_list[j][i+1]
						y2 = y_down_points_list[j][i+1]

						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

				if j != len(x_across_points_list)-1 and i != len(x_across_points_list[0])-1:
					if x_across_points_list[j+1][i+1] >= 0:

						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_across_points_list[j+1][i+1]
						y2 = y_across_points_list[j+1][i+1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)

					if x_down_points_list[j+1][i+1] >= 0:
				
						x1 = x_down_points_list[j][i]
						y1 = y_down_points_list[j][i]
						x2 = x_down_points_list[j+1][i+1]
						y2 = y_down_points_list[j+1][i+1]
						draw.line([(x1,y1), (x2,y2)], fill=128, width=3)
			


#im = Image.new('RGBA', (400, 400), (0, 255, 0, 0)) 
#draw = ImageDraw.Draw(im) 
#draw.line((100,200, 150,300), fill=128, width=3)
	#img.show()
	img.save('testcontourimage5.jpg')
if __name__ == "__main__":main()
