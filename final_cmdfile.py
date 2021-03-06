# -*- coding: utf-8 -*-
"""final_cmdfile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1z26R5-bNBHudtzmg8LChlgO8KgqtC8nP

# Importing Libraries

---



*  PIL-Python Imaging Library (abbreviated as PIL)) is a free library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats
*  Pyperclip-Pyperclip is a cross-platform Python module for copy and paste clipboard functions. 

* Image-The Image module  provides a number of factory functions, including functions to load images from files, and to create new images.

* ImageFilter -The ImageFilter module contains definitions for a pre-defined set of filters, which can be be used with the Image.filter() method.

* Ipython-IPython (Interactive Python) is a command shell for interactive computing in multiple programming languages, originally developed for the Python programming language, that offers introspection, rich media, shell syntax, tab completion, and history.
"""

from PIL import ImageFilter,Image
from IPython import get_ipython

"""# Intitializing   variables with  values

---
"""

"""# Defining module to save an image

---
"""


"""# Function for an image of 28X28

---

* The image to be predicted is opened.
* The image is converted to gray scale
* The image is then rescaled,normalized.
* The image returned is the original image ,rescaled image and normalized image.
"""

def input_emnist(st):
	#opening the input image to be predicted
    im_open = Image.open(st)
    im = Image.open(st).convert('LA') #conversion to gray-scale image
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L',(28,28),(255))


    if width > height: #check which dimension is bigger
        #Width is bigger. Width becomes 20 pixels.
        nheight = int(round((28.0/width*height),0)) #resize height according to ratio width
        if (nheight == 0): #rare case but minimum is 1 pixel
            nheight = 1
        # resize and sharpen
        img = im.resize((28,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight)/2),0)) #caculate horizontal pozition
        newImage.paste(img, (0,wtop)) #paste resized image on white canvas
    else:
    #Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((28.0/height*width),0)) #resize width according to ratio height
        if (nwidth == 0): #rare case but minimum is 1 pixel
            nwidth = 1
     # resize and sharpen
        img = im.resize((nwidth,28), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth)/2),0)) #calculate vertical pozition
        newImage.paste(img, (wleft,0)) #paste resize


# # Normalizing image into pixel values
    tv = list(newImage.getdata())
    tva = [ (255-x)*1.0/255.0 for x in tv]
       
    n_image = np.array(tva)
    
    # return all the images
    return n_image,im_open,newImage

"""#  Emnist Training

---
* Loading EMNIST dataset
* Getting the stored dataset
* Defining functions
* Creating model
"""

####  emnist training
# # Loading EMNIST dataset


import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
def model_predict(n_image):
	# the below is commented due to the model already been trained

    
    #getting the stored dataset
    
    from sklearn.preprocessing import OneHotEncoder
    #train data
    get_ipython().magic('store -r n_labels')
    
    shaped_n_labels  = n_labels.reshape(-1,1)
    enc = OneHotEncoder()
    enc.fit(shaped_n_labels)
    train_labels = enc.transform(shaped_n_labels).toarray()
    

# ## Functions

# initialising weights
    def init_weights(shape):
        init_random_dist = tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(init_random_dist)
    # initialising bias
    def init_bias(shape):
        init_bias_vals = tf.constant(0.1,shape=shape)
        return tf.Variable(init_bias_vals)
    #conv2d
    def conv2d(x,W):
        #x -> [bias,height,width,channels]
        #W -> [Filter H,filter W,Channel In,Channel Out]
        return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
    #pooling layer
    def max_pool_2by2(x):
        return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
    #Convolutional layer
    def convolutional_layer(input_x,shape):
        W=init_weights(shape)
        bias = init_bias([shape[3]])
        return tf.nn.relu(conv2d(input_x,W)+bias)
    #Fully connected layer
    def normal_full_layer(input_layer,size):
        input_size = int(input_layer.get_shape()[1])
        W = init_weights([input_size,size])
        bias = init_bias([size])
        return tf.matmul(input_layer,W) + bias


    # ## Creating model


    #placeholders
    x = tf.placeholder(tf.float32,shape=[None,784])
    y_true=tf.placeholder(tf.float32,shape=[None,47])

    #layers(input)
    x_image = tf.reshape(x,[-1,28,28,1])

    #first convolutional layer
    convo_1 = convolutional_layer(x_image,shape=[5,5,1,32])
    convo_1_pooling = max_pool_2by2(convo_1)

    #second convolutional layer
    convo_2 = convolutional_layer(convo_1_pooling,shape=[5,5,32,64])
    convo_2_pooling = max_pool_2by2(convo_2)

    #fully connected layer
    convo_flat = tf.reshape(convo_2_pooling,[-1,7*7*64])
    full_layer_one = tf.nn.relu(normal_full_layer(convo_flat,1024))


    #drop out (used to overcome overfitting)

    hold_prob = tf.placeholder(tf.float32)
    full_one_dropout = tf.nn.dropout(full_layer_one,keep_prob=hold_prob)

    y_pred = normal_full_layer(full_one_dropout,47)

    #Loss Function
    
    init = tf.global_variables_initializer()



    saver = tf.train.Saver()
    with tf.Session() as sess:
            sess.run(init)
            saver.restore(sess,"C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/model/cnn_model_1_without_tamil.ckpt")

            prediction=tf.argmax(y_pred,1)
            var = prediction.eval(feed_dict={x: [n_image],y_true:train_labels,hold_prob: 0.5}, session=sess)


    labels_dict ={0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:'A',11:'B',12:'C',13:'D',14:'E',15:'F',16:'G',17:'H',18:'I',19:'J',20:'K',21:'l',22:'M',23:'N',24:'O',25:'P',26:'Q',27:'R',28:'S',29:'T',30:'u',31:'V',32:'W',33:'X',34:'Y',35:'Z',36:'a',37:'b',38:'d',39:'e',40:'f',41:'g',42:'h',43:'n',44:'q',45:'r',46:'t'}


    s = "Predicted Character : {}".format(labels_dict[var[0]])
    return s,labels_dict[var[0]]

"""# Printing the character

---

It will print the character on command prompt
"""

path='Dataset/Z21.png'

n_image,image,convo_image = input_emnist(path) #call to Function with name of the file as parameter
res,cpy = model_predict(n_image)
print(res)
