import pickle

train_clean = pickle.load(open('./data/remake_data/clean_data/train_clean_urls.pkl'))
test_clean = pickle.load(open('./data/remake_data/clean_data/test_clean_urls.pkl'))
val_clean = pickle.load(open('./data/remake_data/clean_data/val_clean_urls.pkl'))
train_clean_del = train_clean[0]
train_clean_kept = train_clean[1]
test_clean_del = test_clean[0]
test_clean_kept = test_clean[1]
val_clean_del = val_clean[0]
val_clean_kept = val_clean[1]

train_nums = pickle.load(open('./data/train_urls.pkl'))
test_nums = pickle.load(open('./data/test_urls.pkl'))
val_nums = pickle.load(open('./data/validate_urls.pkl'))

weed_image_nums = set([])
nonweed_image_nums = set([])

print(train_nums[0].intersection(train_nums[1]).intersection(train_nums[2]).intersection(train_nums[3]).intersection(val_nums[0]).intersection(val_nums[1]).intersection(val_nums[2]).intersection(val_nums[3]).intersection(test_nums[0]).intersection(test_nums[1]).intersection(test_nums[2]).intersection(test_nums[3]))

## FIXING DEL
tmp = set([])
for x in train_nums[0]:
	num = int(x[3:-4])
	if num <= 16800 or x in train_clean_del['nonweeds']:
		tmp.add(x)
train_nums[0] = tmp

tmp = set([])
for x in train_nums[3]:
	num = int(x[3:-4])
	if num <= 6886 or x in train_clean_del['trimmed']:
		tmp.add(x)
train_nums[3] = tmp


### GETTING WEEDS
weeds_1 = train_nums[0].intersection(train_clean_del['nonweeds'])
nonweeds_0 = train_nums[0].difference(train_clean_del['nonweeds'])
nonweeds_1 = train_nums[1].intersection(train_clean_del['weeds'])
weeds_2 = train_nums[1].intersection(train_clean_kept['weeds'])
weeds_3 = train_nums[2].intersection(train_clean_del['not_green'])
nonweeds_2 = train_nums[2].intersection(train_clean_kept['not_green'])
weeds_4 = train_nums[3].intersection(train_clean_del['trimmed'])
nonweeds_3 = train_nums[3].intersection(train_clean_kept['trimmed'])

weeds_5 = val_nums[0].intersection(val_clean_del['nonweeds'])
nonweeds_4 = val_nums[0].difference(val_clean_del['nonweeds'])
nonweeds_5 = val_nums[1].intersection(val_clean_del['weeds'])
weeds_6 = val_nums[1].intersection(val_clean_kept['weeds'])
weeds_7 = val_nums[2].intersection(val_clean_del['not_green'])
nonweeds_6 = val_nums[2].intersection(val_clean_kept['not_green'])
weeds_8 = val_nums[3].intersection(val_clean_del['trimmed'])
nonweeds_7 = val_nums[3].intersection(val_clean_kept['trimmed'])

weeds_9 = test_nums[0].intersection(test_clean_del['nonweeds'])
nonweeds_8 = test_nums[0].difference(test_clean_del['nonweeds'])
nonweeds_9 = test_nums[1].intersection(test_clean_del['weeds'])
weeds_10 = test_nums[1].intersection(test_clean_kept['weeds'])
weeds_11 = test_nums[2].intersection(test_clean_del['not_green'])
nonweeds_10 = test_nums[2].intersection(test_clean_kept['not_green'])
weeds_12 = test_nums[3].intersection(test_clean_del['trimmed'])
nonweeds_11 = test_nums[3].intersection(test_clean_kept['trimmed'])


weed_image_nums =  weeds_1.union(weeds_2).union(weeds_3).union(weeds_4).union(weeds_5).union(weeds_6).union(weeds_7).union(weeds_8).union(weeds_9).union(weeds_10).union(weeds_11).union(weeds_12)

nonweed_image_nums = nonweeds_0.union(nonweeds_1).union(nonweeds_2).union(nonweeds_3).union(nonweeds_4).union(nonweeds_5).union(nonweeds_6).union(nonweeds_7).union(nonweeds_8).union(nonweeds_9).union(nonweeds_10).union(nonweeds_11)

pickle.dump(  weed_image_nums, open( "./data/remake_data/clean_data/weed_image_numbers.pkl", "wb" ) )
pickle.dump( nonweed_image_nums, open( "./data/remake_data/clean_data/nonweed_image_numbers.pkl", "wb" ) )

