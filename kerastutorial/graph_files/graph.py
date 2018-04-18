import matplotlib.pyplot as plt
#plt.ioff()

#model C large img continued

def get_val_and_train(file_prefix):
	'''
	training_acc = [[], [], []]
	i = 1
	for j in range(3):
		ind = 0
		for line in open(file_prefix + '_train_' + str(i) + '.txt'):
			line = line.rstrip('\n') 
			if ind == 3:
				training_acc[j].append(float(line))
				ind = 0
			else:
				ind +=1
		i += 1
	'''
	val_acc = [[], [], []]
	i = 1
	for j in range(3):
		ind = 0
		print(file_prefix + '_val_' + str(i) + '.txt')
		for line in open(file_prefix + '_val_' + str(i) + '.txt'):
			line = line.rstrip('\n') 
			if ind == 2:
				print(line)
				val_acc[j].append(float(line))
				ind = 0
			else:
				ind +=1
		i += 1
	val_avg = []
	for i in range(len(val_acc[0])):
		val_avg.append((val_acc[0][i] + val_acc[1][i] + val_acc[2][i])/3)
	return val_avg
	

fig = plt.figure()

X = get_val_and_train('norm')
X_2 = get_val_and_train('no_context')
X_3 = get_val_and_train('stretch')

Y = range(1, len(X) + 1, 1)
#X_2 = range(45, len(training_acc_2) + 45, 1)


#plt.plot(X, train_acc, 'r-')
plt.plot(Y, X, 'b-')
plt.plot(Y, X_2, 'r-')
plt.plot(Y, X_3, 'g-')
#plt.plot(X_2, training_acc_2, 'm-')
#plt.plot(X_2, val_acc_2, 'c-')
plt.axis([0, len(Y) + 1, .6, 1])
#plt.show()
fig.savefig('norm_graph.png')

