# -*- coding: utf-8 -*-
"""EHSAN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ao2i4VbO-Is-RR7Yn99WybDYcbpCyrFI
"""

# Commented out IPython magic to ensure Python compatibility.
import os
try:
  # %tensorflow_version only exists in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass
# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import tensorflow as tf
import numpy as np
import pandas as pd
from tqdm import tqdm

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from keras.models import Model, load_model
from keras.layers import Input
from keras.layers.core import Dropout, Lambda
#from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K
from keras.optimizers import SGD
from keras.utils import np_utils

np.random.seed(1671) # for reproducibility





#########################################################################################################################
#########################################################################################################################
# Parameters


# Loading Parameters
TRAIN_NETWORK = True
LOADING_EPOCH_NUMBER = 30
TRANING_EXPIREMENT_FOR_LOAD = 'default'


# Training parameters
NB_EPOCH = 10
BATCH_SIZE = 10
VALIDATION_SPLIT=0.3 # how much TRAIN is reserved for VALIDATION
VERBOSE = 1

#NB_CLASSES = 10 # number of outputs = number of digits





#########################################################################################################################
#########################################################################################################################

# Dataset Generation

#df = pd.read_csv('data.txt')
#df = pd.read_csv(filename, index_col=0, dtype=np.float64)
#cols = df.columns
##cols.remove('fistcolumn')
#for col in cols:
#    df[col] = df[col].astype('float32')



from google.colab import drive
drive.mount('/content/gdrive')
gdrive_cwd = '/content/gdrive/My Drive/'
cwd = gdrive_cwd + '/NN_WorkSpace/'
print(cwd)

dataset_path = '/content/gdrive/My Drive/House B/DAY_' ###################################################################################

day_counter = 1
raw_file = open(dataset_path + day_counter.__str__() + '.txt', 'r')
print ('Reading Day ' + day_counter.__str__()) 
all_lines = raw_file.readlines() 
day_counter += 1

while day_counter < 31:
  raw_file = open(dataset_path + day_counter.__str__() + '.txt', 'r')
  print ('Reading Day ' + day_counter.__str__()) 
  all_lines += raw_file.readlines() 
  day_counter += 1


line_index = 0
number_of_lines_to_average = 60
#zero_list_num = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
averaged_all_lines =[]

while line_index < len(all_lines):#-number_of_lines_to_average:
  sum=[]
  for v in range(74):
    sum.append(0)


  for ii in range(number_of_lines_to_average):
    temp_line = all_lines[line_index + ii]
    temp_line = temp_line.split(' ')
    
    for j in range(20): 
       temp_line[j] = float(temp_line[j]) # Type casting
       sum[j] = sum[j] + temp_line[j]

    temp_line[20] = int(temp_line[20]) # Type casting
    sum [temp_line[20]+ 19] = float(sum[temp_line[20]+ 19] + 1)

    temp_line[21] = int(temp_line[21]) # Type casting
    sum [temp_line[21]+ 46] = float(sum[temp_line[21]+ 46] + 1)
 
  for m in range(74):
    sum[m] = sum[m]/number_of_lines_to_average
 
  averaged_all_lines.append(sum)
  line_index += number_of_lines_to_average

print ('Number of averaged lines: ',len (averaged_all_lines))
print ('Number of Features: ',len (averaged_all_lines[0]))
#print(sum)








number_of_latest_data = 1440 #####################################   How many samples it should combine - for example all the samples from last 24 hour
number_of_features = 20 + 2*27  ######################################   Number features to add for each sample
number_of_data = 7200 ############################################   Total number of input vectors created for the training
index_of_label = 20 ############################################   Index of the label column - starting from zero


X_train = np.zeros((number_of_data, number_of_latest_data*number_of_features - 2*27), dtype=np.float32)
Y_train = np.zeros((number_of_data, 27), dtype=np.float32)

#index_of_label = (number_of_latest_data-1)*number_of_features + index_of_label
index = number_of_latest_data
for i in range(number_of_data):
  latest = averaged_all_lines[index-number_of_latest_data:index]
  index += 1
  #print ('Latest index-lenght: ' + index.__str__() + ' - ' + len(latest).__str__()) 


  vector = []
  counter = 1 # Starting from 1 (dont change!)
  for line in latest:
    
    

    if counter < len(latest):  # This is to exclude the information from last time stamp that we want to predict
      vector += line
    
    else: 
      vector += line[0:20]
      activity1 = line[20:47]
      activity2 = line[47:74]

    counter+=1
    #print ('Vector is: ', vector)
    # End of for


  if index_of_label == 20:
      answer = activity1
  elif index_of_label == 21:
      answer = activity2
  else : answer = zero_list
  for j in range(0, len(vector)): 
       vector[j] = float(vector[j]) # Type casting 
  #print ('Answer: ', answer)
  for j in range(0, len(answer)): 
       answer[j] = float(answer[j]) # Type casting

  #print ('Vectors lenght: ' + len(vector).__str__()) 


 
  Y_train[i] = np.array(answer)
  X_train[i] = np.array(vector)
  print ('Input: ', X_train[i])
  print ('Answer: ', Y_train[i])
  print ('Input Vector Created: ' + i.__str__())





