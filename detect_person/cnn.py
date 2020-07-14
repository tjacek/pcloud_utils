import numpy as np
import keras
from keras.models import Model
from keras.layers import Input,Conv2D,MaxPooling2D
from keras.layers import Flatten,Dense,Dropout
from keras import regularizers

def basic_model(img_shape=(64,64,1)):
    input_img = Input(shape=img_shape)
    x=input_img
    kern_size,pool_size,filters=(3,3),(2,2),[32,16,16,16]
    for filtr_i in filters:
        x = Conv2D(filtr_i, kern_size, activation='relu', padding='same')(x)
        x = MaxPooling2D(pool_size, padding='same')(x)
    x=Flatten()(x)
    x=Dense(32, activation='relu',name="hidden",kernel_regularizer=regularizers.l1(0.01),)(x)
    x=Dropout(0.5)(x)
    return x,input_img

def make_model(img_shape=(64,64,1)):
    x=basic_model(img_shape)
    x=Dense(units=2,activation='softmax')(x)
    model = Model(input_img, x)
    model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.SGD(lr=0.001,  momentum=0.9, nesterov=True))
    model.summary()
    return model

def make_regression(img_shape=(64,64,1)):
    x,input_img=basic_model(img_shape)
    x=Dense(1, activation="linear")(x)  
    model = Model(input_img, x)
    model.compile(loss='mean_squared_error',
              optimizer=keras.optimizers.SGD(lr=0.00001,  momentum=0.9, nesterov=True))
    model.summary()
    return model