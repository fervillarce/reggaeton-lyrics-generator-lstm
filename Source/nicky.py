import numpy as np
from keras.models import load_model
import pickle
 
def load_obj(name):
    with open('../obj/'+ name + '.pkl', 'rb') as f:
        return pickle.load(f)

def sample(preds, temperature=1.0):
    # Helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def predict(sentence):
    model = load_model('../Output/model.h5')
    MAXLEN = 40
    chars = load_obj('chars_list')
    char_indices = load_obj('char_indices_dict')
    indices_char = load_obj('indices_char_dict')
    
    prediction = ''

    for i in range(40):
        x_pred = np.zeros((1, MAXLEN, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        # Make probability predictions with the model
        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, 0.2)
        next_char = indices_char[next_index]

        prediction += next_char
        
        pred = prediction.split(" ")[:8] # Prevent from half words. 8 is the number of total words in the prediction.
        pred = " ".join(pred)
    return pred