print ('======================================================================================')
print ('Input Vector Size: ' , X_train.shape[1])




train_dataset = (X_train, Y_train)


# (X_test, y_test) = mnist.load_data()

#X_train = X_train.astype('float32')
#X_test = X_test.astype('float32')
# normalize
#
#X_train /= 255
#X_test /= 255

print('Number of Train Samples: ', X_train.shape[0])
#print(X_test.shape[0], 'Number of Test Samples')

# convert class vectors to binary class matrices
#Y_train = np_utils.to_categorical(y_train, NB_CLASSES)
#Y_test = np_utils.to_categorical(y_test, NB_CLASSES)





#########################################################################################################################
#########################################################################################################################

# Model Creation 

model = tf.keras.Sequential()
#model.add(tf.keras.layers.Input(shape= (X_train.shape[1],))
model.add(tf.keras.layers.Dense(units=50, activation='relu'))  ####################################################
model.add(tf.keras.layers.Dense(units=100, activation='relu'))
model.add(tf.keras.layers.Dense(units=500, activation='relu'))  ####################################################
model.add(tf.keras.layers.Dense(units=100, activation='relu')) ####################################################
model.add(tf.keras.layers.Dense(units=50, activation='relu'))

#model.add(tf.keras.layers.Dropout(0.5))                      ####################################################

# Last layer (output).
# Activation is Softamx for multiple outputs if only one output then use Sigmoid
model.add(tf.keras.layers.Dense(units=Y_train.shape[1], activation='softmax')) 
model.build(input_shape=(None,X_train.shape[1]))

# Loss
#loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True) 
#loss = tf.keras.losses.BinaryCrossentropy() 
loss = tf.keras.losses.MeanSquaredError()
# learning rate
lr = 1e-3
#lr = 5e-4
optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
#optimizer=keras.optimizers.Adadelta(lr)
#optimizer = tf.keras.optimizers.SGD() # SGD optimizer, explained later in this chapter
# -------------------
#
# Validation metrics
# ------------------

metrics = ['accuracy']
# ------------------

# Compile Model
model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
model.summary()




#########################################################################################################################
#########################################################################################################################

# Training or Loading Model

import os
from datetime import datetime


# from tensorflow.compat.v1 import ConfigProto
# from tensorflow.compat.v1 import InteractiveSession

# config = ConfigProto()
# config.gpu_options.allow_growth = True
# session = InteractiveSession(config=config)


exps_dir = os.path.join(cwd, 'nn_trainig_experiments')
if not os.path.exists(exps_dir):
    os.makedirs(exps_dir)

now = datetime.now().strftime('%b%d_%H-%M-%S')

model_name = 'EHSAN_MODEL'

exp_dir = os.path.join(exps_dir, model_name + '_' + str(now))
if not os.path.exists(exp_dir):
    os.makedirs(exp_dir)
    
callbacks = []

# Model checkpoint
# ----------------
ckpt_dir = os.path.join(exp_dir, 'ckpts')
if not os.path.exists(ckpt_dir):
    os.makedirs(ckpt_dir)

ckpt_callback = tf.keras.callbacks.ModelCheckpoint(filepath=os.path.join(ckpt_dir, 'cp_{epoch:02d}.ckpt'), 
                                                   save_weights_only=True)  # False to save the model directly
callbacks.append(ckpt_callback)

# Visualize Learning on Tensorboard
# ---------------------------------
tb_dir = os.path.join(exp_dir, 'tb_logs')
if not os.path.exists(tb_dir):
    os.makedirs(tb_dir)
    
# By default shows losses and metrics for both training and validation
tb_callback = tf.keras.callbacks.TensorBoard(log_dir=tb_dir,
                                             profile_batch=0,
                                             histogram_freq=0)  # if 1 shows weights histograms
callbacks.append(tb_callback)

# Early Stopping
# --------------
early_stop = False
if early_stop:
    es_callback = tf.keras.callback.EarlyStopping(monitor='val_loss', patience=10)
    callbacks.append(es_callback)



if TRAIN_NETWORK:
    with tf.device('/device:GPU:0'):
        results = model.fit(X_train,Y_train,validation_split=VALIDATION_SPLIT, batch_size=BATCH_SIZE, epochs=NB_EPOCH, verbose=VERBOSE, callbacks=callbacks)


else:
    load_this = cwd + 'nn_trainig_experiments/' + TRANING_EXPIREMENT_FOR_LOAD + '/ckpts/cp_' + LOADING_EPOCH_NUMBER.__str__() + '.ckpt'#data-00000-of-00001'
    print ('Loading Weights From:' + load_this)
    model.load_weights(load_this)  # use this if you want to restore saved model

print('\n=======================================================================')
print('Trained and Ready! Now lets make some predictions!!')

