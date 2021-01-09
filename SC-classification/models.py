import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.compat.v1.keras.layers import Embedding, SpatialDropout1D
from tensorflow.compat.v1.keras.layers import Dense, Input, GRU, LSTM 
from tensorflow.compat.v1.keras.layers import Bidirectional, Dropout, GlobalMaxPool1D 
from tensorflow.compat.v1.keras.layers import CuDNNLSTM, CuDNNGRU, GlobalAveragePooling1D
from tensorflow.compat.v1.keras.layers import Conv1D, GlobalMaxPooling1D, TimeDistributed
from tensorflow.compat.v1.keras.layers import Dense, Embedding, Input

from tensorflow.compat.v1.keras.models import Model, Sequential
from tensorflow.compat.v1.keras.optimizers import RMSprop
import tensorflow.compat.v1.keras.backend as K
from tensorflow.compat.v1.keras.models import load_model

from tensorflow.compat.v1.keras.preprocessing import text, sequence
from tensorflow.keras import initializers as initializers, regularizers, constraints

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.metrics import precision_score, recall_score, f1_score

from nltk import tokenize 
import nltk
nltk.download('punkt')


#############################################
#####              MODELS              ######
#############################################  

def gru_keras(max_features, maxlen, bidirectional, dropout_rate, embed_dim, rec_units,mtype='GRU', reduction = None, classes=4, lr=0.001):
    
    if K.backend == 'tensorflow':        
        K.clear_session()
        
    input_layer     = Input(shape=(maxlen,))
    embedding_layer = Embedding(max_features, output_dim=embed_dim, trainable=True)(input_layer)
    x               = SpatialDropout1D(dropout_rate)(embedding_layer)
    
    if reduction:
        if mtype   == 'GRU':
            if bidirectional:
                x = Bidirectional(CuDNNGRU(units=rec_units, return_sequences=True))(x)
            else:
                x = CuDNNGRU(units=rec_units, return_sequences=True)(x)
        elif mtype == 'LSTM':
            if bidirectional:
                x = Bidirectional(CuDNNLSTM(units=rec_units, return_sequences=True))(x)
            else:
                x = CuDNNLSTM(units=rec_units, return_sequences=True)(x) 
        
        if reduction == 'average':
          x = GlobalAveragePooling1D()(x)
        elif reduction == 'maximum':
          x = GlobalMaxPool1D()(x)
    else: 
        if mtype   == 'GRU':
            if bidirectional:
                x           = Bidirectional(CuDNNGRU(units=rec_units, return_sequences=False))(x)
            else:
                x           = CuDNNGRU(units=rec_units, return_sequences=False)(x)
        elif mtype == 'LSTM':
            if bidirectional:
                x           = Bidirectional(CuDNNLSTM(units=rec_units, return_sequences=False))(x)
            else:
                x           = CuDNNLSTM(units=rec_units, return_sequences=False)(x) 
                
    output_layer = Dense(classes, activation="sigmoid")(x)
    model        = Model(inputs=input_layer, outputs=output_layer)
    model.compile(loss='categorical_crossentropy',
                  optimizer=RMSprop(learning_rate=lr, clipvalue=1, clipnorm=1),
                  metrics=['acc'])
    return model
    
def cnn_keras(max_features, maxlen, dropout_rate, embed_dim, num_filters=300, classes=4, lr=0.001):
    if K.backend == 'tensorflow':        
        K.clear_session()
    input_layer = Input(shape=(maxlen,))
    embedding_layer = Embedding(max_features, output_dim=embed_dim, trainable=True)(input_layer)
    x = SpatialDropout1D(dropout_rate)(embedding_layer)
    x = Conv1D(num_filters, 7, activation='relu', padding='same')(x)
    x = GlobalMaxPooling1D()(x)
    output_layer = Dense(classes, activation="sigmoid")(x)
    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(loss='categorical_crossentropy',
                  optimizer=RMSprop(learning_rate=lr, clipvalue=1, clipnorm=1),
                  metrics=['acc'])
    return model

