import pickle


all_stats = pickle.load(open("./all_stats_info.pkl"))

config = pickle.load(open("./config22715.pkl"))

num_ncg = 0
num_cg = 0
for x in config['train']:
	pic = all_stats[x]
	num_cg += pic[0]
	num_ncg += pic[1]
print('Train stats: \nThere are ' + str(num_ncg) + ' non-crabgrass photos and ' + str(num_cg) + ' crabgrass photos')
num_ncg = 0
num_cg = 0
for x in config['validation']:
	pic = all_stats[x]
	num_cg += pic[0]
	num_ncg += pic[1]
print('Val stats: \nThere are ' + str(num_ncg) + ' non-crabgrass photos and ' + str(num_cg) + ' crabgrass photos')
num_ncg = 0
num_cg = 0
for x in config['test']:
	pic = all_stats[x]
	num_cg += pic[0]
	num_ncg += pic[1]
print('Test stats: \nThere are ' + str(num_ncg) + ' non-crabgrass photos and ' + str(num_cg) + ' crabgrass photos')
