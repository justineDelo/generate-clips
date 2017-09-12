from keras.models import Sequential
from keras.layers.recurrent import LSTM, GRU, SimpleRNN

import numpy

X_train = numpy.random.random((64, 3, 1)) #  (# samples, # timesteps, # features) 
Y_train = numpy.random.random((64, 3, 1))

model = Sequential()
model.add(LSTM(1, 1, activation='sigmoid', inner_activation='hard_sigmoid', return_sequences=True))

print X_train.shape
print Y_train.shape

model.compile(loss='mean_squared_error', optimizer='sgd')
model.fit(X_train, Y_train, batch_size=8, nb_epoch=10)