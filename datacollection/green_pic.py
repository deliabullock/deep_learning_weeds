import webcolors
from PIL import Image

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

def green_pic(img):
	X_,Y_ = img.size
	num_green = 0
	for x in range(X_/16):
        	for y in range(Y_/16):
                	pic = img.crop((16*x, 16*y, 16*x + 16, 16*y + 16))
                	colors = pic.getcolors()
			if green_square(colors):
				num_green += 1
#			print (col_one + " " + col_two)
	if num_green  >= 10:
		return True
	return False

def green_square(colors):
	green_pixels = 0
	nongreen_pixels = 0
	for pixel in colors:
		color = get_colour_name(pixel[1])[1]
		if 'green' in color:
			green_pixels += pixel[0]
		elif 'grey' in color:
			continue
		else:
			nongreen_pixels += pixel[0]
	if green_pixels > nongreen_pixels: 
		return True
	return False

def green_square_2(colors):
	color_dict = {}
	top_pix_count = 0
	top_pix_label = ""
	for pixel in colors:
		color = get_colour_name(pixel[1])[1]
		if color in color_dict:
			color_dict[color] = color_dict[color] + pixel[0]
		else:
			color_dict[color] = pixel[0]
		if color_dict[color] > top_pix_count:
			top_pix_count = color_dict[color]
			top_pix_label = color
#	print color_dict
	if 'green' in top_pix_label: 
		return True
	return False

#img = Image.open('./data/validate/weeds/img154.jpg')
#print(green_pic(img))
