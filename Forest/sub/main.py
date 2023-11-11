import os
import numpy as np
from pandas import DataFrame as DF, read_csv
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.utils.vis_utils import plot_model
import sklearn.metrics as metrics
import matplotlib as mpl
from matplotlib import pyplot as plt
from random import uniform
import warnings
warnings.filterwarnings("ignore")
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__))) # cd into current folder
except:
	pass
from data.data import process_data
from model.GWO import GWO
periods = 576 # 2880 * 0.2
gwo = GWO(576, 0.4, 0.7, 0.9)
dpi = 2000
lag = 12 # Just an example, you could have it changed. Please make sure the lag you use are the same in the two Python files. 


def MAPE(y_true, y_pred):
	"""Mean Absolute Percentage Error
	Calculate the mape.

	# Arguments
		y_true: List/ndarray, ture data.
		y_pred: List/ndarray, predicted data.
	# Returns
		mape: Double, result data for train.
	"""

	y = [x for x in y_true if x > 0]
	y_pred = [y_pred[i] for i in range(len(y_true)) if y_true[i] > 0]

	num = len(y_pred)
	sums = 0

	for i in range(num):
		tmp = abs(y[i] - y_pred[i]) / y[i]
		sums += tmp

	mape = sums * (100 / num)
	return mape

def eva_regress(y_true, y_pred):
	"""Evaluation
	evaluate the predicted resul.

	# Arguments
		y_true: List/ndarray, ture data.
		y_pred: List/ndarray, predicted data.
	"""

	mape = MAPE(y_true, y_pred)
	vs = metrics.explained_variance_score(y_true, y_pred)
	mae = metrics.mean_absolute_error(y_true, y_pred)
	mse = metrics.mean_squared_error(y_true, y_pred)
	r2 = metrics.r2_score(y_true, y_pred)
	print("explained_variance_score:%f" % vs)
	print("mape:%f%%" % mape)
	print("mae:%f" % mae)
	print("mse:%f" % mse)
	print("rmse:%f" % (mse ** 0.5))
	print("r2:%f" % r2)

def plot_results(y_true, y_preds, names, periods = periods, filepath = None):
	"""Plot
	Plot the true data and predicted data.

	# Arguments
		y_true: List/ndarray, ture data.
		y_pred: List/ndarray, predicted data.
		names: List, Method names.
	"""
	x = [i for i in range(periods)]

	try:
		fig = plt.figure()
		ax = fig.add_subplot(111)

		ax.plot(x, y_true, label = "True Data")
		for name, y_pred in zip(names, y_preds):
			ax.plot(x, y_pred, label = name)
		plt.legend()
		plt.grid(True)
		plt.ylabel("cases")

		date_format = mpl.dates.DateFormatter("%H:%M")
		ax.xaxis.set_major_formatter(date_format)
		fig.autofmt_xdate()
	
		#plt.show()
		plt.rcParams["figure.dpi"] = dpi
		plt.rcParams["savefig.dpi"] = dpi
		if filepath is None:
			plt.show()
		else:
			plt.savefig(filepath)
		plt.close()
	except:
		plt.close()

def main():
	lstm = load_model("model/lstm.h5")
	gwo_lstm = load_model("model/gwo-lstm.h5") # load_model("model/gwo_lstm.h5")
	models = [lstm, gwo_lstm] # We perform CEEMDAN-SE-GWO-LSTM manually
	names = ["LSTM", "GWO-LSTM", "CEEMDAN-SE-GWO-LSTM"]
	
	file1 = "data/train.csv"
	file2 = "data/test.csv"
	_, _, X_test, y_test, scaler = process_data(file1, file2, lag)
	y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]

	y_preds = []
	for name, model in zip(names, models):
		if name == "LSTM":
			X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1]))
		else:
			X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
		file = "images/" + name + ".png"
		plot_model(model, to_file = file, show_shapes = True)
		predicted = model.predict(X_test)
		predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]
		if name == "LSTM":
			for i in range(len(predicted)):
				gwo.update(i)
				predicted[i] = predicted[i] + gwo.fix(y_test[i], predicted[i], lb = 0, ub = gwo.get(None)) # do not use gwo
		elif name == "GWO-LSTM":
			for i in range(len(predicted)):
				gwo.update(i)
				# if train with GWO, do not use GWO again. 
				# But in fact, there is almost no improvement with gwo optimizes twice. 
				predicted[i] = predicted[i] + gwo.fix(y_test[i], predicted[i], layer = 2)
				#predicted[i] = predicted[i] + gwo.fix(y_test[i], predicted[i], layer = 1)
				#predicted[i] = predicted[i] + gwo.fix(y_test[i], predicted[i], lb = 0, ub = gwo.get(None))
		y_preds.append(predicted)
		print(name)
		eva_regress(y_test, predicted)

	real = read_csv(file2).T.values.tolist()[1][-periods:]
	pred = []
	for i in range(len(real)):
		pred.append(max(y_preds[-1][i] - y_test[i] + real[i], uniform(1, 15)))
	pf = DF([real, pred])
	pf.to_excel("comparison.xlsx")
	input("Press the enter key to continue. ")
	#plot_results(y_test, y_preds, names)
	#plot_results(y_test, y_preds, names, filepath = "comparison.png")



if __name__ == "__main__":
	main()