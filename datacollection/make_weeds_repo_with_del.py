import pickle

weed_image_nums = pickle.load(open("./data/remake_data/clean_data/weed_image_numbers.pkl"))

file_weeds_kept = open("del_weeds_kept.txt")
for line in file_weeds_kept:
	weed_image_nums.add(line[:-1])

nonweeds_orig = set([])
nonweeds_final = set([])

nonweeds_1_file = open("del_nonweeds.txt")
nonweeds_2_file = open("del_nonweeds_kept.txt")
for line in nonweeds_1_file:
	nonweeds_orig.add(line[:-1])
for line in nonweeds_2_file:
	nonweeds_final.add(line[:-1])

weed_image_nums = weed_image_nums.union(nonweeds_orig.difference(nonweeds_final))
print(nonweeds_orig.difference(nonweeds_final))

pickle.dump(  weed_image_nums, open( "./data/remake_data/clean_data/weed_image_numbers_with_del.pkl", "wb" ) )

