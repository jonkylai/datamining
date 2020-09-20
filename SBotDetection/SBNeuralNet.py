from keras.models import *
from keras.layers import Dense, Activation
from keras.optizers import *


def main():
    model = Sequential()
    model.add(Dense(10, input_dim=9, activation='sigmoid'))
    model.add(Dense(1))
    sgd = SGD(lr=0.01, decay=0.00001, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='mse')
    model.fit(Xdata, Ydata, nb_epoch=200, batch_size=100)
    Score = model.evaluate(XdataT, YdataT, verbose=0)
    print('Score: %f' % Score*100)


if __name__ == "__main__":
    main()