def dl_model(model_type='BGRU', max_features=40000, embed_dim=50, rec_units=150, dropout_rate=0.25, maxlen=400, classes=4, lr=0.001):
                
    if model_type == 'GRU':
        return gru_keras(max_features=max_features, maxlen=maxlen, bidirectional=False, mtype='GRU', 
                         dropout_rate=dropout_rate, embed_dim=embed_dim, rec_units=rec_units, classes=classes)
    if model_type == 'LSTM':
        return gru_keras(max_features=max_features, maxlen=maxlen, bidirectional=False, mtype='LSTM', 
                         dropout_rate=dropout_rate, embed_dim=embed_dim, rec_units=rec_units, classes=classes)
    if model_type == 'BGRU':
        return gru_keras(max_features=max_features, maxlen=maxlen, bidirectional=True, mtype='GRU', 
                         dropout_rate=dropout_rate, embed_dim=embed_dim, rec_units=rec_units, classes=classes)
    if model_type == 'BLSTM':
        return gru_keras(max_features=max_features, maxlen=maxlen, bidirectional=True, mtype='LSTM', 
                         dropout_rate=dropout_rate, embed_dim=embed_dim, rec_units=rec_units, classes=classes)
    if model_type == 'BGRU_avg':
        return gru_keras(max_features=max_features, maxlen=maxlen, bidirectional=True, mtype='GRU', 
                         dropout_rate=dropout_rate, embed_dim=embed_dim, rec_units=rec_units, 
                         reduction='average', classes=classes)
    if model_type == 'BGRU_max':
        return gru_keras(max_features=max_features, maxlen=maxlen, bidirectional=True, mtype='GRU', 
                         dropout_rate=dropout_rate, embed_dim=embed_dim, rec_units=rec_units, 
                         reduction='maximum', classes=classes)
    if model_type == 'CNN': 
        return cnn_keras(max_features=max_features, maxlen=maxlen, dropout_rate=dropout_rate, embed_dim=embed_dim, classes=classes)
        
#############################################
#####            TRAINING              ######
#############################################

