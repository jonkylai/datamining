from SBFeatureExtraction import HUMAN_PICKLE, BOT_PICKLE, TEST_PICKLE

import numpy as np
import pickle

from keras.models import Sequential
from keras import layers, activations, Input, callbacks

from matplotlib import pyplot as plt


def clean_data(list_in: list) -> np.array:
    """ Takes in a list of pickled data and combines them
        Cleans out any string data (must be consistently in same columns)
        Then outputs these results into an array """
    final_list = list()
    for pickle_in in list_in:
        pickle_list = pickle.load(open(pickle_in, 'rb'))

        for single_list in pickle_list:
            append_list = list()
            for item in single_list:
                try:
                    append_list.append(float(item))
                except:
                    pass
            final_list.append(append_list)

    return np.array(final_list)



def main():
    # To do list: Attempt to train test set and use those layers to input into the development set

    #data = clean_data( [HUMAN_PICKLE, BOT_PICKLE] )
    data = clean_data( [TEST_PICKLE] )

    num_features = len(data[0,:]) - 1
    X = data[:,1:num_features+1]
    y = data[:,0]

    # For debugging
    print(X)
    bot_count = np.count_nonzero(y)
    baseline_percentage = bot_count / float( len(y) )
    print('Bot percentage = %.2f' % baseline_percentage)

    model = Sequential()
    # Rectified linear unit activation function
    model.add( Input(shape=num_features) )
    model.add( layers.Dense(20) )
    model.add( layers.Activation(activations.relu) )
    model.add( layers.Dense(6) )
    model.add( layers.Activation(activations.relu) )
    # Sigmoid activation function
    model.add( layers.Dense(1) )
    model.add( layers.Activation(activations.sigmoid) )

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    es = callbacks.EarlyStopping(monitor='val_loss', mode='min', patience=5, verbose=1)
    history = model.fit(X, y, validation_split=0.1, epochs=50, batch_size=16, callbacks=[es])

    model.summary()

    _, accuracy = model.evaluate(X, y, verbose=0)

    print('Number of Features: %i' % num_features)
    print('Accuracy: %4.2f' % accuracy)

    #new_data = np.array( [[1,2,3,2]] )
    #result = model.predict(new_data)[0][0]
    #print( 'Input: %s' % new_data)
    #print( 'Prediction: %i' % round(result) )

    # Plot metrics
    fig, (ax1, ax2) = plt.subplots(2)

    ax1.plot(history.history['val_accuracy'])
    ax1.plot(history.history['accuracy'])
    ax1.set_title('Accuracy')
    ax1.legend(['train', 'val'])
    ax1.set_xlabel('epoch')
    ax1.set_ylabel('accuracy')

    ax2.plot(history.history['val_loss'])
    ax2.plot(history.history['loss'])
    ax2.set_title('Loss')
    ax2.legend(['train', 'val'])
    ax2.set_xlabel('epoch')
    ax2.set_ylabel('accuracy')

    plt.show()


if __name__ == "__main__":
    main()
