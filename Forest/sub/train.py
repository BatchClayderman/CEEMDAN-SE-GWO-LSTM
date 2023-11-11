import os
from sys import argv
import argparse
import numpy as np
import pandas as pd
from data.data import process_data
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.callbacks import EarlyStopping
import warnings
warnings.filterwarnings("ignore")
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__))) # cd into current folder
except:
	pass
from model import model
from model.GWO import GWO
gwo = GWO(576, 0.4, 0.7, 0.9) # just a demo
lag = 12 # Just an example, you could have it changed. Please make sure the lag you use are the same in the two Python files. 


def train_model(model, X_train, y_train, name, config):
	"""train
	train a single model.

	# Arguments
		model: Model, NN model to train.
		X_train: ndarray(number, lags), Input data for train.
		y_train: ndarray(number, ), result data for train.
		name: String, name of model.
		config: Dict, parameter for train.
	"""

	model.compile(loss = "mse", optimizer = "rmsprop", metrics = ["mape"])
	# early = EarlyStopping(monitor = "val_loss", patience  = 30, verbose = 0, mode = "auto")
	hist = model.fit(
		X_train, y_train,
		batch_size = config["batch"],
		epochs = config["epochs"],
		validation_split = 0.05
	)

	model.save("model/" + name + ".h5")
	df = pd.DataFrame.from_dict(hist.history)
	df.to_csv("model/" + name + " loss.csv", encoding = "utf-8", index = False)

def train_saes(models, X_train, y_train, name, config):
	"""train
	train the SAEs model.

	# Arguments
		models: List, list of SAE model.
		X_train: ndarray(number, lags), Input data for train.
		y_train: ndarray(number, ), result data for train.
		name: String, name of model.
		config: Dict, parameter for train.
	"""

	temp = X_train
	# early = EarlyStopping(monitor = "val_loss", patience = 30, verbose = 0, mode = "auto")

	for i in range(len(models) - 1):
		if i > 0:
			p = models[i - 1]
			hidden_layer_model = Model(input = p.input, output = p.get_layer("hidden").output)
			temp = hidden_layer_model.predict(temp)

		m = models[i]
		m.compile(loss = "mse", optimizer = "rmsprop", metrics = ["mape"])

		m.fit(temp, y_train, batch_size = config["batch"], epochs = config["epochs"], validation_split = 0.05)

		models[i] = m

	saes = models[-1]
	for i in range(len(models) - 1):
		weights = models[i].get_layer("hidden").get_weights()
		saes.get_layer("hidden%d" % (i + 1)).set_weights(weights)

	train_model(saes, X_train, y_train, name, config)

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--model",
		default="gwo-lstm",
		help="Model to train."
	)
	args = parser.parse_args()

	config = {"batch": 1024, "epochs": 10000}
	file1 = "data/train.csv"
	file2 = "data/test.csv"
	X_train, y_train, _, _, _ = process_data(file1, file2, lag)

	if args.model == "lstm":
		X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
		m = model.get_lstm([12, 64, 64, 1])
		train_model(m, X_train, y_train, args.model, config)
	elif args.model == "gwo-lstm":
		X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
		m = model.get_lstm([12, 64, 64, 1])
		gwo.train_model(m, X_train, y_train, args.model, config)
	elif args.model == "gru":
		X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
		m = model.get_gru([12, 64, 64, 1])
		train_model(m, X_train, y_train, args.model, config)
	elif args.model == "saes":
		X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1]))
		m = model.get_saes([12, 400, 400, 400, 1])
		train_saes(m, X_train, y_train, args.model, config)



if __name__ == "__main__":
	main(argv)