def train_model(X, y,  mtype, cv, epochs, 
                cv_models_path, train, X_test=None, y_test=None, nfolds=None,
                rs=42, max_features=40000, maxlen=400, dropout_rate=0.25, 
                rec_units=150, embed_dim=50, batch_size=256, fscore=False, threshold=0.3):
    if cv:
        kf = StratifiedKFold(n_splits=nfolds, random_state=rs)
        auc = []
        roc = []
        fscore_ = [] 

        for c, (train_index, val_index) in enumerate(kf.split(X, y)):
            
            print(f' fold {c}')
            
            X_train, X_val = X[train_index], X[val_index]
            y_train, y_val = y[train_index], y[val_index] 
            
            tokenizer = keras.preprocessing.text.Tokenizer(num_words=max_features)
            tokenizer.fit_on_texts(X_train)
            
            list_tokenized_train = tokenizer.texts_to_sequences(X_train)
            list_tokenized_val   = tokenizer.texts_to_sequences(X_val)
            
            X_train = sequence.pad_sequences(list_tokenized_train, maxlen=maxlen)
            X_val   = sequence.pad_sequences(list_tokenized_val, maxlen=maxlen)
            
            model = dl_model(model_type=mtype, 
                            max_features=max_features, 
                            maxlen=maxlen, 
                            dropout_rate=dropout_rate, 
                            embed_dim=embed_dim, 
                            rec_units=rec_units, 
                            max_sent_len=max_sen_len, 
                            max_sent_amount=max_sent_amount)
            
            print('Fitting')
            if train:
                model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=True, verbose=1)
                model.save_weights(f'{cv_models_path}/{mtype}_fold_{c}.h5')
            else: 
                model.load_weights(f'{cv_models_path}/{mtype}_fold_{c}.h5')
            
            probs = model.predict(X_val, batch_size=batch_size, verbose=1)

            if fscore:
                #for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
                threshold = threshold
                probs_class = probs.copy()
                probs_class[probs_class >= threshold] = 1 
                probs_class[probs_class < threshold] = 0
                precision = precision_score(y_val, probs_class) 
                recall    = recall_score(y_val, probs_class)
                fscore    = f1_score(y_val, probs_class)
                print(f' {threshold} fold {c} precision {round(precision, 3)} recall {round(recall, 3)} fscore {round(fscore,3)}')
                fscore_.append(fscore)

            auc_f = average_precision_score(y_val, probs)
            auc.append(auc_f)
            roc_f = roc_auc_score(y_val, probs)
            roc.append(roc_f)
            
            print(f'fold {c} average precision {round(auc_f, 3)} ++++  roc auc {round(roc_f, 3)}')
            
            del model
            K.clear_session()

        if fscore:
            print(f'PR-C {round(np.array(auc).mean(), 3)}  ++++ ROC AUC {round(np.array(roc).mean(), 3)}  ++++ FScore {round(np.array(fscore_).mean(), 3)}')
            print(f'PR-C std {round(np.array(auc).std(), 3)}  ++++ ROC AUC std {round(np.array(roc).std(), 3)}  ++++ FScore std {round(np.array(fscore_).std(), 3)}')
        else:
            print(f'PR-C {round(np.array(auc).mean(), 3)}  ++++ ROC AUC {round(np.array(roc).mean(), 3)}')
            print(f'PR-C std {round(np.array(auc).std(), 3)}  ++++ ROC AUC std {round(np.array(roc).std(), 3)}')
        
    else:
            X_train   = X
            y_train   = y
            tokenizer = keras.preprocessing.text.Tokenizer(num_words=max_features, oov_token='unknown')
            tokenizer.fit_on_texts(X_train)
            
            list_tokenized_train = tokenizer.texts_to_sequences(X_train)
            list_tokenized_test  = tokenizer.texts_to_sequences(X_test)
            X_train = sequence.pad_sequences(list_tokenized_train, maxlen=maxlen)
            X_test  = sequence.pad_sequences(list_tokenized_test, maxlen=maxlen)
                
            y_train = np.array(y_train)
            y_test  = np.array(y_test)

            model = dl_model(model_type=mtype, max_features=max_features, 
            maxlen=maxlen, dropout_rate=dropout_rate, embed_dim=embed_dim, 
            rec_units=rec_units, max_sent_len=max_sen_len, max_sent_amount=max_sent_amount)
            
            print('Fitting')

            if train:
                model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=True, verbose=1)
                model.save_weights(f'{cv_models_path}/{mtype}.h5')
            else: 
                model.load_weights(f'{cv_models_path}/{mtype}.h5')
            probs = model.predict(X_test, batch_size=batch_size, verbose=1)
            auc_f = average_precision_score(y_test, probs)
            roc_f = roc_auc_score(y_test, probs)
            
            if fscore:
                threshold = threshold
                probs_class = probs.copy()
                probs_class[probs_class >= threshold] = 1 
                probs_class[probs_class < threshold] = 0
                precision = precision_score(y_test, probs_class) 
                recall    = recall_score(y_test, probs_class)
                fscore    = f1_score(y_test, probs_class)



            if fscore:
                    print('_________________________________')
                    print(f'PR-C is {round(auc_f,3)}     ++++   ROC AUC is {round(roc_f,3)}   +++++ FScore is {round(fscore,3)}')
                    print('_________________________________\n')
            else:
                    print('_________________________________')
                    print(f'PR-C is {round(auc_f,3)}     ++++   ROC AUC is {round(roc_f,3)}')
                    print('_________________________________\n')
            
