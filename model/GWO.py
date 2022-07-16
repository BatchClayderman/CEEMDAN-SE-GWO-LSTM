from numpy import array
from numpy.random import uniform as np_uniform
from pandas import DataFrame as DF
from random import uniform

class GWO:
	def __init__(self, n, a, b, c, learning_rate = 0.01): # bound
		assert(0 < a < b < c < 1)
		self.n = n
		self.a = a
		self.b = b
		self.c = c
		self.learning_rate = learning_rate
		self.lb = 0
		self.ub = 1
		self.use_np = True
		self.na = int(n * a)
		self.nb = int(n * (b - a))
		self.nc = int(n * (c - b))
		self.nd = self.n - self.na - self.nb - self.nc
		self.lists = [						\
			[self.generator(0, a) for _ in range(self.na)], 		\
			[self.generator(a, b) for _ in range(self.nb)], 		\
			[self.generator(b, c) for _ in range(self.nc)], 		\
			[self.generator(c, 1) for _ in range(self.nd)], 		\
		] # generate the four layers
		self.X = sorted([self.generator(self.lb, self.ub) for _ in range(n)])
	def _generator(self):
		return np_uniform if self.use_np else uniform
	def generator(self, a, b):
		return np_uniform(a, b) if self.use_np else uniform(a, b)
	def update(self, t):
		self.lists[3] = abs(array(self.lists[2]) * abs(self.X[min(len(self.X) - 1, t)]) - self.X[min(len(self.X) - 1, t)]).tolist()
		if t >= len(self.X): # sifted out
			del self.X[0]
			self.X.append(self.generator(self.lb, self.ub))
			self.c -= 1 / self.n
		for i in range(len(self.lists) - 1):
			self.lists[3] = abs(self.lists[3][t % len(self.lists[3])] * array(self.lists[i]) - self.X[min(self.n - 1, t)]).tolist()
		tmp_a = array(self.X[:self.na])
		tmp_b = (array(self.lists[0]) * array([self.lists[3]]).T)[0]
		tmp_c = array(self.X[self.na:self.na + self.nb])
		tmp_d = (array(self.lists[1]) * array([self.lists[3]]).T)[0]
		tmp_e = array(self.X[self.nb:self.nb + self.nc])
		tmp_f = (array(self.lists[2]) * array([self.lists[3]]).T)[0]
		self.X.append(													\
			(													\
				(tmp_a - tmp_b).tolist()[0]		\
				+ (tmp_c - tmp_d).tolist()[0]		\
				+ (tmp_e - tmp_f).tolist()[0]		\
			) / 3													\
		)
		self.learning_rate = abs(self.X[-1] - self.X[-2])
	def fix(self, test, predict, lb = 0, ub = 1, layer = None):
		if layer is None: # do not use gwo
			return (test - predict) * self.get((lb, ub))
		else:
			return (test - predict) * self.get((layer, ))
	def get(self, target):
		if "A" == target:
			return self.lists[0]
		elif "B" == target:
			return self.lists[1]
		elif "C" == target:
			return self.lists[2]
		elif "D" == target:
			return self.lists[3]
		elif 1== target or "a" == target or "alpha" == str(target).lower() or target is None:
			return self.a
		elif 2 == target or "b" == target or "beta" == str(target).lower():
			return self.b
		elif 3 == target or "c" == target or "gamma" == str(target).lower():
			return self.c
		elif type(target) == tuple:
			if 1 == len(target):
				layer = target[0]
				return self.generator(self.get(layer) + (1 - self.get("gamma")) * self.get("alpha"), self.get(layer) + (1 - self.get(layer + 1)) * self.get(layer))
			if 2 == len(target):
				return self.generator(target[0], target[1])
			else:
				return None
		else:
			return None
	
	def train_model(self, model, X_train, y_train, name, config):
		model.compile(loss = "mse", optimizer = "rmsprop", metrics = ['mape'])
		print(X_train.shape, y_train.shape)
		X = X_train.tolist()[0][0] # get initial
		Y = y_train.tolist()
		print(len(X), len(Y))
		for i in range(min(len(X), len(Y))):
			self.update(i)
			Y[i] += self.fix(X[i], Y[i], layer = 1)
		X_train[0] = X
		y_train = array(Y).reshape(y_train.shape)
		hist = model.fit(
			X_train, y_train,
			batch_size = config["batch"],
			epochs = config["epochs"],
			validation_split = 0.05
		)
		model.save('model/' + name + '.h5')
		pf = DF.from_dict(hist.history)
		pf.to_csv('model/' + name + ' loss.csv', encoding = 'utf-8', index = False)